#!/bin/bash
# 把 PM Workflow 安装进当前目录（macOS / Linux）。
#
#   在项目目录里执行：bash /路径/到/edu-pm-workflow/scripts/init.sh
#
# 这里只做两件事：找到一个能用的 python、把活交给 initialize.py。
# 所有安装逻辑都在 initialize.py 里，Windows 的 init.bat 走的是同一份代码——
# 两套并行的安装脚本一定会各自腐烂，这是上一版踩过的坑。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 用「打印出哨兵」判定解释器可用，不看退出码：macOS 12.3 起系统不自带 python3，
# /usr/bin/python3 是 Command Line Tools 的垫片，会弹 GUI 安装框。
for PY in python3 python; do
  if command -v "$PY" >/dev/null 2>&1 &&
     [ "$("$PY" -c 'print("PMPYOK")' 2>/dev/null)" = "PMPYOK" ]; then
    exec "$PY" "${SCRIPT_DIR}/initialize.py" --project "$(pwd)"
  fi
done

echo "❌ 没找到可用的 Python 3.9+。" >&2
echo "" >&2
echo "请二选一安装后重试：" >&2
echo "  1. 打开 https://www.python.org/downloads/ 下载安装包" >&2
echo "  2. 已装 Homebrew 的话，执行：brew install python" >&2
exit 1
