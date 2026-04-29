#!/usr/bin/env python3
"""
通用 HTML 原型导出服务器
================================
功能：
  1. 在 http://localhost:8765 提供项目文件预览
  2. 提供 /api/screenshot 接口，供 HTML 里的导出按钮触发
  3. 使用 Playwright/Chromium 截取浏览器真实渲染后的 .device，避免 html-to-image 重绘差异

使用方法：双击项目根目录的「启动原型导出服务.command」，或执行：
  python3 scripts/prototype_server.py
"""

import asyncio
import json
import os
import re
import sys
import threading
import time
import webbrowser
from html import unescape
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import quote, unquote, urlparse


PORT = int(os.environ.get("PROTOTYPE_SERVER_PORT", "8765"))
PROJECT_DIR = Path(__file__).resolve().parent.parent
PROTOTYPE_DIR = PROJECT_DIR / "原型"
OUTPUT_ROOT = PROJECT_DIR / "原型截图"
SERVER_URL = f"http://localhost:{PORT}"
DEFAULT_HTML = PROTOTYPE_DIR / "AI试卷分析-prototype.html"
DEFAULT_VIEWPORT = {"width": 1440, "height": 900}
EXPORT_DEVICE_SCALE = 2


_state = {
    "running": False,
    "progress": 0,
    "total": 0,
    "current": "",
    "done": False,
    "error": None,
    "success_count": 0,
    "output_dir": "",
    "html": "",
    "files": [],
}
_state_lock = threading.Lock()


def _update_state(**kwargs):
    with _state_lock:
        _state.update(kwargs)


def _get_state():
    with _state_lock:
        return dict(_state)


def _is_under(path, parent):
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _first_prototype_html():
    if DEFAULT_HTML.exists():
        return DEFAULT_HTML

    files = sorted(PROTOTYPE_DIR.glob("*.html"))
    return files[0] if files else None


def _resolve_html_path(raw_path):
    raw_path = raw_path or ""

    if raw_path.startswith(("http://", "https://", "file://")):
        raw_path = urlparse(raw_path).path

    raw_path = unquote(raw_path).split("?", 1)[0].split("#", 1)[0]
    candidates = []

    if raw_path:
        incoming = Path(raw_path)
        if incoming.is_absolute() and _is_under(incoming, PROJECT_DIR):
            candidates.append(incoming)
        candidates.append(PROJECT_DIR / raw_path.lstrip("/"))
        candidates.append(PROJECT_DIR / raw_path)

    fallback = _first_prototype_html()
    if fallback:
        candidates.append(fallback)

    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue

        if (
            resolved.exists()
            and resolved.is_file()
            and resolved.suffix.lower() == ".html"
            and _is_under(resolved, PROJECT_DIR)
        ):
            return resolved

    raise FileNotFoundError(f"找不到原型 HTML：{raw_path or '(empty)'}")


