---
title: Obsidian CLI
date: 2026-07-12
tags: [Obsidian, CLI, AI-Agent, 知识管理]
aliases:
  - Obsidian 命令行界面
  - obsidian-cli
  - Obsidian CLI
---

# 一、Obsidian CLI 的概念

Obsidian CLI 是 Obsidian 提供的命令行接口，用于让终端、脚本或 AI Agent 与正在运行的 Obsidian 应用交互。它不是给普通用户替代图形界面的主要入口，而是给自动化流程和 AI Agent 使用的操作接口。

Obsidian CLI 的关键价值在于：它不是只修改 Markdown 文件，而是通过 Obsidian 的应用能力操作仓库，例如读取笔记、创建笔记、搜索内容、管理属性、查看反向链接、追加日记和调用模板。

需要注意的是，Obsidian CLI 不是一个脱离 Obsidian 独立工作的 Markdown 工具。它依赖 Obsidian 应用本身，因此使用前需要先打开 Obsidian，并在 Obsidian 中启用 Obsidian CLI。

# 二、为什么要使用 Obsidian CLI

## 1、给 AI 使用

人使用 Obsidian 时，主要还是通过图形界面完成阅读、编辑、拖拽、重命名、插入模板、查看反向链接等操作。Obsidian CLI 的主要使用对象不是人，而是 AI Agent、脚本和自动化工具。

AI Agent 虽然可以直接读写 Markdown 文件，但它很难完整复现 Obsidian 图形界面背后的语义操作。一个 Obsidian 仓库通常还包含双向链接、属性、标签、Bases、附件嵌入、模板和反向链接等知识管理结构。如果只让 AI 使用普通文件读写，它需要自己判断这些结构如何维护，既容易出错，也会消耗更多上下文。

使用 Obsidian CLI 后，AI 可以通过稳定命令完成常见仓库操作：

```bash
obsidian read file="Obsidian CLI"
obsidian create name="新笔记" content="# 新笔记" silent
obsidian append file="每日记录" content="- [ ] 整理 Obsidian CLI 笔记"
obsidian search query="双向链接" limit=10
obsidian backlinks file="Obsidian CLI"
```

这样，AI 不只是“会修改文件”，而是可以更接近“会使用 Obsidian”。

## 2、Obsidian 官方接口

普通文本编辑和 shell 命令只能从文件系统层面操作 `.md` 文件。它们适合简单改字、追加内容、批量查找，但不理解 Obsidian 的应用语义。

典型局限包括：

- **链接同步**：直接用 `mv` 重命名文件时，其他笔记中的 `[[旧笔记名]]` 可能不会同步更新；Obsidian 中启用“始终更新内部链接”后，应用层操作可以同步维护链接关系。
- **属性管理**：直接编辑 YAML 需要自己保证日期、列表、标签、内部链接等类型正确；Obsidian CLI 可以通过属性命令管理元数据。
- **模板调用**：普通 shell 可以创建空文件，但不会自然调用 Obsidian 的模板机制；Obsidian CLI 可以在创建笔记时指定模板。
- **知识关系查询**：普通 shell 可以全文搜索，但不理解反向链接、标签统计、日记、任务等 Obsidian 语义；Obsidian CLI 可以调用这些应用能力。

因此，Obsidian CLI 更适合承接 AI 对 Obsidian 仓库的结构化操作；普通 shell 命令则更适合处理纯文本层面的简单修改。

# 三、使用 Obsidian CLI

## 1、启用 Obsidian CLI

开始之前，需要先在 Obsidian 中启用 CLI。

打开 Obsidian，进入 **设置 -> 关于 -> 高级**，开启 **命令行界面**：

![[assets/Pasted image 20260621225242.png|600]]

如下图所示，点击 **注册** 后，Obsidian 会将 `obsidian` 命令行程序加入 `PATH` 环境变量。

![[assets/Pasted image 20260621225254.png|600]]

完成后，就可以在终端中通过 `obsidian` 命令操作 Obsidian 仓库，例如查看当前仓库、列出所有仓库、新建文件等：

![[assets/Pasted image 20260621225330.png|600]]

可以先运行帮助命令查看当前版本支持的命令：

```bash
obsidian help
```

需要注意的是，Obsidian CLI 默认定位最近获得焦点的仓库。如果同时打开多个仓库，可以使用 `vault=<仓库名>` 指定目标仓库：

```bash
obsidian vault="My Vault" search query="模板"
```

日常使用时，不需要手动记住所有 Obsidian CLI 命令。它更重要的价值，是作为 AI Agent 操作 Obsidian 仓库的标准接口。

## 2、安装 Obsidian CLI Skill

为了让 AI Agent 更容易使用 Obsidian CLI，可以为 AI Agent 安装对应的 Obsidian CLI Skill。

Skill 的作用是把 Obsidian CLI 的使用规则、常用命令、参数格式和注意事项告诉 AI。这样，当用户要求“读取 Obsidian 笔记”“创建笔记”“搜索仓库内容”“管理属性”时，AI 更容易自动选择 Obsidian CLI，而不是退回到普通 shell 文件操作。

Obsidian 的 CEO Kepano 编写了一组 Obsidian 相关的 skills，仓库地址是：[obsidian-skills](https://github.com/kepano/obsidian-skills)

Obsidian CLI Skill 解决的是“AI 如何通过 Obsidian 官方接口操作仓库”的问题。但在实际任务中，AI 还需要区分不同的 Obsidian 文件类型和写作规则，因此通常会配合多个 Obsidian 相关 Skill。

五个 skill 的常见分工如下：

| Skill               | 作用                                   | 定位                                        |
| ------------------- | ------------------------------------ | ----------------------------------------- |
| `obsidian-cli`      | 调用 `obsidian` 命令，与运行中的 Obsidian 实例交互 | 操作入口，负责读取、创建、搜索、追加笔记，管理属性、标签、任务和反向链接      |
| `obsidian-markdown` | 规范 Obsidian 风格 Markdown 写法           | 语法规范，负责属性、维基链接、嵌入、Callout、标签等 Markdown 细节 |
| `json-canvas`       | 创建和编辑 JSON Canvas 文件                 | Canvas 专用，负责 `.canvas` 文件中的节点、边线、分组和连接关系  |
| `obsidian-bases`    | 创建和编辑 Obsidian Bases 文件              | Bases 专用，负责 `.base` 文件中的视图、筛选器、公式、摘要和属性展示 |
| `defuddle`          | 从网页中提取干净的 Markdown 内容                | 网页清洗入口，负责移除导航、广告和杂乱内容，保留可读正文              |

最简单的安装方式，是将该 Git 仓库中的 `skills` 目录复制到当前 Obsidian 仓库根目录下的对应目录中：

| Agent | 目录 |
|---|---|
| Claude Code | `.claude/skills/` |
| Codex | `.agents/skills/` |

或者直接把仓库地址丢给 Agent 让 AI Agent 自动帮你安装。

安装完成后，可以通过简单对话验证 skill 是否可以正确加载。例如，可以询问 AI：

```text
你现在可以调用 Obsidian CLI Skill 吗
```

如果 AI 能主动使用 `obsidian` 命令，说明 skill 基本生效。

需要注意的是，如果请求比较泛化，例如“请帮我在当前目录创建一篇名为 LLM 的笔记”，AI Agent 未必会自动调用 Obsidian CLI Skill。

更稳妥的做法是在 Agent 全局记忆文件中补充明确规则。例如，在 `CLAUDE.md` 或 `AGENTS.md` 中写明：

```markdown
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
```

这样可以提高 AI 调用 Obsidian CLI 的触发率。

