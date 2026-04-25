---
name: edu-pm-workflow
description: "Education PM workflow: generate PRD, prototypes, flowcharts, acceptance checklists, and data analysis reports from a single requirement description. Supports Claude Code, Cursor, Codex, and other agents."
user-invocable: true
---

# Education PM Workflow Skill

**Description**:
教育产品经理全流程工作流。输入一句需求描述，自动产出完整的 PRD 文档、交互原型、流程图、验收清单和数据分析报告。

---

## Quick Start

When the user invokes this skill, execute the initialization script to scaffold the project structure.

### Step 1: Execute Init Script

Find and run the `init.sh` script bundled with this skill:

```bash
SKILL_PATH=""
for root in \
  ".agents/skills" \
  "$HOME/.agents/skills" \
  ".claude/skills" \
  "$HOME/.claude/skills" \
  ".cursor/skills" \
  "$HOME/.cursor/skills" \
  ".codex/skills" \
  "$HOME/.codex/skills"
do
  [ -d "$root" ] || continue
  SKILL_PATH="$(find "$root" -path "*/edu-pm-workflow/scripts/init.sh" -print -quit 2>/dev/null)"
  [ -n "$SKILL_PATH" ] && break
done

if [ -n "$SKILL_PATH" ]; then
  bash "$SKILL_PATH"
else
  echo "Error: Could not find edu-pm-workflow/scripts/init.sh"
fi
```

### Step 2: Verify

Confirm the following structure has been created:

- `.agents/workflows/edu-pm-prd.md` (main workflow)
- `.agents/workflows/edu-pm-demand.md` (demand analysis)
- `.agents/workflows/edu-pm-acceptance.md` (acceptance checklist)
- `.agents/workflows/edu-pm-data-analysis.md` (data analysis)
- `关键点.md` (version history)
- `scripts/prototype_server.py` and `scripts/prototype-export-client.js` (real-render PNG export)
- `启动原型导出服务.command` (local export service launcher)
- Empty output directories: `需求文档/`, `原型/`, `原型截图/`, `流程图/`, `数据分析/`, `验收清单/`, `需求挖掘/`, `.handoff/`

### Step 3: Report

Tell the user:

> **Education PM Workflow initialized!**
>
> Your project is ready. Here's what you can do:
>
> | Command | What it does |
> |---------|-------------|
> | Describe a requirement | AI will guide you through requirement collection, then produce PRD + prototype + flowchart |
> | "Generate acceptance checklist" | Auto-generate a testable checklist from an existing PRD |
> | "Analyze data" | Turn raw metrics into a visual analysis report |
> | "Dig into demands" | Competitive analysis and user pain point discovery |
>
> **Workflow files are in `.agents/workflows/`** — edit them to customize for your team.

---

## How to Use (User Guide)

### Core Workflows

This skill includes 4 workflows that can be triggered by natural language:

| Workflow | Trigger | Output |
|----------|---------|--------|
| **PRD Production** | Describe any product requirement | PRD (HTML) + Interactive Prototype (HTML) + Flowchart (HTML) |
| **Demand Analysis** | "Help me analyze user demands for [feature]" | User insight report (HTML) |
| **Acceptance Checklist** | "Generate acceptance checklist for [PRD]" | Interactive checklist with progress tracking (HTML) |
| **Data Analysis** | "Analyze this data: [paste metrics]" | Visual BI-style analysis report (HTML) |

### PRD Workflow Detail

The main workflow follows this pipeline:

