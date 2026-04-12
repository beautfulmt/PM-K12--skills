#!/bin/bash

# =================================================================
# Education PM Workflow — Project Initializer
#
# Scaffolds the directory structure and copies workflow files
# into the current working directory.
#
# All operations are idempotent: existing files are never overwritten.
# =================================================================

set -euo pipefail

echo "🚀 Initializing Education PM Workflow..."

# --- Locate this script's assets directory ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
ASSETS_DIR="${SKILL_DIR}/assets"

if [ ! -d "$ASSETS_DIR" ]; then
    echo "❌ Error: Cannot find assets directory at ${ASSETS_DIR}" >&2
    exit 1
fi

# --- Helper: safe_copy (never overwrites existing files) ---
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

# --- Step 1: Create output directories ---
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

# --- Step 2: Copy workflow files ---
echo ""
echo "📋 Installing workflow files..."

safe_copy "${ASSETS_DIR}/workflows/edu-pm-prd.md"           ".agents/workflows/edu-pm-prd.md"
safe_copy "${ASSETS_DIR}/workflows/edu-pm-demand.md"         ".agents/workflows/edu-pm-demand.md"
safe_copy "${ASSETS_DIR}/workflows/edu-pm-acceptance.md"     ".agents/workflows/edu-pm-acceptance.md"
safe_copy "${ASSETS_DIR}/workflows/edu-pm-data-analysis.md"  ".agents/workflows/edu-pm-data-analysis.md"

# --- Step 3: Copy templates & config references ---
echo ""
echo "📄 Installing templates and references..."

safe_copy "${ASSETS_DIR}/templates/关键点.md"                  "关键点.md"
safe_copy "${ASSETS_DIR}/templates/pencil-draw-prompt.md"     "scripts/pencil-draw-prompt.md"
safe_copy "${ASSETS_DIR}/config/mcp.json.example"             ".mcp.json.example"

# --- Step 4: Add .gitkeep to empty directories ---
echo ""
echo "📌 Adding .gitkeep to empty directories..."

for dir in "需求文档" "原型" "原型截图" "流程图" "数据分析" "验收清单" "需求挖掘" ".handoff"; do
    gitkeep="$dir/.gitkeep"
    if [ ! -e "$gitkeep" ] && [ -z "$(ls -A "$dir" 2>/dev/null)" ]; then
        touch "$gitkeep"
        echo "  ✅ Added: $gitkeep"
    fi
done

# --- Done ---
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
