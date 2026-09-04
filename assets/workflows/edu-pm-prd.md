---
description: 教育PM需求产出工作流 — 输入需求描述，产出PRD+原型+流程图
---

# 教育PM需求产出工作流

## 触发方式

当用户提供一个需求描述时，按以下步骤产出标准化交付物。

---

## 需求目录归属规则（所有步骤的前置约定 · 极度重要）

> **铁律：产物一律按「需求名」收纳到同一个顶层文件夹里，谁先开工谁负责建这个文件夹，后续步骤一律复用它，不再另起。**

1. **开工前先查同名目录**：任何一步（需求采集/PRD/原型/流程图，乃至需求挖掘、验收、数据分析）真正落盘前，先看项目根目录下是否已存在该需求的同名文件夹 `[需求名]/`。
   - **已存在** → 直接复用，把本步产出放进它对应的子目录（如 `[需求名]/需求文档/`、`[需求名]/原型/`）。
   - **不存在** → 以需求名新建顶层文件夹 `[需求名]/`，再在其下建本步需要的子目录。
2. **谁先做谁建家**：本工作流不假设一定先有 PRD。若用户先做的是需求挖掘或数据分析，则由那一步首次创建 `[需求名]/`；之后做 PRD/原型/流程图时复用同一个 `[需求名]/`，所有产物都收在这一个需求目录内，不重复另建。
3. **子目录用到才建**：一个需求目录下最多包含这 7 类子目录 —— `需求文档/ 原型/ 流程图/ 原型截图/ 需求挖掘/ 验收清单/ 数据分析/`，外加 `沟通记录.md`。**只创建当前步骤实际用到的子目录**，不预建空文件夹。
4. **共享资源不进需求目录**：`scripts/`、`启动原型导出服务.command`、`.handoff/`、`关键点.md`、`.mcp.json`、`.agents/` 为所有需求共享，始终留在项目根目录。
5. **需求名一致性**：同一需求在所有工作流中使用**完全相同**的 `[需求名]`，确保各步产出归入同一文件夹；命名有歧义时先与用户确认。

---

## 步骤一：对话式需求采集与确认

采用「灵活对话式」而非固定模板：用户自由描述需求，AI主动评估、追问、确认。

### 1.1 接收需求

- 用户可以用**任意形式**输入需求：一句话、一段描述、截图、语音转文字均可
- 不要求用户填写固定模板，降低输入门槛

### 1.2 信息完整度评估

收到需求后，AI对照以下 **6个关键维度** 评估信息完整度：

| 维度 | 说明 | 重要程度 |
|------|------|----------|
| **问题/背景** | 为什么要做？现状数据是什么？ | ⭐⭐⭐ 必须 |
| **目标** | 做了之后要达成什么？量化指标？ | ⭐⭐⭐ 必须 |
| **用户与场景** | 谁在什么场景下使用？课前/课中/课后？ | ⭐⭐⭐ 必须 |
| **现有方案** | 当前做法是什么？有何不足？ | ⭐⭐ 重要 |
| **业务规则** | 核心规则和限制条件 | ⭐⭐ 重要 |
| **参考/方向** | 竞品参考、心中初步方案、设计稿草图 | ⭐ 加分 |

### 1.3 智能追问或确认

根据评估结果，采取两种策略：

**信息不足时 → 追问**
- 只追问缺失的关键维度，不重复已有信息
- 追问控制在 **3-5个问题** 以内，避免信息轰炸
- 问题要具体，不要问"还有什么要补充的吗"这种开放式问题
- 示例：
  > 了解了你要优化课后作业提交流程，再确认几点：
  > 1. 当前提交率大概多少？目标提升到多少？
  > 2. 作业类型有哪些？（选择题/主观题/拍照上传）
  > 3. 有没有参考的竞品做法？

**信息充足时 → 反向确认**
- 将理解到的需求**结构化复述**给用户
- 明确列出：要做什么、不做什么、关键规则、成功指标
- 请用户确认无误后再开始撰写
- 示例：
  > 和你确认下我的理解：
  > - **目标**：课后作业提交率 60% → 80%
  > - **范围**：学生端，课后场景
  > - **核心改动**：优化作业入口+增加提醒机制
  > - **不做**：不改作业批改流程
  > - **产出**：PRD + 原型
  > 以上理解正确吗？确认后我开始写。

### 1.3.1 章节裁剪预告（撰写 PRD 前必做）

> PRD 章节按需求大小裁剪（见 2.2）。在反向确认的同时，AI 必须**根据需求复杂度预判本次 PRD 拟保留/省略哪些章节，并先告知用户**，确认后再写。**不得默默省略。**

- 评估方式：核心骨架（项目信息+版本记录、需求背景、需求目标、详细方案）始终保留；其余 8 个可选章节（需求概述/流程图/交互流程图/异常边界/数据埋点/时序图/上线计划/附录）按 2.2 的判断依据逐一评估留还是省。
- 在确认消息里附一行「本次章节」说明，例如：
  > 这个需求比较小（仅调整一处文案，无新流程/无新埋点），我打算这样组织 PRD：
  > - **保留**：项目信息、版本记录、需求背景、需求目标、详细方案
  > - **省略**：流程图（无多步骤流程）、数据埋点（无新事件）、上线计划（直接全量）、异常边界（无新场景）
  > 你看这样可以吗？或者有哪章你希望保留？
- 用户若要求保留某章，则照办；用户认可后再进入撰写。
- **产出物联动**：若省略「四、流程图」章节，则**不产出** `[需求名]/流程图/[需求名]-flow.html`（步骤四 4.1–4.5 跳过）；若省略「五、交互流程图」章节，则**不产出** `[需求名]/流程图/[需求名]-screenflow.html`（§4.6 跳过）；两者都省略则不产出 `[需求名]/流程图/` 目录。「九、时序图」是 PRD 内的文本章节（Mermaid 源码块，见 §4.7），不产出独立文件，省略则整章不写。其余可选章节的省略只影响 PRD 内对应章节，不影响原型产出。

### 1.4 确认后进入下一步

- 用户确认「没问题」+ 认可章节组织后，进入PRD撰写阶段

---

## 步骤二：产出PRD（HTML格式）

### 2.1 格式规范

> **重要：** 输出格式必须是 **HTML文件**，而非Markdown。原因：Markdown粘贴至钉钉文档时会丢失表格格式，HTML经浏览器渲染后截图或复制保留格式效果最佳。

1. 将PRD保存为 `[需求名]/需求文档/[需求名]-PRD.html`（相对于项目根目录）
   > **目录归属：** 遵循文档顶部「需求目录归属规则」——先查 `[需求名]/` 是否已存在（可能由先行的需求挖掘/数据分析创建），有则复用、没有则新建，PRD 放进其 `需求文档/` 子目录。
2. HTML中内嵌所有CSS，无需外部依赖，确保脱机可用

### 2.2 PRD结构（按需求裁剪，章节顺序固定）

> **核心原则：章节不再全部固定必出，而是根据需求大小/复杂度按需取舍。** 小需求（如纯文案调整、单点优化）无需硬塞流程图、灰度策略等章节；复杂需求则完整覆盖。**保留的章节其相对顺序不变**（始终按下表从上到下排列），只是允许整章省略。

**① 核心骨架（任何需求都必出，不可省）：**

| 章节 | 说明 |
|------|------|
| 📋 项目信息 | 项目名/版本号/负责人等文档元信息 |
| 📝 版本记录 | 变更历史表 |
| 一、需求背景 | 为什么要做 |
| 二、需求目标 | 要达成什么 |
| 六、详细方案（四列表格：一级模块 \| 二级功能 \| 原型 \| 描述） | PRD 核心，绝不省 |

**② 按需裁剪（AI 根据需求判断是否需要，可整章省略）：**

| 章节 | 建议省略的判断依据 |
|------|----------|
| 三、需求概述（功能清单表格） | 功能点极少（如仅 1-2 个）时可省，直接进详细方案 |
| 四、流程图（嵌入交互式 iframe） | 无多步骤流程、无分支/状态流转的小需求 → 省 |
| 五、交互流程图（全部核心界面拼成一整张带箭头跳转链路图，嵌入 iframe，见 §4.6） | 核心界面 ≤2 个、或页面间无跳转链路且无状态流转 → 省 |
| 七、异常与边界处理 | 不引入任何新异常/边界场景 → 省 |
| 八、数据埋点 | 不涉及新增埋点事件 → 省 |
| 九、时序图（Mermaid **源码文本块**：端侧互动编排总时序 + 关键对象状态图，研发/测试向，见 §4.7） | 无复杂端侧编排的简单需求（无语音/流式/多端协同/复杂动效状态机）→ 省 |
| 十、上线计划与灰度策略 | 小需求直接全量上线、无灰度 → 省或一句话带过 |
| 📎 附录（决策对齐表/产品风格定位等） | 无决策项、无特殊风格约定 → 省 |

> **编号说明：** 章节编号（一～八）跟随实际保留的章节**连续重排**，不要因为省略了"四、流程图"就让正文出现"三、五"的跳号。即按保留章节重新顺序编号，但顺序仍遵循上表自上而下。

> **裁剪须先告知（极度重要）：** AI **不得默默省略章节**。在需求确认阶段（步骤一 1.3）必须先列出"本次 PRD 拟保留哪些章节、省略哪些、各自原因"，经用户确认后再撰写。详见 1.3。

### 2.3 详细方案表格格式

**必须使用四列表格**，格式如下：

| 一级模块 | 二级功能 | 原型 | 描述 |
|----------|----------|------|------|
| （使用rowspan合并相同模块） | 具体操作 | （原型iframe） | 结构化分块描述，格式见 §2.3.1 |

- 原型列放置对应界面的 `<iframe>` 嵌入
- 一级模块使用 `rowspan` 合并跨行单元格

#### 2.3.1 描述列结构化分块（必做）

> 描述列按「页面」维度写，采用**固定分块结构**：块标题用【】标注，块内条目编号 `1、2、3…`，块与块之间空一行。先把页面本身说清楚，再说交互，最后按需补规则与边界。**废弃旧的 `0、功能说明 / 1、xxx` 松散编号叙述法。**

**① 必出块（每行描述都要有，顺序固定在最前）：**

| 分块 | 写什么 |
|------|--------|
| 【页面元素】 | 该页面**所有**元素自上而下逐一说明：布局区块、控件、文案、数据展示、入口/悬浮件。要求评审者只读这一块就能在脑中还原整个页面 |
| 【交互说明】 | 逐条描述该页面的交互行为，统一用「操作 → 结果」句式（点击/长按/滑动/输入 → 跳转/弹层/Toast/状态变化） |

**② 按需块（该页面涉及才写；不涉及就整块不出现，不硬凑、不写"无"）：**

| 分块 | 写什么 | 出现条件 |
|------|--------|----------|
| 【功能逻辑】 | 该页面背后的功能规则与策略：次数扣减规则、排序规则、推荐/命中策略、优先级、频控等 | 页面涉及规则或策略时 |
| 【边界说明】 | 该页面的所有边界情况**逐条穷举**：空态、极值/上限、权限不足、网络异常、超时、重复操作、并发冲突等 | 页面存在任何边界场景时 |
| 【数据与内容规则】 | 展示内容的产品口径：数据从哪来（用户视角）、取数/排序规则、示例数据口径 | 列表页、报告页等数据驱动页面 |
| 【前置条件与权限】 | 进入该页面/触发该功能的前置条件：登录态、剩余额度、年级/学科设置、不同角色可见性差异 | 页面有准入门槛或角色差异时 |
| 【文案规范】 | 关键文案的**确切措辞**：按钮文字、Toast、空态文案、弹窗标题/正文，防止开发自行发挥 | 文案需要精确锁定时 |

**③ 硬性禁令（极度重要）：** 描述列**不得出现任何技术接口说明**——不写 API 名称、请求参数、字段 key、错误码、表结构、缓存/存储方案。一律用产品语言表述：写「上传成功后当日剩余额度减 1」，不写「调用 quota/deduct 接口扣减」。

**④ 示例（一行描述列的完整形态）：**

```
【页面元素】
1、顶部导航栏：标题"试卷分析"+左侧返回按钮
2、额度卡片：文案"hello-你的分析剩余额度"+剩余次数"8/10"
3、分析历史列表：每项含试卷名称、状态标签、创建日期
4、右下角悬浮相机按钮：常驻

【交互说明】
1、点击历史列表项 → 进入该试卷的分析报告页
2、点击悬浮相机按钮 → 唤起"选择拍照类型"半屏弹层

【功能逻辑】
1、分析历史按创建时间倒序排列
2、上传成功即扣减 1 次额度，分析失败自动返还

【边界说明】
1、无历史记录 → 展示空态插画+文案"暂无分析记录"+拍照引导按钮
2、剩余额度为 0 → 相机按钮置灰，点击 Toast 提示"今日额度已用完"
3、网络异常 → 列表加载失败，展示重试按钮
```

> **一致性联动：** 原型 ↔ PRD 对齐（3.1 第12条、3.6 自查）以【页面元素】【交互说明】【文案规范】的内容为对照基准；【边界说明】覆盖的场景与「七、异常与边界处理」章节（若保留）保持互相印证、不冲突。

### 2.4 写作风格

- 先图（原型）后文
- 逐条编号描述交互规则；详细方案「描述」列一律按 §2.3.1 的【】分块结构组织
- **极度重要（全文档可编辑）：** PRD **整篇正文**都要能在浏览器里直接改——不再只让「描述」列可编辑。具体的可编辑范围、排除项、表格增删行与行列拖拽，全部由 **§2.7 通用编辑模块** 统一实现并固化为必做项；§2.4 这里只描述配套的保存动作。
- **极度重要：** 必须在 HTML 底部插入“悬浮动作面板”，代码大纲如下（AI需补全标准JS）：
  1. 编辑变更追踪：所有可编辑块的 `blur` 事件，如内容相对 `data-original` 被修改，则为该块加 `data-changed="true"` 属性和绿色 `edited-cell` 高亮类（追踪逻辑由 §2.7 模块统一提供，无需另写）。
  2. 页面右下角的悬浮 `.save-btn-container` 区只保留一个按钮：“保存并通知AI”。截图导出功能已移至原型和流程图各自的 HTML 中，PRD 不再承载导出功能。另：**页面左下角**固定一个「📋 一键复制全文」按钮（实现见 §2.8），与右下角保存按钮分居两侧、互不遮挡。
  3. 点击保存按钮时，抓取 `document.documentElement.outerHTML` 并调用系统的文件保存句柄直接物理存档覆盖当前 PRD HTML 文件。**因为保存抓的是 `outerHTML`，§2.7 把列宽/行高写成 inline px、把编辑写回 DOM，保存即自动持久化，无需额外存储逻辑。**
