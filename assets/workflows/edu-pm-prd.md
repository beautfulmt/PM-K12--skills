---
description: 教育PM需求产出工作流 — 输入需求描述，产出PRD+原型+流程图
---

# 教育PM需求产出工作流

## 触发方式

当用户提供一个需求描述时，按以下步骤产出标准化交付物。

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

### 1.4 确认后进入下一步

- 用户确认「没问题」或补充完信息后，进入PRD撰写阶段

---

## 步骤二：产出PRD（HTML格式）

### 2.1 格式规范

> **重要：** 输出格式必须是 **HTML文件**，而非Markdown。原因：Markdown粘贴至钉钉文档时会丢失表格格式，HTML经浏览器渲染后截图或复制保留格式效果最佳。

1. 将PRD保存为 `需求文档/[需求名]-PRD.html`（相对于项目根目录）
2. HTML中内嵌所有CSS，无需外部依赖，确保脱机可用

### 2.2 PRD结构（固定章节顺序）

按以下顺序组织文档：

```
📋 项目信息
📝 版本记录
一、需求背景
二、需求目标
三、需求概述（功能清单表格）
四、流程图（嵌入交互式 iframe）
五、详细方案（四列表格：一级模块 | 二级功能 | 原型 | 描述）
六、异常与边界处理
七、数据埋点
八、上线计划与灰度策略
📎 附录
```

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
- **极度重要：** 必须给 “描述” 列对应的 `<td>` 元素添加 `contenteditable="true"` 和 `style="outline: none;"` 属性（让文案在浏览器中可直接编辑）。
- **极度重要：** 必须在 HTML 底部插入“悬浮双重动作面板”，代码大纲如下（AI需补全标准JS）：
  1. 监听所有 `contenteditable="true"` 的 `blur` 事件，如果内容被修改，则为该 `td` 添加 `data-changed="true"` 属性和绿色的 `edited-cell` 高亮类。
  2. 页面右下角的悬浮 `.save-btn-container` 区只保留一个按钮：“💾 保存并通知AI”。截图导出功能已移至原型和流程图各自的 HTML 中，PRD 不再承载导出功能。
  3. 点击保存按钮时，抓取 `document.documentElement.outerHTML` 并调用系统的文件保存句柄直接物理存档覆盖 HTML 原型。
- 黄色高亮标注关键变更点（用 `.alert` 样式块）
- 必须覆盖异常和边界情况

### 2.5 表格排版优化

- 页面最大宽度设为 `1400px`（允许原型列有足够展示空间）
- 表格使用 `table-layout: fixed`
- 各列推荐宽度：一级模块 `100px`，二级功能 `100px`，原型 `350px`，描述自动扩展
- `th` 和 `td` **必须同时设置** `resize: both; overflow: auto;`，以此允许用户自由拖动单元格的右下角，既可左右调节列宽，亦可上下调节行高，且支持内容超长时的局部平滑滚动浏览。
- `td` 设置 `word-break: break-word` 避免文字溢出
- **极度重要（原型预览体验）：** PRD 中的原型 iframe 不要直接按原始尺寸硬塞进表格单元格，尤其是 16:9 横屏课堂原型。必须使用“等比例缩放容器”包裹 iframe，并在每个原型预览右下角提供直接拖拽的缩放手柄，拖拽时原型整体按比例同步变化，避免再额外做独立操作面板。

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
6. **极度重要（保存路径与命名）：** 导出 PNG 自动保存到项目根目录 `原型截图/[原型文件名]/`；文件名优先使用原型下方 `.device-label`，其次使用 `.page-title` / 注释中的界面名称，保证和界面名称一致。
7. **极度重要（服务自恢复）：** 项目根目录提供 `启动原型导出服务.command`，初始化时安装 macOS LaunchAgent watcher；点击导出按钮时若 `localhost:8765` 暂未响应，按钮需显示“正在启动/等待导出服务”，等待 watcher 拉起服务后继续导出。浏览器安全限制下，HTML 不能直接启动 Python 进程，必须依赖本地 watcher 或用户双击 `.command`。
8. 同时保留 `trigger-export` 的 `postMessage` 监听，以兼容 iframe 嵌入场景；无 hash 时 body 加 `.tiled` class 平铺展示所有 `.device`，有 hash 时只显示对应单页。
9. **极度重要（单页模式 CSS 陷阱）：** 单页模式下**禁止**对 `.gallery` 等包裹容器设置 `display: none`，否则内部 `.device` 即使有 `!important` 也不会显示（CSS 继承：父隐藏则子不可见）。正确做法：保持 `.gallery` 为 `display: block`，隐藏每个 `.device-wrapper`，仅对 `.device-wrapper.active` 设置 `display: flex`。JS init 中通过 `device.closest('.device-wrapper')` 找到父容器加 `active` 类。
10. 保存路径：`原型/[需求名]-prototype.html`（相对于项目根目录）
11. 原型 HTML 底部必须加入 `<script src="../scripts/prototype-export-client.js?v=YYYYMMDD"></script>`，导出按钮使用 `id="exportFab"` 或 `.export-btn`，不要绑定旧的 `html-to-image` 导出函数。
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
> - 相对路径基于PRD文件所在目录（`需求文档/`）往上一级的 `原型/` 目录

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
   · 输出目录：原型截图/
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
| Pencil 源文件 | `原型/[需求名].pen` | 设计源文件，可反复编辑 |
| 导出截图 | `原型截图/[需求名]-[页面ID].png` | 2x 分辨率 PNG |
| HTML 原型 | `原型/[需求名]-prototype.html` | 保持可交互，视觉对齐 Pencil 稿 |

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

