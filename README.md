# PM Workflow Skill

PM Workflow 是一套面向产品经理的通用工作流，用来把一句需求描述逐步落成可评审、可截图、可持续迭代的产品交付物。核心流程适用于不同业务领域和产品形态。

## Core Features

- **PRD 生产**：输出可直接评审的 HTML PRD。章节顺序固定为 项目信息 → 版本记录 → 需求背景 → 需求目标 → 需求概述 → 业务流程图 → 交互流程图 → 详细方案 → 数据埋点 → 时序图，**按需求大小裁剪**——核心骨架（项目信息 / 版本记录 / 需求背景 / 需求目标 / 详细方案）恒定保留，其余 7 个按需省略；不设独立的「异常与边界」章（边界一律进对应功能的【边界说明】）；裁剪前会先列出保留/省略哪些章节并征得确认。
- **先复制骨架，再跑校验**：`assets/templates/prd-content.html` 提供带正确类名、固定表头、`colgroup`、`.desc-block` 结构和 `data-preview` 占位的正文骨架，写 PRD 从复制它开始而不是从零手写；交付前跑 `assets/scripts/validate_prd.py` 做机械校验（核心章节、表头列数、编号连续、每行 `data-preview`、描述列分块与硬换行、埋点命名、正文样式位置等），红了先修再交。
- **需求目标 / 需求背景 / 需求概述有固定写法**：需求目标写"用户结果 + 衡量口径"的五列表，没有真实基线写「待基线确认」、不编数；需求背景三段式（谁·什么场景·什么问题 → 影响 → 证据）；需求概述带「本期范围 / 本期不做什么」范围块，把确认阶段说过的"不做"钉进文档，并承载跨页共享的规则表；正文末尾集中一份「待后续确认的产品口径」清单。
- **详细方案结构化分块**：一行 = 一个界面或一个状态变体；描述列固定用【页面元素】【交互说明】（每格必出）+【功能逻辑】【边界说明】【数据与内容规则】【前置条件与权限】【文案规范】【策略说明】（按需出）。按需块用一个问题判定该不该写——"把这一页删掉，这条规则还成立吗"：仍成立的是跨页链路规则，上提到需求概述的规则表只写一次，各格只引用，不再逐页抄；不写"无"、不写"同上"；每条独立成段；硬性禁止描述列出现任何技术接口表述（API / 参数 / 字段 key / 错误码）。
- **交互流程图（Screen Flow）**：可裁剪章节，把所有核心界面拼成一整张带跳转箭头的画布——界面节点用缩放 iframe 引真实原型页（原型改动自动同步），箭头一律直角折线（Manhattan 路由），带状态机图例与缩放/拖拽控件，可整张导出 PNG。**零遮挡是硬指标**：先按几何下限（同排 ≥70px、上下排 ≥200px、画布留白 ≥30px、回流轨道错峰）摆位，再用内置 `auditFlow()` 检测标签压节点 / 标签重叠 / 连线穿节点 / 越界并循环修复到通过，导出按钮在审计未过时直接拦截；推荐用内容反推画布尺寸，让越界从根上消失。
- **时序图**：可裁剪章节（研发/测试向，置于正文最后），产出**可复制的 Mermaid 源码文本块**（端侧编排 `sequenceDiagram` + 关键对象 `stateDiagram-v2`），研发照文本写逻辑、测试照文本写用例。
- **右侧双栏交互原型预览**：PRD 内建可切页原型 dock，**默认收起**（打开 PRD 是干净的阅读态，点「双栏预览」才展开，iframe 首次展开才加载），支持滚动联动 scroll-spy——左侧正文滚到某模块，右侧预览自动跟随切页，并提供 －/％/＋/适配 缩放控件放大查看细节。
- **全文档可编辑 + 撤销重做 + 一键复制**：正文全篇 `contenteditable`、全表增删行、列宽/行高拖拽；`⌘Z / Ctrl+Z` 撤销、`⌘⇧Z / Ctrl+Y` 重做，文字、增删行、删表、尺寸调整共用一个撤销栈（删掉的行/表恢复后按钮和手柄仍可用，新编辑清空重做分支，不承诺跨刷新保留）；左下角「📋 一键复制全文」按钮；右下角「💾 保存并通知AI」按钮抓取 `outerHTML` 经系统文件句柄物理覆盖原 PRD 文件，AI 后续读取磁盘即可按用户手写改动同步原型和流程图。
- **一键复制全文自动带原型图**：右侧原型/流程图 iframe 复制时经本地导出服务转成内联 base64 图片（首次生成、之后按文件修改时间缓存命中秒出）；服务不可用或部分页生成失败会在提示里如实说明缺了几张，不静默丢图；图片默认 2000px / 质量 0.9，兼顾清晰度与体积。
- **交互原型**：输出单文件 HTML 原型，支持 hash 跳转、平铺预览、iframe 嵌入和真实渲染 PNG 导出。
- **流程图**：输出 Mermaid 流程图 HTML，并单独导出高清截图到 `流程图截图/`。视觉固定为"浅底 · 细描边 · 深字 · 直角连线"（`theme:'base'` + 固定 `themeVariables`，`curve:'linear'`），与 PRD、交互流程图共用同一套主色与页面外壳，不再使用 Mermaid 默认主题的实心色块。
- **需求挖掘**：输出产品需求洞察报告，覆盖用户场景、痛点、价值与策略建议。
- **验收清单**：输出可浏览器勾选的验收 checklist，方便联调和上线前回归。
- **数据分析**：输出带表格、指标、图表和结论的数据分析报告。
- **Pencil 可选增强**：保留 Pencil MCP 配置示例，用于需要高保真设计稿时接入。

