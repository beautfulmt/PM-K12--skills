#!/bin/bash

# Install a per-user macOS watcher that keeps the prototype export service
# available for HTML prototype export buttons.

set -euo pipefail

PROJECT_DIR="${1:-$(pwd)}"
LABEL="com.elysianspark.pm-prototype-export-watcher"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
LOG_DIR="$HOME/Library/Logs"
START_COMMAND="${PROJECT_DIR}/启动原型导出服务.command"

if [ "$(uname -s)" != "Darwin" ]; then
  echo "  ⏭️  Skipped export watcher: only macOS LaunchAgent is supported."
  exit 0
fi

if [ ! -f "$START_COMMAND" ]; then
  echo "  ⚠️  Skipped export watcher: missing $START_COMMAND"
  exit 0
fi

mkdir -p "$(dirname "$PLIST")" "$LOG_DIR"

cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>-lc</string>
    <string>if ! /usr/sbin/lsof -nP -iTCP:8765 -sTCP:LISTEN >/dev/null 2&gt;&amp;1; then /usr/bin/open "${START_COMMAND}"; fi</string>
  </array>
  <key>StartInterval</key>
  <integer>5</integer>
  <key>RunAtLoad</key>
  <true/>
  <key>StandardOutPath</key>
  <string>${LOG_DIR}/pm-prototype-export-watcher.log</string>
  <key>StandardErrorPath</key>
  <string>${LOG_DIR}/pm-prototype-export-watcher.err.log</string>
</dict>
</plist>
PLIST

launchctl bootout "gui/$(id -u)" "$PLIST" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
launchctl enable "gui/$(id -u)/${LABEL}"
launchctl kickstart -k "gui/$(id -u)/${LABEL}" >/dev/null 2>&1 || true

echo "  ✅ Installed export watcher: ${LABEL}"
