---
name: ingest
description: |
  将知识库 raw/ 目录下的 Markdown 素材提炼、整合到 wiki/。
  当用户提到"ingest"、"处理 raw"、"把文章/素材整合到知识库"、
  "提炼素材"、"归档 raw"、"更新 wiki"等时，**必须**使用此 skill。
  任何涉及将 raw/ 中的 Markdown 文件转化为 wiki 页面的操作都必须使用此 skill。
  即使问题看似简单（如"处理一下这篇文章"），只要目标路径在 raw/ 下，
  也应使用此 skill 完成完整的 ingest 流程（读取、提炼、分类、写入 wiki、
  更新索引、归档 raw、更新 qmd 索引），不要凭通用知识简化处理。
  触发场景包括但不限于：ingest 文章、处理 raw 素材、整理 raw 文件、
  归档已处理素材、更新 wiki 内容。
---

# Ingest Skill

## 概述

将 `<domain>/raw/` 下的 Markdown 素材阅读、提取、整合到 `<domain>/wiki/`，
并更新索引、日志和 qmd 搜索索引。

## 触发条件（必须使用的场景）

- "ingest 这篇文章"
- "处理 raw/ 里的新素材"
- "把 xxx.md 整合到知识库"
- "提炼 raw/articles/ 下的内容"
- "归档 raw/ 中的文件"
- "更新 wiki 内容"
- 任何涉及将 raw 素材转化为 wiki 页面的请求
- 用户要求"处理"、"整理"、"提炼" raw/ 目录下文件的场景

## 输入判断

### 用户指定了具体文件

解析用户提供的文件路径，确认文件存在于 `<domain>/raw/`（或子目录）下。

**单个文件：**
1. 读取文件内容
2. 询问用户是否需要**交互式提炼**：
   - "这篇文章需要我逐轮和你确认提炼角度、分类、重点吗？"
   - 如果用户回答需要（yes/y/是/需要 等），进入交互式模式
   - 如果用户回答不需要（no/n/否/不用 等）或未明确回复，进入自动处理模式
3. 交互式模式下，向用户展示素材的核心观点和结构，询问提炼角度、重点、分类偏好、关联页面等
4. 根据用户反馈调整提炼策略，确认后再写入 wiki

**多个文件（2个及以上）：**
- 默认自动批量处理，不逐轮交互
- 处理完所有文件后，统一报告结果（创建了哪些页面、更新了哪些页面、归档了哪些文件）

### 用户未指定具体文件

1. 扫描 `<domain>/raw/`（不包括 `archive/`），列出所有 `.md` 文件
2. 询问用户要处理哪些文件
3. 根据用户选择的数量，按上述"单个文件"或"多个文件"逻辑处理

## 核心处理流程

### 步骤 1：读取素材

读取用户指定的 raw Markdown 文件。注意：raw/ 内容只读，处理过程中绝不修改原文件。

### 步骤 2：分析内容并决策

- 判断素材来源类型：`articles/`、`papers/`、`books/`、`videos/`、`podcasts/`、`others/`
- 根据"页面分类决策表"判断目标分类
- 判断是否应创建新页面，还是更新现有页面

**核心原则：1 篇 raw 素材 = 1 个 wiki 页面**

每篇 raw 素材原则上只创建**一个** wiki 页面。除非素材明确涵盖了两个完全不同的主题（例如同时讲 Rust 所有权和 Python GIL 的对比文章），否则不拆分。单篇文章的摘要就是 summaries/ 下的一个页面，不需要额外创建 concepts/ 页面。

**分类自检问题（写入前必须回答）：**
- 这篇文章是单篇来源的摘要吗？→ 应该是 summaries/
- 这篇文章介绍的是一个人、产品、框架或组织吗？→ 应该是 entities/
- 这篇文章解释的是一个方法论、技术或理论吗？→ 应该是 concepts/
- 这篇文章对比了两个或多个事物吗？→ 应该是 comparisons/
- 这篇文章梳理了一个子领域的全景吗？→ 应该是 overviews/
- 这篇文章给出的是最佳实践或决策建议吗？→ 应该是 syntheses/
- 这篇文章提供的是某个具体问题的操作步骤吗？→ 应该是 recipes/

**分类互斥原则**：一篇文章只能属于一个分类。不能同时创建 summaries/ 和 concepts/ 两个页面来表示同一篇 raw 素材。

如果一篇文章可以同时归入多个分类，**优先选择最具体的分类**。例如：
- 一篇介绍 TDD 的文章 → summaries/（因为是单篇文章的摘要），不是 concepts/
- 一篇 CI/CD 最佳实践指南 → syntheses/（最佳实践），不是 recipes/（除非是纯操作步骤）

### 步骤 3：提炼内容（交互式或自动）

**交互式模式（单个文件 + 用户选择交互）：**
1. 向用户展示素材的核心观点、结构和关键信息
2. 询问以下问题（可合并提问）：
   - 提炼角度：你希望从哪个角度总结这篇文章？（技术细节、方法论、实践指导等）
   - 重点标注：有哪些内容你认为特别重要，需要重点呈现？
   - 分类偏好：你认为这篇文章应该归入哪个分类？
   - 关联页面：是否需要关联到 wiki 中已有的某个页面？
3. 根据用户反馈生成 wiki 页面草稿
4. 向用户展示草稿，确认后再写入

**自动模式（单个文件用户不交互，或多个文件批量）：**
1. 自主分析素材内容，提取关键信息
2. 自主决定分类和关联页面
3. 直接生成 wiki 页面并写入

### 步骤 4：创建/更新 wiki 页面

