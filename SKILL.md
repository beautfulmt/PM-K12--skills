---
name: edu-pm-workflow
description: "Product management workflow for producing PRDs, interactive HTML prototypes, flowcharts, acceptance checklists, demand analysis, and data reports. Use when the user describes a product requirement, asks for PRD/prototype/flowchart/checklist/data-analysis output, or wants to continue this PM workflow."
user-invocable: true
---

# PM Workflow Skill

This skill turns product requirements into working artifacts: PRD HTML, interactive prototype HTML, flowchart HTML, acceptance checklist, demand analysis, and data reports. It is designed for product work across different business domains and product types.

## First Decision

1. If `.agents/workflows/` exists, do not re-initialize. Read the relevant workflow file and continue from the current project state.
2. If `.agents/workflows/` or required scripts are missing, install this skill into the project once (command below).
3. If the user explicitly asks to reinstall or update the workflow, run the same command. Runtime scripts are always refreshed; files the user has edited are kept and the new version is written to `.pm-workflow/updates/` for comparison. Replaced copies are backed up under `.handoff/skill-backups/`.

Install / update — run `scripts/initialize.py` with the platform's Python. It is the single cross-platform installer; `scripts/init.sh` and `scripts/init.bat` are only thin wrappers around it for users who prefer a double-click.

```bash
# macOS / Linux
python3 <skill-dir>/scripts/initialize.py --project .
```

```bat
rem Windows (py is the official launcher; there is no python3 command)
py -3 <skill-dir>\scripts\initialize.py --project .
```

Locating `<skill-dir>`: use your file-search tool (Glob/Grep) for `**/edu-pm-workflow/scripts/initialize.py` across the project and the user's skill directories (`.agents/skills`, `~/.agents/skills`, `~/.claude/skills`, `~/.cursor/skills`). Do **not** shell out to `find` — on Windows `find` is `System32\find.exe`, a text-search tool that takes entirely different arguments, so the discovery step itself would fail before installation ever starts.

## Workflow Routing

Load only the workflow needed for the user's current request:

Artifacts are organized **per requirement**: each requirement gets ONE top-level folder named after it (`[需求名]/`), holding up to seven artifact subfolders — `需求文档/ 原型/ 流程图/ 原型截图/ 需求挖掘/ 验收清单/ 数据分析/` plus `沟通记录.md`. `scripts/`, the two start-service entries (`启动原型导出服务.command` on macOS, `启动原型导出服务.bat` on Windows), `.handoff/`, `关键点.md`, `.agents/` stay at the project root and are shared across requirements.

**Folder ownership (applies to ALL four workflows):** Whichever workflow runs first creates `[需求名]/`. Before writing, every workflow first checks whether `[需求名]/` already exists — if so it reuses that folder and drops its output into the matching subfolder; if not it creates `[需求名]/`. PRD is **not** assumed to come first: a requirement may begin with demand discovery or data analysis, and all later steps reuse the same `[需求名]/`. Only create the subfolders actually used — never pre-create empty ones. Use an identical `[需求名]` across every workflow so all outputs land in one folder.

| User intent | Read this file first | Primary output |
|---|---|---|
| New requirement, PRD, prototype, flowchart, continue PRD work | `.agents/workflows/edu-pm-prd.md` | `[需求名]/需求文档/[需求名]-PRD.html`, `[需求名]/原型/[需求名]-prototype.html`, `[需求名]/流程图/[需求名]-flow.html`, `[需求名]/流程图/[需求名]-screenflow.html` (交互流程图, as needed) |
| Demand discovery, user needs, competitive/product insight | `.agents/workflows/edu-pm-demand.md` | `[需求名]/需求挖掘/[需求名]-需求洞察.html` |
| Acceptance checklist, test checklist, launch verification | `.agents/workflows/edu-pm-acceptance.md` | `[需求名]/验收清单/[需求名]-验收清单.html` |
| Metrics, BI-style analysis, report from data | `.agents/workflows/edu-pm-data-analysis.md` | `[需求名]/数据分析/[需求名]-数据分析.html` |