- 黄色高亮标注关键变更点（用 `.alert` 样式块）
- 必须覆盖异常和边界情况

### 2.5 表格排版优化

- 页面最大宽度设为 `1400px`（允许原型列有足够展示空间）
- 表格使用 `table-layout: fixed`
- 各列推荐宽度：一级模块 `100px`，二级功能 `100px`，原型 `350px`，描述自动扩展（用 `<colgroup><col>` 承载列宽，便于拖拽时改 `col.style.width`）
- **不要**用 CSS `resize`（`resize:both/horizontal`）来调列宽行高——它会留拖拽残影、破坏表格截图。列宽/行高改用 **§2.7 的专用拖拽手柄**：手柄 `hover` 才出现、拖拽写 **inline px** 尺寸随 `outerHTML` 持久化、鼠标移开即隐藏，静态截图保持干净。
- `td` 设置 `word-break: break-word` 避免文字溢出
- **极度重要（原型预览体验）：** PRD 中的原型 iframe 不要直接按原始尺寸硬塞进表格单元格，尤其是 16:9 横屏课堂原型。必须使用“等比例缩放容器”包裹 iframe，并在每个原型预览右下角提供直接拖拽的缩放手柄，拖拽时原型整体按比例同步变化，避免再额外做独立操作面板。

### 2.6 右侧双栏交互原型预览（必做）

> **背景（踩坑记录）：** 这套右侧「交互原型预览」面板长期只活在历史 PRD 成品里（如 `AI试卷分析-PRD.html`），从未沉淀成规范，导致从零写 PRD 时容易漏掉（2.4 又只让放保存按钮）。**故在此固化为必做项：每份 PRD 都要内建该面板。** 它与「六、详细方案」表格里的静态原型列（截图/小 iframe）不同——这是一个全局常驻、可切页、可缩放的活预览 dock。

**目标：** PRD 左侧正文 + 右侧一个可关闭的深色面板，面板内嵌**活的原型 iframe**，用顶部下拉切换页面/场景，支持拖拽改宽，整体等比缩放。

**① HTML 结构：**
- `<body class="dual-pane">`：默认**打开**双栏。
- `.prototype-sidebar`（`position:fixed; right:0; top:0; height:100vh; 深色 #1a1a2e; flex 纵向`）内含：
  - `.sidebar-header`：`✕` 关闭按钮（`onclick="toggleDualPane()"`）+ 标题「交互原型预览」。
  - `.preview-context`：一行说明（如收口范围、或"完整交互依赖后端、静态预览仅还原界面"等真实约束，**不夸大成全功能可跑**）。
  - `.page-selector > select#pageSelect`（`onchange="switchPage(this.value)"`）。
  - `.preview-zoom`：一行缩放控件 `－ / 百分比 / ＋ / 适配`（详见 ⑨）。
  - `.device-shell > .device-wrapper > iframe#prototypeFrame`。
  - `.prototype-resizer`：面板左缘竖向拖拽手柄。
- `.fab-group`（`position:fixed; right:28px; bottom:28px`）：含「双栏预览」开关按钮（`dual-pane` 时 `display:none`）+「💾 保存并通知AI」按钮。**双栏打开时整组右移**到面板左侧：`body.dual-pane .fab-group { right: calc(var(--panel-w) + 28px); }`。（即 2.4 的保存按钮并入此 fab-group，不再单独悬浮。）

**② CSS 关键：**
- `:root { --panel-w: 520px; }`
- `body.dual-pane { margin:0!important; max-width:none!important; padding-right: calc(var(--panel-w) + 36px); }`（正文让出右侧面板宽度）
- `body.dual-pane .prototype-sidebar { display:flex; }`（默认 `.prototype-sidebar{display:none}`）
- `.device-wrapper iframe { transform-origin: top left; }`、`.device-shell { overflow:auto; }`（竖屏长页可滚）
- **`.device-wrapper { flex: 0 0 auto; }`（极易漏，漏了缩放就是坏的）**：`.device-shell` 通常是 `display:flex` 居中，而 flex item 默认 `flex-shrink:1` —— JS 明明把 wrapper 设成 1170px，实际渲染仍被压回 480px，于是**放大后既不出滚动条、原型还被裁掉一半**。实测踩过：必须显式禁止收缩。放大后若还想从顶部开始看，配 `.device-shell { align-items:flex-start; }`。

**③ JS 关键（内嵌 PRD 底部）：**
```js
// 每项：{value,label,url,w,h}。url 指向可寻址原型；w/h = 该页逻辑尺寸
const CATALOG = [ { value:'p1', label:'P1 · xxx', url:'../原型/xxx-prototype.html#p1', w:375, h:812 }, /* ... */ ];
let previewPage = CATALOG[0].value;
let previewZoom = null;   // null = 适配宽度；数字 = 手动缩放倍率（见 ⑨）
function currentCfg(){ return CATALOG.find(o=>o.value===previewPage) || CATALOG[0]; }
function scalePreview(){
  const shell=document.querySelector('.device-shell'), wrap=document.getElementById('deviceWrapper'), frame=document.getElementById('prototypeFrame');
  const cfg=currentCfg(), innerW=Math.max(120, shell.clientWidth-40);
  const fit=innerW/cfg.w, scale=(previewZoom==null)? fit : previewZoom;
  frame.style.width=cfg.w+'px'; frame.style.height=cfg.h+'px'; frame.style.transform='scale('+scale+')';
  wrap.style.width=Math.round(cfg.w*scale)+'px'; wrap.style.height=Math.round(cfg.h*scale)+'px';
  const lab=document.getElementById('previewZoomLabel');
  if(lab) lab.textContent=Math.round(scale*100)+'%'+(previewZoom==null?' · 适配':'');
}
function switchPage(v){ previewPage=v; const f=document.getElementById('prototypeFrame'); if(f) f.src=currentCfg().url; requestAnimationFrame(scalePreview); setTimeout(scalePreview,350); }
function toggleDualPane(){ document.body.classList.toggle('dual-pane'); if(document.body.classList.contains('dual-pane')) requestAnimationFrame(scalePreview); }
// 拖拽 .prototype-resizer 改 --panel-w（clamp 如 380..min(900, innerWidth-360)）后 scalePreview()
window.addEventListener('resize', scalePreview);
window.addEventListener('load', ()=>{ /* renderSelect() */ switchPage(previewPage); });
```

**④ 横屏适配（极度重要）：** 16:9 横屏课堂原型逻辑尺寸用 `w:1280,h:720`；竖屏/手机页用自身尺寸（如 `375×812`）；报告等长页用其真实高度（如 `480×1360`）。各页按面板内宽 `scale`，`.device-shell` 溢出可滚，**不要把横屏页硬塞成手机竖屏**。

**⑤ iframe 取材：** 优先指向**可按 hash/场景寻址**的原型（`prototype.html#page-id`）。若真实产品依赖后端无法静态跑（如课中语音链路），可指向「截图版/状态版」HTML（每场景一个 hash，活 DOM 还原 UI），并在 `.preview-context` 据实说明交互限制。

**⑥ 与 3.4.2 联动：** 原型内切页时 `postMessage({type:'page-changed',page})`，PRD 既有监听同步 `#pageSelect`（向后兼容）。

**⑦ 裁剪与迭代：** 仅 1 个原型页时可省下拉、只留单页预览，但**面板本身默认保留**；新增页必须同步往 `CATALOG` / `#pageSelect` 加项（见 5.3 第 16 项「PRD 双栏预览下拉项」）。

**⑧ 滚动联动 / scroll-spy（必做）：** 左侧正文滚到某模块，右侧交互预览**自动切到该模块对应的原型页**（滚到「界面1」→预览定位界面1，滚到「界面3」→跟随切界面3），不用手点下拉。
- **取材：** 给「六、详细方案」每个**一级模块单元格**（`td.mod`，或模块首行 `<tr>`）加 `data-preview="<CATALOG 里对应页的 value>"`。新增模块/页时必须同步补这个属性（并入 5.3 迭代清单）。
- **激活判定：** 监听 `window` 滚动（`requestAnimationFrame` 节流），取视口上方约 35% 处「激活线」**之上最后一个** `data-preview` 元素为当前模块；`v !== previewPage` 时才 `switchPage(v)`（避免反复重载 iframe）；仅 `body.dual-pane` 打开时生效。
- **不与用户打架：** 监听 `#pageSelect` 的 `change`，用户**手动选页**后短暂（~4s）暂停联动（`switchPage` 程序化改 `select.value` 不会触发 `change`，故自动切不会误锁）。

```js
function initPreviewScrollSync(){
  var nodes = Array.prototype.slice.call(document.querySelectorAll('.scheme-table [data-preview]'));
  if(!nodes.length) return;
  var lockUntil = 0, sel = document.getElementById('pageSelect');
  if(sel) sel.addEventListener('change', function(){ lockUntil = Date.now() + 4000; });
  function pickActive(){
    if(!document.body.classList.contains('dual-pane') || Date.now() < lockUntil) return;
    var line = window.innerHeight * 0.35, current = null;
    for(var i=0;i<nodes.length;i++){ if(nodes[i].getBoundingClientRect().top <= line) current = nodes[i]; }
    if(!current) current = nodes[0];
    var v = current.getAttribute('data-preview');
    if(v && v !== previewPage) switchPage(v);
  }
  var ticking = false;
  function onScroll(){ if(ticking) return; ticking = true; requestAnimationFrame(function(){ pickActive(); ticking = false; }); }
  window.addEventListener('scroll', onScroll, { passive:true });
  window.addEventListener('resize', onScroll);
  pickActive();
}
// 在 window load 里：renderSelect(); switchPage(previewPage); initPreviewScrollSync();
```

**⑨ 预览缩放（必做）：** 只有「适配宽度」不够用——横屏 `1280×720` 缩进 520px 面板后细节看不清，也没法放大局部看某个控件。故面板内固定提供一组缩放控件。

- **控件形态沿用 §4.6 交互流程图那一组**（`－ / 百分比 / ＋ / 适配`），保持全 skill 一致；侧栏无下载需求，**去掉 §4.6 的 `📸`**。放在 `.page-selector` 与 `.device-shell` 之间，深色底细按钮，不与正文抢空间。
- **档位固定梯**：`25 / 50 / 75 / 100 / 125 / 150 / 200 / 300`（%）。`＋/－` 在梯上跳一格，clamp 在 25%–300%。「适配」把 `previewZoom` 置回 `null` 回到自适应。
- 从适配态第一次点 `＋/－` 时，以**当前适配倍率**为起点在梯上找下一格，不会突然跳到 100% 让画面猛跳。
- **溢出由已有的 `.device-shell{overflow:auto}` 承接**，滚动条即可平移。**前提是 ② 里的 `.device-wrapper{flex:0 0 auto}` 别漏**，否则 wrapper 被 flex 压回面板宽度、放大等于白做。**不做 §4.6 那种按住拖拽平移**——侧栏里的是活原型，拖拽会和原型自身的点击/滑动交互打架。
- **`Ctrl/⌘ + 滚轮`** 在 `.device-shell` 上缩放（`preventDefault`）。**如实记一条限制：指针悬在 iframe 内部时滚轮事件归 iframe 文档，父页收不到**，此时快捷键无效——所以**按钮是主路径、快捷键只是补充**，不要向用户宣传成"随处滚轮缩放"。
- **切页保留缩放模式**：`switchPage()` 与 ⑧ 的 scroll-spy 自动切页都**不重置** `previewZoom`（适配继续适配，手动百分比保持不变），规则简单可预期。拖 `.prototype-resizer` 改 `--panel-w` 同理：适配模式重算、手动模式保持百分比。
- **`previewZoom` 只存 JS 变量，不写进 DOM**（遵守 §2.7「不落 `data-*` 痕迹」的约定），保证 §2.4 保存与 §2.8 复制的产物干净。

```css
.preview-zoom { display:flex; align-items:center; gap:6px; padding:8px 16px; border-bottom:1px solid rgba(255,255,255,.08); }
.preview-zoom button { background:rgba(255,255,255,.08); color:#e8e6ff; border:1px solid rgba(255,255,255,.16); border-radius:6px; padding:3px 10px; font-size:12px; cursor:pointer; line-height:1.6; }
.preview-zoom button:hover { background:rgba(255,255,255,.18); }
.preview-zoom #previewZoomLabel { min-width:82px; text-align:center; font-size:12px; color:#b9b5e0; font-variant-numeric:tabular-nums; }
```

```html
<div class="preview-zoom">
  <button type="button" onclick="zoomPreview(-1)" title="缩小">－</button>
  <span id="previewZoomLabel">100%</span>
  <button type="button" onclick="zoomPreview(1)" title="放大">＋</button>
  <button type="button" onclick="fitPreview()" title="适配面板宽度">适配</button>
</div>
```

```js
const ZOOM_STEPS = [0.25,0.5,0.75,1,1.25,1.5,2,3];
function currentPreviewScale(){
  if(previewZoom!=null) return previewZoom;
  const shell=document.querySelector('.device-shell');
  if(!shell) return 1;
  return Math.max(120, shell.clientWidth-40)/currentCfg().w;   // 当前适配倍率
}
function zoomPreview(dir){
  const now=currentPreviewScale();
  let next;
  if(dir>0) next=ZOOM_STEPS.find(s=>s>now+1e-4);
  else      next=[...ZOOM_STEPS].reverse().find(s=>s<now-1e-4);
  previewZoom = next==null ? Math.min(3, Math.max(0.25, now)) : next;
  scalePreview();
}
function fitPreview(){ previewZoom=null; scalePreview(); }
// Ctrl/⌘ + 滚轮（限制：指针在 iframe 内时事件归 iframe，父页收不到）
document.querySelector('.device-shell')?.addEventListener('wheel', function(e){
  if(!e.ctrlKey && !e.metaKey) return;
  e.preventDefault();
  zoomPreview(e.deltaY < 0 ? 1 : -1);
}, { passive:false });
```

### 2.7 全文档可编辑 · 表格行列拖拽 · 全表增删行（必做）

> **背景（踩坑记录）：** 旧版只给「六、详细方案」描述列加 `contenteditable`、只有详细方案表能增删行；其余正文（背景/目标/版本记录/埋点…）在浏览器里都改不了，且 §2.5 旧规曾**禁用**列宽行高调整。**现固化为必做项：每份 PRD 都内建下面这套自包含的「通用编辑模块」**，一次性提供①全文档可编辑 ②全表增删行 ③列宽/行高拖拽。模块**幂等、纯内嵌、无外部依赖**，直接整段贴进 PRD 底部 `<script>`（在保存按钮逻辑之前），无需逐个单元格手写 `contenteditable`。

