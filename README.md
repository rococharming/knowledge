# LLM Wiki 个人知识库

基于 [Karpathy LLM Wiki](llm-wiki.md) 规范的多领域个人知识库。`README.md` 是人类入口说明；LLM 路由以顶层 [index.md](index.md) 和各领域 `domain.md` 为准。

> **LLM 维护** · **Obsidian 浏览** · **Git 管理**

---

## 仓库架构

```
knowledge/
├── README.md              # 本文件
├── AGENTS.md              # 全局规则主文件（所有领域通用）
├── CLAUDE.md -> AGENTS.md # Claude Code 兼容入口
├── llm-wiki.md            # LLM Wiki 规范原文（Karpathy）
├── index.md               # 顶层目录 — 领域列表与路由
├── assets/                # 共享媒体资产
├── <领域>/                # 每个领域独立目录
│   ├── domain.md          # 领域规则：名称约定、分类体系、qmd collection 名等
│   ├── raw/               # 不可变层 — 来源文档（只读）
│   │   ├── articles/      # 网络文章、博客
│   │   ├── papers/        # 学术论文
│   │   ├── books/         # 书籍章节
│   │   ├── videos/        # 视频转录
│   │   ├── podcasts/      # 播客转录
│   │   ├── others/        # 其他来源
│   │   └── archive/       # 已归档（ingest 后移动）
│   ├── wiki/              # 编译输出层 — LLM 专属工作区
│   │   ├── index.md       # 领域总目录：按分类组织的页面索引
│   │   ├── log.md         # 操作日志（仅追加）
│   │   ├── summaries/     # 单篇来源摘要
│   │   ├── entities/      # 实体页面（人、组织、产品、框架）
│   │   ├── concepts/      # 概念页面（方法论、技术、理论）
│   │   ├── comparisons/   # 对比分析
│   │   ├── overviews/     # 领域概览
│   │   ├── syntheses/     # 综合结论与最佳实践
│   │   └── recipes/       # 可复用方法、操作指南
│   └── notes/             # 个人笔记区 — 用户手写，LLM 不修改
│
└── <新领域>/
```

### 三层分离

| 层 | 目录 | 权限 | 说明 |
|---|---|---|---|
| **不可变层** | `raw/` | **内容只读** | 来源文档按类型分子目录。LLM 从中读取但**绝不修改文件内容**；ingest 完成后将原文件移动到 `archive/`，并在 `log.md` 中记录归档路径。 |
| **编译输出层** | `wiki/` | **LLM 专属** | LLM 创建、更新、提炼知识页面，解决矛盾，维护交叉引用。若手动修改 wiki，应让 LLM 随后检查链接、`index.md`、`log.md` 与内容一致性。 |
| **个人笔记区** | `notes/` | **禁止修改** | 用户手写的个人笔记、日记、思考。LLM **绝不写入或修改**此目录。 |

---

## 现有领域

| 领域                         | 描述             | 当前状态 |
| -------------------------- | -------------- | ---- |
| [AI](AI/wiki/index.md)     | AI 编程工具、LLM 辅助编程与知识检索范式 | 活跃   |
| [macOS](macOS/wiki/index.md) | macOS 开发环境设置、工具链配置及系统相关知识 | 活跃   |
| [Rust](Rust/wiki/index.md) | Rust 编程语言学习与实践 | 活跃   |
| [前后端](前后端/wiki/index.md) | Web 前后端开发入门学习，从前端基础到后端架构的系统知识 | 活跃   |
| [Python](Python/wiki/index.md) | Python 编程语言语法、标准库、工程实践与生态 | 活跃 |
| [通用计算机知识](通用计算机知识/wiki/index.md) | 操作系统、计算机网络、数据结构与算法、计算机组成原理等通用计算机科学基础知识 | 活跃 |
| [BlueOS开发](BlueOS开发/wiki/index.md) | BlueOS（蓝河操作系统）应用层开发：UI 框架、前端框架、快应用（RPK）、开发工具链与工程实践 | 活跃 |
| [Obsidian](Obsidian/wiki/index.md) | Obsidian 工具与插件生态，以及基于 Obsidian 搭建 llm-wiki 知识库的方法 | 活跃 |
---

## 核心操作

知识库有三种核心操作，每种操作由独立的 Agent Skill 实现：

