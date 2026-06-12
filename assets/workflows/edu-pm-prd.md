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

- 评估方式：核心骨架（项目信息+版本记录、需求背景、需求目标、详细方案）始终保留；其余 6 个可选章节（需求概述/流程图/异常边界/数据埋点/上线计划/附录）按 2.2 的判断依据逐一评估留还是省。
- 在确认消息里附一行「本次章节」说明，例如：
  > 这个需求比较小（仅调整一处文案，无新流程/无新埋点），我打算这样组织 PRD：
  > - **保留**：项目信息、版本记录、需求背景、需求目标、详细方案
  > - **省略**：流程图（无多步骤流程）、数据埋点（无新事件）、上线计划（直接全量）、异常边界（无新场景）
  > 你看这样可以吗？或者有哪章你希望保留？
- 用户若要求保留某章，则照办；用户认可后再进入撰写。
- **产出物联动**：若省略「四、流程图」章节，则**不产出** `[需求名]/流程图/[需求名]-flow.html`（步骤四整步跳过）；若保留则正常产出。其余可选章节的省略只影响 PRD 内对应章节，不影响原型产出。

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
| 五、详细方案（四列表格：一级模块 \| 二级功能 \| 原型 \| 描述） | PRD 核心，绝不省 |

**② 按需裁剪（AI 根据需求判断是否需要，可整章省略）：**

| 章节 | 建议省略的判断依据 |
|------|----------|
| 三、需求概述（功能清单表格） | 功能点极少（如仅 1-2 个）时可省，直接进详细方案 |
| 四、流程图（嵌入交互式 iframe） | 无多步骤流程、无分支/状态流转的小需求 → 省 |
| 六、异常与边界处理 | 不引入任何新异常/边界场景 → 省 |
| 七、数据埋点 | 不涉及新增埋点事件 → 省 |
| 八、上线计划与灰度策略 | 小需求直接全量上线、无灰度 → 省或一句话带过 |
| 📎 附录（决策对齐表/产品风格定位等） | 无决策项、无特殊风格约定 → 省 |

> **编号说明：** 章节编号（一～八）跟随实际保留的章节**连续重排**，不要因为省略了"四、流程图"就让正文出现"三、五"的跳号。即按保留章节重新顺序编号，但顺序仍遵循上表自上而下。

> **裁剪须先告知（极度重要）：** AI **不得默默省略章节**。在需求确认阶段（步骤一 1.3）必须先列出"本次 PRD 拟保留哪些章节、省略哪些、各自原因"，经用户确认后再撰写。详见 1.3。

### 2.3 详细方案表格格式

**必须使用四列表格**，格式如下：

| 一级模块 | 二级功能 | 原型 | 描述 |
|----------|----------|------|------|
| （使用rowspan合并相同模块） | 具体操作 | （原型iframe） | `<td contenteditable="true">` 0、功能说明 / 1、xxx / 2、xxx `</td>` |

- 描述采用 **编号叙述法**：`0、功能说明` `1、页面元素` `2、交互逻辑` 等
- 原型列放置对应界面的 `<iframe>` 嵌入
- 一级模块使用 `rowspan` 合并跨行单元格

### 2.4 写作风格

- 先图（原型）后文
- 逐条编号描述交互规则
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

> **背景（踩坑记录）：** 这套右侧「交互原型预览」面板长期只活在历史 PRD 成品里（如 `AI试卷分析-PRD.html`），从未沉淀成规范，导致从零写 PRD 时容易漏掉（2.4 又只让放保存按钮）。**故在此固化为必做项：每份 PRD 都要内建该面板。** 它与「五、详细方案」表格里的静态原型列（截图/小 iframe）不同——这是一个全局常驻、可切页、可缩放的活预览 dock。

**目标：** PRD 左侧正文 + 右侧一个可关闭的深色面板，面板内嵌**活的原型 iframe**，用顶部下拉切换页面/场景，支持拖拽改宽，整体等比缩放。