**① 能力与边界**
- **全文档可编辑：** 自动给正文内容块（`td/th/p/li/h1~h4/.alert/blockquote/dd/dt`）加 `contenteditable` 并接管变更追踪（`blur` 后内容变化 → `data-changed="true"` + `.edited-cell` 高亮）。
- **reload 安全（极易踩坑）：** 「已接管」「原始内容」用内存态 `WeakMap`/`WeakSet` 守卫，**绝不把 `data-pm-tracked`/`data-original` 写进 DOM**——否则保存（`outerHTML`）后这些脏属性被存档，重新打开时守卫命中、`blur` 监听不再挂载，编辑高亮静默失效。仅 `contenteditable`、`data-changed`、`.edited-cell` 会随存档保留（前者保持可编辑、后两者作为评审标记，符合预期）。
- **排除项（保持交互骨架不被误编辑）：** 右侧 `.prototype-sidebar` 预览面板、`.fab-group`/`.save-btn(-container)`/`.dual-pane-toggle` 悬浮按钮、各拖拽手柄、`.pm-anchor`、`iframe`/`script`/`style`/`button`；**含 `img`/`iframe`/`table`/`video`/`canvas` 的容器单元格（详细方案「原型」列无论用 iframe 还是截图 `<img>`）整体不接管**，避免原型/截图被改坏。
- **全表增删行：** 作用于**所有数据表**（版本记录/功能清单/详细方案/埋点…）。**表头行自动识别**：整行均为 `<th>`（含写在 `<tbody>` 里的表头行）或位于 `<thead>` 的行都不加增删/行高控件、仅用于列宽手柄定位。每个数据行首格 `hover` 出现 `＋`（下方插一行）/`－`（删除本行，留 1 行兜底）；新行克隆结构、**去掉 `id`/`rowspan`/`colspan`** 防重复 id、清空文本、自动接管编辑。
- **列宽/行高拖拽：** 表头每列右缘 `.col-resizer`（改 `<col>` 宽，下限 48px）、每数据行首格下缘 `.row-resizer`（改 `tr` 高，下限 24px）。手柄默认 `opacity:0`、`hover` 才显、写 inline px → 随 `outerHTML` 保存，且静态截图无残影。无 `<colgroup>` 的表会按表头单元格当前宽度自动补一个。

**② CSS 关键（手柄一律 hover-only）：**
```css
.edited-cell { background:#e8f5e9 !important; }
.editable-table-wrap { position:relative; margin:14px 0; }
.editable-table-wrap > table { margin:0 !important; }
.pm-anchor { position:relative; }
.row-ctrl { position:absolute; left:-30px; display:flex; flex-direction:column; gap:3px; opacity:0; pointer-events:none; transition:opacity .15s; z-index:4; }
tr:hover > * .pm-anchor > .row-ctrl, tr:hover .pm-anchor > .row-ctrl { opacity:1; pointer-events:auto; }
.row-ctrl button { width:22px; height:18px; border:none; border-radius:5px; cursor:pointer; color:#fff; font-size:13px; font-weight:700; line-height:1; }
.row-add { background:#00b894; } .row-del { background:#e74c3c; }
.editable-table-remove { position:absolute; top:-12px; right:8px; z-index:5; border:none; border-radius:999px; background:rgba(231,76,60,.96); color:#fff; font-size:12px; padding:6px 10px; cursor:pointer; opacity:0; pointer-events:none; transition:opacity .15s; }
.editable-table-wrap:hover .editable-table-remove { opacity:1; pointer-events:auto; }
.col-resizer { position:absolute; top:0; right:0; width:9px; height:100%; cursor:col-resize; transform:translateX(50%); z-index:3; opacity:0; transition:opacity .15s; }
.col-resizer::after { content:''; position:absolute; left:4px; top:0; width:2px; height:100%; background:#00b894; opacity:0; transition:opacity .15s; }
th:hover .col-resizer, td:hover .col-resizer, body.col-resizing .col-resizer.active { opacity:1; }
.col-resizer:hover::after, body.col-resizing .col-resizer.active::after { opacity:1; }
.row-resizer { position:absolute; left:0; bottom:0; width:100%; height:9px; cursor:row-resize; transform:translateY(50%); z-index:3; }
.row-resizer::after { content:''; position:absolute; top:4px; left:0; width:100%; height:2px; background:#00b894; opacity:0; transition:opacity .15s; }
.row-resizer:hover::after, body.row-resizing .row-resizer.active::after { opacity:1; }
body.col-resizing, body.row-resizing { user-select:none !important; }
body.col-resizing { cursor:col-resize !important; } body.row-resizing { cursor:row-resize !important; }
```

**③ JS 模块（已在无头 Chrome 对真实 PRD 结构实测全绿：全文档可编辑/排除 img 原型列/`<th>`-in-`<tbody>` 表头识别/增删行/列宽±与48px下限/行高/edited 高亮/无脏属性泄漏/幂等再init，整段照贴）：**
```js
(function () {
  var EDITABLE_BLOCK_SELECTOR = 'td, th, p, li, h1, h2, h3, h4, .alert, blockquote, dd, dt';
  var EXCLUDE_SELECTOR = '.prototype-sidebar, .fab-group, .save-btn, .save-btn-container, .dual-pane-toggle, ' +
    '.col-resizer, .row-resizer, .row-ctrl, .pm-anchor, .editable-table-remove, script, style, iframe, button';
  var SKIP_CELL_CONTENT = 'table, iframe, video, canvas, img';   // 含这些的容器格不整体接管（如原型/截图列）
  var origMap = new WeakMap(), rowDone = new WeakSet();
  function isExcluded(el){ return !!(el.closest && el.closest(EXCLUDE_SELECTOR)); }
  function isHeaderRow(tr){ return tr.cells.length > 0 && Array.prototype.every.call(tr.cells, function(c){ return c.tagName === 'TH'; }); }
  function headerRowOf(table){
    if (table.tHead && table.tHead.rows[0]) return table.tHead.rows[0];
    for (var i=0;i<table.rows.length;i++) if (isHeaderRow(table.rows[i])) return table.rows[i];
    return table.rows[0] || null;
  }
  function markEditableCellChanged(el){ if(!el) return; el.setAttribute('data-changed','true'); el.classList.add('edited-cell'); }
  function trackEditable(el){
    if (origMap.has(el)) return; origMap.set(el, el.innerHTML);   // 内存态守卫，不写入 HTML
    el.setAttribute('contenteditable','true'); el.style.outline='none';
    el.addEventListener('blur', function(){ if(this.innerHTML !== origMap.get(this)) markEditableCellChanged(this); });
  }
  function makeDocumentEditable(root){
    (root||document).querySelectorAll(EDITABLE_BLOCK_SELECTOR).forEach(function(el){
      if (isExcluded(el)) return;
      if (el.querySelector(SKIP_CELL_CONTENT)) return;
      trackEditable(el);
    });
  }
  function wrapTable(table){
    if (table.closest('.editable-table-wrap')) return table.closest('.editable-table-wrap');
    var wrap=document.createElement('div'); wrap.className='editable-table-wrap'; wrap.setAttribute('contenteditable','false');
    table.parentNode.insertBefore(wrap, table); wrap.appendChild(table);
    var rm=document.createElement('button'); rm.type='button'; rm.className='editable-table-remove'; rm.textContent='删除表格';
    rm.addEventListener('click', function(e){ e.preventDefault(); wrap.remove(); }); wrap.appendChild(rm); return wrap;
  }
  function blankRowFrom(tr){
    var clone=tr.cloneNode(true); clone.style.height=''; clone.removeAttribute('id');
    Array.prototype.forEach.call(clone.cells, function(c){
      c.removeAttribute('rowspan'); c.removeAttribute('colspan'); c.removeAttribute('id');
      c.removeAttribute('data-changed'); c.classList.remove('edited-cell');
      c.querySelectorAll('.row-ctrl, .col-resizer, .row-resizer, .pm-anchor').forEach(function(n){
        if(n.classList.contains('pm-anchor')){ while(n.firstChild) n.parentNode.insertBefore(n.firstChild,n); n.remove(); } else n.remove();
      });
      if(!c.querySelector('iframe, img, video, canvas')) c.innerHTML='<br>';
      c.removeAttribute('contenteditable');
    });
    return clone;
  }
  function installRowControls(tr){
    var first=tr.cells[0]; if(!first || first.querySelector(':scope > .pm-anchor > .row-ctrl')) return;
    first.style.position='relative';
    var anchor=document.createElement('span'); anchor.className='pm-anchor'; anchor.setAttribute('contenteditable','false');
    var ctrl=document.createElement('span'); ctrl.className='row-ctrl';
    var add=document.createElement('button'); add.type='button'; add.className='row-add'; add.textContent='+'; add.title='在下方插入一行';
    var del=document.createElement('button'); del.type='button'; del.className='row-del'; del.textContent='−'; del.title='删除本行';
    add.addEventListener('click', function(e){ e.preventDefault(); var nr=blankRowFrom(tr); tr.parentNode.insertBefore(nr, tr.nextSibling); decorateRow(nr); makeDocumentEditable(nr); });
    del.addEventListener('click', function(e){ e.preventDefault(); var body=tr.parentNode; var dataRows=Array.prototype.filter.call(body.rows, function(r){return !isHeaderRow(r);}); if(dataRows.length<=1) return; tr.remove(); });
    ctrl.appendChild(add); ctrl.appendChild(del); anchor.appendChild(ctrl); first.insertBefore(anchor, first.firstChild);
  }
  function ensureCols(table){
    if (table.querySelector('colgroup')) return table.querySelector('colgroup');
    var headRow=headerRowOf(table); if(!headRow) return null;
    var cg=document.createElement('colgroup');
    for(var i=0;i<headRow.cells.length;i++){ var col=document.createElement('col'); col.style.width=headRow.cells[i].offsetWidth+'px'; cg.appendChild(col); }
    table.insertBefore(cg, table.firstChild); return cg;
  }
  function installColResizers(table){
    var cg=ensureCols(table); if(!cg) return; var cols=cg.querySelectorAll('col');
    var headRow=headerRowOf(table); if(!headRow) return;
    Array.prototype.forEach.call(headRow.cells, function(th, idx){
      if(idx>=cols.length) return; if(th.querySelector(':scope > .col-resizer')) return;
      th.style.position='relative';
      var h=document.createElement('span'); h.className='col-resizer'; h.setAttribute('contenteditable','false');
      h.addEventListener('mousedown', function(e){
        e.preventDefault(); e.stopPropagation();
        var startX=e.clientX, startW=cols[idx].offsetWidth||th.offsetWidth;
        h.classList.add('active'); document.body.classList.add('col-resizing');
        function mv(ev){ cols[idx].style.width=Math.max(48, startW+(ev.clientX-startX))+'px'; }
        function up(){ document.removeEventListener('mousemove',mv); document.removeEventListener('mouseup',up); h.classList.remove('active'); document.body.classList.remove('col-resizing'); }
        document.addEventListener('mousemove',mv); document.addEventListener('mouseup',up);
      });
      th.appendChild(h);
    });
  }
  function installRowResizer(tr){
    var first=tr.cells[0]; if(!first || first.querySelector(':scope > .row-resizer')) return;
    first.style.position='relative';
    var h=document.createElement('span'); h.className='row-resizer'; h.setAttribute('contenteditable','false');
    h.addEventListener('mousedown', function(e){
      e.preventDefault(); e.stopPropagation();
      var startY=e.clientY, startH=tr.offsetHeight;
      h.classList.add('active'); document.body.classList.add('row-resizing');
      function mv(ev){ tr.style.height=Math.max(24, startH+(ev.clientY-startY))+'px'; }
      function up(){ document.removeEventListener('mousemove',mv); document.removeEventListener('mouseup',up); h.classList.remove('active'); document.body.classList.remove('row-resizing'); }
      document.addEventListener('mousemove',mv); document.addEventListener('mouseup',up);
    });
    first.appendChild(h);
  }
  function decorateRow(tr){ if(rowDone.has(tr) || isHeaderRow(tr) || tr.closest('thead')) return; rowDone.add(tr); installRowControls(tr); installRowResizer(tr); }
  function installTableControls(root){
    (root||document).querySelectorAll('table').forEach(function(table){
      if(isExcluded(table) || table.closest('.no-edit')) return;
      wrapTable(table); installColResizers(table);
      Array.prototype.forEach.call(table.rows, decorateRow);
    });
  }
  function init(root){ installTableControls(root); makeDocumentEditable(root); }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', function(){ init(document); }); else init(document);
  window.PMEdit={ init:init, makeDocumentEditable:makeDocumentEditable, installTableControls:installTableControls };
})();
```

**④ 接入约定：**
- 详细方案及其它定宽表必须带 `<colgroup><col>`（见 §2.5），列宽拖拽改的就是这些 `<col>`。
- 某张表确实不想被编辑/加控件时，给该 `<table>` 加 `class="no-edit"` 豁免（如纯展示装饰表）。
- **迭代联动（接 §5.3）：** 新增表格/新增整块正文后，调用 `PMEdit.init(新节点)` 让控件对新节点幂等生效；`PMEdit.init`、`installTableControls`、`makeDocumentEditable` 均可重复安全调用，不会重复加手柄。
- 保存仍走 §2.4 的「💾 保存并通知AI」按钮抓 `outerHTML`；编辑内容、`edited-cell`、inline 列宽/行高都会一并落盘。

### 2.8 左下角「一键复制全文」（必做 · 原型 iframe 自动转图片）

> **目的：** 方便把整份 PRD 一键拷到钉钉/飞书/Word 等外部文档。复制必须是**富文本**（`text/html`，保留表格/标题/加粗/列表），并在导出前**剥离所有交互骨架与编辑痕迹**，否则粘出去会带一堆手柄、绿色高亮和 `contenteditable` 脏属性。
>
> **踩坑记录（v2.6 修正）：** 旧版直接 `iframe.remove()`，PRD 粘出去后**原型/流程图全部消失**，PM 每次都要手动重新截图再贴一遍。现固化为：复制前先把每个 iframe 通过本地导出服务换成 **base64 内联图片**，一次粘贴即完整。

