---
title: "llm-wiki"
source: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
author:
  - "262588213843476"
published:
created: 2026-07-13
description: "llm-wiki. GitHub Gist: instantly share code, notes, and snippets."
tags:
  - "clippings"
  - "article"
---
# llm-wiki

> 来源：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## AI 摘要

### 为什么值得读这篇文章

这篇文章提出了一种利用大语言模型（LLM）构建**持久化、自维护的个人知识库**的新模式，挑战了传统 RAG（检索增强生成）系统“每次查询从零开始”的局限。它提供了一套完整、可操作且富有远见的蓝图，解决了传统知识管理中最棘手的维护成本问题，让你能把精力放在思考与探索上，而将繁重的整理、关联、更新工作交给 AI。如果你希望你的笔记和知识积累能像代码库一样持续演化、不断增值，这篇文章不容错过。

### 核心思想：从“临时检索”到“持续编译”的范式转变

-   **传统 RAG 的痛点**：每次提问时，LLM 都需要重新检索、阅读并拼凑原始文档中的碎片信息。知识没有积累，每一个新问题都是“重新发明轮子”。
-   **新模式的核心理念**：LLM 不再是临时检索助手，而是你知识库的**“主动维护者”**。它会在你每次添加新资料时，**持续构建并更新一个结构化的、互联的 Wiki**。这个 Wiki 是**持久化、可复利的知识工件**，其中的交叉引用、矛盾标记和综合结论都已预先完成，查询时直接调用，高效且精准。

### 如何实现：三层架构 + 三大操作 + 两件神器

#### 架构：三层分离，各司其职

-   **原始资料 (Raw Sources)**：你收集的不可修改的源文件（文章、论文等）。这是知识的“原材料”库。
-   **Wiki**：LLM 生成和维护的 Markdown 文件目录。包含摘要、实体页、概念页、对比表等。**你阅读它，LLM 编写它**。
-   **Schema**：核心配置文件（如 CLAUDE.md）。它定义了 Wiki 的结构、约定和工作流程，是 LLM 成为“专业 Wiki 维护者”的关键。它由你与 LLM 共同进化。

#### 操作：三大核心工作流

-   **1. 摄取 (Ingest)**：你放入新资料，LLM 阅读、总结、讨论，然后更新 Wiki 中 10-15 个相关页面（摘要、索引、实体页等）。建议单次处理，保持你的参与度。
-   **2. 查询 (Query)**：你向 Wiki 提问，LLM 搜索、阅读相关页面后合成答案并附上引用。**关键技巧：有价值的答案（如分析、对比表）应被“归档”回 Wiki 作为新页面**，使探索成果不断沉淀。
-   **3. 检查 (Lint)**：定期让 LLM 对 Wiki 进行“健康检查”，查找矛盾、过时信息、孤立页面和缺失的连接。这能保持 Wiki 在增长中依然条理清晰。

#### 神器：导航与时间线

-   **index.md**：Wiki 的所有页面目录，按类别组织，附有链接和简要说明。LLM 用它快速定位相关内容，在小规模下效果极佳，可替代昂贵的向量数据库。
-   **log.md**：只增不减的操作日志，记录每次摄取、查询和检查。让你和 LLM 清晰了解知识库的演化历程。

### 它能做什么：广泛的应用场景
-   **个人成长**：追踪健康、心理、自我提升，建立随时间演化的结构化自我认知。
-   **深度研究**：在数周或数月内阅读大量论文和报告，逐步构建具有不断演化论点的综合性 Wiki。
-   **读书笔记**：每章读完就整理人物、主题、情节线，最终形成像“托尔金之门”那样丰富的伴随式 Wiki。
-   **团队协作**：持续从 Slack、会议记录、客户通话中更新内部 Wiki，AI 完成无人愿做的维护工作。
-   **其他**：竞品分析、尽职调查、旅行规划、课程笔记、兴趣爱好——任何需要长期积累和整理知识的场景。

### 核心原因：为什么这套模式能成功

知识库维护之所以失败，是因为**维护成本的增长速度超过了其价值增长速度**。人类会因枯燥的更新工作而放弃。LLM 不会。它们不会感到无聊，不会忘记更新交叉引用，可以一次性修改 15 个文件。**当维护成本趋近于零时，Wiki 就能持续保持活力**。你的角色是策划来源、引导分析、提出好问题、深入思考——把“全部剩余工作”交给 AI。这与 Vannevar Bush 在 1945 年提出的“Memex”愿景一脉相承，而 LLM 恰好解决了这个古老构想的最大难题——谁来负责维护。

### 关键原则：灵活模块化，按需选取

