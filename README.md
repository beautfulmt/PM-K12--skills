# Edu PM Workflow Skills

`edu-pm-workflow` 是一套面向教育产品经理的 Codex skill，用来把一句需求描述逐步落成可评审、可截图、可持续迭代的产品交付物。

## Core Features

- **PRD 生产**：输出可直接评审的 HTML PRD，详细方案单元格支持浏览器内编辑。
- **保存并通知 AI**：PRD 点击保存后通过本地服务把浏览器 DOM 写回原 HTML 文件，AI 后续读取磁盘内容即可按用户手写改动同步原型和流程图。
- **交互原型**：输出单文件 HTML 原型，支持 hash 跳转、平铺预览、iframe 嵌入和真实渲染 PNG 导出。
- **流程图**：输出 Mermaid 流程图 HTML，并单独导出高清截图到 `流程图截图/`。
- **需求挖掘**：输出教育产品需求洞察报告，覆盖用户场景、痛点、价值与策略建议。
- **验收清单**：输出可浏览器勾选的验收 checklist，方便联调和上线前回归。
- **数据分析**：输出带表格、指标、图表和结论的数据分析报告。
- **Pencil 可选增强**：保留 Pencil MCP 配置和稳定连接脚本，用于需要高保真设计稿时接入。

## Stability Improvements

- **本地保存写回**：`prd-save-client.js` 调用 `prototype_server.py` 的 `/api/save-html`，避免浏览器只下载副本却没有覆盖原 PRD 文件。
- **按需启动服务**：`prototype_launcher.py` 常驻 8766 端口，只有保存/导出时才拉起 8765 的完整服务。
- **高清导出**：原型和流程图通过 Playwright 真实渲染截图，不再依赖 `html2canvas` / `html-to-image`。
- **Pencil MCP 稳定连接**：`pencil-mcp-wrapper.sh` 探活 Pencil desktop socket、清理残留进程、必要时拉起 Pencil，再接入官方 MCP server。

## Installed Project Shape

运行 `scripts/init.sh` 后，目标项目会获得：

- `.agents/workflows/*.md`：PRD、需求挖掘、验收清单、数据分析工作流规范。
- `scripts/prototype_server.py`：本地 HTML 服务，提供预览、截图导出、PRD 写回。
- `scripts/prd-save-client.js`：PRD 浏览器编辑保存客户端。
- `scripts/prototype-export-client.js`：原型/流程图截图导出客户端。
- `启动原型导出服务.command`：手动启动本地服务的 macOS 双击入口。

## Repository Scope

这个仓库只存 skill 本体：

- `SKILL.md`
- `scripts/`
- `assets/workflows/`
- `assets/scripts/`
- `assets/templates/`
- `assets/config/`

不包含任何具体项目的 PRD、原型 HTML、流程图 HTML、截图或分享包产物。