**① 按钮：** 页面**左下角**固定一个 `.copy-all-fab`（`position:fixed; left:28px; bottom:28px`），`onclick="copyAllContent()"`，文案「📋 一键复制全文」。与右下角 `.fab-group`（双栏/保存）分居两侧；双栏打开时右侧面板不影响左下角，无需偏移。另配一个 `.copy-toast`（左下、`bottom:80px`）做轻量结果反馈，默认 `opacity:0`、`.show` 时淡入，2 秒后自动隐藏。**取图期间 toast 常驻**（「正在生成原型图片 n/N…」），出结果后才进入 2 秒自动隐藏。

**② 两类图都要内联成 base64（本节核心）：**

PRD 里的图有两种来源，**都得处理**，只处理 iframe 是不够的：

| 来源 | 形态 | 接口 |
|---|---|---|
| 活原型 / 流程图 | `<iframe src="../原型/x.html#p1">` | `POST /api/snapshot` → Playwright 渲染出 PNG |
| 详细方案「原型」列的截图版 | `<img src="../原型截图/x.png">` | `POST /api/asset` → 直接读本地文件转 base64 |

- **必须走本地导出服务**，理由与 §4.5 同源：`file://` 下浏览器既不能 `fetch` 本地 PNG、canvas 也会被跨源污染，**base64 只能由服务端下发**。禁止为此新造 `html2canvas` / `html-to-image` 前端截图路径。
- PRD 底部引入 `<script src="../../scripts/prototype-export-client.js?v=YYYYMMDD-prd"></script>`（PRD 在 `[需求名]/需求文档/` 下，故是 `../../scripts/`），拿到 `window.snapshotPrototypeViaServer(src,{base})` 与 `window.inlineAssetViaServer(src,{base})`。
- `/api/snapshot` 入参 `{src, base, scale?}` → 回 `{ok, dataUrl, cached, bytes}`。**取图策略＝缓存优先 + 自动重渲**：截图存在且比原型 HTML 新 → 直接复用 `[需求名]/原型截图/`（或 `流程图截图/`）里已有的 PNG；否则实时用 Playwright 只渲这一页再落盘。`scale` 默认 `2`（与整轮导出一致，保证同一份文档里图片清晰度统一），体积敏感时可传 `1`。
- **服务端会自动适配四种 iframe**（不用 PRD 侧操心）：平铺原型的 `.device[id]`（按 hash 定位）、流程图的 `.chart-container`、单屏页（`.screen`/`.device`/`main`）、带 query 的片段（如 `?only=flow-main`，query 会原样带上并单独缓存）。
- `/api/asset` 只放行 `png/jpg/jpeg/gif/webp/svg` 且必须落在项目目录内、单张 ≤12MB —— 它把文件原样吐成 base64，不能退化成任意文件读取。
- **按 `src` 去重 + 页面内 `Map` 缓存**：同一份 PRD 里同一个 src 只取一次；同一次会话第二次复制直接秒出。

**③ 三步走：剥骨架 → 取图 → 落图（顺序不能反）**

1. **`stripSkeleton()`**：`document.body.cloneNode(true)` 后删掉 `.prototype-sidebar`、`.fab-group`、`.copy-all-fab`、`.copy-toast`、`.col-resizer`、`.row-resizer`、`.row-ctrl`、`.pm-anchor`、`.editable-table-remove`、`script`/`noscript`；`.editable-table-wrap` 用其内部 `<table>` 替换自身。**iframe/img 此时先留着。**
2. **`collectMedia(clone)`**：**只扫 clone 里活下来的节点**去取图。
   > **踩坑（必须照做）：** 早期版本按 `document` 扫 iframe，把 §2.6 右侧双栏预览的 `#prototypeFrame` 也算了进去——它随 `.prototype-sidebar` 一起被删了，结果**白渲一张图、toast 还多报一张**（说"3 张"实际只贴出 2 张）。按 clone 扫天然规避。
   > **踩坑 2（同样必须照做）：** 页面 CSS 全在 `<head>` 里，`document.body.cloneNode(true)` **带不走**，`.proto-shot` 那类尺寸约束会整个丢失，1200px 的截图直接把表格撑爆、描述列被挤成"一行一个字"。所以 `stripSkeleton()` 要**趁 clone 与实时 DOM 还一一对应**（删节点之前，两边 `querySelectorAll('img')` 索引一致），把每张图的实际显示宽度 `getBoundingClientRect().width` 固化成内联 `width` + `max-width:100%`。
3. **`finalizeClone(clone, jobs)`**：iframe 换成 `<img src="data:image/png;base64,…">`（失败的才删）、本地 `<img>` 的 `src` 换成 dataUrl（失败的保留原样）；再移除 `contenteditable`、`data-changed`/`data-original`/`data-orig`/`data-pm-tracked` 与 `.edited-cell`；给 `table` 补 `border-collapse/width`、`th,td` 补 `1px` 边框+内边距、`th` 补浅底色（内联 style，确保粘到无样式环境也有框）；最后把 `img` 的 `src` 绝对化——**`data:` 开头的要跳过**，否则会把 base64 改坏。

**④ 三档降级（必须据实告知，不许静默失败）：**

| 情况 | 行为 | toast 文案 |
|---|---|---|
| 全部取图成功 | iframe 换成图、本地 img 内联 | `已复制全文（含 N 张图），可直接粘贴到钉钉/飞书/Word` |
| 部分失败 | 失败的 iframe 删掉、失败的 img 保留原样 | `已复制全文，含 N 张图，M 张生成失败已跳过` |
| 服务整体不可用 | 退回旧行为（删所有 iframe、img 留本地路径） | `导出服务未启动，已按纯文本复制（原型图缺失）` |

**⑤ 体积控制（不做会直接失败）：** 服务下发的是 `scale=2` 的交付级 PNG，单张能到 3MB —— 一份含 3 个 iframe + 8 张原型截图的真实 PRD 实测**原始合计约 19.5MB**，转 base64 后 26MB，远超各家文档粘贴能吃下的量。故取到 dataUrl 后**在 PRD 页面本地降采样**：宽度上限 `MAX_IMG_WIDTH = 2000`，超出的按比例缩到 2000px 宽再以 `image/jpeg`（质量 0.9）重编码，先铺白底再画（JPEG 无透明通道）。
- **为什么可以在前端做**：`data:` URL 属同源，**不会污染 canvas**——被 `file://` 封死的只有"读本地文件"，不是"处理已经拿到手的 base64"。所以服务只负责突破 `file://` 的读取限制，缩放留在浏览器，无需任何图像库。
- 缩放失败（`onerror`/`toDataURL` 抛错）**一律退回原图**，绝不因为压缩失败就丢图。
- **粘出去「发虚」是降采样造成的，不是 JPEG 造成的（v2.8 实测，别改错地方）：** 上限曾定在 1200 + 质量 0.85，PM 反馈粘进文档发虚。同一素材同一区域四档对照 —— JPEG .85 / JPEG .95 / PNG 无损 / WebP .92，**都缩到 1200 后几乎无差别**，而不降采样的原图明显锐利。细节是在缩放那一步丢的，换编码格式救不回来，唯一有效的是抬高 `MAX_IMG_WIDTH`。9 张素材实测合计：`1200/.85 = 0.90MB`、`1600/.9 = 1.65MB`、`2000/.9 = 2.20MB`、`2880 原尺寸/.9 = 3.60MB`；取 **2000** 是清晰度与体积的拐点。
- **别用「贴出来看着还行」判断够不够。** 图在文档里的显示宽度由 ④ 固化的表格列宽决定（实测 335px），**这个尺寸下 1200 和 2880 肉眼无差别**，差异只在读者放大看细节时暴露。验收要放大到 1000px 以上再看。
- 再要更清晰只能继续调大 `MAX_IMG_WIDTH`，代价是体积近似平方级上升；**WebP 体积更优（`2000/.9` 仅 1.34MB）但钉钉/飞书/Word 对剪贴板内 base64 WebP 的支持未实测，不要默认切过去**。

**⑥ 写剪贴板：** 优先 `navigator.clipboard.write([new ClipboardItem({'text/html':blobHtml,'text/plain':blobText})])`（`text/plain` = 清洗后 `clone.innerText` 兜底）；不支持或被拒时**回退**到离屏 `contenteditable` 容器 + 选区 + `document.execCommand('copy')`。成功/失败都用 `.copy-toast` 提示。

**⑦ JS（整段照贴到 PRD 底部，须在 `prototype-export-client.js` 之后）：**
```js
(function(){
  var mediaCache = new Map();   // src → dataUrl，同一次会话复用（iframe 与 img 共用）
  var MAX_IMG_WIDTH = 2000;     // 粘出去的图片宽度上限，见 ⑤ 体积控制（1200 会让放大看时发虚）

  // 服务下发的是 2 倍图（一张能到 3MB），直接塞剪贴板会几十 MB。
  // data: URL 不会污染 canvas，所以缩放可以在本页做完，不用再依赖任何图像库。
  function shrinkDataUrl(dataUrl, maxWidth){
    return new Promise(function(resolve){
      var im = new Image();
      im.onload = function(){
        if(!im.naturalWidth || im.naturalWidth <= maxWidth){ resolve(dataUrl); return; }
        try{
          var r = maxWidth / im.naturalWidth;
          var c = document.createElement('canvas');
          c.width = Math.round(im.naturalWidth * r);
          c.height = Math.round(im.naturalHeight * r);
          var ctx = c.getContext('2d');
          ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, c.width, c.height);  // JPEG 没有透明通道，先铺白底
          ctx.drawImage(im, 0, 0, c.width, c.height);
          resolve(c.toDataURL('image/jpeg', 0.9));
        }catch(e){ resolve(dataUrl); }   // 缩放失败就用原图，不能因此丢图
      };
      im.onerror = function(){ resolve(dataUrl); };
      im.src = dataUrl;
    });
  }

  // ① 先剥交互骨架，iframe/img 都先留着
  function stripSkeleton(){
    var clone = document.body.cloneNode(true);
    // 页面 CSS 在 <head> 里，克隆 body 带不走 → 原型列截图会按 1200px 原图把表格撑爆、
    // 描述列被挤成一行一个字。趁 clone 与实时 DOM 还一一对应，把实际显示宽度固化成内联样式。
    var live = document.body.querySelectorAll('img'), copies = clone.querySelectorAll('img');
    for(var i=0; i<live.length && i<copies.length; i++){
      var w = Math.round(live[i].getBoundingClientRect().width);
      if(w > 0){ copies[i].style.width = w + 'px'; copies[i].style.height = 'auto'; }
      copies[i].style.maxWidth = '100%';
    }
    clone.querySelectorAll('.prototype-sidebar, .fab-group, .copy-all-fab, .copy-toast, .col-resizer, .row-resizer, .row-ctrl, .pm-anchor, .editable-table-remove, script, noscript').forEach(function(n){ n.remove(); });
    clone.querySelectorAll('.editable-table-wrap').forEach(function(w){ var t=w.querySelector('table'); if(t) w.replaceWith(t); else w.remove(); });
    return clone;
  }

  // ② 只扫 clone 里活下来的节点，逐个取 base64
  async function collectMedia(clone){
    var jobs = [];
    clone.querySelectorAll('iframe[src]').forEach(function(el){
      jobs.push({ el: el, src: el.getAttribute('src'), kind: 'frame' });
    });
    clone.querySelectorAll('img[src]').forEach(function(el){
      var s = el.getAttribute('src');
      if(s && !/^data:/i.test(s)) jobs.push({ el: el, src: s, kind: 'asset' });
    });

    var out = { ok:0, fail:0, serviceDown:false, jobs: jobs };
    if(!jobs.length) return out;
    if(typeof window.snapshotPrototypeViaServer !== 'function' || typeof window.inlineAssetViaServer !== 'function'){
      out.serviceDown = true; out.fail = jobs.length; return out;
    }

    var srcs = [];
    jobs.forEach(function(j){ if(srcs.indexOf(j.src) === -1) srcs.push(j.src); });

    // 先把"服务在不在"一次性问清楚，再逐张取图。
    // 别靠嗅探第一张的报错文案来判断服务死活——那既不准，又会让每张图都白等一遍探测。
    // 这一步最慢：8765 探测 8s + 唤起 launcher + 等 Chromium 冷启动最多 30s，实测服务确实没起时约 39s，
    // 所以必须挂常驻 toast 说明在等什么，不能让用户对着不动的界面猜。
    if(mediaCache.size < srcs.length){
      showToast('正在唤起原型导出服务（首次启动较慢，最长约 40 秒）…', false, true);
      try{
        await window.ensureExportServerReady();
      }catch(e){
        console.warn('[copy-all] 导出服务不可用', e);
        out.serviceDown = true; out.fail = srcs.length; return out;
      }
    }

    for(var i=0;i<srcs.length;i++){
      var src = srcs[i];
      if(mediaCache.has(src)){ out.ok++; continue; }
      showToast('正在生成图片 '+(i+1)+'/'+srcs.length+'…', false, true);
      var kind = jobs.filter(function(j){ return j.src === src; })[0].kind;
      try{
        var data = kind === 'frame'
          ? await window.snapshotPrototypeViaServer(src, {})
          : await window.inlineAssetViaServer(src, {});
        mediaCache.set(src, await shrinkDataUrl(data.dataUrl, MAX_IMG_WIDTH)); out.ok++;
      }catch(e){
        console.warn('[copy-all] 取图失败', src, e);
        out.fail++;   // 单张失败不影响其余，最后由 toast 如实报数
      }
    }
    return out;
  }

  // ③ 落图 + 清编辑痕迹 + 补排版
  function finalizeClone(clone, jobs){
    (jobs||[]).forEach(function(j){
      var url = mediaCache.get(j.src);
      if(j.kind === 'frame'){
        if(!url){ j.el.remove(); return; }              // 原型取图失败 → 退回删除
        var img = document.createElement('img');
        img.src = url;
        img.alt = j.el.getAttribute('title') || '原型预览';
        img.style.cssText = 'max-width:100%;height:auto;border:1px solid #e5e3f5;border-radius:8px;';
        j.el.replaceWith(img);
      } else if(url){
        j.el.setAttribute('src', url);                  // 截图内联失败 → 保留原样，由 toast 如实报数
      }
    });
    clone.querySelectorAll('[contenteditable]').forEach(function(el){ el.removeAttribute('contenteditable'); });
    ['data-changed','data-original','data-orig','data-pm-tracked'].forEach(function(a){ clone.querySelectorAll('['+a+']').forEach(function(el){ el.removeAttribute(a); }); });
    clone.querySelectorAll('.edited-cell').forEach(function(el){ el.classList.remove('edited-cell'); });
    clone.querySelectorAll('table').forEach(function(t){ t.style.borderCollapse='collapse'; t.style.width='100%'; });
    clone.querySelectorAll('th,td').forEach(function(c){ c.style.border='1px solid #ccc'; c.style.padding='6px 10px'; c.style.verticalAlign='top'; });
    clone.querySelectorAll('th').forEach(function(c){ if(!c.style.background) c.style.background='#f2f1f8'; });
    clone.querySelectorAll('img').forEach(function(img){
      try{ if(!/^data:/i.test(img.getAttribute('src')||'')) img.setAttribute('src', img.src); }catch(e){}
    });
    return clone;
  }

  function showToast(msg, err, sticky){
    var t=document.querySelector('.copy-toast');
    if(!t){ t=document.createElement('div'); t.className='copy-toast'; document.body.appendChild(t); }
    t.textContent=msg; t.style.background= err? '#c0392b' : '#2a2459'; t.classList.add('show');
    clearTimeout(showToast._t);
    if(!sticky) showToast._t=setTimeout(function(){ t.classList.remove('show'); }, 2600);
  }

  async function writeClipboard(html, text){
    try{
      if(navigator.clipboard && window.ClipboardItem){
        await navigator.clipboard.write([new ClipboardItem({
          'text/html': new Blob([html],{type:'text/html'}),
          'text/plain': new Blob([text],{type:'text/plain'})
        })]);
        return true;
      }
      throw new Error('no async clipboard');
    }catch(e){
      var holder=document.createElement('div'); holder.setAttribute('contenteditable','true');
      holder.style.cssText='position:fixed;left:-99999px;top:0;opacity:0;'; holder.innerHTML=html;
      document.body.appendChild(holder);
      var range=document.createRange(); range.selectNodeContents(holder);
      var sel=window.getSelection(); sel.removeAllRanges(); sel.addRange(range);
      var okc=document.execCommand('copy'); sel.removeAllRanges(); holder.remove();
      if(!okc) throw new Error('execCommand 拒绝');
      return true;
    }
  }

  async function copyAllContent(){
    try{
      var clone = stripSkeleton();
      var media = await collectMedia(clone);
      finalizeClone(clone, media.jobs);
      await writeClipboard('<meta charset="utf-8">'+clone.innerHTML, clone.innerText);
      if(media.serviceDown)     showToast('导出服务未启动，已按纯文本复制（原型图缺失）', true);
      else if(media.fail)       showToast('已复制全文，含 '+media.ok+' 张图，'+media.fail+' 张生成失败已跳过', true);
      else if(media.ok)         showToast('已复制全文（含 '+media.ok+' 张图），可直接粘贴到钉钉/飞书/Word');
      else                      showToast('已复制全文，可直接粘贴到钉钉/飞书/Word');
    }catch(e){
      showToast('复制失败，请手动全选复制：'+(e.message||e), true);
    }
  }
  window.copyAllContent=copyAllContent;
})();
```

