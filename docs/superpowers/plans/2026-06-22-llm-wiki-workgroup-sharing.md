# LLM Wiki 工作小组分享 HTML PPT Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 交付一份 15 页、30 分钟、带演讲者逐字稿的 LLM Wiki 工作小组 HTML 演示文稿。

**Architecture:** 基于 `html-ppt` 的 `presenter-mode-reveal` 全 deck 模板创建独立副本，在其中替换为 15 张中文幻灯片和与之配套的隐藏 `.notes`。演示稿复用 skill 的 CSS、运行时和主题令牌，最后使用 headless Chrome 对每张页面渲染为 PNG 进行视觉检查。

**Tech Stack:** 静态 HTML、CSS、JavaScript；html-ppt skill；headless Google Chrome。

## Global Constraints

- 输出为 15 张 `section.slide`，面向工作小组的 30 分钟中文分享。
- LLM Wiki 必须是叙事主体；Obsidian 与 Web Clipper 仅作为人机协作与素材入口。
- 使用 `presenter-mode-reveal` 基础模板，所有逐字稿放在 `<aside class="notes">` 中。
- 逐字稿每页 150–300 字，使用中文口语和可扫读的强调标签。
- 不修改三篇参考笔记，不触碰用户已有的未提交改动，不执行 git add / commit / push。
- 每页均须通过静态渲染检查，且不能出现可见讲稿、文字溢出或低对比度。

---

## File Structure

- Create: `presentations/llm-wiki-workgroup-sharing/index.html` — 15 张幻灯片、观众可见文本及逐字稿。
- Create: `presentations/llm-wiki-workgroup-sharing/style.css` — 基于模板的局部排版与流程图样式。
- Create: `presentations/llm-wiki-workgroup-sharing/README.md` — 打开、演讲者模式和渲染命令。
- Create: `presentations/llm-wiki-workgroup-sharing/rendered/slide-01.png` … `slide-15.png` — 验收用渲染产物。

### Task 1: 搭建可播放的演示稿骨架

**Files:**
- Create: `presentations/llm-wiki-workgroup-sharing/index.html`
- Create: `presentations/llm-wiki-workgroup-sharing/style.css`

**Interfaces:**
- Consumes: `/Users/11185032/.codex/skills/html-ppt-skill/templates/full-decks/presenter-mode-reveal/{index.html,style.css}`。
- Produces: 引入 `../../../.codex/skills/html-ppt-skill/assets/runtime.js` 的本地 15 页 deck；每页通过 `data-title` 提供导航标题。

- [ ] **Step 1: 复制演讲者模式模板到交付目录**

Run:

```bash
mkdir -p presentations
cp -R /Users/11185032/.codex/skills/html-ppt-skill/templates/full-decks/presenter-mode-reveal presentations/llm-wiki-workgroup-sharing
```

Expected: 交付目录包含 `index.html` 与 `style.css`。

- [ ] **Step 2: 将主题和资源路径替换为绝对本地 skill 资源**

在 `index.html` 的 `<head>` 保留以下资源顺序，主题改为 `obsidian-claude-gradient.css`：

```html
<link rel="stylesheet" href="/Users/11185032/.codex/skills/html-ppt-skill/assets/fonts.css">
<link rel="stylesheet" href="/Users/11185032/.codex/skills/html-ppt-skill/assets/base.css">
<link rel="stylesheet" id="theme-link" href="/Users/11185032/.codex/skills/html-ppt-skill/assets/themes/obsidian-claude-gradient.css">
<link rel="stylesheet" href="/Users/11185032/.codex/skills/html-ppt-skill/assets/animations/animations.css">
<link rel="stylesheet" href="style.css">
```

在 `</body>` 前引入：

```html
<script src="/Users/11185032/.codex/skills/html-ppt-skill/assets/runtime.js"></script>
```

- [ ] **Step 3: 检查骨架的幻灯片数量**

Run:

```bash
rg -c '<section class="slide"' presentations/llm-wiki-workgroup-sharing/index.html
```

Expected: 后续完成内容替换时输出 `15`。

### Task 2: 编写 LLM Wiki 主线与可见内容

**Files:**
- Modify: `presentations/llm-wiki-workgroup-sharing/index.html`
- Modify: `presentations/llm-wiki-workgroup-sharing/style.css`

**Interfaces:**
- Consumes: 三篇参考笔记和设计说明中的 15 页表格。
- Produces: 15 个按 `data-title` 命名的 slide，标题依次为 `开场`、`问题`、`定义`、`转变`、`三层架构`、`维护闭环`、`导航与演进`、`Obsidian`、`人机协作`、`Web Clipper`、`剪藏质量`、`端到端`、`最小实践`、`成功标准`、`行动`。

- [ ] **Step 1: 写入 1–7 页的 LLM Wiki 心智模型**

将下列观众可见结论分别放进标题、卡片、时间线或流程图：

```text
1  知识为什么总在聊天记录里消失？
2  文件问答解决“找到”，却没有解决“沉淀”。
3  LLM Wiki = 原始资料 + 持续整理 + 结构化 Markdown Wiki。
4  角色转变：从临时问答工具，到长期知识库维护者。
5  raw / wiki / schema：原料不可变、页面可演进、规则可约束。
6  Ingest → Query → Lint：一次处理不是结束，而是下一次回答的起点。
7  index.md 帮你找内容，log.md 帮你看知识如何演进。
```