## Stability Improvements

- **macOS 上点导出即自动起服务**：不用先双击任何东西——点原型页的「一键导出」或 PRD 的「一键复制全文」，服务自己就起来了。靠的是 launchd 的 socket 激活：端口由系统持有，**空闲时本项目零进程**，有请求才拉起、起完自退。随安装默认注册，`bash scripts/install_launcher.sh --uninstall` 可随时卸掉。
- **一个双击入口，Mac / Windows 同源**：Windows 上（以及 macOS 上想手动起时）双击项目根的 `启动原型导出服务.bat` / `.command`，脚本自己找解释器、备好运行环境、起服务；保持窗口开着即可导图。两个入口都只是薄壳，实际逻辑在 `scripts/start_service.py` 一处。
- **端口按项目推导且可自愈**：端口由项目路径确定性推导到 20000–32767（避开系统临时端口段与 Windows 的 Hyper-V/WSL 保留块），一台机器上多个项目各用各的端口、互不抢占；启动时端口被占就自动换一个并回写配置，不会卡死在"端口已被使用"。
- **运行环境跨项目共享，不落项目目录**：Python venv 放在用户目录（`~/Library/Application Support/pm-workflow/` / `%LOCALAPPDATA%\pm-workflow\`），避免项目在 OneDrive/iCloud 里被同步、以及 Windows 路径超长。截图引擎优先复用系统已装的 Edge / Chrome，**正常情况零下载**，没有才回落 Playwright 自带 Chromium。
- **`--doctor` 自检**：`python3 scripts/start_service.py --doctor`（Windows 用 `py -3`）一次打印解释器、运行环境、浏览器引擎、端口实测、配置与代理变量，排查问题不用来回试。
- **自动启动不留常驻进程**：macOS 的按需启动器按项目注册（多个项目互不覆盖），plist 里只有 `Sockets`、没有 `RunAtLoad`/`KeepAlive`，所以它不是守护进程——空闲时 `ps` 里找不到任何本项目的东西，端口却照样应答。启动器端口固定不随自愈漂移，避免注册信息过期后自动启动静默失效。
- **高清导出**：原型、流程图、交互流程图通过 Playwright 真实渲染截图，不再依赖 `html2canvas` / `html-to-image`。
- **导出统一走服务**：所有 `.export-btn` 由 `prototype-export-client.js` 拦截交给本地服务，截图落到所属需求目录的一级截图目录。
- **兼容内网 http 环境**：`navigator.clipboard` / `showSaveFilePicker` 缺失时自动降级（`execCommand` 复制、下载副本保存），导出服务按项目相对路径兜底解析调用页，避免纯 http 内网访问时功能大面积失效。

## 安装与启动

### 一、装进项目（只需一次）

安装器是 `scripts/initialize.py`，Mac 和 Windows 共用同一份代码。三种用法任选：

| 平台 | 做法 |
|---|---|
| macOS / Linux | 在项目目录执行 `bash /路径/到/edu-pm-workflow/scripts/init.sh` |
| Windows | 在项目目录执行 `\路径\到\edu-pm-workflow\scripts\init.bat`（或在资源管理器里双击它，它会装到当前目录） |
| 任意平台 | `python3 /路径/到/scripts/initialize.py --project .`（Windows 换 `py -3`） |

重复执行是安全的：服务运行时代码每次都刷到最新（旧版留在 `.handoff/skill-backups/`），你改过的 workflow 说明书会保留，新版写到 `.pm-workflow/updates/` 供你对照合并。

### 二、启动导出服务

**macOS：什么都不用做。** 直接打开原型或 PRD 点导出，服务会自动启动（安装时已注册按需启动器）。想手动起也行，双击 `启动原型导出服务.command` 效果一样。

**Windows：双击 `启动原型导出服务.bat`，保持那个窗口开着**，然后打开原型/流程图页点导出。

首次启动会自动准备运行环境（装 Playwright、探测可用浏览器），大约一两分钟；之后每次都是秒开。

没装 Python 的话，入口脚本会停在窗口里告诉你去 <https://www.python.org/downloads/> 装 3.9+（Windows 安装时务必勾选 **Add python.exe to PATH**）。

### 三、出问题时

```bash
python3 scripts/start_service.py --doctor      # Windows: py -3 scripts\start_service.py --doctor
```

一次打印解释器、运行环境、浏览器引擎、端口实测、配置状态和代理变量。

### 四、按需启动器（仅 macOS，随安装默认注册）

```bash
bash scripts/install_launcher.sh               # 重新注册（换过端口、或装的时候失败了）
bash scripts/install_launcher.sh --uninstall   # 卸载
```

它让「点导出自动起服务」成立，但**不是常驻进程**：plist 里只给 `Sockets`，端口交给 launchd 持有，浏览器一连上来才把启动器拉起，起完服务就自退。空闲时本项目在 `ps` 里一个进程都没有。正因为不留常驻，才敢随安装默认装上。

卸掉之后导出功能照常，只是要先双击 `启动原型导出服务.command`。装的时候若因权限等原因注册失败，安装器只会警告、不会中断，同样回退到手动双击。

Windows 不需要它：服务本体就是你开着的那个窗口，没有东西需要被拉起。

## Installed Project Shape

安装后目标项目会获得（仅创建共享目录，产物目录写需求时按需创建）：

- `.agents/workflows/*.md`：PRD、需求挖掘、验收清单、数据分析工作流规范。
- `scripts/start_service.py`：服务启动入口（`--check` / `--serve` / `--doctor`）。
- `scripts/pm_bootstrap.py`：解释器探测、运行环境准备、浏览器引擎探测、子进程拉起。
- `scripts/pm_runtime.py`：项目标识与端口推导、配置读写、健康检查。
- `scripts/prototype_server.py`：本地 HTML 服务，提供预览、截图导出、PRD 写回。
- `scripts/prototype_launcher.py`：轻量 launcher，收到浏览器请求后拉起完整服务；macOS 上由 launchd socket 激活，起完自退。
- `scripts/pm_launchagent.py`：macOS 按需启动器的注册/卸载/状态查询（LaunchAgent plist 的唯一写入方）。
- `scripts/prototype-export-client.js`：原型/流程图截图导出客户端。
- `scripts/install_launcher.sh`：macOS 按需启动器的安装/卸载脚本（安装时已默认注册，这里是重注册与卸载入口）。
- `scripts/pencil-draw-prompt.md`：Pencil 高保真绘制提示词模板。
- `scripts/prd-content.html`：PRD 正文骨架，写 PRD 先复制它（源在 skill 的 `assets/templates/`）。
- `scripts/validate_prd.py`：PRD 机械校验，交付前必跑（源在 skill 的 `assets/scripts/`）。
- `关键点.md`：版本演进与踩坑记录。
- `.mcp.json.example`：Pencil MCP 配置示例（需要时复制成 `.mcp.json`）。
- `启动原型导出服务.command` / `启动原型导出服务.bat`：启动本地服务的双击入口（macOS / Windows）。
- `.pm-workflow/`：本项目的运行配置与安装清单，已自动写进 `.gitignore`（含机器相关信息，不该提交）。

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
├── 启动原型导出服务.command     # 共享：macOS 手动启动（通常不用，点导出会自动起）
├── 启动原型导出服务.bat         # 共享：Windows 双击启动，保持窗口开着
├── .handoff/                 # 共享：会话交接
├── .pm-workflow/             # 共享：运行配置（已 gitignore）
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