For PRD work, treat `.agents/workflows/edu-pm-prd.md` as the authoritative project workflow. Do not use root-level `edu-pm-prd.md` if both exist.

## PRD Workflow Rules

- **Confirm the requirement before writing when core information is missing; ask only focused questions.** The six-dimension completeness check has a **材料** dimension (§1.2): ask once for the tracking dictionary, design spec / brand accent, and any existing prototype screenshots — finding out at §数据埋点 that no dictionary exists means interrupting the user mid-draft or inventing field names.
- **Carry the confirmation into the document.** §1.4 maps each confirmed item to its PRD location: 核心改动 → 功能清单+详细方案; 成功指标 → 需求目标表; **不做 / 范围外 → 需求概述的「范围块」**; 背景证据 → 需求背景三段式; 跨页规则 → 需求概述规则表; 待确认项 → 正文末尾清单. A "不做" that was agreed verbally but never written into the PRD does not count as confirmed.
- **Copy `assets/templates/prd-content.html` and fill it in — do not hand-write the HTML skeleton.** That file already carries the right class names, table headers, `colgroup` widths, `.desc-block` structure and `data-preview` placeholders; nearly every historical defect (descriptions using `<br>` instead of `<p>`, wrong column counts, missing `colgroup`) came from rebuilding the structure from memory.
- **Run `assets/scripts/validate_prd.py` before delivery and report the result honestly.** It mechanically checks: core chapters present, 项目信息/版本记录 not merged, no standalone boundary chapter, continuous chapter numbering, all six table headers and column counts, meta-table is two-column, every 详细方案 row has `data-preview` and a non-empty 原型 cell, description cells use `.desc-block` with no `<br>` and no multi-number cramming, snake_case tracking names with six columns, `#prdContent` contains its own `<style>`, and the goal table header. A pass does NOT mean the document is good (visual and editorial quality still need human review) — but a failure means it is definitely not done.
- **Fixed chapter order, tailored to the requirement's size — do not force all sections.** Order is 项目信息 → 版本记录 → 需求背景 → 需求目标 → 需求概述 → 业务流程图 → 交互流程图 → 详细方案 → 数据埋点 → 时序图（上线计划/附录 only if genuinely needed）. Core skeleton always kept: 项目信息, 版本记录 (two separate tables — never merged), 需求背景, 需求目标, 详细方案. The other seven (需求概述/业务流程图/交互流程图/数据埋点/时序图/上线计划/附录) are dropped when the requirement doesn't need them. Never drop sections silently — state which are kept/dropped and why during requirement confirmation. If 业务流程图 is dropped, skip producing the flowchart file; if 交互流程图 is dropped, skip the screenflow file. See edu-pm-prd.md §2.2 and §1.3.1.
- **No standalone 异常/边界 chapter.** Boundary cases live in the owning row's 【边界说明】 block inside 详细方案 (§2.3.1), never as a document-level chapter.
- **需求目标 states the user outcome and how it is measured, not implementation actions.** Quantifiable goals go in a 用户结果/衡量指标/统计口径/预期方向/目标值 table; with no real baseline write 「待基线确认」 — never invent a percentage. Non-quantifiable goals must still be observable and verifiable. Same rule for numbers cited in 需求背景: give the source or mark it unconfirmed. See §2.2 ④.
- **The 原型 column accepts a high-res screenshot (`img.proto-shot` with real width/height, optionally linked to the clickable prototype) or an interactive iframe — do not convert existing screenshots into iframes.** See §2.3 and §3.3.
- **详细方案 description cells: two mandatory blocks, the rest by a written test — not by habit** (§2.3.1). 【页面元素】and【交互说明】are mandatory in every cell. For any optional block the test is: **"if this page were deleted, would the rule still hold?"** If yes, it is a cross-page rule and belongs in the 需求概述 rule table (§2.3.1 ③), not repeated in each cell — 签到 1/3/7-day reward tiers, cumulative score/quota accounting, grant timing, role-permission matrices and global rate limits are the usual offenders. If no, it belongs to this page. Typical symptoms of over-writing: the same shared rule copy-pasted into three cells, or four-plus blocks in one cell. 【功能逻辑】 in particular should carry only rules that stop being true when this page is gone. Also: never write "同上" / "详见 x.x" — a row gets copied into review documents on its own; never pad with "无"; every item is its own `<p>`/`<li>` inside a `.desc-block`; multiple numbered items crammed into one paragraph is a defect. Absolutely no technical API/interface wording in description cells.
- **One row = one screen or one state variant** (§2.2 ⑦). A 二级功能 spanning three screens becomes three rows, each with its own prototype asset; a screen's multiple states stay in one row and are enumerated in 【页面元素】. If you cannot name the single image the 原型 cell shows, the granularity is wrong.
- **需求概述 is more than a feature list** (§2.2 ⑤): it carries a **范围块** (本期范围 / 本期不做什么·暂不展开) plus the feature-list table plus, when needed, the cross-page rule tables (`h3` + small table). If the whole chapter is dropped for a small requirement, the 范围块 and rule tables must relocate — 功能清单 may go, but "what we are NOT doing" and the shared rules may not.
- **需求背景 is three parts** (§2.2 ⑥): who hits what problem in what scenario → what impact it has → what evidence supports it (state plainly when there is none; never invent). **需求目标** closes with a 「待后续确认的产品口径」 list collecting every 待确认 in the document, each with owner and impact.
- **The edit module ships undo/redo** (§2.7 ⑤): ⌘Z / Ctrl+Z undo, ⌘⇧Z / Ctrl+Y (also Ctrl+⇧Z) redo, covering text edits, row add/delete, table delete and column/row resize on one stack; a new edit clears the redo branch. Deleted rows/tables are kept alive as **DOM nodes** in the stack (not HTML strings) so restored controls still work, and the native contenteditable undo must be `preventDefault`ed in the capture phase or both stacks fire at once. History is memory-only — never promise it survives a refresh.
- **时序图 (sequence diagram)** is an optional dev/QA-facing PRD chapter placed AFTER 数据埋点 (the last body chapter): copyable **Mermaid source-code text blocks — never rendered images or iframes** (devs/QA reuse the text directly; a rendered picture was rejected). Contains an end-side orchestration `sequenceDiagram` (real participants, e.g. 用户/端/Cocos/服务端) plus a key-object `stateDiagram-v2`, each block with a "复制源码" button and 说明 bullets. Technical field/interface names ARE allowed in this chapter (the §2.3.1 ban only covers 详细方案 description cells). See edu-pm-prd.md §4.7.
- **交互流程图 (screen flow)** is an optional PRD chapter placed before 详细方案: one whole image-style HTML canvas stitching all core screens (scaled live prototype iframes) with labeled **right-angle (Manhattan-routed) arrows** for navigation — never bezier curves or diagonal lines; same-side loop-back edges run on offset rails — plus an explicit state-machine legend. Produce per edu-pm-prd.md §4.6; export via the local screenshot service.
- Produce HTML artifacts, not Markdown artifacts, unless the user asks otherwise.
- Keep PRD, prototype, and flowchart synchronized. When one changes, inspect the other two for necessary updates.
- The HTML prototype is the primary interactive artifact. Pencil is optional visual enhancement only.
- Use the local PNG export service through `scripts/prototype-export-client.js`; do not build new `html2canvas`/`html-to-image` exporters.
- **「一键复制全文」must turn prototype iframes into inline base64 images** via `POST /api/snapshot` on that same local service (cache-first, auto re-render on stale) — never `iframe.remove()`, which silently drops every prototype from the pasted document. Under `file://` the browser blocks both local `fetch` and canvas readback, so base64 can only come from the service; do not add a front-end screenshot library for this. Degrade in three explicit tiers and always tell the user what was lost. See edu-pm-prd.md §2.8.
- **When pasted images look blurry, raise `MAX_IMG_WIDTH` — do not touch the encoder.** Measured on real assets: JPEG .85, JPEG .95, lossless PNG and WebP .92 are indistinguishable once all four are downsampled to 1200px; the detail is lost in the resize, not the compression. Ship 2000px at quality 0.9. Verify by zooming a pasted image past 1000px — at the default in-document width (≈335px, fixed to the table's 原型 column) every resolution looks identical, so "looks fine pasted" proves nothing. Report clipboard size as the base64 payload (1.33× the decoded bytes), not the decoded bytes. See edu-pm-prd.md §2.8 ⑤.
- **`原型截图/` is the PM's asset folder, not the tool's scratch folder.** When an export run clears "last round's output", delete only the filenames this HTML registered in `.export-manifest.json` — never glob `*.png`. That glob has already wiped 8 hand-made screenshots (captured state-by-state from `[需求名]-shots.html` and hand-named, referenced directly by the PRD's 原型 column) during an export of a `-prototype.html` that produced a single image. Those PNGs are not in git. See edu-pm-prd.md §4.4 item 6.
- **The dual-pane preview is CLOSED by default** (§2.6). The PRD opens as plain readable prose; the panel appears only when the user clicks 双栏预览 (the toggle label flips to 收起预览), and the iframe `src` stays empty until first open so nothing loads in the background. A non-empty prototype folder is NOT a reason to auto-open. The only automatic open is an explicit `#preview=<page-id>` deep link.
- **The dual-pane preview must ship zoom controls** (`－ / % / ＋ / 适配`, same control group as §4.6), keeping `previewZoom` in a JS variable only — never written into the DOM, so saved/copied output stays clean. See edu-pm-prd.md §2.6 ⑨.
- **Business flowcharts must NOT use Mermaid's default theme** (§4.1). `theme:'default'` produces saturated blocks with white text that clash with the light PRD shell. Use `theme:'base'` with the fixed `themeVariables` block (near-white node fill `#faf9ff`, thin `#cbc4e7` border, dark `#30285b` text, `lineColor #8d82b1`), `flowchart.curve:'linear'` for right-angle connectors, `nodeSpacing:60`/`rankSpacing:70` as minimums, and the shared page shell (`#f8f8fc` body, white 14px-radius card). Distinguish node types by shape, not fill colour.
- **Zero text overlap is a hard gate for both diagrams, not a best effort** (§4.3 ②, §4.6 ③④). Fix order when the audit fails: enlarge the canvas → widen gaps → reroute/add rails → split into two canvases. Never fix overlap by shrinking type, hiding a label, deleting the offending branch, or using a background colour as a cover-up. Deliver only after the geometry audit returns `ok:true` AND you have looked at the diagram at 100% zoom both standalone and inside the PRD iframe — a diagram that is clean at 60% can still be overlapping when embedded. See §4.6 ④ for the audit snippet and the export-time guard that blocks shipping an overlapping diagram.
- **Anything the PRD does over `http://` must survive an insecure context.** On the intranet `navigator.clipboard`, `ClipboardItem` and `showSaveFilePicker` do not exist: copy paths need an `execCommand` fallback and save degrades to downloading a copy. The export service must resolve the calling page by project-relative path too, or `/api/snapshot` and `/api/asset` return 400 and 一键复制全文 silently loses every image. See edu-pm-prd.md §2.9.
- Before delivery, verify scripts render and the prototype pages match the PRD descriptions, and run `validate_prd.py`.

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
启动原型导出服务.command     [shared] macOS — optional manual start; normally the service
                                   auto-starts on the first export click (launchd socket activation)
启动原型导出服务.bat         [shared] Windows — double-click and keep the window open
.handoff/                 [shared] cross-session handoff files
.agents/workflows/        [shared] editable workflow definitions
.agents/skills/edu-pm-workflow/assets/
  templates/prd-content.html   PRD body skeleton — copy and fill, do not hand-write
  scripts/validate_prd.py      mechanical PRD validation — must pass before delivery
```

## Customization

Edit `.agents/workflows/*.md` for project-specific behavior. Edit the bundled files under `.agents/skills/edu-pm-workflow/assets/workflows/` only when changing the reusable skill template for future installs.
