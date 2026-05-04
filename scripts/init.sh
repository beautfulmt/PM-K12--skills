#!/bin/bash

# =================================================================
# Education PM Workflow — Project Initializer
#
# Scaffolds the directory structure and installs workflow files into
# the current working directory.
#
# Project artifacts are never overwritten. Managed workflow and helper
# files are updated from the skill template with timestamped backups.
# =================================================================

set -euo pipefail

echo "🚀 Initializing Education PM Workflow..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
ASSETS_DIR="${SKILL_DIR}/assets"
BACKUP_DIR=".handoff/skill-backups/init-$(date +%Y%m%d-%H%M%S)"

if [ ! -d "$ASSETS_DIR" ]; then
    echo "❌ Error: Cannot find assets directory at ${ASSETS_DIR}" >&2
    exit 1
fi

safe_copy() {
    local src="$1"
    local dst="$2"
    if [ -e "$dst" ]; then
        echo "  ⏭️  Skipped (exists): $dst"
    else
        mkdir -p "$(dirname "$dst")"
        cp "$src" "$dst"
        echo "  ✅ Created: $dst"
    fi
}

managed_copy() {
    local src="$1"
    local dst="$2"
    if [ -e "$dst" ]; then
        if cmp -s "$src" "$dst"; then
            echo "  ⏭️  Current: $dst"
            return
        fi
        mkdir -p "$BACKUP_DIR/$(dirname "$dst")" "$(dirname "$dst")"
        cp "$dst" "$BACKUP_DIR/$dst"
        cp "$src" "$dst"
        echo "  🔄 Updated: $dst (backup: $BACKUP_DIR/$dst)"
    else
        mkdir -p "$(dirname "$dst")"
        cp "$src" "$dst"
        echo "  ✅ Created: $dst"
    fi
}

echo ""
echo "📁 Creating output directories..."

DIRS=(
    "需求文档"
    "原型"
    "原型截图"
    "流程图"
    "数据分析"
    "验收清单"
    "需求挖掘"
    ".handoff"
    "scripts"
)

for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ⏭️  Skipped (exists): $dir/"
    else
        mkdir -p "$dir"
        echo "  ✅ Created: $dir/"
    fi
done

echo ""
echo "📋 Installing managed workflow files..."

managed_copy "${ASSETS_DIR}/workflows/edu-pm-prd.md"           ".agents/workflows/edu-pm-prd.md"
managed_copy "${ASSETS_DIR}/workflows/edu-pm-demand.md"         ".agents/workflows/edu-pm-demand.md"
managed_copy "${ASSETS_DIR}/workflows/edu-pm-acceptance.md"     ".agents/workflows/edu-pm-acceptance.md"
managed_copy "${ASSETS_DIR}/workflows/edu-pm-data-analysis.md"  ".agents/workflows/edu-pm-data-analysis.md"

echo ""
echo "📄 Installing templates and references..."

safe_copy    "${ASSETS_DIR}/templates/关键点.md"                 "关键点.md"
managed_copy "${ASSETS_DIR}/templates/pencil-draw-prompt.md"    "scripts/pencil-draw-prompt.md"
safe_copy    "${ASSETS_DIR}/config/mcp.json.example"            ".mcp.json.example"

echo ""
echo "📸 Installing prototype export service..."

managed_copy "${ASSETS_DIR}/scripts/prototype_server.py"              "scripts/prototype_server.py"
managed_copy "${ASSETS_DIR}/scripts/prototype-export-client.js"       "scripts/prototype-export-client.js"
managed_copy "${ASSETS_DIR}/scripts/setup_prototype_export_watcher.sh" "scripts/setup_prototype_export_watcher.sh"
managed_copy "${ASSETS_DIR}/scripts/启动原型导出服务.command"          "启动原型导出服务.command"

chmod +x "scripts/setup_prototype_export_watcher.sh" "启动原型导出服务.command" 2>/dev/null || true

if [ "$(uname -s)" = "Darwin" ] && [ "${EDU_PM_SKIP_EXPORT_WATCHER:-0}" != "1" ]; then
    bash "scripts/setup_prototype_export_watcher.sh" "$(pwd)" || echo "  ⚠️  Export watcher install skipped; double-click 启动原型导出服务.command when needed."
fi

echo ""
echo "📌 Adding .gitkeep to empty directories..."

for dir in "需求文档" "原型" "原型截图" "流程图" "数据分析" "验收清单" "需求挖掘" ".handoff"; do
    gitkeep="$dir/.gitkeep"
    if [ ! -e "$gitkeep" ] && [ -z "$(ls -A "$dir" 2>/dev/null)" ]; then
        touch "$gitkeep"
        echo "  ✅ Added: $gitkeep"
    fi
done

echo ""
echo "=========================================="
echo "✅ Education PM Workflow initialized!"
echo "=========================================="
echo ""
echo "📂 Workflow files:  .agents/workflows/"
echo "📂 Output dirs:     需求文档/ 原型/ 流程图/ ..."
echo "📄 Version history: 关键点.md"
echo ""
echo "💡 To start: describe a product requirement to AI"
echo "💡 To customize: edit files in .agents/workflows/"
echo "💡 To use Pencil: copy .mcp.json.example → .mcp.json"
echo ""