**① HTML 结构：**
- `<body class="dual-pane">`：默认**打开**双栏。
- `.prototype-sidebar`（`position:fixed; right:0; top:0; height:100vh; 深色 #1a1a2e; flex 纵向`）内含：
  - `.sidebar-header`：`✕` 关闭按钮（`onclick="toggleDualPane()"`）+ 标题「交互原型预览」。
  - `.preview-context`：一行说明（如收口范围、或"完整交互依赖后端、静态预览仅还原界面"等真实约束，**不夸大成全功能可跑**）。
  - `.page-selector > select#pageSelect`（`onchange="switchPage(this.value)"`）。
  - `.device-shell > .device-wrapper > iframe#prototypeFrame`。
  - `.prototype-resizer`：面板左缘竖向拖拽手柄。
- `.fab-group`（`position:fixed; right:28px; bottom:28px`）：含「双栏预览」开关按钮（`dual-pane` 时 `display:none`）+「💾 保存并通知AI」按钮。**双栏打开时整组右移**到面板左侧：`body.dual-pane .fab-group { right: calc(var(--panel-w) + 28px); }`。（即 2.4 的保存按钮并入此 fab-group，不再单独悬浮。）

**② CSS 关键：**
- `:root { --panel-w: 520px; }`
- `body.dual-pane { margin:0!important; max-width:none!important; padding-right: calc(var(--panel-w) + 36px); }`（正文让出右侧面板宽度）
- `body.dual-pane .prototype-sidebar { display:flex; }`（默认 `.prototype-sidebar{display:none}`）
- `.device-wrapper iframe { transform-origin: top left; }`、`.device-shell { overflow:auto; }`（竖屏长页可滚）

**③ JS 关键（内嵌 PRD 底部）：**
```js
// 每项：{value,label,url,w,h}。url 指向可寻址原型；w/h = 该页逻辑尺寸
const CATALOG = [ { value:'p1', label:'P1 · xxx', url:'../原型/xxx-prototype.html#p1', w:375, h:812 }, /* ... */ ];
let previewPage = CATALOG[0].value;
function currentCfg(){ return CATALOG.find(o=>o.value===previewPage) || CATALOG[0]; }
function scalePreview(){
  const shell=document.querySelector('.device-shell'), wrap=document.getElementById('deviceWrapper'), frame=document.getElementById('prototypeFrame');
  const cfg=currentCfg(), innerW=Math.max(120, shell.clientWidth-40), scale=innerW/cfg.w;
  frame.style.width=cfg.w+'px'; frame.style.height=cfg.h+'px'; frame.style.transform='scale('+scale+')';
  wrap.style.width=Math.round(cfg.w*scale)+'px'; wrap.style.height=Math.round(cfg.h*scale)+'px';
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

**⑦ 裁剪与迭代：** 仅 1 个原型页时可省下拉、只留单页预览，但**面板本身默认保留**；新增页必须同步往 `CATALOG` / `#pageSelect` 加项（见 5.3 第 14 项「PRD 双栏预览下拉项」）。

**⑧ 滚动联动 / scroll-spy（必做）：** 左侧正文滚到某模块，右侧交互预览**自动切到该模块对应的原型页**（滚到「界面1」→预览定位界面1，滚到「界面3」→跟随切界面3），不用手点下拉。
- **取材：** 给「五、详细方案」每个**一级模块单元格**（`td.mod`，或模块首行 `<tr>`）加 `data-preview="<CATALOG 里对应页的 value>"`。新增模块/页时必须同步补这个属性（并入 5.3 迭代清单）。
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

### 2.7 全文档可编辑 · 表格行列拖拽 · 全表增删行（必做）

> **背景（踩坑记录）：** 旧版只给「五、详细方案」描述列加 `contenteditable`、只有详细方案表能增删行；其余正文（背景/目标/版本记录/埋点…）在浏览器里都改不了，且 §2.5 旧规曾**禁用**列宽行高调整。**现固化为必做项：每份 PRD 都内建下面这套自包含的「通用编辑模块」**，一次性提供①全文档可编辑 ②全表增删行 ③列宽/行高拖拽。模块**幂等、纯内嵌、无外部依赖**，直接整段贴进 PRD 底部 `<script>`（在保存按钮逻辑之前），无需逐个单元格手写 `contenteditable`。

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

### 2.8 左下角「一键复制全文」（必做）