本文描述的是**模式而非具体实现**。所有建议（如图片处理、搜索工具、幻灯片格式）都是**可选且模块化**的。最佳做法是**把本文分享给 LLM 智能体，与它协作，为你的特定需求“实例化”一个版本**。本文的唯一使命是传达这个模式，剩下的细节，你的 LLM 可以帮你搞定。



## 正文

## LLM Wiki

A pattern for building personal knowledge bases using LLMs.

This is an idea file, it is designed to be copy pasted to your own LLM Agent (e.g. OpenAI Codex, Claude Code, OpenCode / Pi, or etc.). Its goal is to communicate the high level idea, but your agent will build out the specifics in collaboration with you.

## The core idea

Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation. Ask a subtle question that requires synthesizing five documents, and the LLM has to find and piece together the relevant fragments every time. Nothing is built up. NotebookLM, ChatGPT file uploads, and most RAG systems work this way.

The idea here is different. Instead of just retrieving from raw documents at query time, the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files that sits between you and the raw sources. When you add a new source, the LLM doesn't just index it for later retrieval. It reads it, extracts the key information, and integrates it into the existing wiki — updating entity pages, revising topic summaries, noting where new data contradicts old claims, strengthening or challenging the evolving synthesis. The knowledge is compiled once and then *kept current*, not re-derived on every query.

This is the key difference: **the wiki is a persistent, compounding artifact.** The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read. The wiki keeps getting richer with every source you add and every question you ask.

You never (or rarely) write the wiki yourself — the LLM writes and maintains all of it. You're in charge of sourcing, exploration, and asking the right questions. The LLM does all the grunt work — the summarizing, cross-referencing, filing, and bookkeeping that makes a knowledge base actually useful over time. In practice, I have the LLM agent open on one side and Obsidian open on the other. The LLM makes edits based on our conversation, and I browse the results in real time — following links, checking the graph view, reading the updated pages. Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.

This can apply to a lot of different contexts. A few examples:

