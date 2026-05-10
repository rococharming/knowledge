---
name: query
description: |
  当用户明确向知识库/wiki 提问、查询 wiki 内容、要求基于已有 wiki 知识回答问题时，**务必使用此 skill**。触发场景包括但不限于：用户说"query：xxx"、"wiki 里关于 xxx 怎么说"、"根据我的知识库回答"、"帮我查一下 wiki 里关于 xxx 的内容"、要求总结/对比/解释 wiki 中已有概念。不要把普通代码审查、文件编辑、流程检查或不依赖 wiki 内容的一般问题自动归入 query。该 skill 指导 Claude 基于 wiki/ 中已编译的知识综合回答，**禁止基于通用知识编造**，回答必须带 [[引用]] 标注来源，支持小规模（index.md 模式）和大规模（qmd 模式）两种检索策略，有价值的答案可归档为新 wiki 页面。
---

# Query Skill

基于 `wiki/` 中已编译的知识回答用户问题。回答必须带 `[[引用]]`，来源透明。

## 核心理念

Query 不是从零生成答案，而是**综合已有知识**。LLM 阅读相关 wiki 页面，提取信息，拼合成有出处的回答。如果 wiki 中缺乏相关信息，如实告知，不编造。

## 触发条件

以下用户表达应触发本 skill：

- "query：Claude Code 的缓存机制是什么？"
- "帮我查一下 wiki 里关于 RAG 的内容"
- "wiki 里是怎么说 xxx 的？"
- 任何明确要求“根据 wiki/知识库”回答的问题（尤其是用户使用了 `query：` 前缀时）

**不触发场景**：普通代码审查、编辑本仓库规则文件、检查 skill 实现逻辑、终端操作、或用户没有要求基于 wiki 内容的一般知识问答。

## 执行流程

### 1. 解析问题

明确用户问什么：
- **问题核心**：提取关键词和主题
- **涉及领域**：问题可能涉及哪些领域（AI、心理学、投资等）
- **是否跨领域**：问题是否需要综合多个领域的知识
- **问题类型**：
  - **概念查询**：问"是什么"（如 "Prompt Caching 是什么？"）
  - **对比查询**：问"有什么区别"（如 "RAG 和 Prompt Caching 有什么区别？"）
  - **综合查询**：问"发生了什么变化"（如 "从 RAG 到 Prompt Caching 的知识检索范式发生了什么变化？"）

### 2. 判断规模，选择检索策略

根据知识库规模选择检索方式：

| 指标 | 小规模（index.md 模式） | 大规模（qmd 模式） |
|---|---|---|
| 单领域 wiki 页面数 | < 200 页 | ≥ 200 页 |
| index.md 行数 | < 500 行 | ≥ 500 行 |
| 领域总数 | < 5 个 | ≥ 5 个 |

**判断方法**：
- 先扫一眼 `knowledge/index.md` 了解领域数量和规模。如果文件不存在，说明知识库刚初始化，直接告知用户 wiki 中暂无内容
- 如果涉及的领域 `wiki/index.md` 很短（< 100 行），视为小规模
- 如果读一遍 index.md 后再读 2-3 个页面，上下文明显紧张，**检查 `qmd` 是否可用**（`qmd --version`）
  - qmd 已安装：切换为 qmd 模式
  - qmd 未安装：**告知用户安装方法**，请用户安装后重试

### 3. 小规模检索：index.md 模式

适用于知识库较小、index.md 足够导航的情况。

**步骤**：

1. **读取顶层索引**：读 `knowledge/index.md`，了解有哪些领域
2. **判断相关领域**：根据问题内容判断涉及哪些领域（用户也可能显式指定）
3. **并行读取领域索引**：同时读取相关领域的 `wiki/index.md`
4. **定位相关页面**：从各领域的 `index.md` 中找到最相关的页面链接
5. **读取页面内容**：读取具体 wiki 页面，必要时读取其链接的关联页面
6. **综合回答**：基于读取的内容组织答案

### 4. 大规模检索：qmd 模式

适用于 wiki 页面多、index.md 过长的情况。qmd 是本地 Markdown 检索层，不是知识来源；最终回答仍必须读取 `wiki/` 页面并标注 `[[引用]]`。进入此模式前确认 `qmd` 可用；未安装时不要擅自安装，先告知用户安装命令，若当前环境允许再请求用户确认。

