---
name: edu-pm-workflow
description: "Education PM workflow for producing PRDs, interactive HTML prototypes, flowcharts, acceptance checklists, demand analysis, and data reports for education-product work. Use when the user describes an education product requirement, asks for PRD/prototype/flowchart/checklist/data-analysis output, or wants to continue this PM workflow."
user-invocable: true
---

# Education PM Workflow Skill

This skill turns education product requirements into working artifacts: PRD HTML, interactive prototype HTML, flowchart HTML, acceptance checklist, demand analysis, and data reports.

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

Artifacts are organized **per requirement**: each requirement gets ONE top-level folder named after it (`[需求名]/`), holding up to seven artifact subfolders — `需求文档/ 原型/ 流程图/ 原型截图/ 需求挖掘/ 验收清单/ 数据分析/` plus `沟通记录.md`. `scripts/`, `启动原型导出服务.command`, `.handoff/`, `关键点.md`, `.agents/` stay at the project root and are shared across requirements.

**Folder ownership (applies to ALL four workflows):** Whichever workflow runs first creates `[需求名]/`. Before writing, every workflow first checks whether `[需求名]/` already exists — if so it reuses that folder and drops its output into the matching subfolder; if not it creates `[需求名]/`. PRD is **not** assumed to come first: a requirement may begin with demand discovery or data analysis, and all later steps reuse the same `[需求名]/`. Only create the subfolders actually used — never pre-create empty ones. Use an identical `[需求名]` across every workflow so all outputs land in one folder.

| User intent | Read this file first | Primary output |
|---|---|---|
| New requirement, PRD, prototype, flowchart, continue PRD work | `.agents/workflows/edu-pm-prd.md` | `[需求名]/需求文档/[需求名]-PRD.html`, `[需求名]/原型/[需求名]-prototype.html`, `[需求名]/流程图/[需求名]-flow.html` |
| Demand discovery, user needs, competitive/product insight | `.agents/workflows/edu-pm-demand.md` | `[需求名]/需求挖掘/[需求名]-需求洞察.html` |
| Acceptance checklist, test checklist, launch verification | `.agents/workflows/edu-pm-acceptance.md` | `[需求名]/验收清单/[需求名]-验收清单.html` |
| Metrics, BI-style analysis, report from data | `.agents/workflows/edu-pm-data-analysis.md` | `[需求名]/数据分析/[需求名]-数据分析.html` |

For PRD work, treat `.agents/workflows/edu-pm-prd.md` as the authoritative project workflow. Do not use root-level `edu-pm-prd.md` if both exist.

## PRD Workflow Rules

- Confirm the requirement before writing when core information is missing; ask only focused questions.
- **Tailor PRD sections to the requirement's size — do not force all sections.** Core skeleton always kept: 项目信息+版本记录, 需求背景, 需求目标, 详细方案. The other six (需求概述/流程图/异常边界/数据埋点/上线计划/附录) are dropped when the requirement doesn't need them (e.g. a tiny copy tweak needs no flowchart). Never drop sections silently — state which sections are kept/dropped and why during requirement confirmation, and get user sign-off first. If 流程图 is dropped, skip producing the flowchart file too. See edu-pm-prd.md §2.2 and §1.3.1.
- Produce HTML artifacts, not Markdown artifacts, unless the user asks otherwise.
- Keep PRD, prototype, and flowchart synchronized. When one changes, inspect the other two for necessary updates.
- The HTML prototype is the primary interactive artifact. Pencil is optional visual enhancement only.
- Use the local PNG export service through `scripts/prototype-export-client.js`; do not build new `html2canvas`/`html-to-image` exporters.
- Before delivery, verify scripts render and the prototype pages match the PRD descriptions.

## Optional Pencil Path

Offer Pencil enhancement only after the HTML prototype is usable, or when the user asks for high-fidelity design. If Pencil is used:

- Confirm Pencil is running and the MCP connection is available.
- Keep HTML and Pencil color/spacing decisions synchronized.
- Use Pencil screenshots as visual validation, but keep the HTML prototype as the PRD iframe source.

## Output Structure

Per-requirement folders at the project root; shared tooling stays at root.

```text
[需求名]/                  one top-level folder per requirement
  需求文档/                  PRD HTML
  原型/                     interactive prototype HTML and optional .pen
  原型截图/                  exported PNG screenshots (this requirement)
  流程图/                    flowchart HTML
  数据分析/                  data analysis reports (created on demand)
  验收清单/                  acceptance checklists (created on demand)
  需求挖掘/                  demand analysis reports (created on demand)
  沟通记录.md                per-requirement conversation log

scripts/                  [shared] prototype export service
启动原型导出服务.command     [shared] double-click to start PNG export service
.handoff/                 [shared] cross-session handoff files
.agents/workflows/        [shared] editable workflow definitions
```

## Customization

Edit `.agents/workflows/*.md` for project-specific behavior. Edit the bundled files under `.agents/skills/edu-pm-workflow/assets/workflows/` only when changing the reusable skill template for future installs.
