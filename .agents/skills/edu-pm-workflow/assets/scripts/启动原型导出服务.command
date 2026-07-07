#!/bin/bash
# 双击此文件即可启动通用原型导出服务。
# 启动后打开任意 原型/*.html 或 流程图/*.html，点击「导出截图 / 一键导出所有截图」即可保存 PNG。
#
# 自举：首次运行（或 Homebrew 升级 Python 导致依赖丢失）时，会自动建立独立虚拟环境
# scripts/.venv 并安装 playwright + chromium，之后都用这个 venv 跑服务，
# 不再受系统 python 升级影响（避免「playwright 未安装 / 导出服务未启动」）。

cd "$(dirname "$0")"

VENV="scripts/.venv"
PY="$VENV/bin/python"

if /usr/sbin/lsof -nP -iTCP:8765 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "原型导出服务已经在运行：http://localhost:8765"
  exit 0
fi

# 1) 没有 venv → 创建
if [ ! -x "$PY" ]; then
  echo "首次启动：创建虚拟环境 $VENV ..."
  python3 -m venv "$VENV" || { echo "创建虚拟环境失败，请确认已安装 python3"; exit 1; }
fi

# 2) venv 里缺 playwright → 安装 playwright + chromium（首次较慢，需联网下载 ~150MB）
if ! "$PY" -c "import playwright" >/dev/null 2>&1; then
  echo "安装 playwright（首次较慢，请耐心等待）..."
  "$PY" -m pip install -q --upgrade pip
  "$PY" -m pip install -q playwright || { echo "playwright 安装失败"; exit 1; }
fi
# chromium 浏览器是否就绪（装过 playwright 但没装浏览器时也要补）
if ! "$PY" -m playwright install --dry-run chromium >/dev/null 2>&1; then
  "$PY" -m playwright install chromium
else
  "$PY" -m playwright install chromium >/dev/null 2>&1 || true
fi

# 3) 启动服务（用 venv 的 python）
exec "$PY" scripts/prototype_server.py