**qmd 安装**：

如果 `qmd --version` 返回命令不存在，说明 qmd 未安装。告知用户：

> qmd 未安装，可用 npm 或 Bun 安装后重试：
> ```bash
> npm install -g @tobilu/qmd
> # 或
> bun install -g https://github.com/tobi/qmd
> ```
> 如果安装时 `better-sqlite3` 编译失败，可尝试：
> ```bash
> cd $(npm root -g)/@tobilu/qmd/node_modules/better-sqlite3 && npm run install
> ```

安装前提：Node.js >= 22，或 Bun >= 1.0；macOS 如遇 SQLite extension 问题，先 `brew install sqlite`。

安装完成后配置各领域的 collection（每个领域只需配置一次，init-domain skill 已写入 qmd 配置到领域 CLAUDE.md）。所有 qmd 命令都从 `knowledge/` 仓库根目录执行；领域 `CLAUDE.md` 中的 `./wiki/` 表示领域内路径，执行命令时转换为仓库根目录下的 `<领域>/wiki`。如果后续执行 `qmd embed` 时模型下载缓慢或卡住，设置 HuggingFace 镜像：
```bash
export HF_ENDPOINT=https://hf-mirror.com
export HF_HUB_ENABLE_HF_TRANSFER=0
```

然后配置 collection：

```bash
qmd collection add ./<领域>/wiki --name knowledge-<领域小写> --mask "**/*.md"
```

**检查并创建 collection**：

新机器首次使用时 collection 可能不存在。进入搜索前，在 `knowledge/` 仓库根目录检查涉及的领域是否有对应 collection：

```bash
qmd collection list
```

如果目标领域的 collection 不存在，自动创建（领域名称和路径遵循该领域 `CLAUDE.md` 中的 qmd 配置；相对路径需转换为仓库根目录路径）：

```bash
qmd collection add ./<领域>/wiki --name knowledge-<领域小写> --mask "**/*.md"
```

**同步索引**：

qmd 索引是本地文件，不随 Git 同步。当用户跨机器切换（`git pull` 后 wiki 文件已更新但索引仍旧）或长时间未查询时，搜索可能漏掉新内容。进入 qmd 搜索前，先在 `knowledge/` 仓库根目录执行：

```bash
qmd update
```

该命令是增量的，已索引文件不会重复处理，耗时通常在 1 秒以内。

**注意**：`qmd update` 完成后可能提示 "Run 'qmd embed' to update embeddings"。如果之前已通过 `qmd status` 确认 vectors 已就绪（`Vectors: N embedded`），**忽略此提示**，不需要运行 embed。

**qmd 命令**：

| 命令 | 原理 | 速度 | 适用场景 |
|---|---|---|---|
| `qmd search` | BM25 关键词匹配 | **即时** | 默认首选 |
| `qmd vsearch` | 向量语义搜索 | **慢，且可能卡在 Gathering information** | 仅在 BM25 不足且语义索引就绪时尝试 |
| `qmd query` | 混合搜索 + query expansion + reranking | **最慢，且可能卡在 Gathering information** | 用户明确要最高质量且能等待时才尝试 |

**默认策略**：先用 `qmd search`。只有关键词检索失败、概念模糊、或用户明确要求语义/最高质量时，才考虑 `qmd vsearch` 或 `qmd query`。实测 `qmd vsearch` 和 `qmd query` 在 qmd 2.1.0 上可能长时间停留在 `Gathering information`，进程 CPU 很低、pending embedding 不变化。不要把这两个命令作为必须完成的验证路径；它们只能作为可中止的可选增强。

**检索流程**：

1. **BM25 快速筛选**：
   ```bash
   qmd search "用户问题" --json -n 20
   ```
   默认搜索所有 include-by-default collection，天然支持跨领域。若用户限定领域，使用一个或多个 `-c`：
   ```bash
   qmd search "用户问题" --json -n 20 -c knowledge-ai -c knowledge-rust
   ```

   **注意**：qmd 的 BM25 tokenizer 对纯中文查询支持有限。如果用户问题以中文为主，优先提取问题中的**英文关键词**（如概念名、产品名）进行搜索。例如用户问"Prompt Caching 是什么"，搜索 `"Prompt Caching"` 而非完整中文句子。