**⑧ CSS 草图：**
```css
.copy-all-fab { position:fixed; left:28px; bottom:28px; z-index:1001; background:#fff; color:#3b357a; border:1px solid #d8d4f0; border-radius:12px; padding:13px 20px; font-size:14px; font-weight:700; cursor:pointer; box-shadow:0 4px 16px rgba(91,91,214,.18); display:flex; align-items:center; gap:8px; }
.copy-all-fab:hover { transform:translateY(-2px); border-color:#5b5bd6; }
.copy-toast { position:fixed; left:28px; bottom:80px; z-index:1002; max-width:360px; background:#2a2459; color:#fff; padding:11px 16px; border-radius:10px; font-size:13px; box-shadow:0 8px 24px rgba(20,16,70,.28); opacity:0; transform:translateY(8px); pointer-events:none; transition:opacity .2s, transform .2s; }
.copy-toast.show { opacity:1; transform:translateY(0); }
```

> **取材限制（据实说明，勿夸大）：**
> - base64 内联图**不依赖本地路径**，这正是必须走服务出 base64、而不是贴相对路径 `<img>` 的原因。
> - 但**目标文档是否真的会把 base64 图存下来，取决于它自己的粘贴实现**——钉钉/飞书/Word 各不相同，首次接入某个目标文档时**必须人工粘一次确认**，不要向用户承诺"一定能带图"。
> - **耗时实测**（AI口述题 PRD，2 个 iframe + 8 张原型截图）：截图已存在时**全程 0.7 秒**（10 张全部命中缓存）；服务没起、需要唤起并冷启动 Chromium 时最长约 **40 秒**；确认服务起不来时也是这个量级才出降级提示——所以那句常驻 toast 不能省。
> - 复制出的富文本约 **3.8MB**（10 张图解码后 2.83MB，base64 文本再膨胀 1.33×；原始素材 19.5MB，经 ⑤ 降采样）。**报体积给用户时要报剪贴板里的 base64 量，不是解码后的字节数**——两者差 1/3，按后者承诺会低估。

---

### 2.9 内网（http · 不安全上下文）下的真实边界（必须如实告知用户，不许含糊）

PRD HTML 会被推到公司内网供多人浏览。内网是 `http://` 非 localhost，属**不安全上下文**——`navigator.clipboard`、`ClipboardItem`、`showSaveFilePicker` 一律不存在。不要按"我本机点着好使"就当功能可用。

| 能力 | 作者本机（`file://`） | 内网访客（`http://` 非 localhost） |
|---|---|---|
| `💾 保存并通知AI` | ✅ 覆写本地文件 | ⚠️ 无 File System Access → 降级为**下载一份副本** |
| `📋 一键复制全文` | ✅ | ✅ 但 `navigator.clipboard` 在不安全上下文不存在，**必须有 `execCommand` 兜底**否则整个复制哑火 |
| 原型取图（`/api/snapshot`、`/api/asset`） | ✅ | ✅ 但服务端要按项目目录相对解析发起页，见下面这条踩坑 |

> **踩坑（v2.7 修正）：** 内网用 http 打开时 `location.pathname` 是**站点根路径**、磁盘上并不存在，导出服务旧版只按绝对路径解析发起页，导致 `/api/snapshot` 与 `/api/asset` 全返 400、「一键复制全文」**一张图都取不到**（toast 还只说"生成失败"）。服务端 `_resolve_base_html()` 必须**再按项目目录相对解一次**。

> 任何一档降级都要在 toast 里讲清楚丢了什么（§2.8 降级三档），不许静默失败。

---

## 步骤三：产出原型

### 3.1 规范

1. 根据PRD中的详细方案设计交互原型
2. 使用 **HTML单文件** 实现所有页面状态，通过 URL hash 切换视图，如：
   - `prototype.html#home`
   - `prototype.html#camera`
   - `prototype.html#result-success`
3. 无 hash 打开时默认平铺展示全部页面状态，便于评审和截图；带 hash 时只展示对应页面
4. 技术栈：**Tailwind CSS + Font Awesome**（CDN引入），无需构建工具
5. **极度重要（真实渲染导出）：** 页面内建悬浮导出按钮 `📸 一键导出所有截图`，仅在平铺模式下显示；按钮必须接入 `../scripts/prototype-export-client.js`，优先调用本地 `scripts/prototype_server.py`，用 Playwright/Chromium 对真实 HTML 渲染结果截图，不再用 `html-to-image` / `html2canvas` 作为默认导出方案。
6. **极度重要（保存路径与命名）：** 导出 PNG 自动保存到该需求自己的目录 `[需求名]/原型截图/`（由导出服务根据原型 HTML 所在位置自动推导）；文件名优先使用原型下方 `.device-label`，其次使用 `.page-title` / 注释中的界面名称，保证和界面名称一致。
   > **极度重要（截图目录是 PM 的资产目录，不许通配符清场）：** 每轮导出前清理上一轮产物时，**只能删本 HTML 在 `.export-manifest.json` 里登记过的文件名**，绝不能用 `*.png` 把整个 `原型截图/` 清空。
   > **实测踩过（删了 8 张补 1 张）：** `原型截图/` 里同时躺着 PM 手工产物 —— 用 `[需求名]-shots.html`（状态可寻址的截图版）按 hash 一个状态一张手截、手工命名（`01-章节详情页.png`…），PRD 的「原型」列直接 `<img>` 引这些名字。而对 `[需求名]-prototype.html` 跑一次导出时，它本身没有 `.device` 节点、只出 1 张整页图，`*.png` 却把那 8 张全删了，PRD 当场变一片碎图，且**这些图不在 git 里，删了就没了**。


7. **极度重要（导出服务）：** 项目根目录提供 `启动原型导出服务.command`。初始化时会尝试安装 macOS LaunchAgent watcher；点击导出按钮时若 `localhost:8765` 暂未响应，按钮需显示“正在连接导出服务”，并提示用户双击 `.command` 或等待 watcher 拉起服务。浏览器安全限制下，HTML 不能直接启动 Python 进程。
8. 同时保留 `trigger-export` 的 `postMessage` 监听，以兼容 iframe 嵌入场景；无 hash 时 body 加 `.tiled` class 平铺展示所有 `.device`，有 hash 时只显示对应单页。
9. **极度重要（单页模式 CSS 陷阱）：** 单页模式下**禁止**对 `.gallery` 等包裹容器设置 `display: none`，否则内部 `.device` 即使有 `!important` 也不会显示（CSS 继承：父隐藏则子不可见）。正确做法：保持 `.gallery` 为 `display: block`，隐藏每个 `.device-wrapper`，仅对 `.device-wrapper.active` 设置 `display: flex`。JS init 中通过 `device.closest('.device-wrapper')` 找到父容器加 `active` 类。
10. 保存路径：`[需求名]/原型/[需求名]-prototype.html`（相对于项目根目录）
11. 原型 HTML 底部必须加入 `<script src="../../scripts/prototype-export-client.js?v=YYYYMMDD"></script>`，导出按钮使用 `id="exportFab"` 或 `.export-btn`，不要绑定旧的 `html-to-image` 导出函数。
    > **路径说明：** 原型位于 `[需求名]/原型/`，而导出脚本在项目根目录 `scripts/` 共享，因此需 `../../`（退两级）回到根目录再进 `scripts/`。
12. **极度重要（原型 ↔ PRD 内容对齐）：** 原型中展示的所有文案、数据、状态标签、按钮文字、提示信息必须与 PRD「六、详细方案」中对应行的「描述」列内容逐条一致。具体对齐规则：
    - **文案对齐**：原型中的标题、按钮文字、提示文案、空状态文案必须与 PRD 描述中的文字完全一致，不允许原型上写"开始分析"而 PRD 写"立即分析"
    - **数据对齐**：原型中使用的示例数据（如"剩余额度 8/10次"、"综合得分 82分"）必须与 PRD 描述中提到的数据保持一致
    - **状态对齐**：原型中展示的状态标签（已完成/分析中/失败等）及其颜色必须与 PRD 描述的状态定义一致
    - **流程对齐**：原型中的页面跳转逻辑（点击A → 跳转到B）必须与 PRD 描述的交互流程一致

### 3.2 设计规范

- K12教育风格：活泼配色（主色绿/蓝）、圆角卡片、质感阴影
- 原型容器尺寸必须与真实业务端一致，**不要默认套手机竖屏**；例如大班课课中场景优先使用课堂横屏比例
- 无 hash 预览场景下，页面容器需要支持多页平铺；iframe 单页预览场景再按 hash 精确展示
- 容器使用 `.device` 类；建议通过 `.gallery-mode` 和 `.single-mode` 两种状态切换展示方式
- 若页面使用字体图标、彩色图标按钮或状态徽标，必须提前考虑导出后的还原效果，优先采用内联 SVG 或为导出单独准备 fallback

### 3.3 嵌入PRD的方式

原型通过 **等比例缩放容器 + `<iframe>`** 嵌入到 PRD 表格对应行的「原型」列：

```html
<div class=”prototype-frame” data-pw=”375” data-ph=”700”>
  <iframe 
    class=”prototype-iframe”
    src=”../原型/[需求名]-prototype.html#page-id”>
  </iframe>
</div>
```

> **⚠️ 关键实现约束（踩坑记录）：**
>
> **禁止使用 CSS 变量 + calc 来设置 iframe 尺寸。** `calc(var(--prototype-width) * 1px)` 这种 unitless 变量乘 px 的写法在多数浏览器中不生效，会导致原型区域一片空白。
>
> **正确做法：** 原始宽高通过 `data-pw` / `data-ph` data 属性传递，由 JS 读取后显式设置 iframe 的 `width`、`height`（带 px 单位）和 `transform: scale()`。

**CSS 规范：**
```css
.prototype-frame {
  position: relative; overflow: hidden; border-radius: 8px;
  background: #f5f5f5; width: 320px; /* 默认预览宽度 */
}
.prototype-iframe {
  position: absolute; top: 0; left: 0;
  border: none; background: transparent;
  transform-origin: top left;
}
```

**JS 缩放逻辑（必须内嵌在 PRD HTML 底部）：**
```js
function scalePrototypes() {
  document.querySelectorAll('.prototype-frame').forEach(frame => {
    const pw = parseInt(frame.dataset.pw) || 375;
    const ph = parseInt(frame.dataset.ph) || 700;
    const iframe = frame.querySelector('.prototype-iframe');
    if (!iframe) return;
    iframe.style.width = pw + 'px';
    iframe.style.height = ph + 'px';
    const containerWidth = frame.clientWidth || 320;
    const scale = containerWidth / pw;
    iframe.style.transform = 'scale(' + scale + ')';
    frame.style.height = Math.round(ph * scale) + 'px';
  });
}
window.addEventListener('load', scalePrototypes);
window.addEventListener('resize', scalePrototypes);
setTimeout(scalePrototypes, 500); // 兜底：确保 iframe 加载后尺寸正确
```

> **其他注意事项：**
> - 鼠标 hover 到原型右下角区域时出现可拖拽缩放的交互提示，不要展示常驻箭头或按钮。
> - 用户拖拽任意一个原型后，当前 PRD 页面中的所有原型预览都要保持统一比例同步变化，不能只改当前这一张。
> - 原型列宽和对应容器尺寸要跟随缩放一起自动变化，不允许出现”原型变大了，但表格边界还得手动再拉”的情况。
> - 不要额外做全局”缩放操作面板”。
> - `border: none; background: transparent;` 去除外框，避免双重边框视觉问题。
> - 相对路径基于 PRD 文件所在目录（`[需求名]/需求文档/`）往上一级，再进同需求的 `[需求名]/原型/` 目录。PRD 与原型同属一个需求顶层目录、互为同级，故 iframe 的 `src` 仍写 `../原型/[需求名]-prototype.html#page-id`（路径值不变）。