> **目的：** 方便把整份 PRD 一键拷到钉钉/飞书/Word 等外部文档。复制必须是**富文本**（`text/html`，保留表格/标题/加粗/列表），并在导出前**剥离所有交互骨架与编辑痕迹**，否则粘出去会带一堆手柄、绿色高亮和 `contenteditable` 脏属性。

**① 按钮：** 页面**左下角**固定一个 `.copy-all-fab`（`position:fixed; left:28px; bottom:28px`），`onclick="copyAllContent()"`，文案「📋 一键复制全文」。与右下角 `.fab-group`（双栏/保存）分居两侧；双栏打开时右侧面板不影响左下角，无需偏移。另配一个 `.copy-toast`（左下、`bottom:80px`）做轻量结果反馈，默认 `opacity:0`、`.show` 时淡入，2 秒后自动隐藏。

**② 导出清洗（关键）：** `document.body.cloneNode(true)` 后，在副本上：
- **删除交互骨架**：`.prototype-sidebar`、`.fab-group`、`.copy-all-fab`、`.copy-toast`、`.col-resizer`、`.row-resizer`、`.row-ctrl`、`.pm-anchor`、`.editable-table-remove`、`script`/`noscript`、以及 `iframe`（流程图/原型 iframe 粘不过去）。
- **解包**：`.editable-table-wrap` 用其内部 `<table>` 替换自身。
- **去编辑痕迹**：移除所有 `contenteditable`、`data-changed`/`data-original`/`data-orig`/`data-pm-tracked` 属性与 `.edited-cell` 类。
- **补排版**：给 `table` 补 `border-collapse/width`、给 `th,td` 补 `1px` 边框+内边距、`th` 补浅底色（内联 style，确保粘到无样式环境也有框）；把 `img` 的 `src` 绝对化（`img.setAttribute('src', img.src)`）。

**③ 写剪贴板：** 优先 `navigator.clipboard.write([new ClipboardItem({'text/html':blobHtml,'text/plain':blobText})])`（`text/plain` = 清洗后 `clone.innerText` 兜底）；不支持或被拒时**回退**到离屏 `contenteditable` 容器 + 选区 + `document.execCommand('copy')`。成功/失败都用 `.copy-toast` 提示。

**④ JS（已在无头 Chrome 实测：富文本含表格/加粗、骨架与编辑痕迹全无、内联边框、图片绝对化、纯文本兜底全绿，整段照贴）：**
```js
(function(){
  function buildExportClone(){
    var clone = document.body.cloneNode(true);
    clone.querySelectorAll('.prototype-sidebar, .fab-group, .copy-all-fab, .copy-toast, .col-resizer, .row-resizer, .row-ctrl, .pm-anchor, .editable-table-remove, script, noscript').forEach(function(n){ n.remove(); });
    clone.querySelectorAll('.editable-table-wrap').forEach(function(w){ var t=w.querySelector('table'); if(t) w.replaceWith(t); else w.remove(); });
    clone.querySelectorAll('iframe').forEach(function(f){ f.remove(); });
    clone.querySelectorAll('[contenteditable]').forEach(function(el){ el.removeAttribute('contenteditable'); });
    ['data-changed','data-original','data-orig','data-pm-tracked'].forEach(function(a){ clone.querySelectorAll('['+a+']').forEach(function(el){ el.removeAttribute(a); }); });
    clone.querySelectorAll('.edited-cell').forEach(function(el){ el.classList.remove('edited-cell'); });
    clone.querySelectorAll('table').forEach(function(t){ t.style.borderCollapse='collapse'; t.style.width='100%'; });
    clone.querySelectorAll('th,td').forEach(function(c){ c.style.border='1px solid #ccc'; c.style.padding='6px 10px'; c.style.verticalAlign='top'; });
    clone.querySelectorAll('th').forEach(function(c){ if(!c.style.background) c.style.background='#f2f1f8'; });
    clone.querySelectorAll('img').forEach(function(img){ try{ img.setAttribute('src', img.src); }catch(e){} });
    return clone;
  }
  function showToast(msg, err){
    var t=document.querySelector('.copy-toast');
    if(!t){ t=document.createElement('div'); t.className='copy-toast'; document.body.appendChild(t); }
    t.textContent=msg; t.style.background= err? '#c0392b' : '#2a2459'; t.classList.add('show');
    clearTimeout(showToast._t); showToast._t=setTimeout(function(){ t.classList.remove('show'); }, 2200);
  }
  async function copyAllContent(){
    var clone=buildExportClone();
    var html='<meta charset="utf-8">'+clone.innerHTML;
    var text=clone.innerText;
    try{
      if(navigator.clipboard && window.ClipboardItem){
        await navigator.clipboard.write([new ClipboardItem({
          'text/html': new Blob([html],{type:'text/html'}),
          'text/plain': new Blob([text],{type:'text/plain'})
        })]);
        showToast('已复制全文，可直接粘贴到钉钉/飞书/Word'); return;
      }
      throw new Error('no async clipboard');
    }catch(e){
      try{
        var holder=document.createElement('div'); holder.setAttribute('contenteditable','true');
        holder.style.cssText='position:fixed;left:-99999px;top:0;opacity:0;'; holder.innerHTML=html;
        document.body.appendChild(holder);
        var range=document.createRange(); range.selectNodeContents(holder);
        var sel=window.getSelection(); sel.removeAllRanges(); sel.addRange(range);
        var okc=document.execCommand('copy'); sel.removeAllRanges(); holder.remove();
        if(okc){ showToast('已复制全文，可直接粘贴到钉钉/飞书/Word'); } else { throw new Error('execCommand 拒绝'); }
      }catch(e2){ showToast('复制失败，请手动全选复制：'+(e2.message||e2), true); }
    }
  }
  window.copyAllContent=copyAllContent;
})();
```

