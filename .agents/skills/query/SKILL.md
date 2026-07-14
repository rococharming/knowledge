---
name: query
description: |
  基于知识库 wiki 内容回答用户问题，执行完整的查询流程（判断领域、
  选择查询模式、读取索引和页面、综合回答并标注 [[引用]]）。
  当用户询问任何与知识库相关的问题、寻求信息总结、对比分析、
  概念解释、最佳实践建议时，**必须**使用此 skill。
  即使问题看似简单（如"Rust 所有权是什么"），也应优先查询 wiki 而非凭记忆回答，
  因为 wiki 可能包含用户个人化的笔记和最新 ingest 的内容。
  不要凭通用知识回答知识库相关问题，必须使用此 skill 查询 wiki 后作答。
  触发场景包括但不限于：概念解释、工具对比、最佳实践、知识总结、
  "知识库里关于 X 有什么"、跨领域综合问题、任何涉及 wiki 内容的提问等。
  **此外**：普通 query 只在对话中回答，不写入任何文件；只有当 query 结果被归档为 wiki 页面时，
  才更新 wiki 页面、索引和 Query 日志。
  如果用户在同一条 query 交流里继续要求"将结果归档为 wiki 页面"、
  "根据 query 结果生成 wiki 页面"、"把刚才的回答整理成 wiki"等，
  仍然使用此 skill 完成归档流程，并追加一条 Query 归档日志。
---

# Query — 知识库查询

基于知识库 `wiki/` 中的内容回答用户问题。优先使用 wiki 中的信息，而非模型的训练数据。

## 查询策略

先用可读索引导航，再按规模与问题类型决定是否进入 qmd：

| 场景 | 阈值 | 策略 |
|---|---|---|
| 索引易浏览 | 通常约 300 页以内 | `wiki/index.md` 优先；定位失败、语义模糊或需跨页召回时用 qmd 兜底 |
| 索引成本较高 | 通常超过约 300 页 | qmd 优先召回候选，`wiki/index.md` 用于了解全貌与兜底 |

关键原则：
- **300 页是经验参考，不是必须计算的硬阈值**。以索引是否仍能高效定位为准。
- **qmd 只召回候选，不直接提供最终证据**。搜索后必须回读少量原页面。
- **qmd 是可选加速器**。未安装时回退 `wiki/index.md`；首次使用发现 collection 缺失时，Agent 通过共享同步脚本自动补注册。路径冲突或索引过期时不静默修复。

qmd 命令选择：

| 需求 | 命令 | 前提 |
|---|---|---|
| 标题、实体名、代码符号、精确短语 | `qmd search` | BM25 文本索引可用 |
| 知道概念含义，但不知道原文用词；同义改写较多 | `qmd vsearch` | `qmd status` 中 `Vectors > 0` |
| 需要关键词锚点 + 语义召回 + 消歧 + 重排 | 结构化 `qmd query` | 向量和本地模型可用；手写 `intent:` 与 `lex:`/`vec:` |

不要默认使用裸 `qmd query "用户原话"`。Agent 已知领域、目标与排除项时，应自己构造结构化 query；若只是一个罕见词或精确标题，直接用 `qmd search`。

## 查询流程

### 1. 识别涉及领域

快速扫一眼知识库目录结构，根据用户问题判断涉及领域：
- **显式指定**（如"在 Rust 知识库里..."）→ 直接使用
- **未指定** → 根据关键词推断（如"所有权"→Rust，"RAG"→AI）
- **多领域** → 同时查询多个
- **不确定** → 先用顶层 `index.md` 路由；只有歧义会实质改变答案时才询问用户

### 2. 读取领域规则与索引

领域未明确或涉及多领域时，先读顶层 `index.md` 路由；用户已明确指定领域时可直接进入该领域。随后读取每个相关领域的 `domain.md`。索引易浏览时读取 `wiki/index.md`；索引成本较高时可直接用 qmd 召回，再用 `wiki/index.md` 补充全貌。

### 3. 执行查询

#### 3.1 index-first（小规模默认）

1. 读取涉及领域的 `wiki/index.md`。
2. 根据标题与摘要定位候选页面。
3. 候选明确时，读取相关页面及其直接引用页面并综合回答。
4. 若索引无法定位、用户用词与页面用词差异较大、或问题需要跨多页召回，进入 qmd 候选流程。

