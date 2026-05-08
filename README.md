# Knowledge — 基于 llm-wiki 的个人知识库

遵循 Karpathy 的 [LLM Wiki 规范](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)，由 LLM（Claude Code或其他AI Agent）维护、Obsidian 浏览的多领域结构化知识库。

## 核心理念

不是 RAG——每次查询时从原始文档检索片段、从头重新发现知识。

而是 **编译**：LLM 逐步构建并维护一个持久的 wiki，将碎片化素材提炼为结构化、相互链接的知识页面。知识被编译一次，然后持续更新、交叉引用、标记矛盾，随时间复合增长。

> Obsidian 是 IDE；LLM 是程序员；wiki 是代码库。

## 仓库架构

```
knowledge/
├── CLAUDE.md              # 全局规则：语言设定、多领域架构、wiki 契约
├── llm-wiki.md            # llm-wiki 规范原文（Karpathy）
├── assets/                # 共享媒体资产（所有领域共用，Obsidian 图片引用等）
├── AI/                    # AI领域知识库
│   ├── CLAUDE.md          # 领域专属规则（名称、分类示例、qmd collection）
│   ├── raw/               # 不可变层 — 来源文档，绝对只读
│   ├── wiki/              # 编译输出层 — LLM 专属工作区
│   │   ├── index.md       # 总目录 — wiki 页面索引（按分类组织）
│   │   └── log.md         # 操作日志 — 仅追加记录（ingest/query/lint）
│   └── notes/             # 个人笔记区 — 禁止修改
│       └── Claude Code/   # Claude Code 主题笔记
└── <新领域>/              # 新增领域时创建，结构同上
    ├── CLAUDE.md
    ├── raw/
    ├── wiki/
    │   ├── index.md
    │   └── log.md
    └── notes/
```

### 领域目录内部架构

每个领域目录拥有完整独立的 llm-wiki 结构，内部三层分离：

| 层     | 目录       | 权限        | 说明                                    |
| ----- | -------- | --------- | ------------------------------------- |
| 不可变层  | `raw/`   | 绝对只读      | 来源文档（文章、论文、图片），LLM 从中读取但从不修改          |
| 编译输出层 | `wiki/`  | LLM 专属工作区 | 创建、更新、提炼知识并解决矛盾（人类可阅读并按需修改对应 wiki 页面） |
| 个人笔记区 | `notes/` | 禁止修改      | 用户手写的个人笔记                             |

## 领域

| 领域  | 目录    | 主题              |
| --- | ----- | --------------- |
| AI  | `AI/` |  AI 编程工具、方法论与实践 |

新增领域时，创建对应目录并配置其 `CLAUDE.md`。

## 操作流程

- **Ingest**：LLM 从 `raw/` 原始资料目录阅读、提取、整合到 wiki（可能触及 10+ 页面），更新 index 和 log
- **Query**：基于 wiki 内容回答问题，有价值的答案可归档为新页面
- **Lint**：定期健康检查——孤立页面、矛盾、缺失交叉引用、陈旧主张

## 搜索

回答 **Query**时，当 wiki 页面规模较小（~100个素材、~几百个页面时），LLM 阅读 `index.md` 索引查找相关页面。但规模变大之后，不再依赖`index.md`，使用 [qmd](https://github.com/tobi/qmd) CLI工具 作为 wiki 的本地搜索引擎（BM25/向量搜索 + LLM 重排序），每个领域独立 collection。


## 技术栈

- **Obsidian** — 浏览和阅读 wiki（图谱视图、Dataview、Marp）
- **Claude Code** — 维护 wiki（ingest、query、lint）
- **qmd** — wiki 本地搜索引擎