def _feature_name(html_path):
    name = html_path.stem
    for suffix in ("-prototype", "_prototype", "-原型", " · 交互原型", " - 原型"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
    return _safe_filename(name, fallback="prototype")


def _strip_markup(value):
    value = re.sub(r"<[^>]+>", "", value or "", flags=re.S)
    return unescape(value).strip()


def _safe_filename(name, fallback="prototype"):
    name = _strip_markup(name)
    name = re.sub(r"[/\\:*?\"<>|]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    name = name.strip(". ")
    return name or fallback


def _normalize_viewport(value):
    if not isinstance(value, dict):
        return dict(DEFAULT_VIEWPORT)

    def _num(key, fallback):
        try:
            number = int(float(value.get(key, fallback)))
        except (TypeError, ValueError):
            return fallback
        return max(320, min(number, 4096))

    return {
        "width": _num("width", DEFAULT_VIEWPORT["width"]),
        "height": _num("height", DEFAULT_VIEWPORT["height"]),
    }


def _clean_comment_label(value):
    value = _strip_markup(value)
    value = re.sub(r"^[=\-\s_#]+|[=\-\s_#]+$", "", value)
    value = re.sub(r"^[-\s]*", "", value).strip()
    if not value:
        return ""
    if not re.search(r"[\w\u4e00-\u9fff]", value):
        return ""
    return value


def _parse_attrs(attrs):
    parsed = {}
    for match in re.finditer(r"([:\w-]+)\s*=\s*(['\"])(.*?)\2", attrs, re.S):
        parsed[match.group(1)] = unescape(match.group(3))
    return parsed


def _extract_source_labels(html_path):
    content = html_path.read_text(encoding="utf-8")
    devices = []

    for match in re.finditer(r"(?P<prefix>(?:\s*<!--.*?-->\s*){0,8})<div\b(?P<attrs>[^>]*?)>", content, re.S):
        attrs = _parse_attrs(match.group("attrs"))
        classes = attrs.get("class", "").split()
        if "device" not in classes or not attrs.get("id"):
            continue
        devices.append(
            {
                "id": attrs["id"],
                "attrs": attrs,
                "prefix": match.group("prefix") or "",
                "start": match.end(),
            }
        )

    labels = {}
    for index, device in enumerate(devices):
        next_start = devices[index + 1]["start"] if index + 1 < len(devices) else len(content)
        segment = content[device["start"] : next_start]
        label = (
            device["attrs"].get("data-export-name")
            or device["attrs"].get("data-name")
            or device["attrs"].get("data-title")
            or device["attrs"].get("aria-label")
            or device["attrs"].get("title")
            or ""
        )

        if not label:
            label_match = re.search(r'<div\s+class=["\']device-label["\'][^>]*>(.*?)</div>', segment, re.S)
            if label_match:
                label = label_match.group(1)

        if not label:
            title_match = re.search(r'class=["\'][^"\']*\bpage-title\b[^"\']*["\'][^>]*>(.*?)</', segment, re.S)
            if title_match:
                label = title_match.group(1)

        if not label:
            comments = re.findall(r"<!--(.*?)-->", device["prefix"], re.S)
            for comment in reversed(comments):
                cleaned = _clean_comment_label(comment)
                if cleaned:
                    label = cleaned
                    break

        labels[device["id"]] = _safe_filename(label, fallback=device["id"])

    return labels


def _relative_url_path(html_path):
    rel = html_path.resolve().relative_to(PROJECT_DIR.resolve()).as_posix()
    return "/" + quote(rel, safe="/")


def _dedupe_filename(filename, used):
    stem = filename[:-4] if filename.lower().endswith(".png") else filename
    candidate = f"{stem}.png"
    index = 2
    while candidate in used:
        candidate = f"{stem}-{index}.png"
        index += 1
    used.add(candidate)
    return candidate


async def _discover_pages(page, html_path, source_labels):
    base_url = f"{SERVER_URL}{_relative_url_path(html_path)}"
    await page.goto(base_url, wait_until="networkidle", timeout=30000)
    await page.wait_for_timeout(500)

    dom_pages = await page.evaluate(
        """
        () => Array.from(document.querySelectorAll('.device[id]')).map(device => {
          const wrapper = device.closest('.device-wrapper');
          const labelNode = wrapper ? wrapper.querySelector('.device-label') : null;
          const pageTitle = device.querySelector('.page-title');
          const tabs = Array.from(device.querySelectorAll('.report-seg[data-tab], [data-export-tab]')).map(seg => ({
            tab: seg.dataset.tab || seg.dataset.exportTab || '',
            label: seg.dataset.exportName || seg.dataset.name || seg.textContent.trim()
          })).filter(item => item.tab);
          return {
            id: device.id,
            label: device.dataset.exportName || device.dataset.name || device.dataset.title ||
              device.getAttribute('aria-label') || (labelNode && labelNode.textContent.trim()) ||
              (pageTitle && pageTitle.textContent.trim()) || '',
            tabs
          };
        })
        """
    )

    pages = []
    for item in dom_pages:
        page_id = item["id"]
        base_label = _safe_filename(item.get("label") or source_labels.get(page_id) or page_id, fallback=page_id)
        tabs = item.get("tabs") or []

        if len(tabs) > 1:
            for tab_index, tab in enumerate(tabs):
                tab_id = tab["tab"]
                tab_label = _safe_filename(tab.get("label"), fallback=tab_id)
                if tab_index == 0:
                    label = base_label
                elif "·" in base_label:
                    parts = [part.strip() for part in base_label.split("·")]
                    parts[-1] = tab_label
                    label = " · ".join(parts)
                else:
                    label = f"{base_label}-{tab_label}"
                pages.append({"hash": page_id, "page_id": page_id, "tab": tab_id, "label": label})
        else:
            pages.append({"hash": page_id, "page_id": page_id, "tab": None, "label": base_label})

    if not pages:
        raise RuntimeError("未找到可导出的 .device 原型节点")

    return pages


async def _wait_for_visible_device(page, page_id):
    await page.wait_for_function(
        """
        id => {
          const el = document.getElementById(id);
          if (!el) return false;
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          return rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none';
        }
        """,
        arg=page_id,
        timeout=7000,
    )
    handle = await page.evaluate_handle("id => document.getElementById(id)", arg=page_id)
    element = handle.as_element()
    if not element:
        raise RuntimeError(f"找不到页面节点：{page_id}")
    return element


async def _set_tab(page, tab_id):
    if not tab_id:
        return

    await page.evaluate(
        """
        tabId => {
          if (typeof window.switchTab === 'function') {
            window.switchTab(tabId);
            return;
          }
          document.querySelectorAll('.report-seg[data-tab], [data-export-tab]').forEach(seg => {
            const segTab = seg.dataset.tab || seg.dataset.exportTab;
            seg.classList.toggle('active', segTab === tabId);
          });
          document.querySelectorAll('.report-panel').forEach(panel => {
            panel.style.display = panel.id === tabId ? '' : 'none';
          });
        }
        """,
        tab_id,
    )
    await page.wait_for_timeout(300)


async def _force_tiled_mode(page):
    await page.evaluate(
        """
        () => {
          let exportStyle = document.getElementById('prototype-export-hide-ui-style');
          if (!exportStyle) {
            exportStyle = document.createElement('style');
            exportStyle.id = 'prototype-export-hide-ui-style';
            document.head.appendChild(exportStyle);
          }
          exportStyle.textContent = '.export-btn, #exportFab, [data-export-ui="true"] { display: none !important; }';
          document.body.classList.remove('single');
          document.body.classList.add('tiled');
          document.querySelectorAll('.device-wrapper').forEach(wrapper => wrapper.classList.remove('active'));
        }
        """
    )


async def _wait_for_export_ready(page):
    await page.evaluate(
        """
        async () => {
          if (document.fonts && document.fonts.ready) {
            try { await document.fonts.ready; } catch (_) {}
          }
          const images = Array.from(document.images || []);
          await Promise.all(images.map(img => {
            if (img.complete) return Promise.resolve();
            if (typeof img.decode === 'function') return img.decode().catch(() => undefined);
            return new Promise(resolve => {
              img.addEventListener('load', resolve, { once: true });
              img.addEventListener('error', resolve, { once: true });
            });
          }));
          await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
        }
        """
    )


async def _run_screenshots(html_path, options=None):
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        _update_state(running=False, done=True, error="playwright 未安装，请先执行 pip3 install playwright && python3 -m playwright install chromium")
        return

    options = options or {}
    viewport = _normalize_viewport(options.get("viewport"))
    output_dir = OUTPUT_ROOT / _feature_name(html_path)
    source_labels = _extract_source_labels(html_path)
    files = []
    success = 0

    _update_state(output_dir=str(output_dir), html=str(html_path), files=[])

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        for old_png in output_dir.glob("*.png"):
            old_png.unlink()

        base_url = f"{SERVER_URL}{_relative_url_path(html_path)}"

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport=viewport,
                device_scale_factor=EXPORT_DEVICE_SCALE,
            )
            page = await context.new_page()

            pages = await _discover_pages(page, html_path, source_labels)
            await _force_tiled_mode(page)
            await _wait_for_export_ready(page)
            _update_state(total=len(pages))
            used_names = set()

            for index, item in enumerate(pages, 1):
                label = _safe_filename(item["label"], fallback=item["page_id"])
                filename = _dedupe_filename(f"{label}.png", used_names)
                out_path = output_dir / filename
                _update_state(progress=index - 1, current=label)

                try:
                    await _force_tiled_mode(page)
                    await _set_tab(page, item.get("tab"))
                    await _wait_for_export_ready(page)
                    element = await _wait_for_visible_device(page, item["page_id"])
                    await element.scroll_into_view_if_needed(timeout=3000)
                    await page.wait_for_timeout(120)
                    await element.screenshot(path=str(out_path), type="png", scale="device")
                    files.append(str(out_path))
                    success += 1
                    _update_state(files=list(files))
                except Exception as error:
                    print(f"  ⚠ [{label}] {error}")

            await browser.close()

        _update_state(
            running=False,
            progress=len(pages),
            current="完成",
            done=True,
            error=None,
            success_count=success,
            files=list(files),
        )
        print(f"\n  🎉 截图完成：{success}/{len(pages)} 张 → {output_dir}\n")
    except Exception as error:
        _update_state(running=False, done=True, error=str(error), current="导出失败")
        print(f"\n  ❌ 截图失败：{error}\n")


def _screenshot_thread(html_path, options=None):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_run_screenshots(html_path, options=options))
    loop.close()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"  [{time.strftime('%H:%M:%S')}] {fmt % args}")

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        path = unquote(self.path.split("?", 1)[0])
        if path == "/api/status":
            self._json(_get_state())
        else:
            self._serve_file(path)

    def do_POST(self):
        path = unquote(self.path.split("?", 1)[0])
        if path == "/api/screenshot":
            self._handle_screenshot()
        else:
            self._json({"error": "not found"}, 404)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw) if raw else {}

    def _handle_screenshot(self):
        state = _get_state()
        if state["running"]:
            self._json({"started": False, "message": "截图已在进行中，请等待..."})
            return

        try:
            payload = self._read_json_body()
            html_path = _resolve_html_path(payload.get("path") or payload.get("html") or payload.get("url"))
            options = {
                "viewport": _normalize_viewport(payload.get("viewport")),
            }
        except Exception as error:
            self._json({"started": False, "error": str(error)}, 400)
            return

        _update_state(
            running=True,
            progress=0,
            total=0,
            current="启动浏览器...",
            done=False,
            error=None,
            success_count=0,
            output_dir=str(OUTPUT_ROOT / _feature_name(html_path)),
            html=str(html_path),
            files=[],
        )

        thread = threading.Thread(target=_screenshot_thread, args=(html_path, options), daemon=True)
        thread.start()
        self._json({"started": True, "html": str(html_path), "output_dir": str(OUTPUT_ROOT / _feature_name(html_path))})

    def _serve_file(self, url_path):
        if url_path == "/":
            first = _first_prototype_html()
            if not first:
                self._json({"error": "原型目录中没有 HTML 文件"}, 404)
                return
            url_path = _relative_url_path(first)

        file_path = (PROJECT_DIR / url_path.lstrip("/")).resolve()
        if not _is_under(file_path, PROJECT_DIR) or not file_path.exists() or not file_path.is_file():
            self.send_response(404)
            self._cors()
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        mime = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".svg": "image/svg+xml",
            ".json": "application/json; charset=utf-8",
            ".webp": "image/webp",
        }.get(file_path.suffix.lower(), "application/octet-stream")

        body = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)