#### 3.2 qmd 候选流程（大规模默认或小规模兜底）

collection 注册后，qmd 命令可从任意目录执行；每次搜索必须用 `-c <collection>` 限定领域范围。

1. **确认范围与状态**
   - 从 `domain.md` 读取 collection 名称与 root。
   - 每次进入 qmd 候选流程前执行 `python .agents/skills/init-domain/scripts/qmd_sync.py --check --domain <领域>`。这是低成本只读检查；返回 `needs_sync` 时由 Agent 执行对应的 `--apply`，补注册和根 context，并在配置变化后运行一次 `qmd update`。
   - 返回路径冲突或错误时只报告并回退到 `wiki/index.md`，不自动覆盖本机现有 collection。
   - 只有准备使用 `vsearch` / `query` 且向量状态未知时，才读取 `qmd status`。`Vectors = 0` 时不能使用语义检索；`Pending > 0` 时结果只覆盖已生成向量的文档，不能视为完整召回。已验证的 qmd 2.5.3 中，`vsearch` 还会调用 generation 模型做查询扩展，不能只检查文档向量；模型配置可疑时运行 `qmd_semantic.py --check`，实际推理可疑时运行 `qmd doctor`，失败则回退 BM25。新机器只能由用户显式执行 `qmd_sync.py --apply --semantic` 完成首次语义初始化。
   - 配置已经健康时，普通 query 不执行例行 `qmd update` / `qmd embed`。索引明显过期时回退到 `wiki/index.md` 并报告；只有用户同时要求维护索引时才刷新。

2. **按问题类型搜索候选**

   精确词面：

   ```bash
   qmd search "<标题、实体名、符号或精确短语>" -c <collection> --json -n 10
   ```

   语义改写（仅在向量可用时）：

   ```bash
   qmd vsearch "<自然语言概念描述>" -c <collection> --json -n 10
   ```

   复杂混合问题：

   ```bash
   qmd query -c <collection> --json -n 10 $'intent: <目标与排除项>\nlex: <标题、别名、罕见词>\nvec: <自然语言语义改写>'
   ```

   默认不要使用 `--full`，不要在候选阶段把 10 篇全文塞入上下文。`--explain` 只用于诊断排序；`--min-score` 只在已有查询样本完成阈值校准后使用。

3. **多领域处理**
   - 优先逐 collection 分开搜索，再由 Agent 合并候选。
   - 若确需一次搜索多个 collection，提高 `-n` 或使用 `--all`，防止大 collection 占满全局 Top-K。

4. **回读证据**
   - 从候选中选少量最相关页面；通常 3–5 篇，简单问题可以更少。
   - 单篇用 `qmd get "#docid"` 或 `qmd get "#docid:<from>:<count>"`；批量用 `qmd multi-get 'qmd://<collection>/<path1>,qmd://<collection>/<path2>' --format md` 或 collection glob。qmd 2.5.3 不使用逗号分隔 `#docid` 做 `multi-get`。
   - 最终事实、判断与引用只能来自回读内容，不能只依据搜索摘要。

#### 3.3 失败回退

1. `search` 结果不足：补充标题别名、中英文同义词、精确短语和排除词。
2. `vsearch` 结果不足：改写为更接近页面陈述的自然语言；需要精确锚点时升级为结构化 `query`。
3. 结构化 `query` 结果不足：检查 `intent:`、`lex:`、`vec:`，必要时增加 `hyde:`；不要反复提交裸 query。
4. 向量、模型或 GPU 不可用：回退到 `qmd search`。
5. 多 collection 结果失衡：逐 collection 检索后合并。
6. qmd 仍无合理候选：回读 `wiki/index.md`；若页面本身缺失，明确说明知识库证据不足。

### 4. 组织回答

回答形式服从问题本身，不强制固定模板。需要时可使用段落、列表、表格或其他产物；重点是综合 wiki 内容并保留可追溯引用。只有检索范围、回退或证据不足会影响结论时，才说明检索过程。

**引用规范**：
- 事实、观点必须标注来源，使用 `[[页面名]]` 格式
- 多页面支持同一观点时，引用最关键的 1-2 个
- 引用自然融入句子，不要堆砌

