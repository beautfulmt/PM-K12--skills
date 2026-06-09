#!/bin/bash

# 为 macOS 安装一个极轻的 launcher 守护（端口 8766）。
# 它常驻时仅约 5MB，唯一职责：
#   收到 HTML 原型导出按钮的 /api/launch 请求时，用 `open` 唤起
#   `启动原型导出服务.command`，按需拉起完整的截图导出服务（端口 8765）。
# 优点：不导出时不会有 Chromium/Playwright 之类的重进程常驻；导出时仍能从网页一键触发。

set -euo pipefail

PROJECT_DIR="${1:-$(pwd)}"
LABEL="com.elysianspark.pm-prototype-launcher"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
LAUNCHER_DIR="$HOME/Library/Application Support/pm-prototype"
LAUNCHER_SRC_REL="scripts/prototype_launcher.py"
LAUNCHER_SRC="${PROJECT_DIR}/${LAUNCHER_SRC_REL}"
LAUNCHER_DST="${LAUNCHER_DIR}/prototype_launcher.py"
LOG_DIR="$HOME/Library/Logs"

if [ "$(uname -s)" != "Darwin" ]; then
  echo "  ⏭️  Skipped launcher install: only macOS LaunchAgent is supported."
  exit 0
fi

if [ ! -f "$LAUNCHER_SRC" ]; then
  echo "  ⚠️  Missing $LAUNCHER_SRC; launcher install skipped."
  exit 0
fi

# macOS LaunchAgent 沙箱默认读不到 ~/Documents。把 launcher.py 复制到
# ~/Library/Application Support/pm-prototype 下（可读），项目目录通过环境变量传入。
mkdir -p "$LAUNCHER_DIR" "$LOG_DIR" "$(dirname "$PLIST")"
cp "$LAUNCHER_SRC" "$LAUNCHER_DST"
chmod +x "$LAUNCHER_DST"

# 清理旧的 watcher（5 秒轮询 + 拉重服务的老方案）
OLD_LABEL="com.elysianspark.pm-prototype-export-watcher"
OLD_PLIST="$HOME/Library/LaunchAgents/${OLD_LABEL}.plist"
if [ -f "$OLD_PLIST" ]; then
  launchctl bootout "gui/$(id -u)" "$OLD_PLIST" >/dev/null 2>&1 || true
  mv "$OLD_PLIST" "${OLD_PLIST}.disabled"
  echo "  ℹ️  已停用旧守护 ${OLD_LABEL}（保留为 .disabled 备份）"
fi

cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>${LAUNCHER_DST}</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PROTOTYPE_PROJECT_DIR</key>
    <string>${PROJECT_DIR}</string>
  </dict>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>${LOG_DIR}/pm-prototype-launcher.log</string>
  <key>StandardErrorPath</key>
  <string>${LOG_DIR}/pm-prototype-launcher.err.log</string>
</dict>
</plist>
PLIST

launchctl bootout "gui/$(id -u)" "$PLIST" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
launchctl enable "gui/$(id -u)/${LABEL}"
launchctl kickstart -k "gui/$(id -u)/${LABEL}" >/dev/null 2>&1 || true

echo "  ✅ 已安装极轻 launcher：${LABEL}（端口 8766）"
echo "     点击 HTML 原型的导出按钮时会自动唤起完整截图服务（端口 8765）"