2. **BM25 结果不足时 fallback**：

   如果 BM25 返回空或结果质量明显不足，检查是否需要语义搜索：
   
   ```bash
   qmd status
   ```
   
   如果显示 `Vectors: 0 embedded`：
   - 告知用户"语义索引尚未生成，首次可能需要几分钟；如果 qmd status 显示无 GPU 加速，可能更慢"
   - 仅在用户同意等待语义检索时执行 `qmd embed`。如果下载模型时速度极慢或卡住，先设置 HuggingFace 镜像：
     ```bash
     export HF_ENDPOINT=https://hf-mirror.com
     export HF_HUB_ENABLE_HF_TRANSFER=0
     qmd embed
     ```
   - 完成后继续下一步

   如果有 `Pending: N need embedding` 但 `Vectors: N embedded` 已经不是 0，说明已有语义索引可用但不完整；不要为了查询强制等待 `qmd embed`，除非用户明确要求最新语义召回。

   如果 BM25 已经返回足够相关结果，优先直接读取结果页面，不必为了完整 embedding 等待 `qmd embed`。只有关键词结果不足、问题概念模糊或用户明确需要语义召回时，再尝试向量搜索：
   ```bash
   qmd vsearch "用户问题" --json -n 10
   ```
   若用户明确要最高质量混合检索，可先用低成本参数限制范围：
   ```bash
   qmd query "用户问题" --json -n 10 --no-rerank -C 20
   ```
   只有用户接受更长等待时，才移除 `--no-rerank` 使用完整 reranking：
   ```bash
   qmd query "用户问题" --json -n 10 -C 20
   ```
   `-C/--candidate-limit` 控制进入 reranker 的候选数量，数值越低越快但可能牺牲召回。

3. **语义命令超时回退**：

   - 如果 `qmd vsearch` 或 `qmd query` 30 秒内只输出 `Gathering information` 且没有结果，先向用户说明它可能卡住；不要再并行启动更多同类命令。
   - 如果超过 60 秒仍无结果，停止等待并回退到 `qmd search` + `index.md` + 直接读取页面。
   - 如果需要诊断，查看进程状态；若进程已运行很久但累计 CPU 时间很低、`qmd status` 中 pending embedding 未变化，可判定为 qmd 等待/阻塞，而不是仍在有效计算。
   - 终止已经挂起的 qmd 进程前先征得用户同意。

4. **读取具体内容**：根据结果中的 `qmd://collection/path.md` 读取页面。可用 `qmd get` 截取内容，或映射到仓库内实际文件后直接读取：
   ```bash
   qmd get "qmd://knowledge-ai/concepts/PromptCaching.md" -l 120
   ```

5. **综合回答**：同小规模模式的引用规范

**限制**：
- `-c` 可重复传入多个 collection；未知 collection 会报错，先用 `qmd collection list` 确认名称
- 若用户明确只想查某几个领域，优先用多个 `-c` 限定范围
- 如果 qmd 搜索返回空或语义命令卡住，但 wiki 中明显有相关页面（可通过 index.md 确认），直接回退到读取具体页面，不依赖 qmd 结果
- 如果 `qmd status` 提示 collection 缺少 context，不要阻塞回答；可在最终说明建议用 `qmd context add qmd://<collection> "描述"` 补充领域说明，提升后续检索质量

### 5. 回答格式

**Query 回答是纯文本，不是 wiki 页面。不要包含 frontmatter（`---` 包裹的 YAML），不要包含 `source_count` 等 wiki 元数据。**

回答结构根据问题类型调整：

#### 5.1 概念查询

直接回答定义、原理、优势等，然后列出依据。

```
<直接回答用户问题>

---

**依据**：
- [[PromptCaching]] — 定义和工作原理
- [[LLMWiki]] — 相关背景
```

#### 5.2 对比查询

**必须使用 markdown 表格呈现对比**，表格后给出结论判断。

```
<简短引言>

| 维度 | A | B |
|------|---|---|
| 维度1 | ... | ... |
| 维度2 | ... | ... |

**结论**：...

---

**依据**：
- [[RAGvsPromptCaching]] — 官方对比分析
- [[RAG]] — RAG 的原理和局限
- [[PromptCaching]] — Prompt Caching 的优势
```

