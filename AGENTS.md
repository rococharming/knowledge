# 全局 Schema — LLM Wiki 知识库

本仓库是基于 Karpathy [LLM Wiki](llm-wiki.md) 规范的多领域个人知识库，由 **LLM 维护**、**Obsidian 浏览**、**Git 管理**。

## 一、仓库架构

```text
knowledge/
├── AGENTS.md              # 全局规则主文件
├── CLAUDE.md -> AGENTS.md # Claude Code 兼容入口
├── index.md               # 顶层领域路由
├── assets/                # 共享媒体资产
└── <领域>/
    ├── domain.md          # 领域规则
    ├── raw/               # 来源文档，只读
    ├── wiki/              # LLM 编译输出层
    │   ├── index.md
    │   └── log.md
    └── notes/             # 用户个人笔记，禁止 LLM 修改
```

### 三层分离

| 层 | 目录 | 权限 | 说明 |
|---|---|---|---|
| 不可变层 | `raw/` | 内容只读 | LLM 可读取但不改内容；ingest 后可移动到 `archive/` 并记录日志 |
| 编译输出层 | `wiki/` | LLM 专属 | 创建、更新、提炼页面，维护交叉引用、索引和日志 |
| 个人笔记区 | `notes/` | 禁止修改 | 用户手写笔记、日记、思考，LLM 不写入、不修改 |

### Schema 分层

- 全局规则：`AGENTS.md`。`CLAUDE.md` 必须是指向 `AGENTS.md` 的软链接。
- 领域规则：`<领域>/domain.md`。处理任何领域前必须读取对应 `domain.md`。
- 新增领域必须创建 `domain.md`；补全领域结构使用 `init-domain` skill，不覆盖已有内容。

### 导航与查询

查询通过双层索引定位内容：

1. 顶层 `index.md`：领域路由表，标注各领域 `wiki/index.md` 与页面数。
2. 领域 `wiki/index.md`：该领域内容总目录，按分类组织页面链接与摘要。

处理领域内 ingest、query、lint 或结构维护任务前，必须先读该领域 `domain.md`，再读 `wiki/index.md` 或具体页面。

### Wiki 页面分类

`wiki/` 页面按内容类型组织，领域可在 `domain.md` 中扩展分类：

| 类型 | 说明 | 示例 |
|---|---|---|
| summaries | 单来源摘要 | `[[某篇文章摘要]]` |
| entities | 人、组织、产品、框架等实体 | `[[Claude Code]]` |
| concepts | 概念、方法、理论 | `[[RAG]]` |
| comparisons | 对比分析 | `[[RAG vs Fine-tuning]]` |
| overviews | 领域概览 | `[[AI 编程工具概览]]` |
| syntheses | 综合结论、最终判断 | `[[LLM 编程最佳实践]]` |
| recipes | 可复用流程、配方 | `[[PPT 制作流程]]` |

### raw/ 固定分类

`raw/` 下固定使用：`articles/`、`papers/`、`books/`、`videos/`、`podcasts/`、`others/`、`archive/`。

## 二、核心操作

执行下列操作时必须优先调用对应 skill；skill 不可用时才按本文件原则做最小 fallback，并说明降级原因。

| 操作 | Skill | 含义 |
|---|---|---|
| Ingest | `ingest` | 将 `raw/` 新素材提炼整合到 `wiki/`，更新 `index.md` / `log.md`，归档 raw |
| Query | `query` | 基于 `wiki/` 回答问题，可将高价值结果归档为 wiki 页面 |
| Lint | `lint` | 健康检查：死链、孤立页面、矛盾、陈旧内容、缺失引用、数据空白 |

`log.md` 只记录以上三类操作。`init-domain` 等搭建类操作不写入日志。

## 三、Obsidian 生态与 Skill 使用

本仓库底层是 Markdown 文件，但使用 **Obsidian** 作为浏览和阅读层。因此笔记、画布、Bases、网页素材等操作应优先使用对应 skill，而不是直接用通用文件工具。

| Skill | 定位 | 触发场景 |
|---|---|---|
| `obsidian-cli` | Obsidian 应用操作入口 | 读取、创建、搜索、追加笔记，管理属性、标签、任务、反向链接 |
| `obsidian-markdown` | Obsidian Markdown 语法规范 | `.md` 笔记、frontmatter、维基链接、嵌入、Callout、标签 |
| `json-canvas` | Canvas 专用 | `.canvas`、思维导图、流程图、节点和边线 |
| `obsidian-bases` | Bases 专用 | `.base`、表格/卡片视图、筛选器、公式、摘要 |
| `defuddle` | 网页清洗入口 | 网页 URL、文章、博客、在线文档提取为干净 Markdown |

使用原则：

- 仓库操作优先 `obsidian-cli`：读取、创建、搜索、追加、属性、标签、反向链接等任务，优先通过 Obsidian CLI。
- Markdown 内容规范用 `obsidian-markdown`：任何创建或修改 `.md` 文件的操作，都必须先经过 `obsidian-markdown`skill 检查/生成内容。
- 专门文件用专门 skill：`.canvas` 用 `json-canvas`；`.base` 用 `obsidian-bases`。
- 网页内容先清洗：标准网页 URL 先用 `defuddle` 提取干净 Markdown，再决定写入笔记、进入 `raw/`，或交给 `note-writer` / `ingest`。

