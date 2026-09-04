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
| New requirement, PRD, prototype, flowchart, continue PRD work | `.agents/workflows/edu-pm-prd.md` | `[需求名]/需求文档/[需求名]-PRD.html`, `[需求名]/原型/[需求名]-prototype.html`, `[需求名]/流程图/[需求名]-flow.html`, `[需求名]/流程图/[需求名]-screenflow.html` (交互流程图, as needed) |
| Demand discovery, user needs, competitive/product insight | `.agents/workflows/edu-pm-demand.md` | `[需求名]/需求挖掘/[需求名]-需求洞察.html` |
| Acceptance checklist, test checklist, launch verification | `.agents/workflows/edu-pm-acceptance.md` | `[需求名]/验收清单/[需求名]-验收清单.html` |
| Metrics, BI-style analysis, report from data | `.agents/workflows/edu-pm-data-analysis.md` | `[需求名]/数据分析/[需求名]-数据分析.html` |

For PRD work, treat `.agents/workflows/edu-pm-prd.md` as the authoritative project workflow. Do not use root-level `edu-pm-prd.md` if both exist.

## PRD Workflow Rules

- Confirm the requirement before writing when core information is missing; ask only focused questions.
- **Tailor PRD sections to the requirement's size — do not force all sections.** Core skeleton always kept: 项目信息+版本记录, 需求背景, 需求目标, 详细方案. The other eight (需求概述/流程图/时序图/交互流程图/异常边界/数据埋点/上线计划/附录) are dropped when the requirement doesn't need them (e.g. a tiny copy tweak needs no flowchart). Never drop sections silently — state which sections are kept/dropped and why during requirement confirmation, and get user sign-off first. If 流程图 is dropped, skip producing the flowchart file; if 交互流程图 is dropped, skip producing the screenflow file. See edu-pm-prd.md §2.2 and §1.3.1.
- **详细方案 description cells use the structured block format** (§2.3.1): 【页面元素】and【交互说明】are mandatory per row;【功能逻辑】【边界说明】【数据与内容规则】【前置条件与权限】【文案规范】only when applicable. Absolutely no technical API/interface wording anywhere in description cells.
- **时序图 (sequence diagram)** is an optional dev/QA-facing PRD chapter placed AFTER 数据埋点 (the last body chapter): copyable **Mermaid source-code text blocks — never rendered images or iframes** (devs/QA reuse the text directly; a rendered picture was rejected). Contains an end-side orchestration `sequenceDiagram` (real participants, e.g. 用户/端/Cocos/服务端) plus a key-object `stateDiagram-v2`, each block with a "复制源码" button and 说明 bullets. Technical field/interface names ARE allowed in this chapter (the §2.3.1 ban only covers 详细方案 description cells). See edu-pm-prd.md §4.7.
- **交互流程图 (screen flow)** is an optional PRD chapter placed before 详细方案: one whole image-style HTML canvas stitching all core screens (scaled live prototype iframes) with labeled **right-angle (Manhattan-routed) arrows** for navigation — never bezier curves or diagonal lines; same-side loop-back edges run on offset rails — plus an explicit state-machine legend. Produce per edu-pm-prd.md §4.6; export via the local screenshot service.
- Produce HTML artifacts, not Markdown artifacts, unless the user asks otherwise.
- Keep PRD, prototype, and flowchart synchronized. When one changes, inspect the other two for necessary updates.
- The HTML prototype is the primary interactive artifact. Pencil is optional visual enhancement only.
- Use the local PNG export service through `scripts/prototype-export-client.js`; do not build new `html2canvas`/`html-to-image` exporters.
- **「一键复制全文」must turn prototype iframes into inline base64 images** via `POST /api/snapshot` on that same local service (cache-first, auto re-render on stale) — never `iframe.remove()`, which silently drops every prototype from the pasted document. Under `file://` the browser blocks both local `fetch` and canvas readback, so base64 can only come from the service; do not add a front-end screenshot library for this. Degrade in three explicit tiers and always tell the user what was lost. See edu-pm-prd.md §2.8.
- **When pasted images look blurry, raise `MAX_IMG_WIDTH` — do not touch the encoder.** Measured on real assets: JPEG .85, JPEG .95, lossless PNG and WebP .92 are indistinguishable once all four are downsampled to 1200px; the detail is lost in the resize, not the compression. Ship 2000px at quality 0.9. Verify by zooming a pasted image past 1000px — at the default in-document width (≈335px, fixed to the table's 原型 column) every resolution looks identical, so "looks fine pasted" proves nothing. Report clipboard size as the base64 payload (1.33× the decoded bytes), not the decoded bytes. See edu-pm-prd.md §2.8 ⑤.
- **`原型截图/` is the PM's asset folder, not the tool's scratch folder.** When an export run clears "last round's output", delete only the filenames this HTML registered in `.export-manifest.json` — never glob `*.png`. That glob has already wiped 8 hand-made screenshots (captured state-by-state from `[需求名]-shots.html` and hand-named, referenced directly by the PRD's 原型 column) during an export of a `-prototype.html` that produced a single image. Those PNGs are not in git. See edu-pm-prd.md §4.4 item 6.
- **The dual-pane preview must ship zoom controls** (`－ / % / ＋ / 适配`, same control group as §4.6), keeping `previewZoom` in a JS variable only — never written into the DOM, so saved/copied output stays clean. See edu-pm-prd.md §2.6 ⑨.
- **Anything the PRD does over `http://` must survive an insecure context.** On the intranet `navigator.clipboard`, `ClipboardItem` and `showSaveFilePicker` do not exist: copy paths need an `execCommand` fallback and save degrades to downloading a copy. The export service must resolve the calling page by project-relative path too, or `/api/snapshot` and `/api/asset` return 400 and 一键复制全文 silently loses every image. See edu-pm-prd.md §2.9.
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
  流程图/                    flowchart HTML + screenflow (交互流程图) HTML
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
