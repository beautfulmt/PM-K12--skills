#!/bin/bash
set -euo pipefail

APP_BIN="/Applications/Pencil.app/Contents/MacOS/Pencil"
MCP_BIN="/Applications/Pencil.app/Contents/Resources/app.asar.unpacked/out/mcp-server-darwin-arm64"
SOCKET_PATH="$HOME/.pencil/socket/pencil-desktop.sock"
APP_NAME="desktop"
WAIT_SECONDS=12

if [ ! -x "$APP_BIN" ]; then
  echo "Pencil app binary not found: $APP_BIN" >&2
  exit 1
fi

if [ ! -x "$MCP_BIN" ]; then
  echo "Pencil MCP binary not found: $MCP_BIN" >&2
  exit 1
fi

cleanup_stale_servers() {
  pkill -f "$MCP_BIN --app $APP_NAME" 2>/dev/null || true
}

start_pencil_if_needed() {
  if ! pgrep -x "Pencil" >/dev/null 2>&1; then
    open -a /Applications/Pencil.app
  fi
}

wait_for_socket() {
  local i
  for ((i=0; i<WAIT_SECONDS; i++)); do
    if [ -S "$SOCKET_PATH" ]; then
      python3 - "$SOCKET_PATH" <<'PY' >/dev/null 2>&1
import socket, sys
path = sys.argv[1]
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.settimeout(1)
s.connect(path)
s.close()
PY
      return 0
    fi
    sleep 1
  done
  return 1
}

cleanup_stale_servers
start_pencil_if_needed

if ! wait_for_socket; then
  echo "Timed out waiting for Pencil desktop socket: $SOCKET_PATH" >&2
  exit 1
fi

exec "$MCP_BIN" --app "$APP_NAME"