可直接使用通用文件操作的例外：

- 用户明确要求不使用 skill。
- 操作目标明确不是 Obsidian 文件，如纯代码文件、配置文件。
- 对应 skill 不可用，只能 fallback。

搜索规范：

- 标签搜索优先使用 `obsidian tag` 命令。
- wiki 页面小规模用 `index.md`；大规模用 qmd CLI。每个领域 collection 名见 `domain.md`。

## 四、Wiki 页面规范

### Frontmatter

所有 wiki 页面应包含标准 frontmatter：

```markdown
---
title: 页面标题
date: 2026-05-08
tags: [tag1, tag2]
source_count: 3
---
```

- `title`：页面标题。
- `date`：创建或最后更新日期。
- `tags`：主题标签，可用 frontmatter 或正文 `#标签`。
- `source_count`：页面基于多少个 raw 素材；普通 ingest 页面为正整数，Query 归档页固定为 `0`。
- `type`：页面类型，可选。省略时表示普通 wiki 页面；Query 归档页必须写 `type: query_archive`。
- `source_ids`：可选稳定溯源字段；普通 ingest 页面可记录 raw 归档路径与 ingest 日期，用于后续陈旧检测和来源追踪。

### Query 归档页

Query 归档页是基于已有 wiki 页面和一次查询回答形成的二次综合页面，不直接来自 raw 素材。

Query 归档页必须满足：

- frontmatter 包含 `type: query_archive`。
- `source_count: 0`，表示没有直接 raw 来源。
- 正文包含 `## 基于页面`，列出本次综合依据的 wiki 页面，使用 `[[页面名]]`。
- 正文底部仍保留 `## 来源`，写明 `Query 归档（YYYY-MM-DD）` 和问题摘要。
- 可以放在 `concepts/`、`comparisons/`、`syntheses/`、`overviews/`、`recipes/` 等语义分类下，不单独强制新目录。
- 跨领域 Query 归档默认放入最主要领域；`## 基于页面` 可用 `领域/[[页面名]]` 辅助辨认，正文 wiki 链接仍优先同领域页面。
- Query 归档页是 point-in-time 综合；后续相关基础页面变化时，由 lint 报告是否需要刷新，不自动级联更新。

### Obsidian Markdown 规则

- 内部链接使用 `[[维基链接]]`。
- 图片/附件使用 `![[文件名]]`，附件统一放顶层 `assets/`。
- 粗体语法两侧留空格，避免 Obsidian 解析异常。
- Markdown 标题和普通正文中，未包在反引号或代码块里的 `<` 必须转义为 `\<`，如 `Arc\<Mutex\<T>>`。
- 行内代码和代码围栏内的 `<` 不转义。
- 快捷键统一使用 HTML `<kbd>` 标签标注，例如 <kbd>Ctrl</kbd> + <kbd>G</kbd>。
- 创建或修改 Markdown 笔记后，必须检查标题是否含有未转义的 `<`。
- 标签可写正文 `#标签` 或 frontmatter `tags: [标签1, 标签2]`；领域标签体系写入 `<领域>/domain.md`。

## 五、多领域查询与搜索策略

### 规模阈值

| 查询类型 | 小规模 | 大规模 |
|---|---|---|
| 单领域 | 该领域 wiki 页面数 ≤ 300 | 该领域 wiki 页面数 > 300 |
| 多领域 | 涉及领域页面数总和 ≤ 300 | 涉及领域页面数总和 > 300 |

顶层 `index.md` 应标注各领域当前 wiki 页面数。

### 小规模：index.md 模式

1. 扫顶层 `index.md` 判断领域。
2. 读取相关领域 `domain.md` 与 `wiki/index.md`。
3. 从索引定位具体页面。
4. 读取页面后综合回答，并带 `[[引用]]`。

### 大规模：qmd 模式

超过阈值时启用 `qmd search` 做 BM25 关键词匹配，默认检索相关领域 collection。

qmd 路径语义：

- 所有 qmd 命令从知识库根目录执行，即 `/Users/songpengfei/knowledge`。
- 每个领域的 `domain.md` 必须声明 `collection 名称` 和 `collection root`。
- `collection root` 一律写成相对知识库根目录的路径：`<领域>/wiki`，例如 `Rust/wiki`、`AI/wiki`。
- 禁止在全局规则或领域规则里把 qmd 路径写成裸 `./wiki/`，因为它依赖当前工作目录，容易建错 collection。

索引维护：

- `ingest` 后从知识库根目录执行 `qmd update -c <collection>`。
- `query` 进入 qmd 模式前，从知识库根目录对涉及 collection 执行 `qmd update -c <collection>`，避免跨机器切换导致索引过期。
- `lint` 的确定性检查应体检 qmd 配置和 collection 可用性；缺少 qmd CLI 时只报告，不阻塞其他结构修复。

### README 定位

`README.md` 是给人阅读的入口说明；顶层 `index.md` 才是 LLM 路由的权威来源。两者不一致时，以 `index.md` 和各领域 `domain.md` 为准，并在维护时同步 README。