- [ ] **Step 2: 写入 8–12 页的 Obsidian 支撑链路**

```text
8  Obsidian 是人的浏览与审阅层，不是另一套数据孤岛。
9  CLI / Agent 让双链、属性、附件等结构化操作更可控。
10 Web Clipper 将网页正文和元数据送入本地 Markdown。
11 模板与变量提升剪藏质量；图片本地化规避链接失效；raw 保持不可变。
12 页面 → raw → ingest → wiki → 带引用的答案：一条素材的完整旅程。
```

- [ ] **Step 3: 写入 13–15 页的落地收束**

```text
13 一套 vault、一个试点领域、三条操作规则。
14 可浏览、可追溯、可复用、可持续维护，才是知识资产。
15 本周行动：选 1 篇素材，完成第一个 ingest，约一次 30 分钟复盘。
```

- [ ] **Step 4: 用局部 CSS 实现三层架构和闭环图**

在 `style.css` 中增加 `.layer-grid`、`.flow-loop`、`.pipeline`、`.metric-grid` 的 scoped 样式，只使用 `var(--text-*)`、`var(--surface)`、`var(--border)`、`var(--accent)` 等主题令牌；不添加字面量主题色。

- [ ] **Step 5: 验证主线和页数**

Run:

```bash
rg -c '<section class="slide"' presentations/llm-wiki-workgroup-sharing/index.html
rg -n 'Ingest|Query|Lint|raw|wiki|schema|Web Clipper' presentations/llm-wiki-workgroup-sharing/index.html
```

Expected: 第一条输出 `15`；第二条命中闭环、架构和素材入口内容。

### Task 3: 添加演讲者逐字稿与使用说明

**Files:**
- Modify: `presentations/llm-wiki-workgroup-sharing/index.html`
- Create: `presentations/llm-wiki-workgroup-sharing/README.md`

**Interfaces:**
- Consumes: `presenter-mode.md` 的 150–300 字、口语化、提示信号规则。
- Produces: 每页恰有一个 `<aside class="notes">`，README 可让用户本地播放与演讲。

- [ ] **Step 1: 为每张页面添加口语化提示稿**

每个 `<section class="slide">` 的末尾放入一个 `<aside class="notes">`。逐字稿必须包含：一个 `<strong>` 核心词、一个独立的过渡段、以及引出下一页的收束句；不在幻灯片可见区域加入讲者提示。

- [ ] **Step 2: 写入播放说明**

在 README 中写清以下内容：

```markdown
# LLM Wiki 工作小组分享

直接用浏览器打开 `index.html`。

- `←` / `→`：翻页
- `S`：打开演讲者模式
- `F`：全屏
- `O`：总览
- `#/12`：直接跳到第 12 页
```

- [ ] **Step 3: 验证讲稿结构**

Run:

```bash
rg -c '<aside class="notes">' presentations/llm-wiki-workgroup-sharing/index.html
rg -n 'Speaker:|这一页展示|这里讲' presentations/llm-wiki-workgroup-sharing/index.html
```

Expected: 第一条输出 `15`；第二条无输出，避免可见讲者文案。

### Task 4: 渲染并进行视觉验收

**Files:**
- Create: `presentations/llm-wiki-workgroup-sharing/rendered/slide-01.png` … `slide-15.png`
- Modify: `presentations/llm-wiki-workgroup-sharing/{index.html,style.css}`（仅在发现视觉问题时）

**Interfaces:**
- Consumes: `html-ppt-skill/scripts/render.sh` 与已完成的 deck。
- Produces: 完整 PNG 预览集和通过渲染验证的最终 HTML 文件。

- [ ] **Step 1: 渲染 15 页 PNG**

Run:

```bash
/Users/11185032/.codex/skills/html-ppt-skill/scripts/render.sh presentations/llm-wiki-workgroup-sharing/index.html 15 presentations/llm-wiki-workgroup-sharing/rendered
```

Expected: `rendered/` 中生成 15 个 PNG 文件。

- [ ] **Step 2: 检查每张渲染产物是否齐全**

Run:

```bash
rg --files presentations/llm-wiki-workgroup-sharing/rendered -g '*.png' | wc -l
```

Expected: 输出 `15`。

- [ ] **Step 3: 逐页检查视觉问题并最小化修复**

检查封面、三层架构、闭环、端到端和行动页，以及其余页面的文字是否溢出、遮挡或过密。若发现问题，只调整对应页面的布局类或 `style.css` 的 scoped 样式，然后重跑 Step 1 和 Step 2。

- [ ] **Step 4: 记录最终验证结果**

Run:

```bash
rg -c '<section class="slide"' presentations/llm-wiki-workgroup-sharing/index.html
rg -c '<aside class="notes">' presentations/llm-wiki-workgroup-sharing/index.html
rg --files presentations/llm-wiki-workgroup-sharing/rendered -g '*.png' | wc -l
```

Expected: 三条命令均输出 `15`。
