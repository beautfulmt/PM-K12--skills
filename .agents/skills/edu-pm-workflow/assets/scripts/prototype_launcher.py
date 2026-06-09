#!/usr/bin/env python3
"""
原型导出服务 · 极轻 launcher
====================================
常驻后台（约 5MB），只做一件事：
  收到 POST /api/launch 时，用 `open` 唤起「启动原型导出服务.command」
  让真正的导出服务（8765 端口）跑起来。

设计目的：
  - 浏览器 JS 无法跨域启动本地 .command，必须有一个本地 HTTP 端点代为转发；
  - 完整导出服务依赖 Playwright/Chromium，启动较重；
  - 因此把"常驻"拆成一个极轻 launcher，按需再拉重服务。

使用：
  - 由 ~/Library/LaunchAgents/com.elysianspark.pm-prototype-launcher.plist 自动拉起
  - 也可直接：python3 scripts/prototype_launcher.py
"""

import json
import os
import subprocess
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

LAUNCHER_PORT = int(os.environ.get("PROTOTYPE_LAUNCHER_PORT", "8766"))
EXPORT_PORT = int(os.environ.get("PROTOTYPE_SERVER_PORT", "8765"))
_PROJECT_ENV = os.environ.get("PROTOTYPE_PROJECT_DIR")
if _PROJECT_ENV:
    PROJECT_DIR = Path(_PROJECT_ENV).expanduser()
else:
    PROJECT_DIR = Path(__file__).resolve().parent.parent
COMMAND_FILE = PROJECT_DIR / "启动原型导出服务.command"

_last_launch_at = 0.0
_LAUNCH_COOLDOWN = 3.0  # 秒：避免同一次点击被重复拉起


def export_service_running() -> bool:
    try:
        import socket
        with socket.create_connection(("127.0.0.1", EXPORT_PORT), timeout=0.3):
            return True
    except OSError:
        return False


def launch_export_service() -> dict:
    global _last_launch_at
    now = time.time()
    if export_service_running():
        return {"ok": True, "status": "already-running"}

    if now - _last_launch_at < _LAUNCH_COOLDOWN:
        return {"ok": True, "status": "launching"}

    if not COMMAND_FILE.exists():
        return {"ok": False, "error": f"未找到启动脚本: {COMMAND_FILE}"}

    try:
        # macOS: open 会用默认关联（Terminal）打开 .command
        subprocess.Popen(
            ["/usr/bin/open", str(COMMAND_FILE)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        _last_launch_at = now
        return {"ok": True, "status": "launching"}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


class LauncherHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send_json(204, {})

    def do_GET(self):
        if self.path.startswith("/api/ping"):
            self._send_json(200, {
                "ok": True,
                "launcher": True,
                "export_service_running": export_service_running(),
                "export_port": EXPORT_PORT,
            })
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self):
        if self.path.startswith("/api/launch"):
            result = launch_export_service()
            code = 200 if result.get("ok") else 500
            self._send_json(code, result)
        else:
            self._send_json(404, {"error": "not found"})

    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))


def main():
    try:
        server = HTTPServer(("127.0.0.1", LAUNCHER_PORT), LauncherHandler)
    except OSError as exc:
        # 端口被占 = 已经有 launcher 在跑，直接退出即可
        sys.stderr.write(f"launcher 端口已占用，退出：{exc}\n")
        return 0

    sys.stderr.write(f"🟢 prototype launcher listening on http://127.0.0.1:{LAUNCHER_PORT}\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
