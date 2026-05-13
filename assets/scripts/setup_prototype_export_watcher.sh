#!/bin/bash

# Install a lightweight macOS launcher on port 8766.
# The launcher starts the heavier local HTML service on port 8765 only when
# an HTML artifact needs PNG export or PRD save-back.

set -euo pipefail

PROJECT_DIR="${1:-$(pwd)}"
LABEL="com.elysianspark.pm-prototype-launcher"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
LAUNCHER_DIR="$HOME/Library/Application Support/pm-prototype"
LAUNCHER_SRC="${PROJECT_DIR}/scripts/prototype_launcher.py"
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

mkdir -p "$LAUNCHER_DIR" "$LOG_DIR" "$(dirname "$PLIST")"
cp "$LAUNCHER_SRC" "$LAUNCHER_DST"
chmod +x "$LAUNCHER_DST"

# Disable the older watcher that polled every 5 seconds and eagerly launched
# the full export service.
OLD_LABEL="com.elysianspark.pm-prototype-export-watcher"
OLD_PLIST="$HOME/Library/LaunchAgents/${OLD_LABEL}.plist"
if [ -f "$OLD_PLIST" ]; then
  launchctl bootout "gui/$(id -u)" "$OLD_PLIST" >/dev/null 2>&1 || true
  mv "$OLD_PLIST" "${OLD_PLIST}.disabled"
  echo "  ℹ️  Disabled old watcher ${OLD_LABEL} (kept as .disabled backup)"
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

echo "  ✅ Installed lightweight launcher: ${LABEL} (port 8766)"
echo "     HTML export and PRD save-back will auto-start the local service on port 8765."