- **Personal**: tracking your own goals, health, psychology, self-improvement — filing journal entries, articles, podcast notes, and building up a structured picture of yourself over time.
- **Research**: going deep on a topic over weeks or months — reading papers, articles, reports, and incrementally building a comprehensive wiki with an evolving thesis.
- **Reading a book**: filing each chapter as you go, building out pages for characters, themes, plot threads, and how they connect. By the end you have a rich companion wiki. Think of fan wikis like [Tolkien Gateway](https://tolkiengateway.net/wiki/Main_Page) — thousands of interlinked pages covering characters, places, events, languages, built by a community of volunteers over years. You could build something like that personally as you read, with the LLM doing all the cross-referencing and maintenance.
- **Business/team**: an internal wiki maintained by LLMs, fed by Slack threads, meeting transcripts, project documents, customer calls. Possibly with humans in the loop reviewing updates. The wiki stays current because the LLM does the maintenance that no one on the team wants to do.
- **Competitive analysis, due diligence, trip planning, course notes, hobby deep-dives** — anything where you're accumulating knowledge over time and want it organized rather than scattered.

## Architecture

There are three layers:

**Raw sources** — your curated collection of source documents. Articles, papers, images, data files. These are immutable — the LLM reads from them but never modifies them. This is your source of truth.

**The wiki** — a directory of LLM-generated markdown files. Summaries, entity pages, concept pages, comparisons, an overview, a synthesis. The LLM owns this layer entirely. It creates pages, updates them when new sources arrive, maintains cross-references, and keeps everything consistent. You read it; the LLM writes it.

**The schema** — a document (e.g. CLAUDE.md for Claude Code or AGENTS.md for Codex) that tells the LLM how the wiki is structured, what the conventions are, and what workflows to follow when ingesting sources, answering questions, or maintaining the wiki. This is the key configuration file — it's what makes the LLM a disciplined wiki maintainer rather than a generic chatbot. You and the LLM co-evolve this over time as you figure out what works for your domain.

## Operations

**Ingest.** You drop a new source into the raw collection and tell the LLM to process it. An example flow: the LLM reads the source, discusses key takeaways with you, writes a summary page in the wiki, updates the index, updates relevant entity and concept pages across the wiki, and appends an entry to the log. A single source might touch 10-15 wiki pages. Personally I prefer to ingest sources one at a time and stay involved — I read the summaries, check the updates, and guide the LLM on what to emphasize. But you could also batch-ingest many sources at once with less supervision. It's up to you to develop the workflow that fits your style and document it in the schema for future sessions.

**Query.** You ask questions against the wiki. The LLM searches for relevant pages, reads them, and synthesizes an answer with citations. Answers can take different forms depending on the question — a markdown page, a comparison table, a slide deck (Marp), a chart (matplotlib), a canvas. The important insight: **good answers can be filed back into the wiki as new pages.** A comparison you asked for, an analysis, a connection you discovered — these are valuable and shouldn't disappear into chat history. This way your explorations compound in the knowledge base just like ingested sources do.

**Lint.** Periodically, ask the LLM to health-check the wiki. Look for: contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links, important concepts mentioned but lacking their own page, missing cross-references, data gaps that could be filled with a web search. The LLM is good at suggesting new questions to investigate and new sources to look for. This keeps the wiki healthy as it grows.

## Indexing and logging

Two special files help the LLM (and you) navigate the wiki as it grows. They serve different purposes:

**index.md** is content-oriented. It's a catalog of everything in the wiki — each page listed with a link, a one-line summary, and optionally metadata like date or source count. Organized by category (entities, concepts, sources, etc.). The LLM updates it on every ingest. When answering a query, the LLM reads the index first to find relevant pages, then drills into them. This works surprisingly well at moderate scale (~100 sources, ~hundreds of pages) and avoids the need for embedding-based RAG infrastructure.

**log.md** is chronological. It's an append-only record of what happened and when — ingests, queries, lint passes. A useful tip: if each entry starts with a consistent prefix (e.g. `## [2026-04-02] ingest | Article Title`), the log becomes parseable with simple unix tools — `grep "^## \[" log.md | tail -5` gives you the last 5 entries. The log gives you a timeline of the wiki's evolution and helps the LLM understand what's been done recently.

## Optional: CLI tools

At some point you may want to build small tools that help the LLM operate on the wiki more efficiently. A search engine over the wiki pages is the most obvious one — at small scale the index file is enough, but as the wiki grows you want proper search. [qmd](https://github.com/tobi/qmd) is a good option: it's a local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking, all on-device. It has both a CLI (so the LLM can shell out to it) and an MCP server (so the LLM can use it as a native tool). You could also build something simpler yourself — the LLM can help you vibe-code a naive search script as the need arises.

## Tips and tricks

- **Obsidian Web Clipper** is a browser extension that converts web articles to markdown. Very useful for quickly getting sources into your raw collection.
- **Download images locally.** In Obsidian Settings → Files and links, set "Attachment folder path" to a fixed directory (e.g. `raw/assets/`). Then in Settings → Hotkeys, search for "Download" to find "Download attachments for current file" and bind it to a hotkey (e.g. <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>D</kbd>). After clipping an article, hit the hotkey and all images get downloaded to local disk. This is optional but useful — it lets the LLM view and reference images directly instead of relying on URLs that may break. Note that LLMs can't natively read markdown with inline images in one pass — the workaround is to have the LLM read the text first, then view some or all of the referenced images separately to gain additional context. It's a bit clunky but works well enough.
- **Obsidian's graph view** is the best way to see the shape of your wiki — what's connected to what, which pages are hubs, which are orphans.
- **Marp** is a markdown-based slide deck format. Obsidian has a plugin for it. Useful for generating presentations directly from wiki content.
- **Dataview** is an Obsidian plugin that runs queries over page frontmatter. If your LLM adds YAML frontmatter to wiki pages (tags, dates, source counts), Dataview can generate dynamic tables and lists.
- The wiki is just a git repo of markdown files. You get version history, branching, and collaboration for free.

## Why this works

The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping. Updating cross-references, keeping summaries current, noting when new data contradicts old claims, maintaining consistency across dozens of pages. Humans abandon wikis because the maintenance burden grows faster than the value. LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass. The wiki stays maintained because the cost of maintenance is near zero.

The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else.

The idea is related in spirit to Vannevar Bush's Memex (1945) — a personal, curated knowledge store with associative trails between documents. Bush's vision was closer to this than to what the web became: private, actively curated, with the connections between documents as valuable as the documents themselves. The part he couldn't solve was who does the maintenance. The LLM handles that.

## Note

This document is intentionally abstract. It describes the idea, not a specific implementation. The exact directory structure, the schema conventions, the page formats, the tooling — all of that will depend on your domain, your preferences, and your LLM of choice. Everything mentioned above is optional and modular — pick what's useful, ignore what isn't. For example: your sources might be text-only, so you don't need image handling at all. Your wiki might be small enough that the index file is all you need, no search engine required. You might not care about slide decks and just want markdown pages. You might want a completely different set of output formats. The right way to use this is to share it with your LLM agent and work together to instantiate a version that fits your needs. The document's only job is to communicate the pattern. Your LLM can figure out the rest.
