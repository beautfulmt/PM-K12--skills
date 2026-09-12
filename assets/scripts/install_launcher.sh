#!/bin/bash
# 「点导出自动起服务」的按需启动器（仅 macOS）。
#
# 装了它之后，点原型页的导出按钮或 PRD 的「一键复制全文」时服务会自动起来，
# 不用先双击启动脚本。
#
# 它**不是**常驻进程：端口由 launchd 持有，空闲时本项目没有任何进程在跑，
# 浏览器一连上来才拉起，起完服务就自退。所以 init 时默认就会装上。
#
#   安装/重新注册：bash scripts/install_launcher.sh
#   卸载：        bash scripts/install_launcher.sh --uninstall
#   看状态：      python3 scripts/start_service.py --doctor
#
# 真正写 plist 的逻辑在 scripts/pm_launchagent.py（唯一来源），这里只是个壳，
# 方便不想记 Python 命令的人直接跑。
set -euo pipefail

cd "$(dirname "$0")/.." || exit 1

if [ "$(uname -s)" != "Darwin" ]; then
  echo "按需启动器只支持 macOS。"
  echo "Windows 上不需要它：服务本体就是你双击「启动原型导出服务.bat」后开着的那个窗口。"
  exit 0
fi

PY=""
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1; then PY="$candidate"; break; fi
done
if [ -z "$PY" ]; then
  echo "❌ 没找到 python3，请先安装 Python 3.9+（https://www.python.org/downloads/）"
  exit 1
fi

"$PY" - "$PWD" "${1:-}" <<'PY'
import pathlib
import sys

root = pathlib.Path(sys.argv[1]).resolve()
action = sys.argv[2] if len(sys.argv) > 2 else ""

sys.path.insert(0, str(root / "scripts"))
try:
    import pm_launchagent
    from pm_runtime import ensure_config
except ImportError as error:
    sys.exit(f"❌ 这个目录还没安装 PM Workflow（{error}）。请先在项目目录跑一次 init。")

config = ensure_config(root)

if action in ("--uninstall", "-u", "uninstall"):
    ok, detail = pm_launchagent.uninstall(config)
    if not ok:
        sys.exit(f"❌ 卸载失败：{detail}")
    print(f"✅ 已卸载本项目的按需启动器（{detail}）")
    print("   导出功能不受影响：双击「启动原型导出服务.command」照样能用。")
    sys.exit(0)

ok, detail = pm_launchagent.install(root, config)
if not ok:
    sys.exit(f"❌ 注册失败：{detail}")
print(f"✅ 已为本项目注册按需启动器：{detail}")
print("   空闲时不占进程；点导出时由 launchd 拉起，起完服务自退。")
print("   卸载：bash scripts/install_launcher.sh --uninstall")
PY