**⑤ CSS 草图：**
```css
.copy-all-fab { position:fixed; left:28px; bottom:28px; z-index:1001; background:#fff; color:#3b357a; border:1px solid #d8d4f0; border-radius:12px; padding:13px 20px; font-size:14px; font-weight:700; cursor:pointer; box-shadow:0 4px 16px rgba(91,91,214,.18); display:flex; align-items:center; gap:8px; }
.copy-all-fab:hover { transform:translateY(-2px); border-color:#5b5bd6; }
.copy-toast { position:fixed; left:28px; bottom:80px; z-index:1002; max-width:360px; background:#2a2459; color:#fff; padding:11px 16px; border-radius:10px; font-size:13px; box-shadow:0 8px 24px rgba(20,16,70,.28); opacity:0; transform:translateY(8px); pointer-events:none; transition:opacity .2s, transform .2s; }
.copy-toast.show { opacity:1; transform:translateY(0); }
```

> **取材限制（据实说明，勿夸大）：** 本地相对路径的截图/iframe 粘到钉钉云文档时通常不会自动上传，复制以**文本+表格结构**为主；图片可能需要在目标文档里重新插入。

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
7. **极度重要（导出服务）：** 项目根目录提供 `启动原型导出服务.command`。初始化时会尝试安装 macOS LaunchAgent watcher；点击导出按钮时若 `localhost:8765` 暂未响应，按钮需显示“正在连接导出服务”，并提示用户双击 `.command` 或等待 watcher 拉起服务。浏览器安全限制下，HTML 不能直接启动 Python 进程。
8. 同时保留 `trigger-export` 的 `postMessage` 监听，以兼容 iframe 嵌入场景；无 hash 时 body 加 `.tiled` class 平铺展示所有 `.device`，有 hash 时只显示对应单页。
9. **极度重要（单页模式 CSS 陷阱）：** 单页模式下**禁止**对 `.gallery` 等包裹容器设置 `display: none`，否则内部 `.device` 即使有 `!important` 也不会显示（CSS 继承：父隐藏则子不可见）。正确做法：保持 `.gallery` 为 `display: block`，隐藏每个 `.device-wrapper`，仅对 `.device-wrapper.active` 设置 `display: flex`。JS init 中通过 `device.closest('.device-wrapper')` 找到父容器加 `active` 类。
10. 保存路径：`[需求名]/原型/[需求名]-prototype.html`（相对于项目根目录）
11. 原型 HTML 底部必须加入 `<script src="../../scripts/prototype-export-client.js?v=YYYYMMDD"></script>`，导出按钮使用 `id="exportFab"` 或 `.export-btn`，不要绑定旧的 `html-to-image` 导出函数。
    > **路径说明：** 原型位于 `[需求名]/原型/`，而导出脚本在项目根目录 `scripts/` 共享，因此需 `../../`（退两级）回到根目录再进 `scripts/`。
