# Edu PM Workflow Skills

`edu-pm-workflow` 是一套面向教育产品经理的 Codex skill，用来把一句需求描述逐步落成可评审、可截图、可持续迭代的产品交付物。

## Core Features

- **PRD 生产**：输出可直接评审的 HTML PRD。章节**按需求大小裁剪**——核心骨架（项目信息+版本记录 / 需求背景 / 需求目标 / 详细方案）恒定保留，其余 8 个（需求概述 / 流程图 / 交互流程图 / 异常边界 / 数据埋点 / 时序图 / 上线计划 / 附录）按需省略；裁剪前会先列出保留/省略哪些章节并征得确认。
- **详细方案结构化分块**：描述列固定用【页面元素】【交互说明】（每行必出）+【功能逻辑】【边界说明】【数据与内容规则】【前置条件与权限】【文案规范】（按需出），并硬性禁止描述列出现任何技术接口表述（API / 参数 / 字段 key / 错误码）。
- **交互流程图（Screen Flow）**：可裁剪章节，把所有核心界面拼成一整张带跳转箭头的画布——界面节点用缩放 iframe 引真实原型页（原型改动自动同步），箭头一律直角折线（Manhattan 路由），带状态机图例与缩放/拖拽控件，可整张导出 PNG。
- **时序图**：可裁剪章节（研发/测试向，置于正文最后），产出**可复制的 Mermaid 源码文本块**（端侧编排 `sequenceDiagram` + 关键对象 `stateDiagram-v2`），研发照文本写逻辑、测试照文本写用例。
- **右侧双栏交互原型预览**：PRD 内建常驻可切页原型 dock，支持滚动联动 scroll-spy——左侧正文滚到某模块，右侧预览自动跟随切页，并提供 －/％/＋/适配 缩放控件放大查看细节。
- **全文档可编辑 + 一键复制**：正文全篇 `contenteditable`、全表增删行、列宽/行高拖拽；左下角「📋 一键复制全文」按钮；右下角「💾 保存并通知AI」按钮抓取 `outerHTML` 经系统文件句柄物理覆盖原 PRD 文件，AI 后续读取磁盘即可按用户手写改动同步原型和流程图。
- **一键复制全文自动带原型图**：右侧原型/流程图 iframe 复制时经本地导出服务转成内联 base64 图片（首次生成、之后按文件修改时间缓存命中秒出）；服务不可用或部分页生成失败会在提示里如实说明缺了几张，不静默丢图；图片默认 2000px / 质量 0.9，兼顾清晰度与体积。
- **交互原型**：输出单文件 HTML 原型，支持 hash 跳转、平铺预览、iframe 嵌入和真实渲染 PNG 导出。
- **流程图**：输出 Mermaid 流程图 HTML，并单独导出高清截图到 `流程图截图/`。
- **需求挖掘**：输出教育产品需求洞察报告，覆盖用户场景、痛点、价值与策略建议。
- **验收清单**：输出可浏览器勾选的验收 checklist，方便联调和上线前回归。
- **数据分析**：输出带表格、指标、图表和结论的数据分析报告。
- **Pencil 可选增强**：保留 Pencil MCP 配置示例，用于需要高保真设计稿时接入。

## Stability Improvements

- **按需启动服务**：`prototype_launcher.py` 常驻 8766 端口，只有保存/导出时才拉起 8765 的完整服务，并自举 venv。
- **高清导出**：原型、流程图、交互流程图通过 Playwright 真实渲染截图，不再依赖 `html2canvas` / `html-to-image`。
- **导出统一走服务**：所有 `.export-btn` 由 `prototype-export-client.js` 拦截交给本地服务，截图落到所属需求目录的一级截图目录。
- **兼容内网 http 环境**：`navigator.clipboard` / `showSaveFilePicker` 缺失时自动降级（`execCommand` 复制、下载副本保存），导出服务按项目相对路径兜底解析调用页，避免纯 http 内网访问时功能大面积失效。

## Installed Project Shape

运行 `scripts/init.sh` 后，目标项目会获得（仅创建共享目录，产物目录写需求时按需创建）：

- `.agents/workflows/*.md`：PRD、需求挖掘、验收清单、数据分析工作流规范。
- `scripts/prototype_server.py`：本地 HTML 服务，提供预览、截图导出、PRD 写回。
- `scripts/prototype_launcher.py`：轻量 launcher，按需拉起完整服务。
- `scripts/prototype-export-client.js`：原型/流程图截图导出客户端。
- `scripts/pencil-draw-prompt.md`：Pencil 高保真绘制提示词模板。
- `关键点.md`：版本演进与踩坑记录。
- `.mcp.json.example`：Pencil MCP 配置示例（需要时复制成 `.mcp.json`）。
- `启动原型导出服务.command`：手动启动本地服务的 macOS 双击入口。

## Output Layout（产物按需求名组织）

产物**按「需求名」分文件夹**：每个需求一个顶层目录，自己的产物作为子目录收纳其中。任何工作流（需求挖掘 / PRD / 验收 / 数据分析）开工前先查同名目录——已存在则复用，不存在则新建；**谁先开工谁建家**，不假设 PRD 先行。

```
项目根/
├── [需求名]/                  # 一个需求一个顶层目录
│   ├── 需求文档/[需求名]-PRD.html
│   ├── 原型/[需求名]-prototype.html
│   ├── 流程图/[需求名]-flow.html + [需求名]-screenflow.html
│   ├── 原型截图/              # 该需求导出的 PNG
│   ├── 需求挖掘/ 验收清单/ 数据分析/   # 用到才建
│   └── 沟通记录.md
├── scripts/                  # 共享：本地服务与导出客户端
├── 启动原型导出服务.command     # 共享
├── .handoff/                 # 共享：会话交接
└── .agents/workflows/        # 共享：工作流规范
```

> 导出服务对新嵌套结构与旧扁平结构均兼容：原型/流程图截图自动输出到所属需求目录下的 `原型截图/`、`流程图截图/`（旧扁平结构回退到项目根）。

## Repository Scope

这个仓库只存 skill 本体：

- `SKILL.md`
- `scripts/`
- `assets/workflows/`
- `assets/scripts/`
- `assets/templates/`
- `assets/config/`

不包含任何具体项目的 PRD、原型 HTML、流程图 HTML、截图或分享包产物。