| 操作 | Skill | 功能描述 |
|---|---|---|
| **Ingest** | `ingest` | 将 `raw/` 中的新素材提炼整合到 `wiki/`，维护来源、索引、日志、qmd，并执行同领域有限半径 cascade update。 |
| **Query** | `query` | 基于 `wiki/` 内容回答问题。普通查询只在对话中回答；只有用户要求归档时才创建 Query 归档页并写日志。 |
| **Lint** | `lint` | 健康检查分为确定性检查和启发式检查：结构问题可自动修复，内容矛盾、陈旧、缺页等只报告并给建议。 |

---

## Agent Skills

本项目配置了以下 Agent Skills，用于自动化知识库操作。Skill 源文件位于 `.agents/skills/`，`.claude/skills/` 作为 Claude Code 兼容入口使用。

### 知识库核心 Skills

| Skill | 触发场景 | 功能 |
|---|---|---|
| [`ingest`](.agents/skills/ingest) | "ingest 这篇文章"、"处理 raw 素材"、"把文章整合到知识库" | 将 `raw/` 中的 Markdown 素材提炼、分类、写入 `wiki/`，更新索引与日志，归档 raw，更新 qmd 索引 |
| [`query`](.agents/skills/query) | "知识库里关于 X 有什么"、概念解释、工具对比、最佳实践建议 | 基于 `wiki/` 内容回答问题，支持小规模 index.md 浏览和大规模 qmd 搜索两种模式 |
| [`lint`](.agents/skills/lint) | "lint 知识库"、"检查 wiki"、"health check"、"清理死链" | 运行 Markdown 解析式确定性检查脚本，规范索引、计数、qmd 配置，并报告启发式内容问题 |
| [`init-domain`](.agents/skills/init-domain) | "创建新领域"、"初始化投资知识库"、"搭建新领域" | 通过苏格拉底式提问了解需求，自动生成完整的领域目录结构和 boilerplate 文件 |

### Obsidian 生态 Skills

| Skill | 触发场景 | 功能 |
|---|---|---|
| [`obsidian-markdown`](.agents/skills/obsidian-markdown) | 创建/编辑 `.md` 文件、维基链接、标注、frontmatter | 使用维基链接 `[[Note]]`、嵌入 `![[embed]]`、标注 `> [!type]`、frontmatter 属性等 Obsidian 特定语法 |
| [`obsidian-cli`](.agents/skills/obsidian-cli) | 与 Obsidian 应用交互、管理笔记任务属性 | 通过 `obsidian` CLI 与运行中的 Obsidian 实例交互，读取/创建/搜索笔记、管理任务、标签统计等 |
| [`json-canvas`](.agents/skills/json-canvas) | 创建/编辑 `.canvas` 文件、思维导图、流程图 | 创建和编辑 JSON Canvas 文件，包含节点、边线、分组和连接关系 |
| [`obsidian-bases`](.agents/skills/obsidian-bases) | 创建/编辑 `.base` 文件、表格视图、卡片视图 | 创建 Obsidian Bases，包含视图、筛选器、公式和摘要，实现类似数据库的笔记视图 |
| [`defuddle`](.agents/skills/defuddle) | 读取/分析在线文章、网页文档 | 使用 Defuddle CLI 从网页中提取干净的可读 Markdown，移除导航和杂乱信息 |

---

## 快速开始

### 1. 添加新素材

将文章、论文、视频转录等 Markdown 文件放入对应领域的 `raw/<类型>/` 目录：

```
AI/raw/articles/new-article.md
Rust/raw/papers/new-paper.md
```

然后请求 LLM Agent 进行 ingest：

> "帮我 ingest AI/raw/articles/new-article.md"

Agent 会自动：
- 读取并提炼内容
- 判断分类（summaries/entities/concepts/...）
- 创建/更新 `wiki/` 页面（含标准 frontmatter）
- 更新 `wiki/index.md` 和 `wiki/log.md`
- 将 raw 文件归档到 `raw/archive/`
- 更新 qmd 搜索索引

### 2. 查询知识

向 LLM Agent 提问，它会基于 `wiki/` 内容回答：

> "Rust 所有权和借用的核心规则是什么？"
> "知识库里关于 RAG 和 Fine-tuning 的对比有什么？"

Agent 会自动：
- 判断涉及领域
- 选择查询模式（小规模浏览 index.md / 大规模 qmd 搜索）
- 读取相关页面
- 综合回答，标注 `[[引用]]`
- 普通查询不写入任何文件
- （用户明确要求时）将高价值回答归档为 `type: query_archive` 的新 wiki 页面