12. **极度重要（原型 ↔ PRD 内容对齐）：** 原型中展示的所有文案、数据、状态标签、按钮文字、提示信息必须与 PRD「五、详细方案」中对应行的「描述」列内容逐条一致。具体对齐规则：
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
对照 PRD「五、详细方案」中对应行的「描述」列
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

## 步骤四：产出流程图（可裁剪）

> **前置判断：** 本步骤对应 PRD 的「四、流程图」章节，属于按需裁剪项（见 2.2 / 1.3.1）。若在章节裁剪预告中已与用户确认**省略流程图**（无多步骤流程/无分支的小需求），则**整步跳过**，不产出 `[需求名]/流程图/` 文件，PRD 中也不嵌入流程图 iframe。仅当保留该章节时才执行下面的规范。

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

---

## 步骤五：交付与评审

### 5.1 交付格式

| 产出物 | 生成格式 | 交付方式 |
|--------|----------|----------|
| **PRD文档** | HTML (.html) | 浏览器打开，直接截图到钉钉；或复制页面内容粘贴 |
| **原型** | HTML (.html) | 已内嵌在PRD的iframe中；也可单独提供文件 |
| **流程图** | HTML (.html) | 已内嵌在PRD的iframe中；也可单独提供文件 |

> **交付到钉钉的方式：**
> 在浏览器中打开 PRD HTML 文件，对需要的部分用截图工具（Mac: `Cmd+Ctrl+Shift+4`）截图，然后直接 `Cmd+V` 粘贴到钉钉文档。

### 5.2 PRD最终检查清单

交付前确认（标 ★ 为核心骨架，始终检查；其余仅在该章节本次保留时检查）：
- [ ] ★ 保留的章节按 2.2 顺序自上而下排列，编号连续无跳号
- [ ] ★ 本次省略的章节已在需求确认阶段告知用户并获认可（1.3.1）
- [ ] ★ 详细方案表格为四列格式，rowspan合并一级模块
- [ ] ★ 每个功能行对应的原型列已嵌入iframe（无双边框白边）
- [ ] ★ 原型中所有文案/数据/状态 与 PRD「详细方案」描述列完全一致（已通过 3.6 自查）
- [ ] （若保留流程图）流程图正常渲染（无Syntax error）；若省略则确认未残留空的流程图 iframe
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
| 6 | 五、详细方案（用户端 / 管理端 / 其他端，按当前需求实际存在的端组织） | 功能落地描述；不存在的端不要硬写 |
| 7 | 端侧联动与权限边界 | 若涉及多端、后台、运营台或审核台，检查是否需要同步 |
| 8 | 六、异常与边界处理 | 是否引入新异常场景 |
| 9 | 七、数据埋点 | 是否需要新埋点事件 |
| 10 | 八、上线计划 | 是否影响排期或灰度策略 |
| 11 | 附录 · 决策对齐表 | 是否新增决策项 |
| 12 | 附录 · 产品风格定位 | 是否影响文案风格 |
| 13 | 原型文件（.html） | 新增页面 + 更新 `pages` 数组 + **逐页检查文案/数据/状态是否与 PRD 描述一致（参照 3.6 节）** |
| 14 | PRD 双栏预览下拉项 + 滚动联动 | 新增页的 `CATALOG` 项 / `#pageSelect` option，并给对应「一级模块」单元格补 `data-preview=<value>`（见 2.6 ⑧ scroll-spy） |
| 15 | PRD 的页面映射（如 `pageAliases`、端侧页面集合、预览状态） | 新增页或删除端侧时需同步 |

> **裁剪章节的处理：** 上表第 4/5/8/9/10/11/12 项对应的章节可能在初稿时已按 2.2 裁掉。遍历到这些位置时：
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
│   │   └── [需求名]-flow.html
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