class ThreadedHTTPServer(HTTPServer):
    def process_request(self, request, client_address):
        thread = threading.Thread(
            target=self._process_request_thread,
            args=(request, client_address),
            daemon=True,
        )
        thread.start()

    def _process_request_thread(self, request, client_address):
        try:
            self.finish_request(request, client_address)
        except Exception:
            self.handle_error(request, client_address)
        finally:
            self.shutdown_request(request)


def main():
    os.chdir(PROJECT_DIR)
    server = ThreadedHTTPServer(("", PORT), Handler)

    first = _first_prototype_html()
    first_url = f"{SERVER_URL}{_relative_url_path(first)}" if first else SERVER_URL

    print(f"\n{'─' * 56}")
    print("  🚀 原型导出服务已启动")
    print(f"{'─' * 56}")
    print(f"  项目路径：{PROJECT_DIR}")
    print(f"  原型预览：{first_url}")
    print("  截图输出：原型截图/[原型文件名]/")
    print(f"{'─' * 56}")
    print("  👉 在浏览器里打开任一 原型/*.html，点击「一键导出所有截图」即可")
    print("  ⌃C  停止服务器\n")

    if not os.environ.get("PROTOTYPE_SERVER_NO_OPEN") and first:
        def _open_browser():
            time.sleep(0.8)
            print("  🌐 正在打开浏览器...\n")
            webbrowser.open(first_url)

        threading.Thread(target=_open_browser, daemon=True).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  ✅ 服务器已停止\n")
        server.shutdown()


if __name__ == "__main__":
    try:
        main()
    except OSError as error:
        if "Address already in use" in str(error):
            print(f"端口 {PORT} 已被占用，可能导出服务已经在运行。")
        else:
            raise
