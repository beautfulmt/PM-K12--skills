#!/bin/bash
# 双击此文件启动原型导出服务，然后保持这个窗口开着。
# 打开任意 [需求名]/原型/*.html 或 [需求名]/流程图/*.html，点导出即可存 PNG。
#
# 所有实际逻辑都在 scripts/start_service.py 里（Mac 和 Windows 共用同一套），
# 这里只负责：切到项目目录、找到可用的 python、出错时别把窗口关掉。

cd "$(dirname "$0")" || exit 1

for PY in python3 python; do
  if command -v "$PY" >/dev/null 2>&1; then
    "$PY" scripts/start_service.py --serve
    STATUS=$?
    # 0 = 正常退出（用户按了 ⌃C）。非 0 才需要停下来让人看清提示。
    if [ $STATUS -ne 0 ]; then
      echo ""
      echo "按回车键关闭窗口。"
      read -r _
    fi
    exit $STATUS
  fi
done

echo "❌ 没找到 python3。"
echo ""
echo "请安装 Python 3.9 以上版本，二选一："
echo "  1. 打开 https://www.python.org/downloads/ 下载安装包"
echo "  2. 已装 Homebrew 的话，在终端执行：brew install python"
echo ""
echo "装完后再双击本文件。按回车键关闭窗口。"
read -r _
exit 1
