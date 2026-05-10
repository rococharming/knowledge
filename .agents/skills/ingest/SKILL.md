---
name: ingest
description: |
  ingest、加入 wiki、消化素材、处理 raw 文件、批量 ingest、自动 ingest、归档到 wiki — 当用户用这些词表达将 raw/ 中的新素材（文章、论文、视频、笔记等）编译进 wiki 知识库的意图时触发。涉及 raw 素材到 wiki 页面转换的任何任务都必须使用此 skill。流程：阅读素材 → 创建/更新摘要/实体/概念页面 → 更新 index.md 和 log.md → 归档素材 → 更新 qmd 索引。适用于 LLM Wiki 规范的个人知识库维护。
---

# Ingest Skill

将 `raw/` 中的新素材**编译**进 `wiki/`，使其成为持久、相互链接的知识网络的一部分。

Ingest 不是简单存文件，而是读取素材、提取结构化知识、整合到现有 wiki，可能同时创建或更新多个页面。

## 触发条件

- "ingest `raw/某文章.md`"
- "把这篇文章加入 wiki"
- "消化这个素材"
- "处理 raw 下的新文件"
- "自动 ingest 这 5 篇文章"
- "批量 ingest"

## 执行流程

### 1. 解析指令

提取：素材路径、模式（自动/讨论）、批量/单篇。

**路径规则**：
- `raw/` 下按类型分子目录（articles/papers/books/videos/podcasts/others）
- 提供文件名时在 `raw/` 及其子目录搜索（排除 `archive/`）
- 已归档素材不应重复 ingest
- 页面中记录 raw 来源时使用普通路径文本（如 `raw/archive/xxx.md`），不要用 `[[原始文件名]]`，避免把 raw 文件误判为 wiki 死链。

### 2. 读取素材与领域规则

读取素材内容，同时读取 `<领域>/CLAUDE.md` 了解分类体系和标签体系。

### 3. 可选讨论

非自动模式下，展示关键要点供用户确认：

```
我读完这篇素材了，以下是我提取的关键要点：

1. ...
2. ...
3. ...

你希望我：
- 强调某个特定角度？
- 补充什么背景？
- 直接开始写入 wiki？
```

### 4. 分析与规划

确定需要创建/更新的页面：

1. **Summary**：素材本身的摘要（几乎总是创建）
2. **Entity**：具体实体（人、产品、框架、公司）—— 判断标准：是否在知识库主题范围内、是否会被反复引用
3. **Concept**：概念、方法论、理论
4. **其他分类**：根据领域 `CLAUDE.md` 的分类体系判断
5. **现有页面更新**：素材提及的已有页面是否需要补充或标记矛盾

**页面命名**：读取 `references/naming-convention.md` 了解命名规范。优先中文，英文专有名词保留原文。

### 5. 写入 wiki

**读取 `references/templates.md` 获取页面模板。**

创建/更新以下类型页面：
- **Summary** → `wiki/summaries/`
- **Entity** → `wiki/entities/`
- **Concept** → `wiki/concepts/`
- **Comparison** → `wiki/comparisons/`
- **Overview** → `wiki/overviews/`
- **Synthesis** → `wiki/syntheses/`
- **Recipe** → `wiki/recipes/`

**页面规范**：
- 所有页面包含标准 frontmatter（title, date, source_count, tags）
- 内部链接使用 `[[维基链接]]` 语法
- 标记矛盾时使用 `> 注意：新素材 [来源] 提出不同观点...`
- 实体页面已存在时，追加新素材引用并更新 `source_count`

### 6. 更新 index.md

在对应领域的 `wiki/index.md` 中：
1. 添加新页面条目（链接 + 一行摘要 + 日期 + 来源数）
2. 按分类组织，分类名遵循该领域 `CLAUDE.md`
3. **链接使用纯文件名，不带路径前缀**（如 `[[文章]]` 而非 `[[summaries/文章]]`）

### 7. 更新 log.md

在 `wiki/log.md` 末尾追加：

```markdown
## [YYYY-MM-DD] ingest | 素材标题

- 创建/更新页面：Summary、Entity1、Concept2...
- 关键要点：...
- 归档：raw/articles/某文章.md → raw/archive/
```

### 8. 归档素材

将已处理的素材移动到 `raw/archive/`：
- 默认只移动素材文件本身，不修改文件内容。
- 顶层 `assets/` 中的共享附件不移动。
- 只有当附件位于该素材同级或 raw 私有子目录、且链接会随素材归档失效时，才可一并移动，并同步修正素材内的相对链接。
- 在 log.md 中记录归档路径。