### 3.4 原型交互增强规范

#### 3.4.1 Tab 切换模式

当多个关联页面属于同一层级时（如 报告概览/错题分析/提升计划），**合并为单页 + Tab 面板切换**，而非拆成独立页面。

**HTML 结构模式：**
```html
<!-- Tab 切换栏 -->
<div id="xxxTabs" style="background:#F0F0F5;border-radius:12px;padding:3px;display:flex">
  <div class="xxx-seg active" data-tab="tab-a" style="flex:1;...">标签A</div>
  <div class="xxx-seg" data-tab="tab-b" style="flex:1;...">标签B</div>
  <div class="xxx-seg" data-tab="tab-c" style="flex:1;...">标签C</div>
</div>
<!-- Tab 面板 -->
<div id="tab-a" class="xxx-panel">面板A内容</div>
<div id="tab-b" class="xxx-panel" style="display:none">面板B内容</div>
<div id="tab-c" class="xxx-panel" style="display:none">面板C内容</div>
```

**CSS：**
```css
.xxx-seg { color: #8E8EA0; background: none; font-weight: 500; transition: all .2s; }
.xxx-seg.active { background: #fff; font-weight: 600; color: #1a1a2e; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
```

**JS：**
```js
// 共享切换函数
function switchTab(tabId) {
  document.querySelectorAll('.xxx-seg').forEach(s => s.classList.toggle('active', s.dataset.tab === tabId));
  document.querySelectorAll('.xxx-panel').forEach(p => p.style.display = 'none');
  var target = document.getElementById(tabId);
  if (target) target.style.display = '';
}
// 绑定点击
document.querySelectorAll('.xxx-seg').forEach(seg => {
  seg.addEventListener('click', function() { switchTab(this.dataset.tab); });
});
```

**适用场景：** 报告类（多维度展示）、设置类（分类配置）、详情类（多Tab信息）。

#### 3.4.2 PostMessage 双向通信协议（PRD ↔ 原型 iframe）

**原型 → PRD（页面切换通知）：**
```js
// 原型内部：页面切换时
window.parent.postMessage({ type: 'page-changed', page: 'report-overview' }, '*');
// 原型内部：Tab 切换时（附带 tab 字段）
window.parent.postMessage({ type: 'page-changed', page: 'report-overview', tab: 'tab-errors' }, '*');
```

**PRD → 原型（导航指令）：**
```js
// PRD 页面选择器切换时
frame.contentWindow.postMessage({ type: 'navigate', page: 'camera' }, '*');
```

**Tab 别名映射（向后兼容）：** 当页面合并为 Tab 后，旧的页面名需要映射到新的 Tab ID：
```js
const tabAliases = { 'report-errors': 'tab-errors', 'report-plan': 'tab-plan' };
// 收到 navigate 指令时：若命中 alias 则跳到目标页 + 切换 Tab
if (tabAliases[page]) { navigateTo('report-overview'); switchTab(tabAliases[page]); }
```

**PRD 侧同步处理：** PRD 的消息监听器需要根据 `tab` 字段反查选择器显示值：
```js
const tabToAlias = { 'tab-overview': 'report-overview', 'tab-errors': 'report-errors', 'tab-plan': 'report-plan' };
window.addEventListener('message', function(e) {
  if (e.data && e.data.type === 'page-changed') {
    const sel = document.getElementById('pageSelect');
    if (sel) sel.value = (e.data.tab && tabToAlias[e.data.tab]) ? tabToAlias[e.data.tab] : e.data.page;
  }
});
```

### 3.5 Pencil 高保真设计（可选增强）

> Pencil 是内置 MCP 协议的设计工具，Claude Code 通过 MCP 直接调用其设计能力，可以产出比纯 HTML 更精美的高保真原型。

#### 3.5.1 触发与选择

HTML 原型完成后，**主动询问用户**是否需要 Pencil 增强：

> HTML 交互原型已完成。需要用 Pencil 生成高保真设计稿吗？
> - **使用 Pencil**：设计效果更精美，可导出高清截图，适合对外评审
> - **跳过 Pencil**：直接使用 HTML 原型，适合内部快速迭代
>
> （如果你的电脑没有安装 Pencil，可以跳过，后续随时补做）

用户选择使用 Pencil 后，进入环境检测流程。

#### 3.5.2 Pencil 环境检测与安装引导

**自动检测流程：**

```
用户选择使用 Pencil
    ↓
检测 /Applications/Pencil.app 是否存在
    ├─ 不存在 → 引导安装 Pencil（见下方）
    └─ 存在 → 检测 Pencil 是否正在运行（ps aux | grep Pencil）
         ├─ 未运行 → 提示用户：「请先打开 Pencil 应用，打开后告诉我」
         └─ 已运行 → 检测 MCP 连接是否可用
              ├─ MCP 不可用 → 检查 .mcp.json 配置 + 尝试 WebSocket 直连降级
              └─ MCP 可用 → 开始 Pencil 设计流程 ✅
```

**Pencil 安装引导（未安装时展示）：**

> **Pencil 安装步骤：**
> 1. 前往 Pencil 官网下载 Mac 版安装包
> 2. 将 Pencil.app 拖入 `/Applications/` 目录
> 3. 首次打开后，在 Pencil 设置中启用 **MCP Server**（会自动生成 `~/.pencil/mcp/` 目录）
> 4. 在项目根目录创建 `.mcp.json` 配置文件：
> ```json
> {
>   "mcpServers": {
>     "pencil": {
>       "command": "~/.pencil/mcp/claudeCodeCLI/out/mcp-server-darwin-arm64",
>       "args": ["--app", "claudeCodeCLI", "-enable_spawn_agents"]
>     }
>   }
> }
> ```
> 5. 重启 Claude Code，确认 MCP 连接成功
>
> 安装完成后告诉我，我继续帮你画高保真原型。如果暂时不想装，可以跳过此步骤，HTML 原型不受影响。

#### 3.5.3 设计变量体系

Pencil 设计和 HTML 原型应共用同一套配色体系，确保视觉一致性。K12 教育场景的默认变量：

| 变量 | 色值 | 用途 | HTML CSS 对应 |
|------|------|------|---------------|
| `$primary` | `#00B894` | 主色（薄荷绿） | `--color-primary` |
| `$accent` | `#0EA5E9` | 辅助色（蓝） | `--color-accent` |
| `$bg` | `#F7F8FA` | 页面背景 | `background` |
| `$border` | `#F0F0F5` | 卡片描边 | `border-color` |
| `$text-primary` | `#1A1A2E` | 主文字 | `color` |
| `$text-secondary` | `#8E8EA0` | 辅助文字 | `color` |
| `$danger` | `#FF6B6B` | 错误/失败 | 状态标签 |
| `$warning` | `#FFB946` | 警告/进行中 | 状态标签 |

- 在 Pencil 中通过 `set_variables` 设置全局变量
- 在 HTML 中确保相同色值，不要出现 Pencil 用 `#00B894` 而 HTML 用 `#00c9a7` 的不一致
- 用户可根据产品风格自定义这套变量，但两端必须同步

#### 3.5.4 Pencil 设计工作流程

```
HTML原型（已完成） + 环境检测通过
    ↓
① 打开 Pencil → open_document（新建或打开已有 .pen 文件）
    ↓
② 设置设计变量 → set_variables（写入 3.5.3 中定义的配色变量）
    ↓
③ 加载设计规范 → get_guidelines（获取可用的 guide 和 style 列表）
    ↓
④ 批量创建页面 → batch_design + spawn_agents（多页面可并行）
   · 每次 batch_design 不超过 25 个操作
   · 多页面场景用 spawn_agents 拆分为并行子任务
   · 先创建页面骨架（frame/layout），再逐步填充内容
    ↓
⑤ 截图验证 → get_screenshot（逐页截图检查效果）
   · 必须仔细检查截图：布局对齐、文字可读性、颜色一致性
   · 发现问题立即用 batch_design 修正
    ↓
⑥ 向用户展示确认
   · 将截图展示给用户，逐页确认
   · 用户提出修改意见后迭代
    ↓
⑦ 导出 PNG → export_nodes
   · 格式：PNG，2x 分辨率
   · 输出目录：[需求名]/原型截图/
   · 命名规则：[需求名]-[页面ID].png
    ↓
⑧ HTML ↔ Pencil 视觉一致性校准（见 3.5.5）
    ↓
⑨ 更新 PRD
   · 原型列 iframe 仍指向 HTML 原型（保持可交互预览）
   · 描述列可附上 Pencil 导出的高保真截图作为视觉参考（可选）
```

#### 3.5.5 HTML ↔ Pencil 视觉一致性校准

Pencil 设计稿完成后，**必须反向校准 HTML 原型**使两端视觉一致。否则 PRD 中左侧截图和右侧 iframe 会出现明显的视觉差异。

**校准步骤：**

1. **逐页读取 Pencil 节点属性**：用 `batch_get` 读取每个页面关键节点的颜色、渐变、间距、圆角
2. **对照检查清单**：
   - 渐变色值和方向（如 `linear-gradient(135deg, #00B894, #0EA5E9)` vs `90deg`）
   - 卡片边框（Pencil 用 `border` 还是 `box-shadow`？HTML 需保持一致）
   - 状态标签配色（已完成=绿、分析中=橙、失败=红）
   - 按钮样式（渐变 vs 纯色、圆角大小）
   - 字号和字重
3. **更新 HTML CSS**：逐一修正差异，保持 HTML 原型的交互能力不变
4. **刷新 PRD 验证**：在 PRD 双栏预览中确认左右一致

#### 3.5.6 MCP 工具调用参考

| 步骤 | MCP 工具 | 用途 |
|------|----------|------|
| 打开文件 | `open_document` | 传入 .pen 文件路径，或 `"new"` 新建 |
| 了解规范 | `get_guidelines` | 先不传参获取列表，再按名称加载具体 guide/style |
| 了解结构 | `get_editor_state` | 获取当前画布状态，首次必须 `include_schema: true` |
| 读取节点 | `batch_get` | 查询已有节点、设计系统组件列表 |
| 设计操作 | `batch_design` | I()插入、U()更新、C()复制、R()替换、D()删除、G()生成图片 |
| 并行设计 | `spawn_agents` | 多页面/多区块拆分为并行 Agent |
| 截图检查 | `get_screenshot` | 传入 nodeId 获取截图验证 |
| 布局检查 | `snapshot_layout` | 检查对齐和溢出问题 |
| 导出图片 | `export_nodes` | 导出 PNG/JPEG/WEBP/PDF |
| 设计变量 | `get_variables` / `set_variables` | 管理全局颜色、字体等主题变量 |

#### 3.5.7 文件路径约定

| 文件类型 | 路径 | 说明 |
|----------|------|------|
| Pencil 源文件 | `[需求名]/原型/[需求名].pen` | 设计源文件，可反复编辑 |
| 导出截图 | `[需求名]/原型截图/[需求名]-[页面ID].png` | 2x 分辨率 PNG |
| HTML 原型 | `[需求名]/原型/[需求名]-prototype.html` | 保持可交互，视觉对齐 Pencil 稿 |

#### 3.5.8 注意事项

1. **HTML 原型是主交付物**：Pencil 设计是视觉增强，HTML 原型仍然是 PRD 中嵌入的主要载体。没有 Pencil 不影响整个工作流运转
2. **Pencil 必须处于打开状态**：MCP 工具依赖 Pencil 应用运行，调用前确认 Pencil 已启动
3. **batch_design 操作上限**：单次不超过 25 个操作，大设计拆分多次调用
4. **binding 命名**：每次 batch_design 调用必须使用全新的 binding 名称，禁止跨调用复用
5. **图片节点**：没有 `image` 类型节点，图片通过 `G()` 操作应用为 frame/rectangle 的 fill
6. **spawn_agents 并行**：创建 N 个页面时，spawn N-1 个 Agent，当前会话做最后一个
7. **截图必查**：每次设计操作后必须 `get_screenshot` 验证，不能盲写
8. **设计变量同步**：Pencil 和 HTML 必须使用同一套色值，见 3.5.3

#### 3.5.9 MCP 连接故障排查

当 MCP 连接不可用时，按以下顺序排查：

1. **检查 Pencil 是否运行**：`ps aux | grep -i pencil`
2. **检查 .mcp.json 配置**：确认 `command` 路径指向 `~/.pencil/mcp/claudeCodeCLI/out/mcp-server-darwin-arm64`
3. **检查是否有僵尸进程**：`ps aux | grep mcp-server` 查看是否有多个残留进程，用 `kill` 清理
4. **重启 Claude Code**：退出并重新进入，让 MCP 重新建立连接
5. **WebSocket 直连降级**：若 MCP bridge 始终无法恢复，可通过 Python websockets 直连 Pencil：
   - 连接地址：`ws://[::1]:61969/`
   - 认证：发送 `{"type": "identify", "app": "claudeCodeCLI"}` 获取 `client_id`
   - 调用格式：`{"request_id": "xxx", "client_id": "xxx", "name": "get-editor-state", "payload": {...}}`
   - 方法名使用 **kebab-case**（如 `batch-design`、`export-nodes`），不是 snake_case

### 3.6 原型完成后一致性自查（极度重要）

原型 HTML 全部绘制完成后，**必须逐页对照 PRD 进行一致性校验**，校验通过后才能进入下一步。

#### 自查流程

```
原型绘制完成
    ↓
逐页读取原型 HTML 中的文案/数据/状态
    ↓
对照 PRD「六、详细方案」中对应行的「描述」列
    ↓
发现不一致？
    ├─ 原型错误 → 修改原型 HTML
    └─ PRD 描述不够准确 → 修改 PRD 描述列
    ↓
全部一致 → 进入步骤四
```

#### 逐页校验检查项

对每个原型页面，依次检查：

| # | 检查项 | 说明 |
|---|--------|------|
| 1 | 页面标题/导航栏标题 | 与 PRD 二级功能名一致 |
| 2 | 按钮文字 | 与 PRD 描述中的操作文案一致 |
| 3 | 提示文案/说明文字 | 包括 Toast、弹窗内容、空状态提示 |
| 4 | 示例数据 | 列表项名称、数值、日期等 |
| 5 | 状态标签 | 文字 + 颜色 与 PRD 状态定义一致 |
| 6 | 页面跳转目标 | data-goto / hash 跳转与 PRD 流程一致 |
| 7 | Tab/分段标签 | 标签文字和数量与 PRD 一致 |

#### 交付声明

校验完成后，在回复中附上一致性确认：

> ✅ 原型 ↔ PRD 一致性校验完成，共 N 个页面已逐一核对，全部通过。