创建或更新 `<domain>/wiki/` 下的页面。使用**严格的 frontmatter 格式**：

```markdown
---
title: 页面标题
date: YYYY-MM-DD
tags: [tag1, tag2]
source_count: N
---
```

**frontmatter 规范（必须遵守）：**
- `title`：页面标题，简洁明了
- `date`：创建日期，格式 `YYYY-MM-DD`
- `tags`：标签数组，使用英文小写，遵循各领域 `CLAUDE.md` 中的标签体系
- `source_count`：整数，该页面基于多少个 raw 素材（新建为 1，更新则递增）
- **禁止**添加任何其他 frontmatter 字段（如 `source`、`author`、`url` 等）

**页面内容规范：**
- 内容必须提炼而非照搬原文，突出结构化和可检索性
- 使用 `[[维基链接]]` 语法创建交叉引用
- 如果 wiki 中已有相关页面，新页面应至少引用 1-2 个现有页面
- 标签使用英文，遵循各领域 `CLAUDE.md` 中的标签体系

### 步骤 5：更新索引（wiki/index.md）

更新 `<domain>/wiki/index.md`。使用**严格的格式**：

```markdown
---
title: <Domain> Wiki 索引
date: YYYY-MM-DD
---

# <Domain> Wiki 索引

## summaries

- [[页面名]] — 一句话摘要

## entities

- [[页面名]] — 一句话摘要

## concepts

- [[页面名]] — 一句话摘要

## comparisons

## overviews

## syntheses

## recipes
```

**索引规范：**
- 按分类组织，每个分类下只列出属于该分类的页面
- 使用 `[[页面名]]` 格式的 wiki 链接（**不要**使用 `[[路径/文件名.md|页面名]]` 格式）
- 每个链接后附 1-2 句话的摘要
- 如果某个分类下没有页面，保留空分类标题
- 不要重复列出同一个页面

### 步骤 6：更新日志（wiki/log.md）

在 `<domain>/wiki/log.md` 中追加记录。使用**严格的格式**：

```markdown
## YYYY-MM-DD

- **Ingest**: `raw/<类型>/<文件名>.md`
  - 创建: `[[页面名]]`
  - 类型: <articles/papers/books/videos/podcasts/others>
```

**日志规范：**
- 每个 raw 文件一条独立的 `- **Ingest**: ...` 记录
- 如果多个文件在同一批次处理，每个文件都应有独立的记录条目
- 记录中引用 wiki 页面使用 `[[页面名]]` 格式
- 不要在单条记录中合并多个文件的信息

**批量处理 log 示例：**

```markdown
## 2026-05-10

- **Ingest**: `raw/articles/intro-to-testing.md`
  - 创建: `[[测试驱动开发入门]]`
  - 类型: articles
- **Ingest**: `raw/articles/ci-cd-best-practices.md`
  - 创建: `[[CI-CD最佳实践]]`
  - 类型: articles
- **Ingest**: `raw/papers/distributed-systems-consistency.md`
  - 创建: `[[分布式系统一致性模型综述]]`
  - 类型: papers
```

### 步骤 7：归档 raw 文件

将已处理的文件移动到 `<domain>/raw/archive/<类型>/`：
- `raw/articles/foo.md` → `raw/archive/articles/foo.md`
- 如果 `archive/<类型>/` 目录不存在，先创建

### 步骤 8：更新 qmd 索引

执行 qmd 索引更新：

```bash
qmd update -c knowledge-<domain>
```

其中 `<domain>` 为领域目录名的小写形式（如 `knowledge-rust`、`knowledge-ai`）。

如果该领域尚未创建 qmd collection，先执行：

```bash
qmd collection add ./wiki/ --name knowledge-<domain> --mask "**/*.md"
qmd context add qmd://knowledge-<domain>/ "<领域描述>"
qmd update -c knowledge-<domain>
```

领域描述从该领域的 `CLAUDE.md` 中提取。

## 页面分类决策表

| 素材内容特征 | 目标分类 | 示例 |
|---|---|---|
| 单篇文章、论文、视频摘要 | `summaries/` | `[[测试驱动开发入门]]`（某篇文章的摘要） |
| 人、组织、产品、框架 | `entities/` | `[[Claude Code]]` |
| 方法论、技术、理论 | `concepts/` | `[[RAG]]` |
| 工具对比、方法对比 | `comparisons/` | `[[RAG vs Fine-tuning]]` |
| 子领域全景梳理 | `overviews/` | `[[AI 编程工具概览]]` |
| 最佳实践、决策建议 | `syntheses/` | `[[LLM 编程最佳实践]]` |
| 具体问题的操作步骤 | `recipes/` | `[[PPT 制作流程]]` |

## 完成检查清单

每轮 ingest 完成后，逐项验证：

- [ ] 所有新 wiki 页面都有正确的 frontmatter（title, date, tags, source_count）
- [ ] frontmatter 中没有额外字段（如 source、author 等）
- [ ] 页面分类符合"页面分类决策表"
- [ ] wiki/index.md 按分类正确组织，使用 `[[页面名]]` 格式
- [ ] wiki/log.md 中每个 raw 文件有独立的 Ingest 记录
- [ ] 所有已处理的 raw 文件已移动到 archive/
- [ ] qmd update 已执行

## 关键原则

- **绝不修改 `notes/` 目录**
- **`raw/` 内容只读**，处理完后移动到 `archive/`
- 素材不跨领域，在哪个领域 `raw/` 下就属于哪个领域
- 交互式提炼以用户意图为导向，自动处理以内容质量为导向
- 每次 ingest 后必须更新 qmd 索引
