#!/usr/bin/env python3
"""把 skill 的资产安装进项目目录——Mac 和 Windows 共用的唯一入口。

三类文件，三种策略：

  RUNTIME  服务运行时代码。**永远覆盖**（带时间戳备份）。
           用户本来就不该手改这些；而「发现本地有改动就保留」恰恰是上一版
           最严重的升级缺陷：旧项目升级时 installed.json 是空的，于是每个
           既有文件都被判为用户定制而保留，服务代码永远停在旧版本，
           表现就是「双击启动脚本没反应 / 导出服务未启动」。

  CUSTOM   用户会主动编辑的（workflow 说明书、PRD 骨架、绘图提示词）。
           内容等于任何一个历史发布版 → 视为没改过，直接升级；
           否则保留用户的文件，新版本写进 .pm-workflow/updates/ 供对照合并。

  ONCE     只在缺失时创建。关键点.md 是项目自己的版本记录，
           .mcp.json.example 是样例，两者都不该被 skill 反复覆盖。

不用 bash：Windows 上没有。所有逻辑都在 Python 里。
"""
import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
from datetime import datetime
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SOURCE / "assets/scripts"))
from pm_runtime import VERSION, atomic_write, ensure_config  # noqa: E402

RUNTIME, CUSTOM, ONCE = "runtime", "custom", "once"

# 显式映射，不靠「目录元组 + 特例链」推导。
# 目标路径是被 workflow 文档硬编码引用的（例如 PRD 流程里写死了 scripts/prd-content.html），
# 所以它必须是这里一眼可见、可 grep 的常量，而不是循环里涌现出来的结果。
MAPPING = [
    # ── 服务运行时：缺任何一个，导出/截图就起不来 ──
    ("scripts/pm_runtime.py",              "scripts/pm_runtime.py",              RUNTIME),
    ("scripts/pm_bootstrap.py",            "scripts/pm_bootstrap.py",            RUNTIME),
    ("scripts/start_service.py",           "scripts/start_service.py",           RUNTIME),
    ("scripts/prototype_server.py",        "scripts/prototype_server.py",        RUNTIME),
    ("scripts/prototype_launcher.py",      "scripts/prototype_launcher.py",      RUNTIME),
    ("scripts/pm_launchagent.py",          "scripts/pm_launchagent.py",          RUNTIME),
    ("scripts/prototype-export-client.js", "scripts/prototype-export-client.js", RUNTIME),
    ("scripts/validate_prd.py",            "scripts/validate_prd.py",            RUNTIME),
    ("scripts/install_launcher.sh",        "scripts/install_launcher.sh",        RUNTIME),
    ("scripts/启动原型导出服务.command",     "启动原型导出服务.command",             RUNTIME),
    ("scripts/启动原型导出服务.bat",         "启动原型导出服务.bat",                 RUNTIME),
    # ── 用户会改的 ──
    ("workflows/edu-pm-prd.md",            ".agents/workflows/edu-pm-prd.md",            CUSTOM),
    ("workflows/edu-pm-demand.md",         ".agents/workflows/edu-pm-demand.md",         CUSTOM),
    ("workflows/edu-pm-acceptance.md",     ".agents/workflows/edu-pm-acceptance.md",     CUSTOM),
    ("workflows/edu-pm-data-analysis.md",  ".agents/workflows/edu-pm-data-analysis.md",  CUSTOM),
    ("templates/prd-content.html",         "scripts/prd-content.html",                   CUSTOM),
    ("templates/pencil-draw-prompt.md",    "scripts/pencil-draw-prompt.md",              CUSTOM),
    # ── 只创建一次 ──
    ("templates/关键点.md",                 "关键点.md",                                   ONCE),
    ("config/mcp.json.example",            ".mcp.json.example",                          ONCE),
]

# 参考资料是可选的：老版本仓库里没有 assets/references/，缺了不影响功能。
REFERENCE_DIR = "references"
REFERENCE_TARGET = ".agents/references"

# 需要可执行位。copy2 只保留源文件的模式，而 zip 分发、网盘中转、
# Windows 检出再传回 Mac 都会丢权限位——丢了就是「双击没反应」。
EXECUTABLE = {
    "启动原型导出服务.command",
    "scripts/install_launcher.sh",
    "scripts/start_service.py",
    "scripts/prototype_launcher.py",
}