---

## 步骤四：产出流程图与交互流程图（均可裁剪）+ 时序图章节规范

> **前置判断：** 本步骤覆盖 PRD 三个按需裁剪章节（见 2.2 / 1.3.1）：「四、流程图」（Mermaid 文件，业务逻辑层，§4.1–4.5）、「五、交互流程图」（界面跳转链路层，独立 HTML，§4.6）与「九、时序图」（端侧编排层，研发/测试向，**PRD 内 Mermaid 源码文本章节**，§4.7）。三者各自独立裁剪：省略哪章就跳过对应小节；前两者都省略则不产出 `[需求名]/流程图/` 目录。以下规范仅对保留的章节执行。

### 4.1 规范

1. 使用 **Mermaid** 语法绘制，保存为独立 HTML 文件
2. `mermaid.esm.min.mjs` 通过 jsdelivr CDN 引入
3. 每个图表是独立的 `<div class="chart-container">` 块
4. 保存路径：`[需求名]/流程图/[需求名]-flow.html`（相对于项目根目录）

### 4.2 常用图表类型

| 图表类型 | Mermaid关键字 | 适用场景 |
|----------|--------------|----------|
| 时序图 | `sequenceDiagram` | 多角色/多系统交互（用户→客户端→服务端→AI） |
| 活动/流程图 | `flowchart TD` | 单用户操作路径、异常分支处理 |
| 状态图 | `stateDiagram` | 订单/任务状态流转 |

### 4.3 Mermaid语法注意事项

- 活动图中若节点标签含有 `()` 等特殊字符，容易触发 **Syntax error**，建议将此类图表拆分为独立文件，逐一验证
- 如果某个图表渲染报错，**直接删除该段**，不影响文档其他内容
- 流程图节点标签如包含中文括号或引号，先用浏览器渲染验证后再嵌入

### 4.4 嵌入PRD的方式

```html
<iframe 
  src="../流程图/[需求名]-flow.html"
  style="width: 100%; height: 800px; border: none; background: transparent;">
</iframe>
```

### 4.5 导出截图必走本地导出服务（必做 · 踩坑记录）

> **背景（踩坑记录）：** 流程图常常比视口高很多。若导出按钮**直接在浏览器里用 `html-to-image`/`html2canvas` 截 `.chart-container`**，长图会被**截掉一半**（受浏览器画布尺寸/视口限制）。项目早已为此做了**本地导出服务**（`scripts/prototype_server.py`，Playwright 对每个 `.chart-container` 做**整元素截图**，不受视口高度限制），却容易在新生成流程图时漏接，退化成半张图。**故固化为必做项。**

**① 每个流程图 HTML 必须接入导出服务客户端**（与原型导出同一套）：
```html
<button class="export-btn" onclick="exportChart()">📸 导出截图</button>
<!-- 路径取决于嵌套层级：[需求名]/流程图/ 下为 ../../scripts/；旧扁平 流程图/ 下为 ../scripts/ -->
<script src="../../scripts/prototype-export-client.js?v=YYYYMMDD-flow"></script>
```
- 客户端会在**捕获阶段**拦截 `.export-btn`/`.export-fab`/`#exportFab` 的点击，转而 POST `http://localhost:8765/api/screenshot`，由服务用 Playwright 截图，输出到 `[需求名]/流程图截图/`（旧扁平结构回退项目根 `流程图截图/`）。服务未启动时会自动尝试 launcher 唤起，仍失败则提示用户双击根目录「启动原型导出服务.command」。

**② `onclick` 仅作降级兜底**：服务客户端加载时它不会触发（点击已被捕获）。兜底实现必须**服务优先 + 整图**：先 `window.exportPrototypeViaServer(btn)`，失败再 `html-to-image`，且**必须按完整 scroll 尺寸截**，否则仍是半张：
```js
async function exportChart(){
  const btn=document.querySelector('.export-btn'), t=btn.textContent, bg=btn.style.background;
  btn.textContent='⏳ 导出中...'; btn.disabled=true;
  if(window.exportPrototypeViaServer){ try{ await window.exportPrototypeViaServer(btn); return; }catch(e){ console.warn('服务导出失败，降级',e); } }
  try{
    const {toBlob}=await import('https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/+esm');
    const node=document.querySelector('.chart-container'), s=2;
    const blob=await toBlob(node,{cacheBust:true,backgroundColor:'#ffffff',pixelRatio:s,
      width:node.scrollWidth,height:node.scrollHeight,canvasWidth:node.scrollWidth*s,canvasHeight:node.scrollHeight*s,style:{transform:'none'}});
    const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='[需求名]-流程图.png'; a.click(); URL.revokeObjectURL(a.href);
    btn.textContent='✅ 已导出';
  }catch(e){ console.error(e); btn.textContent='❌ 失败'; btn.style.background='#ef4444'; }
  setTimeout(()=>{ btn.textContent=t; btn.style.background=bg; btn.disabled=false; },2200);
}
```
**③ 自检：** 流程图产出后，按「四、原型一致性自查」同理确认导出按钮已 `include` 客户端脚本、路径层级正确（嵌套 `../../`）、点击能走服务出全图——**不允许只留裸 `html-to-image` 按钮**。

### 4.6 交互流程图（Screen Flow · 界面跳转链路整图，可裁剪）

> **前置判断：** 对应 PRD「五、交互流程图」章节，按需裁剪（见 2.2 / 1.3.1）。核心界面 ≤2 个、或页面间无跳转链路且无状态流转 → 整节跳过。
>
> **定位：** 与 §4.1 的 Mermaid 流程图**并存、各管一层**——Mermaid 管业务/时序/状态逻辑，交互流程图管「界面长什么样、从哪跳到哪」。目标是：**所有核心界面的缩略图拼成一整张图，界面之间用带触发标签的箭头连线标注跳转关系**，评审者不读正文也能看懂整条产品链路。

**① 文件与嵌入：**
- 保存路径：`[需求名]/流程图/[需求名]-screenflow.html`
- PRD「五、交互流程图」章节以 iframe 嵌入（同 §4.4 方式，高度按画布实际高度给足），一整张图即可，不拆多图
- **章节内只放 iframe，不加说明段落**：图本身自解释（箭头标签+状态机图例），导出入口等说明在 screenflow 页头自带，PRD 里不重复写"这是什么图/怎么导出"之类的引导文字
- **必须带缩放控件（放大/缩小/适配）**：右上角 `position:fixed` 一组 `📸 下载图片 / ＋ / 百分比 / － / 适配` 按钮 + 按住画布拖拽平移（节点 iframe 已 `pointer-events:none`，整个画布可抓取）。**嵌入 PRD（`self!==top`）默认"适配宽度"**，未手动缩放时窗口 resize 自动重新适配（如 PRD 开关双栏）；**独立打开默认 100%**——导出服务是独立加载页面，必须保证无缩放变换、按原尺寸截图
- **「📸 下载图片」按钮放在缩放控件组里（而非只放页头）**：页头在嵌入模式下隐藏，控件组常驻——PRD 内嵌预览里也能直接下载整张 PNG。按钮保留 `class="export-btn"` 以被导出服务客户端捕获拦截（同 §4.5，服务优先、html-to-image 兜底按原始尺寸截）
- **画布底部留白**：最外侧底部轨道的标签之下再留 ≥30px，防止贴边被 iframe/截图裁切；顶部轨道同理
- **界面节点直接用缩放 iframe 引真实原型 hash 页**（`../原型/[需求名]-prototype.html#page-id`，同级相对路径），原型改动自动同步到交互流程图，**禁止用截图 `<img>` 拼贴**（会随原型迭代失真）

**② HTML 结构：**
- 唯一画布 `<div class="chart-container screenflow-canvas">`（`position:relative`，白底，宽度按布局撑开）——**必须带 `chart-container` 类**，本地导出服务（§4.5）按该类做整元素截图，长图/宽图不裁切
- 界面节点 `.flow-node`：内含 `.node-frame`（缩放 iframe，复用 §3.3 的 `data-pw`/`data-ph` + JS 显式设宽高与 `transform:scale()` 方案，禁 CSS 变量 calc）+ `.node-label`（节点下方界面名）+ 可选 `.node-badge`（状态标记，如「首次使用」「上传成功」）
- 布局：主链路从左到右一行排开，分支/状态变体（如 非首次使用）另起一行放在对应节点下方——与示意图的排布方式一致
- 连线层 `<svg class="screenflow-svg">`：`position:absolute` 铺满画布、`pointer-events:none`，置于节点之上

**③ 箭头绘制（关键实现约束）：**
- **禁止手写死坐标画线。** 连线关系用数据驱动，JS 动态计算：

```js
// 每条边：from/to = 节点 id；label = 触发动作/条件；fromSide/toSide = 锚点方位
// bend = 同侧轨道外扩距离（多条同侧边用不同 bend 错峰）；fromOffset/toOffset = 锚点沿边平移，防同点多线重叠
// labelT = 标签在折线总长上的比例位置（默认取最长一段的中点）
const EDGES = [
  { from:'node-entry',  to:'node-scan',   label:'点击 拍照分析试卷', fromSide:'right', toSide:'left' },
  { from:'node-entry',  to:'node-history',label:'非首次使用',        fromSide:'bottom', toSide:'top'  },
  { from:'node-report', to:'node-entry',  label:'点「返回」',        fromSide:'top', toSide:'top', bend:130, toOffset:-25 },
];
```
- **连线必须是直角折线（Manhattan 路由），禁止贝塞尔曲线/斜线**（踩坑记录：曲线在长回环、多分支时相互交叉压节点，评审看不清）。逐段只能水平或垂直，按出/入方位路由：
  - 横出横入（right→left 等）：同 y 直连；不同 y 走中线 Z 形（`midX = (x1+x2)/2` 处两个直角）
  - 横出竖入 / 竖出横入：一个直角拐点（`(x2,y1)` / `(x1,y2)`）
  - 竖出竖入对穿（bottom→top）：同 x 直连；不同 x 走中线 Z 形
  - **同侧对（top→top / bottom→bottom，典型是"返回/重答"长回环）：走"轨道"** —— `rail = 端点外侧 bend px` 的水平横杆，多条同侧边用不同 `bend` 错峰，互不交叉且不越出画布
- JS 在 load 后读节点 `getBoundingClientRect()`（相对画布、除以当前缩放系数）取锚点 → 生成途经点数组 → 拼 `M/L` 折线 path + `marker-end` 三角箭头；`resize` 与 iframe load 后 `setTimeout` 兜底重算
- 标签放**最长一段的中点**（白底 `<rect>`+`<text>`，避免压线；密集处用 `labelT` 挪位）；分支从同一节点引出多条边，每条各带条件标签
- 节点/边一旦增删，只改 DOM 节点与 `EDGES` 数组，连线自动重算——不存在改布局后箭头错位的问题
- 参考实现：`AI口述题/流程图/AI口述题-screenflow.html`（已无头实测：17 边全为水平/垂直段、0 越界、0 交叉压节点）

**④ 状态机说明（必做）：**
- **同一界面的不同状态拆成独立节点**（如「试卷分析·首次使用」vs「试卷分析·非首次使用」、「确认上传」vs「上传成功」），节点标签注明状态，不允许一个节点糊多个状态
- 边上的 label 写「触发动作＋条件」（如「点击确认上传」「上传成功后自动」「额度=0 时」），条件分支必须每条边都有标签
- 画布角落放一个「状态机图例」块（`.state-legend`）：列出关键对象的完整状态流转链（如 `分析任务：待上传 → 上传中 → 等待分析 → 已完成/失败`），状态名称、颜色与 PRD 状态定义及原型状态标签一致

**⑤ 内容禁令：** 节点标签、箭头标签、状态图例全部用产品语言，**不出现任何技术接口表述**（同 §2.3.1 ③）。

**⑥ 导出与自检：**
- 按 §4.5 同一套规范接入本地导出服务：`<script src="../../scripts/prototype-export-client.js?v=YYYYMMDD-screenflow"></script>` + `.export-btn` 按钮，Playwright 对 `.chart-container`（即整张画布）整元素截图 → `[需求名]/流程图截图/`；**不允许裸 `html-to-image`**，降级兜底同 §4.5 ②
- 产出后自检：a) 节点覆盖 PRD 详细方案中的全部核心界面及其状态变体；b) 每条箭头与描述列【交互说明】的「操作 → 结果」逐条对应，无缺边、无多边；c) 状态机图例与 PRD 状态定义一致；d) 导出按钮走服务出整图

### 4.7 时序图（研发/测试向 · PRD 内文本章节 · 可裁剪）

> **前置判断：** 对应 PRD「九、时序图」章节（**位于「数据埋点」之后、上线计划/附录之前，即正文最后**），按需裁剪（见 2.2 / 1.3.1）。**受众是研发与测试**——研发照文本写逻辑、测试照文本写用例。无复杂端侧编排的简单需求（无语音/流式/多端协同/复杂动效状态机）→ 整章跳过。

**① 形态（极度重要）：Mermaid 源码文本，不渲染成图**
- 本章内容是**可复制的 Mermaid 源码文本块**（`<pre class="seq-code">` 等宽深色代码块），**不做 Mermaid 渲染、不出图片、不用 iframe**——渲染图研发/测试不好复用；源码文本可直接读、可整段复制到任意支持 Mermaid 的工具二次使用（踩坑记录：首版做成渲染图被打回）
- 每个代码块右上角一个「📋 复制源码」按钮（`navigator.clipboard` 优先、选区 `execCommand` 兜底）
- `<pre>` 不在 §2.7 编辑模块的可编辑选择器内，源码不会被误编辑，符合预期

**② 固定格式（两图为基本盘，可按需增减）：**
- 章首一句话说明本节构成与用途（1 张端侧总时序 + N 张关键对象状态图，给研发/测试直接复制使用）
- **图 1 · 端侧互动编排总时序**：`sequenceDiagram`，泳道按当前需求实际参与方设置（如 用户 / 端 / Cocos / 服务端），覆盖从进入页面到最终产物的完整编排：初始化、资源播放顺序、录音/输入开关时机、请求与返回、alt/loop 分支、收尾跳转
- **图 2 · 关键对象状态图**：`stateDiagram-v2`，对核心展示对象（如角色动效、任务状态）画完整状态流转
- 每个代码块下方附「**说明**」要点列表：列出图内不展开的约定（如末帧延续、重试进入顺序）与未纳入项

