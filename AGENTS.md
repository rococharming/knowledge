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
- wiki 查询默认先用 `index.md`；大规模时优先用 qmd，小规模定位失败或存在语义表述差异时可用 qmd 兜底。每个领域 collection 名见 `domain.md`。

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
- 跨领域 Query 归档默认放入最主要领域；`## 基于页面` 和正文可链接其他领域的依据页。跨领域或重名页面使用路径限定链接，如 `[[AI/wiki/concepts/RAG|RAG]]`。
- Query 归档页是 point-in-time 综合；后续相关基础页面变化时，由 lint 报告是否需要刷新，不自动级联更新。

### Obsidian Markdown 规则

- 同领域且名称唯一时使用 `[[页面名]]`；跨领域或重名页面使用 `[[领域/wiki/分类/页面名|页面名]]`。
- 图片/附件使用 `![[文件名]]`，附件统一放顶层 `assets/`。
- 粗体语法两侧留空格，避免 Obsidian 解析异常。
- Markdown 标题和普通正文中，未包在反引号或代码块里的 `<` 必须转义为 `\<`，如 `Arc\<Mutex\<T>>`。
- 行内代码和代码围栏内的 `<` 不转义。
- 快捷键统一使用 HTML `<kbd>` 标签标注，例如 <kbd>Ctrl</kbd> + <kbd>G</kbd>。
- 创建或修改 Markdown 笔记后，必须检查标题是否含有未转义的 `<`。
- 标签可写正文 `#标签` 或 frontmatter `tags: [标签1, 标签2]`；领域标签体系写入 `<领域>/domain.md`。

## 五、查询与搜索策略

`index.md` 是默认导航入口，qmd 是可选的本地搜索加速器，不替代 wiki，也不应成为 ingest/query 的前置依赖。约 300 页只作为经验参考：索引仍易浏览时优先 index-first；页面较多、索引定位失败、表述差异明显或需要跨页召回时使用 qmd。

1. 领域不明确或涉及多领域时，先读顶层 `index.md` 完成路由。
2. 读取相关领域的 `domain.md`；小规模查询再读 `wiki/index.md` 定位页面。
3. 需要 qmd 时按问题类型召回候选：

| 问题类型 | 命令 | 条件 |
|---|---|---|
| 已知标题、实体名、代码符号或精确短语 | `qmd search` | 只需 BM25 文本索引 |
| 知道概念含义，但不知道原文用词 | `qmd vsearch` | `qmd status` 显示向量已生成，且 `qmd doctor` 确认本地模型与推理环境可用 |
| 同时需要关键词锚点、语义召回、消歧和重排 | 结构化 `qmd query` | 提供 `intent:` + `lex:`/`vec:`，向量与本地模型可用 |

4. qmd 结果只作候选：默认以 `--json -n 10` 获取结果，不在搜索阶段使用 `--full`。选出少量高相关页面后，用 `qmd get` / `qmd multi-get` 回读原文，再综合并标注 `[[引用]]`。
5. 多领域查询优先逐 collection 检索，再由 Agent 合并，避免大 collection 占满全局 Top-K。

qmd collection 规则：

- 每个领域的 `domain.md` 声明建议的 `collection 名称` 和 `collection root`，供启用 qmd 的机器注册。
- `collection root` 一律写成相对知识库根目录的路径：`<领域>/wiki`，例如 `Rust/wiki`、`AI/wiki`。
- qmd 的本机配置（默认 `~/.config/qmd/index.yml`）保存绝对路径，不进入 Git；collection 注册后，`search`、`query`、`get` 等命令可从任意目录执行，并用 `-c <collection>` 限定范围。
- 统一使用 `.agents/skills/init-domain/scripts/qmd_sync.py` 同步本机配置：`--check` 只读检查，普通 `--apply` 补注册缺失 collection 和根 context，只维护 BM25。路径冲突只报告，不自动覆盖。
- 本知识库锁定并验证 qmd `2.5.3`。首次启用语义检索必须由用户显式执行 `qmd_sync.py --apply --semantic`：脚本下载并校验固定模型、将机器本地 qmd 配置指向本机 GGUF 文件、执行 `qmd embed` 与 `qmd doctor`。不要用 `qmd pull` 代替这套流程。
- `init-domain` 默认对新领域执行 `qmd_sync.py --apply --domain <领域>`；qmd 未安装时跳过。每次进入 qmd 检索前由 Agent 对相关领域执行低成本 `--check`，缺失时执行 `--apply`；新机器因而会在首次使用时自动恢复配置。

索引维护：

- `ingest` 或 Query 归档改变 wiki 后执行 `qmd_sync.py --apply --refresh --domain <领域>`：先补齐本机配置，再统一运行一次 `qmd update`；语义/混合检索已启用时随后增量 `qmd embed`。
- 普通 query 不做例行 `update/embed`。只有首次使用发现缺失 collection 时，`--apply` 会在注册后运行一次 `qmd update`；配置健康但索引过期时回退到 `wiki/index.md`，除非用户同时要求维护索引。
- `lint` 只执行 `qmd_sync.py --check` 与 `qmd_semantic.py --check`，并体检文档数、路径、context、模型与向量状态，不执行 `--apply`、`update` 或 `embed`。
- qmd 未安装不是知识库结构错误，不阻塞 index-first 工作流。