**回答原则**：
- 基于 wiki 内容；知识库证据不足时直接说明。若用户还需要库外补充，应与 wiki 结论明确分开并标注来源
- 若 wiki 内容有矛盾，指出矛盾并说明各来源立场
- 若信息不足，明确说明"知识库中关于 X 的信息有限"
- 跨领域问题时，显式说明各领域视角差异

### 5. 可选：归档为 wiki 页面

若回答具有长期价值（系统性对比分析、综合结论、最佳实践），可以建议归档；未经用户明确授权不写入 wiki：

- 概念解释 → `concepts/`
- 对比分析 → `comparisons/`
- 最佳实践/综合结论 → `syntheses/`
- 领域概览 → `overviews/`

归档流程：
1. 创建新页面，包含 Query 归档页 frontmatter（title, date, tags, source_count, type）
2. 内容精炼为可独立阅读的 wiki 页面
3. 正文包含 `## 基于页面`，列出本次综合依据的 wiki 页面
4. 正文底部包含 `## 来源`，写明 Query 归档日期和问题摘要
5. 同领域且名称唯一的页面使用 `[[页面名]]`；跨领域或重名依据页使用路径限定链接，如 `[[AI/wiki/concepts/RAG|RAG]]`
6. 更新 `wiki/index.md` 和顶层 `index.md`
7. 在 `wiki/log.md` 追加 Query 归档条目
8. 执行 `python .agents/skills/init-domain/scripts/qmd_sync.py --apply --refresh --domain <领域>`，补齐本机配置并统一更新一次文本索引；语义/混合检索已启用时再增量 `qmd embed`。qmd 不可用时跳过，不阻塞归档

**Query 归档页格式**：

```markdown
---
title: 页面标题
date: YYYY-MM-DD
tags: [tag1, tag2]
source_count: 0
type: query_archive
---

# 页面标题

[归档后的综合内容]

## 基于页面

- [[来源页面1]]
- [[来源页面2]]

## 来源

Query 归档（YYYY-MM-DD）：<问题摘要>
```

**Query 归档页规则**：
- `type: query_archive` 是正式页面类型，必须写入 frontmatter
- `source_count` 固定为 `0`，表示没有直接 raw 来源
- `## 基于页面` 只列 wiki 页面，不列 raw 文件
- `## 来源` 记录归档动作本身，不伪造 raw 来源
- 跨领域 Query 归档默认放入最主要领域；`## 基于页面` 和正文可以引用其他领域的依据页，并用路径限定链接避免 Obsidian 重名歧义
- Query 归档页是 point-in-time 综合；基础页面后续更新时，由 lint 报告是否需要刷新，不自动级联更新

**后续交互中归档的处理**

用户在后续对话中要求归档（如"把刚才的回答整理成 wiki"）时：
1. **仍然触发此 skill**
2. **复用仍在当前上下文且未过期的查询结果**；上下文不完整或基础页面已变化时重新核对
3. **直接执行归档**：创建页面 → 更新 Markdown 索引与日志 → 在 qmd 已启用时刷新索引

**日志规则**：
- **普通 query 不写日志**：只读查询只在对话中回答，不修改 `wiki/log.md`、`wiki/index.md` 或任何 wiki 页面
- **只有归档 query 结果时才写日志**：当用户明确要求归档、整理成 wiki、保存为 wiki 页面，或 query 流程实际创建/更新了 wiki 页面时，追加 Query 日志
- **同一条归档操作只写一条 Query 日志**：一条 query 结果同时创建/更新多个页面时，在同一条日志里列出
- **不要记录 `结果: 仅查询` 的 Query 条目**；历史日志中这类普通查询记录可删除
- 记录日志时只在 `wiki/log.md` 末尾追加，保留已有历史

**log.md 记录格式**：

```markdown
## [YYYY-MM-DD] Query | <问题摘要>

- 范围: <单领域 / 多领域 / 全库>
- 基于: `[[来源页面1]]`, `[[来源页面2]]`, ...
- 结果: 查询并归档
- 类型: query
- 归档分类: <concepts/comparisons/syntheses/overviews/recipes>
- 创建: `[[新页面名]]`（如创建了新页面）
- 更新: `[[已有页面名]]`（如更新了已有页面）
```
