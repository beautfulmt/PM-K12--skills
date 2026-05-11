# PM K12 Skills

`edu-pm-workflow` 是一套面向教育产品经理的工作流 skill，用来把一句需求描述逐步落成可交付产物。

## Core Features

- PRD 生产：输出可直接评审和截图的 HTML PRD
- 交互原型：输出单文件 HTML 原型，支持 hash 跳转、平铺预览、PNG 导出
- 流程图：输出 Mermaid 流程图 HTML，并支持高清截图导出
- 需求挖掘：输出需求洞察报告
- 验收清单：输出验收 checklist
- 数据分析：输出带图表的数据分析报告

## Stability Improvements

- Pencil MCP 稳定连接：
  通过 `scripts/pencil-mcp-wrapper.sh` 先探活 Pencil desktop socket、清理残留 MCP 进程、必要时拉起 Pencil，再接入官方 MCP server，减少 `failed to connect to running Pencil app: desktop after 3 retries` 这类连接问题。

- 高清导出：
  原型和流程图优先通过 `prototype_server.py` 走 Playwright 真实渲染导出。
  流程图截图单独输出到 `流程图截图/`，不再和原型导出混在 `原型截图/`。

## Repository Scope

这个仓库只存 skill 本体：

- `SKILL.md`
- `scripts/`
- `assets/workflows/`
- `assets/scripts/`
- `assets/templates/`
- `assets/config/`

不包含任何具体项目的 PRD、原型 HTML、流程图 HTML、截图或分享包产物。
