# LLM Wiki 个人知识库

基于 [Karpathy LLM Wiki](llm-wiki.md) 规范的多领域个人知识库。

> **LLM 维护** · **Obsidian 浏览** · **Git 管理**

---

## 仓库架构

```
knowledge/
├── README.md              # 本文件
├── CLAUDE.md              # 全局规则（所有领域通用）
├── llm-wiki.md            # LLM Wiki 规范原文（Karpathy）
├── index.md               # 顶层目录 — 领域列表与路由
├── assets/                # 共享媒体资产
├── <领域>/                # 每个领域独立目录
│   ├── CLAUDE.md          # 领域规则：名称约定、分类体系、qmd collection 名等
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

| 领域 | 描述 | 当前状态 |
|---|---|---|
| [AI](AI/wiki/index.md) | AI 编程工具、方法论与实践 | 活跃 |
| [Rust](Rust/wiki/index.md) | Rust 编程语言学习与实践 | 活跃 |

---

## 核心操作

知识库有三种核心操作，每种操作由独立的 Claude Code Skill 实现：

| 操作 | Skill | 功能描述 |
|---|---|---|
| **Ingest** | `ingest` | 将 `raw/` 中的新素材阅读、提取、整合到 `wiki/`。自动分类、生成 frontmatter、更新索引与日志、归档 raw、更新 qmd 搜索索引。 |
| **Query** | `query` | 基于 `wiki/` 内容回答问题。自动判断领域与规模，选择 index.md 浏览模式或 qmd BM25 搜索模式，综合回答并标注 `[[引用]]`。 |
| **Lint** | `lint` | 定期健康检查：死链检测、孤立页面修复、索引同步、陈旧内容标记、数据空白识别、矛盾主张检查、缺失交叉引用、重要概念缺页等 9 项专业检查。 |

---

## Claude Code Skills

本项目配置了以下 Claude Code Skills，用于自动化知识库操作：

### 知识库核心 Skills

| Skill | 触发场景 | 功能 |
|---|---|---|
| [`ingest`](.claude/skills/ingest) | "ingest 这篇文章"、"处理 raw 素材"、"把文章整合到知识库" | 将 `raw/` 中的 Markdown 素材提炼、分类、写入 `wiki/`，更新索引与日志，归档 raw，更新 qmd 索引 |
| [`query`](.claude/skills/query) | "知识库里关于 X 有什么"、概念解释、工具对比、最佳实践建议 | 基于 `wiki/` 内容回答问题，支持小规模 index.md 浏览和大规模 qmd 搜索两种模式 |
| [`lint`](.claude/skills/lint) | "lint 知识库"、"检查 wiki"、"health check"、"清理死链" | 对知识库执行 9 项系统化健康检查，自动修复结构问题，生成诊断报告 |
| [`init-domain`](.claude/skills/init-domain) | "创建新领域"、"初始化投资知识库"、"搭建新领域" | 通过苏格拉底式提问了解需求，自动生成完整的领域目录结构和 boilerplate 文件 |

### Obsidian 生态 Skills

| Skill | 触发场景 | 功能 |
|---|---|---|
| [`obsidian-markdown`](.claude/skills/obsidian-markdown) | 创建/编辑 `.md` 文件、维基链接、标注、frontmatter | 使用维基链接 `[[Note]]`、嵌入 `![[embed]]`、标注 `> [!type]`、frontmatter 属性等 Obsidian 特定语法 |
| [`obsidian-cli`](.claude/skills/obsidian-cli) | 与 Obsidian 应用交互、管理笔记任务属性 | 通过 `obsidian` CLI 与运行中的 Obsidian 实例交互，读取/创建/搜索笔记、管理任务、标签统计等 |
| [`json-canvas`](.claude/skills/json-canvas) | 创建/编辑 `.canvas` 文件、思维导图、流程图 | 创建和编辑 JSON Canvas 文件，包含节点、边线、分组和连接关系 |
| [`obsidian-bases`](.claude/skills/obsidian-bases) | 创建/编辑 `.base` 文件、表格视图、卡片视图 | 创建 Obsidian Bases，包含视图、筛选器、公式和摘要，实现类似数据库的笔记视图 |

### 辅助 Skills

| Skill | 触发场景 | 功能 |
|---|---|---|
| [`defuddle`](.claude/skills/defuddle) | 读取/分析在线文章、网页文档 | 使用 Defuddle CLI 从网页中提取干净的可读 Markdown，移除导航和杂乱信息 |
| [`baoyu-translate`](.claude/skills/baoyu-translate) | "翻译这篇文章"、"改成中文/英文"、"精翻" | 三模式翻译：quick（快速）、normal（分析后翻译）、refined（分析→翻译→审校→润色），支持术语表和自定义风格 |
| [`update-todo`](.claude/skills/update-todo) | "扫描 todo"、"更新待办"、"检查哪些笔记需要完善" | 扫描 `Claude Code/` 目录，识别空文件和含"待补充"标记的笔记，生成/更新 `todo.md` |

---

## 快速开始

### 1. 添加新素材

将文章、论文、视频转录等 Markdown 文件放入对应领域的 `raw/<类型>/` 目录：

```
AI/raw/articles/new-article.md
Rust/raw/papers/new-paper.md
```

然后请求 Claude Code 进行 ingest：

> "帮我 ingest AI/raw/articles/new-article.md"

Claude 会自动：
- 读取并提炼内容
- 判断分类（summaries/entities/concepts/...）
- 创建/更新 `wiki/` 页面（含标准 frontmatter）
- 更新 `wiki/index.md` 和 `wiki/log.md`
- 将 raw 文件归档到 `raw/archive/`
- 更新 qmd 搜索索引

### 2. 查询知识

向 Claude Code 提问，它会基于 `wiki/` 内容回答：

> "Rust 所有权和借用的核心规则是什么？"
> "知识库里关于 RAG 和 Fine-tuning 的对比有什么？"

Claude 会自动：
- 判断涉及领域
- 选择查询模式（小规模浏览 index.md / 大规模 qmd 搜索）
- 读取相关页面
- 综合回答，标注 `[[引用]]`
- （可选）将高价值回答归档为新 wiki 页面

### 3. 健康检查

定期请求 Claude Code 执行 lint：

> "lint 一下知识库"

Claude 会自动：
- 扫描所有领域的 wiki 页面
- 检测死链、孤立页面、索引不同步、陈旧内容、数据空白等问题
- 自动修复结构问题（孤立页面加入索引、移除死链、更新计数）
- 生成 `lint-report-YYYYMMDD.md` 诊断报告

### 4. 创建新领域

> "帮我创建一个心理学领域"

Claude 会通过 `init-domain` skill：
- 简短询问领域主题、分类偏好、初始标签
- 自动生成完整目录结构
- 生成个性化领域 `CLAUDE.md`
- 更新顶层 `index.md`

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

---

## 规范参考

- [全局规则](CLAUDE.md) — 所有领域通用的架构约定、文件规范、操作原则
- [LLM Wiki 规范](llm-wiki.md) — Karpathy 原始规范
- [AI 领域规则](AI/CLAUDE.md) — AI 领域的分类体系、标签体系、特殊约定
- [Rust 领域规则](Rust/CLAUDE.md) — Rust 领域的分类体系、标签体系、特殊约定

---

## 贡献与维护

- **Git 管理**：所有变更通过 Git 跟踪，便于跨设备同步和版本回溯
- **LLM 维护**：日常 ingest、query、lint 操作由 Claude Code 执行
- **手动编辑**：可直接编辑 `wiki/` 和 `notes/` 中的文件，但修改后建议让 Claude 执行 lint 确保一致性