**③ 书写规范：**
- **动作名/资源名直接复用真实资源目录名**，不做二次命名（如 `出现-打招呼-介绍`、`倾听循环`）
- 关键时序约束用 `Note` 标注（如「control 先返回也要等 done 且播报完成后再提交新 control 推进状态」这类门控规则）
- 全局异常处理用图末 `Note over` 统一标注（网络异常重试、无识别文本补录等），口径与详细方案【边界说明】一致
- **技术字段豁免**：本章允许出现接口/字段/事件名（如 `voicechat/stream`、`nextStage`、`audio_chunk`）——§2.3.1 的"禁技术接口表述"只约束详细方案描述列，时序图本就是给研发/测试看的
- 源码虽不在 PRD 内渲染，交付前仍须在支持 Mermaid 的环境验证一遍**无 Syntax error**（语法注意事项同 §4.3），保证研发复制即可用
- 参考实现：`AI口述题/需求文档/AI口述题-PRD.html` 的「八、时序图」章节

**④ 一致性自检：** 时序图的分支与推进条件必须与详细方案【功能逻辑】【边界说明】口径一致（异常处理、重试规则、次数限制等）——两处冲突时**先对齐再交付**。

---

## 步骤五：交付与评审

### 5.1 交付格式

| 产出物 | 生成格式 | 交付方式 |
|--------|----------|----------|
| **PRD文档** | HTML (.html) | 浏览器打开，直接截图到钉钉；或复制页面内容粘贴 |
| **原型** | HTML (.html) | 已内嵌在PRD的iframe中；也可单独提供文件 |
| **流程图** | HTML (.html) | 已内嵌在PRD的iframe中；也可单独提供文件 |
| **时序图** | PRD 内文本章节 | Mermaid 源码代码块 + 一键复制按钮（「九、时序图」，正文最后）；研发/测试直接复制源码使用，不渲染成图 |
| **交互流程图** | HTML (.html) | 已内嵌在PRD「五、交互流程图」章节iframe中；可经本地导出服务导出整张PNG |

> **交付到钉钉的方式：**
> 在浏览器中打开 PRD HTML 文件，对需要的部分用截图工具（Mac: `Cmd+Ctrl+Shift+4`）截图，然后直接 `Cmd+V` 粘贴到钉钉文档。

### 5.2 PRD最终检查清单

交付前确认（标 ★ 为核心骨架，始终检查；其余仅在该章节本次保留时检查）：
- [ ] ★ 保留的章节按 2.2 顺序自上而下排列，编号连续无跳号
- [ ] ★ 本次省略的章节已在需求确认阶段告知用户并获认可（1.3.1）
- [ ] ★ 详细方案表格为四列格式，rowspan合并一级模块
- [ ] ★ 描述列按 §2.3.1 分块结构组织：【页面元素】【交互说明】必出、按需块不硬凑，且全文**无任何技术接口表述**
- [ ] ★ 每个功能行对应的原型列已嵌入iframe（无双边框白边）
- [ ] ★ 原型中所有文案/数据/状态 与 PRD「详细方案」描述列完全一致（已通过 3.6 自查）
- [ ] ★ 「📋 一键复制全文」实测粘贴一次：原型 iframe 已变成图片（或服务未启动时**如实提示**了「原型图缺失」，不是静默丢图）——见 §2.8
- [ ] ★ 粘出去的图**放大到 1000px 以上**再看一眼是否清晰——按文档里的默认显示尺寸（约 335px）看，任何分辨率都一样，糊不糊在这个尺寸下根本看不出来。见 §2.8 ⑤
- [ ] ★ 双栏预览的 `－/百分比/＋/适配` 可用：放大后 `.device-shell` 出滚动条、「适配」能回正、切页后缩放模式保持——见 §2.6 ⑨
- [ ] （若保留流程图）流程图正常渲染（无Syntax error）；若省略则确认未残留空的流程图 iframe
- [ ] （若保留时序图）为**源码文本块**（非渲染图）且复制按钮可用、源码经 Mermaid 环境验证无 Syntax error、分支与推进条件与详细方案【功能逻辑】/【边界说明】口径一致、技术字段仅出现在本章（§4.7 自检）
- [ ] （若保留交互流程图）节点覆盖全部核心界面与状态变体、箭头标签与描述列【交互说明】逐条对应、状态机图例齐全、导出走本地服务（§4.6 自检）
- [ ] （若保留异常与边界）异常场景全部覆盖（不清晰/非题目/无结果/网络异常/超时）
- [ ] （若保留数据埋点）埋点参数完整
- [ ] （若保留上线计划）排期/灰度策略已写明

### 5.3 迭代更新规则（极度重要）

> **铁律：每次用户新增或修改需求时，不能只更新直接提到的那一处。必须遍历整份 PRD 文档以及关联的原型、流程图，把所有相关位置都同步更新。**

**Why：** PRD 是多处交叉引用的结构，漏改一处就会让文档前后不一致、失去权威性。用户曾反馈过只更新"五-2详细方案"的模块却忘了同步"三、需求概述"的功能清单表，导致文档失真。

**每次变更后必须遍历的位置清单**：

| # | 位置 | 判断是否需更新 |
|---|------|----------------|
| 1 | 📝 版本记录表 | 新增一行 + 更新文档头部版本号（必做） |
| 2 | 一、需求背景 | 是否影响业务视角、覆盖产品、用户洞察 |
| 3 | 二、需求目标 | 是否影响量化指标或目标项 |
| 4 | **三、需求概述 · 功能清单表** | 新增模块**必须加行**；功能调整必须改描述 |
| 5 | 四、流程图 | 新增流程节点、分支、状态流转 |
| 6 | 五、交互流程图（screenflow.html） | 新增/删除界面或状态变体 → 补/删 `.flow-node` 节点与 `EDGES` 边；跳转关系变化 → 改箭头与触发标签；状态定义变化 → 同步状态机图例（见 §4.6） |
| 7 | 六、详细方案（用户端 / 管理端 / 其他端，按当前需求实际存在的端组织） | 功能落地描述；不存在的端不要硬写；描述列保持 §2.3.1 分块结构 |
| 8 | 端侧联动与权限边界 | 若涉及多端、后台、运营台或审核台，检查是否需要同步 |
| 9 | 七、异常与边界处理 | 是否引入新异常场景（与描述列【边界说明】及时序图异常 Note 互相印证） |
| 10 | 八、数据埋点 | 是否需要新埋点事件 |
| 11 | 九、时序图（PRD 内源码文本块） | 编排顺序/分支/推进条件/异常口径变化 → 同步总时序源码；新增关键对象或状态 → 补状态图源码（见 §4.7） |
| 12 | 十、上线计划 | 是否影响排期或灰度策略 |
| 13 | 附录 · 决策对齐表 | 是否新增决策项 |
| 14 | 附录 · 产品风格定位 | 是否影响文案风格 |
| 15 | 原型文件（.html） | 新增页面 + 更新 `pages` 数组 + **逐页检查文案/数据/状态是否与 PRD 描述一致（参照 3.6 节）** |
| 16 | PRD 双栏预览下拉项 + 滚动联动 + 复制出图 | 新增页的 `CATALOG` 项 / `#pageSelect` option，并给对应「一级模块」单元格补 `data-preview=<value>`（见 2.6 ⑧ scroll-spy）；**并确认该页能被 `/api/snapshot` 取到图**（起服务后点一次「一键复制全文」，看 toast 有没有报"生成失败"），否则复制出去会缺这张原型（见 §2.8） |
| 17 | PRD 的页面映射（如 `pageAliases`、端侧页面集合、预览状态） | 新增页或删除端侧时需同步 |

> **裁剪章节的处理：** 上表第 4/5/6/9/10/11/12/13/14 项对应的章节可能在初稿时已按 2.2 裁掉。遍历到这些位置时：
> - 该章节**当前存在** → 按上表正常同步。
> - 该章节**当前不存在，但本次变更触及了它**（如小需求升级后新增了流程分支、引入了新异常或新埋点）→ **需补回该章节**：先按 1.3.1 的方式告知用户"本次需补回 X 章节，原因…"，确认后补写，并按 2.2 顺序插回正确位置、重排编号。
> - 该章节不存在且本次也不触及 → 跳过。

**反向规则**：对原型 / 流程图的独立变更，同样要反向检查 PRD 各位置是否需要跟着改。

**交付声明**：迭代完成后，在对用户的回复中明确列出"本次同步更新了哪些位置"（含新增/省略/补回的章节），让用户能快速复核。

### 5.4 评审与迭代

1. 用户评审PRD内容，提出修改意见
2. 根据反馈迭代修改
3. 最终确认后归档到 `[需求名]/需求文档/` 目录

---

## 步骤六：上下文交接（会话续接）

> 需求沟通 + PRD 撰写往往跨越多轮对话。当上下文即将耗尽时，必须将关键状态持久化，确保新会话能无缝衔接。

### 6.1 触发时机

以下任一情况出现时，**主动**执行交接流程：

- 系统出现上下文压缩提醒（消息被自动摘要/截断）
- 用户说"开新窗口""换个会话""继续聊"等意图
- AI 判断当前会话剩余空间不足以完成下一步骤

**触发后立即提醒用户**：
> 上下文快满了，我先生成交接文件，你开新窗口后发一句话就能恢复。

### 6.2 交接前：更新沟通记录

在生成交接文件之前，先把**本次会话中所有未记录的沟通内容**追加到 `[需求名]/沟通记录.md`（沟通记录随需求存放在其顶层目录内），确保下个会话能读到完整历史。

### 6.3 生成交接文件

保存到固定路径：**`PM工作流/.handoff/[需求名]-handoff.md`**

文件结构：

```markdown
# [需求名] · 会话交接摘要

> 生成时间：YYYY-MM-DD HH:mm
> 上一会话阶段：[需求采集 / PRD撰写 / 评审迭代]

## 一、当前进度

| 状态 | 事项 |
|------|------|
| ✅ 已完成 | xxx |
| 🔄 进行中 | xxx |
| ⬚ 待开始 | xxx |

## 二、已对齐的关键决策

（从沟通记录中提取完整决策表，保持 | 决策项 | 结论 | 格式）

## 三、已产出文件

| 产出物 | 路径 | 状态 |
|--------|------|------|
| PRD | [需求名]/需求文档/xxx-PRD.html | 初稿完成 / 待修改 |
| 原型 | [需求名]/原型/xxx-prototype.html | 已完成 |
| 流程图 | [需求名]/流程图/xxx-flow.html | 已完成 |
| 沟通记录 | [需求名]/沟通记录.md | 已更新至第N轮 |

## 四、未解决问题 / 待确认项

- [ ] 问题1
- [ ] 问题2

## 五、下一步行动

新会话应该从 [步骤X：具体描述] 继续。

## 六、关键上下文片段

（记录无法从文件推导出的重要信息：用户原话中的偏好、语气要求、否决过的方案、特殊约束等）
```

### 6.4 生成恢复指令

交接文件末尾**必须**附带一段用户可直接复制到新窗口的恢复指令：

```markdown
---

## 🔄 新窗口恢复指令（复制以下内容到新会话）

请读取以下文件恢复上下文，然后继续工作：
1. @.handoff/[需求名]-handoff.md （交接摘要，优先读）
2. @[需求名]/沟通记录.md （完整沟通历史）
3. @.agents/workflows/edu-pm-prd.md （工作流规范）
4. @[需求名]/需求文档/[需求名]-PRD.html （如已产出）

读完后从「[具体步骤描述]」继续，不需要重新确认已对齐的决策。
```

### 6.5 新会话恢复流程

新会话收到恢复指令后，按以下顺序操作：

1. **读取交接文件** → 快速掌握进度、决策、文件状态
2. **读取沟通记录** → 了解完整沟通上下文
3. **读取工作流规范** → 确保产出格式一致
4. **读取已有产出物**（如有）→ 了解当前文件内容
5. **向用户确认** → 简要复述当前状态，确认从哪里继续
6. **继续工作** → 无需重复已对齐的决策

---

## 目录结构

> **核心原则：产物按「需求名」分文件夹。** 每个需求一个顶层目录，自己的需求文档/原型/流程图/截图等都收纳其中；`scripts/`、`启动原型导出服务.command`、`.handoff/`、`关键点.md`、`.mcp.json`、`.agents/` 为所有需求**共享**，留在项目根目录。

```
PM工作流/
├── [需求名]/                       # ← 顶层 = 需求名，每个需求一个独立目录
│   ├── 需求文档/
│   │   └── [需求名]-PRD.html       # ← 输出格式为 HTML，非 Markdown
│   ├── 原型/
│   │   ├── [需求名]-prototype.html # HTML 交互原型（主交付物，始终产出）
│   │   └── [需求名].pen            # Pencil 设计源文件（可选，高保真模式）
│   ├── 流程图/
│   │   ├── [需求名]-flow.html        # Mermaid 业务流程图（按需；时序图为 PRD 内文本章节，不落此处）
│   │   └── [需求名]-screenflow.html  # 交互流程图·界面跳转链路整图（按需，见 §4.6）
│   ├── 原型截图/                    # 该需求导出的原型截图
│   │   └── [页面名].png            # HTML 导出或 Pencil 导出的 PNG
│   ├── 验收清单/                    # 用到时才建（见 edu-pm-acceptance）
│   ├── 数据分析/                    # 用到时才建（见 edu-pm-data-analysis）
│   ├── 需求挖掘/                    # 用到时才建（见 edu-pm-demand）
│   └── 沟通记录.md                  # 该需求沟通全记录（跨会话持久化）
│
├── （另一个需求名）/                 # 结构同上，与上面互不混放
│
├── scripts/                        # 【共享】辅助脚本和导出服务
│   ├── pencil-draw-prompt.md       # Pencil 绘图 Prompt 模板（参考用）
│   ├── prototype_server.py         # Playwright 真实渲染 PNG 导出服务（已支持嵌套目录）
│   ├── prototype-export-client.js  # 原型导出按钮客户端
│   └── setup_prototype_export_watcher.sh # macOS 导出服务自恢复 watcher
├── 启动原型导出服务.command           # 【共享】双击启动 PNG 导出服务
├── .handoff/                       # 【共享】会话交接文件（上下文续接用）
│   └── [需求名]-handoff.md
├── 关键点.md                        # 【共享】工作流版本迭代记录
├── .mcp.json                       # 【共享】Pencil MCP 连接配置（可选）
└── .agents/workflows/              # 【共享】工作流定义
    ├── edu-pm-prd.md               # 主工作流：需求→PRD→原型→流程图
    ├── edu-pm-demand.md            # 需求挖掘与分析工作流
    ├── edu-pm-acceptance.md        # 功能验收清单工作流
    └── edu-pm-data-analysis.md     # 数据分析报告工作流
```