```
Step 1: Conversational Requirement Collection
  → AI evaluates 6 key dimensions, asks smart follow-ups
  → User confirms understanding before proceeding

Step 2: Generate PRD (HTML)
  → 8-section structured document
  → Editable cells (contenteditable) for quick text tweaks
  → Embedded prototype iframes with drag-to-resize

Step 3: Generate Prototype (HTML)
  → Single-file, hash-routed interactive prototype
  → Tiled view (all pages) + Single page view (per hash)
  → One-click PNG export via local Playwright service
  → [Optional] Pencil high-fidelity design enhancement

Step 4: Generate Flowchart (HTML)
  → Mermaid-based sequence/flow/state diagrams
  → Embedded in PRD via iframe

Step 5: Deliver & Review
  → All outputs are self-contained HTML, ready for screenshot → DingTalk/Feishu
```

### Optional: Pencil High-Fidelity Design

If you have [Pencil](https://pencil.elysiantech.com) installed, you can enhance prototypes with high-fidelity designs:

1. After HTML prototype is done, AI will ask if you want Pencil enhancement
2. If yes, AI auto-detects Pencil installation and MCP connection
3. Pencil generates polished designs → exports PNG → reverse-calibrates HTML to match

**No Pencil? No problem.** The entire workflow runs perfectly with HTML-only prototypes.

### Output Directory Structure

```
YourProject/
├── 需求文档/                 # PRD documents
│   └── [Feature]-PRD.html
├── 原型/                     # Interactive prototypes
│   ├── [Feature]-prototype.html
│   └── [Feature].pen         # (optional, Pencil source)
├── 原型截图/                  # Exported prototype screenshots
│   └── [Feature]-[Page].png
├── scripts/                   # Export service + helper scripts
│   ├── prototype_server.py
│   └── prototype-export-client.js
├── 启动原型导出服务.command      # macOS launcher for PNG export service
├── 流程图/                    # Flowcharts
│   └── [Feature]-flow.html
├── 数据分析/                  # Data analysis reports
│   └── [Feature]-数据分析.html
├── 验收清单/                  # Acceptance checklists
│   └── [Feature]-验收清单.html
├── 需求挖掘/                  # Demand analysis reports
│   └── [Feature]-需求洞察.html
├── .handoff/                  # Session handoff files
└── .agents/workflows/         # Workflow definitions (editable!)
```

---

## How to Customize (Remix Guide)

This workflow is built for K12 education PMs, but you can easily adapt it to your own industry and style.

### Level 1: Change Content (Easiest)

Edit the text in workflow files without changing structure. Good for same-industry, different-company PMs.

| What to change | File | Section |
|---------------|------|---------|
| PRD chapter structure | `edu-pm-prd.md` | 2.2 PRD Structure |
| Design colors & device size | `edu-pm-prd.md` | 3.2 Design Specs + 3.5.3 Design Variables |
| Requirement dimensions | `edu-pm-prd.md` | 1.2 Information Completeness |
| Report visual style | `edu-pm-data-analysis.md` | Step 4 UI Specs |

> Just tell AI: "Open `.agents/workflows/edu-pm-prd.md`, change the color scheme from green to blue"

### Level 2: Change Industry (Moderate)

Adapt from education PM to e-commerce, healthcare, finance, etc.

**Recommended approach:**
1. Feed AI one of your best existing PRDs as a reference
2. Tell AI: "Rewrite `.agents/workflows/edu-pm-prd.md` to match my industry style based on this PRD"
3. AI will adapt terminology, requirement dimensions, design style, and PRD structure

**Key areas to adapt:**
- Requirement dimensions: "K12 classroom scenarios" → "user purchase funnel"
- Design style: "playful K12" → "professional fintech"
- PRD structure: add/remove chapters for your domain
- Flowchart types: education uses sequence diagrams, e-commerce might prefer state diagrams

### Level 3: Change Workflow (Advanced)

Add, remove, or reorder entire workflows.

- **Add a workflow**: Create a new `.md` file in `.agents/workflows/`, follow the same frontmatter + step-by-step format
- **Remove a workflow**: Delete the corresponding `.md` file
- **Reorder steps**: Edit the step numbers in `edu-pm-prd.md`

> Tip: Look at how the 4 existing workflow files are structured — they're your best template for writing new ones.