#### 5.3 综合查询

需要跨越多个页面综合信息，回答应覆盖问题的各个维度。

```
<综合回答，分章节组织>

---

**依据**：
- [[从RAG到PromptCaching]] — 综合摘要
- [[LLMWiki]] — 背景知识
- [[RAG]] — 原始范式
- [[PromptCaching]] — 新范式
```

#### 引用规范

- 回答中的事实必须标注来源，使用 `[[页面名]]` 语法
- **页面名必须准确匹配文件名（不含 `.md` 后缀）**。例如文件是 `PromptCaching.md`，引用写作 `[[PromptCaching]]`，不是 `[[Prompt Caching]]`
- 直接引用原文时标注页码或段落（如 `[[PromptCaching]]` 第 3 节）
- 多个页面支持同一观点时，可并列引用：`[[页面A]]`、`[[页面B]]`
- 只有在确实读取了该页面的情况下才引用，不编造引用

#### 回答原则

- 先给结论，再给依据
- 如果 wiki 中没有相关信息，明确说"wiki 中目前没有关于 xxx 的内容"
- 如果信息不足但有关联内容，给出关联内容并说明差距
- 不编造 wiki 中没有的信息

### 6. 归档（可选）

如果用户说"归档这个回答"、"把这个存成 wiki 页面"、"记下来"：

1. **判断归档类型**：
   - 单一问题的综合回答 → `syntheses/`（或领域 CLAUDE.md 规定的综合类目录）
   - 跨素材的对比分析 → `comparisons/`（或领域 CLAUDE.md 规定的对比类目录）
   - 新发现的概念定义 → `concepts/`（或领域 CLAUDE.md 规定的概念类目录）
   - 其他根据领域 CLAUDE.md 判断

2. **创建页面**（**这时才写 frontmatter**，因为 wiki 页面需要元数据）：
   ```markdown
   ---
   title: "问题核心"
   date: YYYY-MM-DD
   wiki_source_count: <引用的 wiki 页面数>
   tags: [tag1, tag2]
   ---

   # 问题核心

   ## 回答

   <综合回答全文>

   ## 依据

   - [[页面 1]]
   - [[页面 2]]
   ```

   如果能够从被引用页面准确追溯到底层 raw 来源数，可额外写入 `source_count`；不确定时不要用 wiki 页面数冒充 raw 来源数。

3. **更新 index.md**：在对应分类下添加新页面条目
4. **更新 log.md**：追加归档记录

### 7. 更新 log.md

在对应领域的 `wiki/log.md` **末尾追加**（使用 Edit 工具追加，不要覆盖已有内容）：

```markdown
## [YYYY-MM-DD] query | 问题简述

- 涉及领域：AI、心理学...
- 引用页面：[[页面1]]、[[页面2]]...
- 是否归档：是/否
```

如果涉及多个领域，在主要领域（问题最相关的那个）的 log.md 中记录，或分别记录。

## 约束

1. **绝不回答 raw/ 内容**：query 只基于 `wiki/` 中已编译的知识，不直接读取 `raw/`
2. **query 回答纯文本，无 frontmatter**：只有归档为 wiki 页面时才写 frontmatter
3. **引用必须准确**：每个 `[[引用]]` 必须确实在读取的页面中存在，页面名必须匹配文件名
4. **对比必须表格**：对比类问题的回答必须包含 markdown 表格
5. **诚实面对空白**：wiki 中没有的信息，不编造
6. **保持领域隔离**：不同领域的知识分别引用，跨领域综合时明确标注
7. **log.md 仅追加**：不修改历史记录

## 验证

修改 ingest/query/lint 任一 skill 后，运行：

```bash
python3 .agents/skills/ingest/scripts/test-wiki-skills.py
```

该脚本覆盖小规模 index 模式、大规模 qmd 模式、qmd 缺失/创建/失败路径，以及 `qmd search`、`qmd vsearch`、`qmd query` 三类命令路径。真实 qmd 的 `vsearch/query` 可能挂起，验证时只把 `qmd search` 作为必跑实时命令；语义命令使用 fake qmd 覆盖流程，不作为长时间阻塞测试。