## 步骤四：产出流程图

### 4.1 规范

1. 使用 **Mermaid** 语法绘制，保存为独立 HTML 文件
2. `mermaid.esm.min.mjs` 通过 jsdelivr CDN 引入
3. 每个图表是独立的 `<div class="chart-container">` 块
4. 保存路径：`流程图/[需求名]-flow.html`（相对于项目根目录）

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

交付前确认：
- [ ] 章节顺序：背景 → 目标 → 概述 → **流程图 → 详细方案** → 异常 → 埋点 → 上线计划
- [ ] 详细方案表格为四列格式，rowspan合并一级模块
- [ ] 每个功能行对应的原型列已嵌入iframe（无双边框白边）
- [ ] 流程图正常渲染（无Syntax error）
- [ ] 异常场景全部覆盖（不清晰/非题目/无结果/网络异常/超时）
- [ ] 埋点参数完整
- [ ] 原型中所有文案/数据/状态 与 PRD「详细方案」描述列完全一致（已通过 3.6 自查）

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
| 6 | 五-1、详细方案（C端） | C端功能落地描述 |
| 7 | 五-2、详细方案（后台） | 后台功能落地描述 |
| 8 | 六、异常与边界处理 | 是否引入新异常场景 |
| 9 | 七、数据埋点 | 是否需要新埋点事件 |
| 10 | 八、上线计划 | 是否影响排期或灰度策略 |
| 11 | 附录 · 决策对齐表 | 是否新增决策项 |
| 12 | 附录 · 产品风格定位 | 是否影响文案风格 |
| 13 | 原型文件（.html） | 新增页面 + 更新 `pages` 数组 + **逐页检查文案/数据/状态是否与 PRD 描述一致（参照 3.6 节）** |
| 14 | PRD 双栏预览下拉项 | 新增页的 option |
| 15 | PRD 的 `adminPages` / `pageAliases` 等映射 | 新增页需同步 |

**反向规则**：对原型 / 流程图的独立变更，同样要反向检查 PRD 各位置是否需要跟着改。

**交付声明**：迭代完成后，在对用户的回复中明确列出"本次同步更新了哪些位置"，让用户能快速复核。

### 5.4 评审与迭代

1. 用户评审PRD内容，提出修改意见
2. 根据反馈迭代修改
3. 最终确认后归档到 `需求文档/` 目录

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

在生成交接文件之前，先把**本次会话中所有未记录的沟通内容**追加到 `沟通记录.md`，确保下个会话能读到完整历史。

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
| PRD | 需求文档/xxx-PRD.html | 初稿完成 / 待修改 |
| 原型 | 原型/xxx-prototype.html | 已完成 |
| 流程图 | 流程图/xxx-flow.html | 已完成 |
| 沟通记录 | 沟通记录.md | 已更新至第N轮 |

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
2. @沟通记录.md （完整沟通历史）
3. @.agents/workflows/edu-pm-prd.md （工作流规范）
4. @需求文档/[需求名]-PRD.html （如已产出）

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

```
PM工作流/
├── PRD模板.md                    # 标准化PRD模板（参考用）
├── 需求文档/                     # 所有PRD存放目录
│   └── [需求名]-PRD.html         # ← 输出格式为 HTML，非 Markdown
├── 原型/                         # 所有原型存放目录
│   ├── [需求名]-prototype.html   # HTML 交互原型（主交付物，始终产出）
│   └── [需求名].pen              # Pencil 设计源文件（可选，高保真模式）
├── 原型截图/                     # 导出的原型截图
│   └── [需求名]-[页面ID].png     # HTML 导出或 Pencil 导出的 PNG
├── 流程图/                       # 所有流程图存放目录
│   └── [需求名]-flow.html
├── scripts/                      # 辅助脚本和模板
│   ├── pencil-draw-prompt.md     # Pencil 绘图 Prompt 模板（参考用）
│   ├── prototype_server.py       # Playwright 真实渲染 PNG 导出服务
│   ├── prototype-export-client.js # 原型导出按钮客户端
│   └── setup_prototype_export_watcher.sh # macOS 导出服务自恢复 watcher
├── 启动原型导出服务.command         # 双击启动 PNG 导出服务
├── .handoff/                     # 会话交接文件（上下文续接用）
│   └── [需求名]-handoff.md
├── 沟通记录.md                    # 需求沟通全记录（跨会话持久化）
├── 关键点.md                      # 工作流版本迭代记录
├── .mcp.json                     # Pencil MCP 连接配置（可选）
└── .agents/workflows/
    ├── edu-pm-prd.md             # 主工作流：需求→PRD→原型→流程图
    ├── edu-pm-demand.md          # 需求挖掘与分析工作流
    ├── edu-pm-acceptance.md      # 功能验收清单工作流
    └── edu-pm-data-analysis.md   # 数据分析报告工作流
```
