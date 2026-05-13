---
name: edu-pm-workflow
description: "Education PM workflow for producing PRDs, interactive HTML prototypes, flowcharts, acceptance checklists, demand analysis, and data reports for education-product work. Use when the user describes an education product requirement, asks for PRD/prototype/flowchart/checklist/data-analysis output, or wants to continue this PM workflow."
user-invocable: true
---

# Education PM Workflow Skill

This skill turns education product requirements into working artifacts: PRD HTML, interactive prototype HTML, flowchart HTML, acceptance checklist, demand analysis, and data reports.

## Core Capabilities

- **PRD HTML**: create editable PRD files under `需求文档/`, with `contenteditable` detail cells and a “保存并通知AI” button that writes browser edits back to the local HTML file.
- **Prototype HTML**: create single-file interactive prototypes under `原型/`, with hash-based page switching, tiled review mode, and real-render PNG export.
- **Flowchart HTML**: create Mermaid flowcharts under `流程图/`, exported separately to `流程图截图/`.
- **Review Loop**: after a user edits PRD text in the browser and clicks save, read the saved PRD HTML from disk, identify changed requirements, then update prototype and flowchart artifacts to stay aligned.
- **Support Artifacts**: generate demand insight reports, acceptance checklists, and data-analysis reports for education-product work.

## First Decision

1. If `.agents/workflows/` exists, do not re-initialize. Read the relevant workflow file and continue from the current project state.
2. If `.agents/workflows/` or required scripts are missing, run `scripts/init.sh` from this skill once.
3. If the user explicitly asks to reinstall or update the workflow, run `scripts/init.sh`. The script updates managed workflow files and backs up replaced copies.

Find this skill's init script if needed:

```bash
find .agents/skills "$HOME/.codex/skills" "$HOME/.agents/skills" "$HOME/.claude/skills" "$HOME/.cursor/skills" \
  -path "*/edu-pm-workflow/scripts/init.sh" -print -quit 2>/dev/null
```

## Workflow Routing

Load only the workflow needed for the user's current request:

| User intent | Read this file first | Primary output |
|---|---|---|
| New requirement, PRD, prototype, flowchart, continue PRD work | `.agents/workflows/edu-pm-prd.md` | `需求文档/[需求名]-PRD.html`, `原型/[需求名]-prototype.html`, `流程图/[需求名]-flow.html` |
| Demand discovery, user needs, competitive/product insight | `.agents/workflows/edu-pm-demand.md` | `需求挖掘/[需求名]-需求洞察.html` |
| Acceptance checklist, test checklist, launch verification | `.agents/workflows/edu-pm-acceptance.md` | `验收清单/[需求名]-验收清单.html` |
| Metrics, BI-style analysis, report from data | `.agents/workflows/edu-pm-data-analysis.md` | `数据分析/[需求名]-数据分析.html` |

For PRD work, treat `.agents/workflows/edu-pm-prd.md` as the authoritative project workflow. Do not use root-level `edu-pm-prd.md` if both exist.

## PRD Workflow Rules

- Confirm the requirement before writing when core information is missing; ask only focused questions.
- Produce HTML artifacts, not Markdown artifacts, unless the user asks otherwise.
- Keep PRD, prototype, and flowchart synchronized. When one changes, inspect the other two for necessary updates.
- The HTML prototype is the primary interactive artifact. Pencil is optional visual enhancement only.
- Use the local PNG export service through `scripts/prototype-export-client.js`; do not build new `html2canvas`/`html-to-image` exporters.
- Use `scripts/prd-save-client.js` in PRD HTML for browser edit save-back. The local service endpoint is `scripts/prototype_server.py` `/api/save-html`; do not rely on browser downloads as the primary save mechanism.
- When the user says they edited and saved the PRD in the browser, read the PRD HTML file from disk before making updates, then synchronize prototype and flowchart according to the saved text.
- Before delivery, verify scripts render and the prototype pages match the PRD descriptions.

## Optional Pencil Path

Offer Pencil enhancement only after the HTML prototype is usable, or when the user asks for high-fidelity design. If Pencil is used:

- Confirm Pencil is running and the MCP connection is available.
- Keep HTML and Pencil color/spacing decisions synchronized.
- Use Pencil screenshots as visual validation, but keep the HTML prototype as the PRD iframe source.

## Output Structure

```text
需求文档/                 PRD HTML
原型/                     interactive prototype HTML and optional .pen
原型截图/                  exported PNG screenshots
流程图/                    flowchart HTML
数据分析/                  data analysis reports
验收清单/                  acceptance checklists
需求挖掘/                  demand analysis reports
scripts/                  prototype export service
.handoff/                 cross-session handoff files
.agents/workflows/        editable workflow definitions
```

## Customization

Edit `.agents/workflows/*.md` for project-specific behavior. Edit the bundled files under `.agents/skills/edu-pm-workflow/assets/workflows/` only when changing the reusable skill template for future installs.
