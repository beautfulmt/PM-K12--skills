#!/bin/bash
# Double-click to start the universal prototype export service.
# The service writes PNG screenshots to 原型截图/[原型文件名]/.

cd "$(dirname "$0")"

if /usr/sbin/lsof -nP -iTCP:8765 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "原型导出服务已经在运行：http://localhost:8765"
  exit 0
fi

python3 scripts/prototype_server.py