### 3. 健康检查

定期请求 LLM Agent 执行 lint：

> "lint 一下知识库"

Agent 会自动：
- 运行 `.agents/skills/lint/scripts/wiki_lint.py`
- 解析 Markdown，忽略代码块、行内代码和 Obsidian 注释中的伪链接
- 自动修复确定性结构问题（索引缺项/悬空项、重复分类、页面计数、qmd 配置提示）
- 在对话中报告启发式问题（矛盾、陈旧、缺页、缺引用、Query 归档页可能过期）
- 只有发生确定性修复或用户要求留档时才写 `wiki/log.md`

### 4. 创建新领域

> "帮我创建一个心理学领域"

Agent 会通过 `init-domain` skill：
- 简短询问领域主题、分类偏好、初始标签
- 自动生成完整目录结构
- 生成个性化领域 `domain.md`
- 更新顶层 `index.md`
- 如 README.md 存在，更新 README.md 的现有领域表

---

## Wiki 页面规范

### Frontmatter

所有 wiki 页面必须包含标准 frontmatter：

```markdown
---
title: 页面标题
date: 2026-05-10
tags: [tag1, tag2]
source_count: 3
---
```

Query 归档页使用正式类型：

```markdown
---
title: 页面标题
date: 2026-05-10
tags: [tag1]
source_count: 0
type: query_archive
---
```

普通 ingest 页面 `source_count` 为正整数；Query 归档页固定为 `source_count: 0`，正文必须包含 `## 基于页面` 和 `## 来源`。

### 页面分类

| 类型 | 说明 | 示例 |
|---|---|---|
| **summaries** | 单个来源的摘要 | `[[某篇文章摘要]]` |
| **entities** | 实体页面（人、组织、产品、框架） | `[[Claude Code]]` |
| **concepts** | 概念页面（方法论、技术、理论） | `[[RAG]]` |
| **comparisons** | 对比分析 | `[[RAG vs Fine-tuning]]` |
| **overviews** | 领域概览 | `[[AI 编程工具概览]]` |
| **syntheses** | 综合结论、最终判断 | `[[LLM 编程最佳实践]]` |
| **recipes** | 可复用方法、配方、流程模板 | `[[PPT 制作流程]]` |

各领域可在上述基础上扩展额外分类（如 Rust 领域的 `snippets/`、`patterns/`、`projects/`、`exercises/`、`resources/`）。

### 链接与引用

- **内部链接**：`[[维基链接]]`
- **图片嵌入**：`![[文件名]]`
- **附件存放**：统一存放顶层 `assets/`

---

## 依赖工具

| 工具 | 用途 | 安装 |
|---|---|---|
| **Obsidian** | 浏览和阅读知识库 | [obsidian.md](https://obsidian.md) |
| **qmd** | BM25 全文搜索索引 | `cargo install qmd` |
| **defuddle** | 网页内容提取（ingest 外部文章时使用） | `npm install -g defuddle` |
| **obsidian-cli** | 与 Obsidian 实例交互 | 见 [Obsidian CLI 文档](https://help.obsidian.md/cli) |

qmd 路径语义：所有 qmd 命令都从知识库根目录执行；每个领域在 `domain.md` 中声明 `collection 名称` 和相对根目录的 `collection root`，例如 `Rust/wiki`。

---

## 规范参考

- [全局规则](AGENTS.md) — 所有领域通用的架构约定、文件规范、操作原则
- [LLM Wiki 规范](llm-wiki.md) — Karpathy 原始规范
- [AI 领域规则](AI/domain.md) — AI 领域的分类体系、标签体系、特殊约定
- [macOS 领域规则](macOS/domain.md) — macOS 领域的分类体系、标签体系、特殊约定
- [Rust 领域规则](Rust/domain.md) — Rust 领域的分类体系、标签体系、特殊约定
- [前后端 领域规则](前后端/domain.md) — 前后端领域的分类体系、标签体系、特殊约定

---

## 贡献与维护

- **Git 管理**：所有变更通过 Git 跟踪，便于跨设备同步和版本回溯
- **LLM 维护**：日常 ingest、query、lint 操作由 LLM Agent 执行
- **手动编辑**：可直接编辑 `wiki/` 和 `notes/` 中的文件，但修改后建议让 LLM Agent 执行 lint 确保一致性