# 这一项必须排在 MAPPING 的运行时段里，但单独列出来做个说明：
# 注册 LaunchAgent 时 plist 指向的是项目里的 prototype_launcher.py，
# 所以文件必须先落地、再注册，顺序不能颠倒。
LAUNCHER_SCRIPT = "scripts/prototype_launcher.py"

# 上一代留下的文件：留着会误导用户去跑一个装「全局唯一 label」LaunchAgent 的旧脚本
# （那会让一台机器只能服务一个项目）。移走而不是直接删，放进备份目录。
STALE = ["scripts/setup_prototype_export_watcher.sh"]

GITIGNORE = ["/.pm-workflow/", "/scripts/pm-runtime-config.js", "/scripts/.venv/", "/.handoff/"]

# Windows 的 core.autocrlf=true 检出后再传回 Mac，.command 会带上 CRLF，
# bash 报 `$'\r': command not found`；.bat 反过来需要 CRLF 才可靠。
GITATTRIBUTES = [
    "* text=auto",
    "*.command text eol=lf",
    "*.sh text eol=lf",
    "*.bat text eol=crlf",
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def load_known_hashes():
    """历代已发布版本的内容 hash：让「文件等于某个旧版本」被认成没改过而直接升级，
    而不是误判成用户定制。缺这个文件不致命，只是升级时更容易报冲突。"""
    path = Path(__file__).resolve().parent / "known_hashes.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def make_executable(path):
    try:
        mode = path.stat().st_mode
        path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except OSError:
        pass  # Windows 上没有可执行位，失败不算问题


def setup_launcher(root, config, say):
    """在 macOS 上注册按需启动器，让点导出能自动起服务。

    默认就做，因为它不是常驻进程：端口归 launchd 持有，空闲时项目里没有任何
    进程在跑（详见 pm_launchagent.py 顶部说明）。

    **任何失败都只警告、不阻断安装。** 装 skill 的人可能没权限写
    ~/Library/LaunchAgents、可能在没有 launchctl 的沙箱里、可能根本不是 macOS——
    这些都不该让「文件装好了」这件事失败。丢了它只是回退到手动双击启动。
    """
    if not sys.platform == "darwin":
        return
    try:
        sys.path.insert(0, str(root / "scripts"))
        import pm_launchagent
        ok, detail = pm_launchagent.install(root, config)
    except Exception as error:  # noqa: BLE001 — 见上：绝不阻断安装
        say(f"   ⚠️  按需启动器注册失败（{error}）")
        say("      不影响导出：双击「启动原型导出服务.command」照常可用。")
        return
    if ok:
        say(f"   ✅ 按需启动器已注册：点导出/一键复制全文会自动起服务，无需先双击")
        say(f"      空闲时不占进程；不想要就跑 bash scripts/install_launcher.sh --uninstall")
    else:
        say(f"   ⚠️  按需启动器注册失败（{detail}）")
        say("      不影响导出：双击「启动原型导出服务.command」照常可用。")


def install(root, quiet=False, with_launcher=True):
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    say = (lambda *a: None) if quiet else print

    manifest_path = root / ".pm-workflow/installed.json"
    try:
        previous = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        previous = {}
    tracked = previous.get("files", {}) if isinstance(previous, dict) else {}
    known = load_known_hashes()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = root / ".handoff/skill-backups" / f"init-{stamp}"

    entries = list(MAPPING)
    # Path.glob 对不存在的目录返回空列表，所以这里不需要额外的存在性判断。
    for path in sorted((SOURCE / "assets" / REFERENCE_DIR).glob("*")):
        if path.is_file():
            entries.append((f"{REFERENCE_DIR}/{path.name}",
                            f"{REFERENCE_TARGET}/{path.name}", CUSTOM))

    for name in ("scripts", ".handoff"):
        (root / name).mkdir(parents=True, exist_ok=True)

    created, updated, current, skipped, conflicts, missing = [], [], [], [], [], []

    for source_rel, dest_rel, kind in entries:
        source = SOURCE / "assets" / source_rel
        if not source.is_file():
            missing.append(source_rel)
            continue
        dest = root / dest_rel
        incoming, existing = digest(source), digest(dest)

        if existing == incoming:
            tracked[dest_rel] = incoming
            current.append(dest_rel)
            if dest_rel in EXECUTABLE:
                make_executable(dest)
            continue

        if existing is not None:
            if kind == ONCE:
                skipped.append(dest_rel)
                continue
            if kind == CUSTOM:
                # 认得出是某个历史发布版 → 用户没改过 → 照常升级
                unchanged = existing == tracked.get(dest_rel) or existing in known.get(source_rel, [])
                if not unchanged:
                    proposal = root / ".pm-workflow/updates" / dest_rel
                    proposal.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, proposal)
                    conflicts.append(dest_rel)
                    continue
            backup = backup_root / dest_rel
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dest, backup)

        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
        if dest_rel in EXECUTABLE:
            make_executable(dest)
        (updated if existing is not None else created).append(dest_rel)
        tracked[dest_rel] = incoming

    retired = []
    for rel in STALE:
        path = root / rel
        if path.is_file():
            target = backup_root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(target))
            tracked.pop(rel, None)
            retired.append(rel)

    atomic_write(manifest_path, json.dumps(
        {"version": VERSION, "files": tracked, "pending_updates": conflicts},
        ensure_ascii=False, indent=2))

    _write_lines(root / ".gitignore", GITIGNORE)
    _write_lines(root / ".gitattributes", GITATTRIBUTES)
    keep = root / ".handoff/.gitkeep"
    if not any(root.joinpath(".handoff").iterdir()):
        keep.touch()

    config = ensure_config(root)

    say(f"✅ PM Workflow {VERSION} 已安装到 {root}")
    say(f"   项目标识 {config['project_id']}，服务端口 {config['port']}")
    for label, items in (("新增", created), ("更新", updated), ("已是最新", current),
                         ("已存在未覆盖", skipped), ("移入备份", retired)):
        if items:
            say(f"   {label} {len(items)} 项" + ("：" + "、".join(items) if len(items) <= 4 else ""))
    if missing:
        say(f"   ⚠️  skill 里缺少 {len(missing)} 个资产文件：{'、'.join(missing)}")
    if conflicts:
        say("   ⚠️  以下文件你改过，已保留你的版本；新版放在 .pm-workflow/updates/ 供对照：")
        for item in conflicts:
            say("        " + item)
    if (root / "scripts/.venv").is_dir():
        say("   💡 scripts/.venv 是旧版留下的（约 150MB），现在运行环境放在用户目录共享，可以删掉")

    launcher_ready = False
    if with_launcher:
        setup_launcher(root, config, say)
        launcher_ready = _launcher_ready(root, config)

    say("")
    if os.name == "nt":
        say("下一步：双击项目根目录的「启动原型导出服务.bat」，保持窗口开着")
        say("排查问题：py -3 scripts\\start_service.py --doctor")
    elif launcher_ready:
        say("下一步：直接打开原型或 PRD 点导出即可——服务会自动启动。")
        say("        （也可以双击「启动原型导出服务.command」手动起，效果一样）")
        say("排查问题：python3 scripts/start_service.py --doctor")
    else:
        say("下一步：双击项目根目录的「启动原型导出服务.command」，保持窗口开着")
        say("排查问题：python3 scripts/start_service.py --doctor")
    return 0


def _launcher_ready(root, config):
    try:
        sys.path.insert(0, str(root / "scripts"))
        import pm_launchagent
        registered, _port, matched, _pid = pm_launchagent.status(config)
        return registered and matched
    except Exception:  # noqa: BLE001
        return False


def _write_lines(path, entries):
    """逐行补齐，不覆盖用户已有内容。"""
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    lines = text.splitlines()
    added = [entry for entry in entries if entry not in lines]
    if not added:
        return
    body = text.rstrip("\n")
    atomic_write(path, (body + "\n" if body else "") + "\n".join(added) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="把 PM Workflow 安装进项目目录")
    parser.add_argument("--project", default=".", help="项目目录，默认当前目录")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--no-launcher", action="store_true",
                        help="不注册 macOS 按需启动器（那样点导出前需手动双击启动入口）")
    args = parser.parse_args()
    sys.exit(install(args.project, quiet=args.quiet,
                     with_launcher=not args.no_launcher))
