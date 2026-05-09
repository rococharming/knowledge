# Knowledge — 基于 LLM Wiki 的个人知识库

遵循 Karpathy 的 [LLM Wiki](llm-wiki.md) 规范，由 **LLM 维护**、**Obsidian 浏览**、**Git 管理**的多领域结构化知识库。

> Obsidian 是 IDE；LLM 是程序员；wiki 是代码库。

---

## 核心理念：编译，不是检索

传统 RAG（文件上传、ChatGPT 问答）每次提问都重新检索片段、从头拼凑答案——知识没有积累。

LLM Wiki 的做法是 **编译**：LLM 把原始素材逐步整理成持久的、相互链接的 Markdown 页面。知识被编译一次，然后持续更新、交叉引用、标记矛盾，随时间复合增长。

---

## 快速开始

### 1. 创建领域

**方式一：使用 init-domain skill（推荐）**

直接告诉 LLM：

> "创建心理学领域" 或 "帮我初始化投资知识库"

LLM 会通过苏格拉底式提问了解你的需求（领域主题、分类偏好、标签等），然后自动生成完整的目录结构和个性化的 `CLAUDE.md`。

**方式二：手动创建**

新建一个目录，复用标准结构：

```
<领域>/
├── CLAUDE.md          # 领域规则（命名约定、标签体系等）
├── raw/               # 来源文档（文章、论文、图片）
│   ├── articles/      # 网络文章、博客
│   ├── papers/        # 学术论文
│   ├── books/         # 书籍章节
│   ├── videos/        # 视频转录
│   ├── podcasts/      # 播客转录
│   ├── others/        # 其他来源
│   └── archive/       # 已归档（ingest 后移动到这里）
├── wiki/              # LLM 生成的知识页面
│   ├── index.md       # 页面总目录
│   └── log.md         # 操作日志
└── notes/             # 你的个人笔记
```

参考 `AI/` 目录作为示例。新建领域后，在 `CLAUDE.md` 中告诉 LLM 该领域的主题、命名风格和分类偏好。

### 2. 放入素材

把想消化的文章、论文、笔记放进 `<领域>/raw/`。推荐用 [Obsidian Web Clipper](https://obsidian.md/clipper) 一键将网页转为 Markdown。

### 3. 让 LLM 工作

打开 Claude Code，告诉它 **ingest** 哪个素材。例如：

> "把 `AI/raw/某篇文章.md` ingest 进 wiki"

LLM 会阅读素材、和你讨论要点、在 `wiki/` 中创建摘要和实体页面、更新 `index.md` 和 `log.md`。

---

## 日常使用

你的角色是**策展人**——选择素材、提出问题、审阅结果。LLM 做所有维护工作。

| 你想做什么 | 对 LLM 说 | 你会得到什么 |
|---|---|---|
| **消化新素材** | "ingest `raw/某文章.md`" | wiki 中新增的摘要、实体、概念页面，index 和 log 已更新 |
| **提问** | "query：Claude Code 的缓存机制是什么？" 或直接问问题 | 基于 wiki 内容的综合回答，带 `[[引用]]`。好答案可以要求归档为新页面 |
| **健康检查** | "lint 一下 wiki" | 孤立页面、矛盾、陈旧内容、缺失交叉引用的报告 |

### 小技巧

- **ingest 时参与**：LLM 生成摘要后，你先读一遍，再告诉它哪些点需要强调、补充或修正
- **query 时归档**：一次好的对比分析、一个你发现的关联——要求 LLM 把它存成新 wiki 页面，不要让洞察消失在聊天记录里
- **定期 lint**：wiki 增长一段时间后跑一次 lint，保持知识库健康

---

## 文件结构

```
knowledge/
├── CLAUDE.md              # 全局规则（LLM 读取）
├── llm-wiki.md            # 规范原文
├── index.md               # 顶层领域目录 — 跨领域轻量索引与路由
├── assets/                # 共享图片、附件
├── AI/                    # 示例领域
│   ├── CLAUDE.md
│   ├── raw/               # 来源文档 → 你放，LLM 只读
│   │   ├── articles/      # 网络文章、博客
│   │   ├── papers/        # 学术论文
│   │   ├── books/         # 书籍章节
│   │   ├── videos/        # 视频转录
│   │   ├── podcasts/      # 播客转录
│   │   ├── others/        # 其他来源
│   │   └── archive/       # 已归档（ingest 后移动到这里）
│   ├── wiki/              # 知识页面 → LLM 写，你阅读
│   └── notes/             # 个人笔记 → 你写，LLM 不碰
└── <你的新领域>/
```

**权限速记**：
- `raw/` — 你放素材，按类型分子目录（articles、papers 等），ingest 后自动归档到 `archive/`，LLM 不修改内容
- `wiki/` — LLM 维护，你可以阅读并手动修改
- `notes/` — 你专属，LLM 绝不触碰

---

## 搜索方式

wiki 规模决定搜索策略：

**小规模**（单领域 < 200 页）——LLM 直接读 `wiki/index.md` 定位页面，无需额外工具。

**大规模**（wiki 页面多了以后）——启用 [qmd](https://github.com/tobi/qmd) 本地搜索引擎：

```bash
# 初次配置（每个领域一次）
qmd collection add ./AI/wiki --name knowledge-ai --mask "**/*.md"

# 日常维护（ingest 后自动更新）
qmd update
qmd embed
```

qmd 是本地运行的混合搜索引擎（关键词 + 语义 + LLM 重排序），默认跨所有领域搜索，数据不出本机。

---

## 用 Obsidian 浏览

仓库底层是 Markdown，但推荐用 **Obsidian** 打开浏览：

- 点击 `[[双向链接]]` 在页面间跳转
- **关系图谱**查看知识网络形状
- **Dataview** 插件基于 frontmatter 生成动态列表
- **Marp** 插件直接从 wiki 内容生成幻灯片

Obsidian 设置建议：
- 附件文件夹固定为 `assets/`
- 绑定热键"下载当前文件内所有附件"（如 Ctrl+Shift+D），剪辑网页后一键本地化图片

---

## 技术栈

| 工具 | 用途 |
|---|---|
| **Obsidian** | 浏览、阅读、图谱视图 |
| **Claude Code** | 维护 wiki（ingest / query / lint） |
| **qmd** | 大规模时的本地搜索引擎 |
| **Git** | 版本管理、同步 |

---

## 更多参考

- [llm-wiki.md](llm-wiki.md) — Karpathy 的原始规范（英文）
- [AI/notes/llm-wiki/1、LLM Wiki介绍.md](AI/notes/llm-wiki/1、LLM%20Wiki介绍.md) — 中文介绍
- [CLAUDE.md](CLAUDE.md) — LLM 读取的完整 Schema 规范