### 9. 更新 qmd 索引

qmd 在 ingest 中只作为本地 Markdown 检索层使用。目标是让新写入的 `wiki/**/*.md` 立即可被 `qmd search` 的 BM25 关键词检索命中；不要在 ingest 阶段启动本地 LLM、reranker 或长耗时语义流程。

所有 qmd 命令都从 `knowledge/` 仓库根目录执行。领域 `CLAUDE.md` 中的索引路径若写作 `./wiki/`，表示该领域目录内路径；执行 qmd 命令时需转换为仓库根目录下的 `<领域>/wiki`。

如果 qmd 可用，先检查该领域的 collection 是否已创建：

```bash
qmd collection list
```

如果 collection 不存在，根据该领域 `CLAUDE.md` 中的 qmd 配置自动创建。`post-ingest.sh` 已实现此检查；新领域第一次 ingest 时应先创建 collection，再更新索引：

```bash
qmd collection add ./<领域>/wiki --name knowledge-<领域小写> --mask "**/*.md"
```

然后更新索引：

```bash
qmd update
```

**严格边界**：
- `qmd update` 足以刷新 `qmd search` 所需的 BM25 索引；这是 ingest 的唯一必做 qmd 维护动作。
- 不自动安装 qmd。未安装时跳过索引更新，并在报告中说明。
- 不自动执行 `qmd embed`。它会下载/加载本地 GGUF 模型，可能很慢，应留给 query 阶段按需、经用户同意执行。
- 不在 ingest 中运行 `qmd vsearch` 或 `qmd query`。它们可能触发本地模型、reranking 或长时间 `Gathering information`，不属于写入后处理。
- 不自动覆盖用户已有 `qmd context`。如果 `qmd status` 提示 collection 缺 context，可以在报告中建议用户手动补充。

ingest 后只报告 `qmd status` 中的 pending embedding 数。后续 query 需要语义搜索时再按需执行。如果模型下载缓慢，可设置 HuggingFace 镜像：
```bash
export HF_ENDPOINT=https://hf-mirror.com
export HF_HUB_ENABLE_HF_TRANSFER=0
qmd embed
```

### 10. 质量检查

执行以下验证：
1. 所有新页面包含标准 frontmatter
2. index.md 中所有链接都能对应到实际文件
3. log.md 已正确追加
4. 素材已移动到 archive/
5. 检查是否有孤立页面（无入链的新页面）

**修复发现的问题**，然后报告结果。

### 11. 报告结果

```
已完成 ingest `素材标题`：

- 新建页面：N 个（Summary、Entity: X、Concept: Y）
- 更新页面：N 个
- 更新：index.md、log.md
- 归档：raw/articles/素材.md → raw/archive/
- qmd 索引：已更新

你可以通过 [[素材标题摘要]] 查看完整摘要。
```

## 批量 Ingest

1. 列出所有素材，确认文件列表
2. **逐个处理**每个素材（读取 → 分析 → 创建页面），但**暂不更新 index.md 和 log.md**
3. 所有素材处理完成后，**统一更新一次** index.md 和 log.md
4. 统一归档所有素材
5. 执行一次 qmd update
6. 合并报告

批量模式自动跳过讨论环节。

## 错误处理

| 场景 | 处理方式 |
|------|---------|
| 素材文件不存在 | 告知用户，列出 `raw/` 下的可用文件 |
| 领域 `CLAUDE.md` 缺失 | 告知用户该领域结构不完整，建议运行 `init-domain` skill |
| `raw/archive/` 不存在 | 自动创建目录 |
| 同名页面已存在 | 更新现有页面而非覆盖，追加素材引用 |
| qmd 不可用 | 跳过索引更新，在报告中注明 |

## 约束

1. **raw/ 内容只读**：仅读取，不修改文件内容；归档只允许移动路径并记录日志
2. **绝不写入 `notes/` 目录**
3. **保持领域隔离**：不同领域的素材分别 ingest
4. **source_count 准确**：反映页面实际基于的 raw 素材数
5. **关注矛盾**：新素材与现有内容矛盾时显式标记，不默默覆盖

## 验证

修改 ingest/query/lint 任一 skill 后，运行共享 smoke test：

```bash
python3 .agents/skills/ingest/scripts/test-wiki-skills.py
```

该脚本使用临时 wiki 和 fake qmd，覆盖小规模 index 模式、大规模 qmd 模式、qmd 缺失、collection 自动创建、update 失败，以及 `qmd search`/`qmd vsearch`/`qmd query` 三类命令路径。
