# 语言设定与核心角色 (Global Rules)
- **语言指令**：无论输入何种语言，你必须始终使用**简体中文**进行思考、回复和知识库的编写。
- **角色定义**：你正在维护多个领域的 llm-wiki 知识库，遵循 Karpathy 的 [LLM Wiki 规范](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)，任务是将碎片化的学习素材编译成结构化、高度相互链接的 Obsidian 知识库。

# 多领域架构 (Multi-Domain Architecture)
本 repo 包含多个独立领域知识库，每个领域目录拥有完整独立的 llm-wiki 结构。

## 领域识别规则
- 每个领域目录下都有 CLAUDE.md，定义该领域的专属规则
- 当 Claude Code 读取领域子目录中的文件时，会自动加载该目录的 CLAUDE.md
- skill 操作时先读取目标领域的 CLAUDE.md 获取领域配置（名称、分类示例、notes 子目录等）
- 所有路径拼接规则：`<领域目录>/<子目录>`，如 `AI/wiki/tools/`
- obsidian-cli 调用使用 vault 相对全路径：`obsidian create path="AI/wiki/sources/摘要-xxx.md"`

## 领域内目录权限边界
每个领域目录内部遵循相同的权限边界：
- `<领域>/raw/` — 不可变层，绝对只读。禁止修改或删除此目录下的任何文件
- `<领域>/wiki/` — 编译输出层，LLM 专属工作区。创建、更新、提炼知识并解决矛盾
- `<领域>/notes/` — 个人笔记区，禁止修改或删除
  - notes 下新增有内容的笔记时，先复制到 `<领域>/raw/01-articles/`（kebab-case 命名），再 ingest
- `assets/` — 共享媒体资产层（顶层，所有领域共用）。引用时使用 `![[文件名称.png]]`

# Wiki 核心文件契约 (The Wiki Schema)
每个领域的 wiki/ 内部必须维护以下基石：

1. **`wiki/index.md` (总目录)**：
   每次向 wiki 新增知识页后，必须同步更新此文件，将其按分类加入目录中。
   格式要求： [[页面名称]] — 一句话描述。
   - Tools/Entities/Concepts: 使用 TitleCase 命名。
   - Sources/Workflows: 使用 kebab-case 命名。
2. **`wiki/log.md` (操作日志)**：
   只能追加写入（Append-only）。每次操作后记录：`## [YYYY-MM-DD] <动作> | <操作简述>`。
   操作类型： ingest, query, lint, sync
   **边界**：只记录知识库内容层面的操作，不记录基础设施搭建过程。
3. **内容分类**：
   - `wiki/tools/`：存放工具的专题页，涵盖功能、配置、使用场景及对比
   - `wiki/concepts/`：存放概念、框架、方法论
   - `wiki/entities/`：存放人物、公司、组织
   - `wiki/sources/`：存放从 raw/ 提炼出的原始素材摘要
   - `wiki/workflows/`：存放操作指南、最佳实践、配置模板
   - `wiki/syntheses/`：存放综合对比分析页
4. **强制双向链接**：
   每一个 wiki 页面必须包含 `## 关联链接` 区域，使用 `[[页面名称]]` 链接到其他相关概念。绝不能产生孤岛页面。
5. **矛盾处理原则**：
   如果新摄入的知识与旧知识冲突，不要静默覆盖。在页面中新建 `## 知识冲突` 区块，将两种说法都保留并做对比。

## 跨领域链接规则
- wiki 页面内的 [[wikilink]] 默认指向本领域内页面
- 跨领域引用使用 `[[领域名/页面名]]` 格式（如 `[[AI/Claude_Code]]`）
- 不同领域的 wiki 页面不强制互链，但允许选择性引用

# qmd 搜索引擎
- 每个领域独立的 qmd collection：`qmd collection add ./<领域>/wiki --name <领域>-wiki`
- query skill 根据领域参数选择对应 collection
- 每次 ingest 后执行 `qmd embed` 更新索引
- 当领域 wiki 页面超过 100 个时，query skill 内部优先使用 qmd 进行搜索定位
- 安装：`npm install -g @tobilu/qmd`

# 页面 Frontmatter (YAML) 规范
所有生成的 wiki 页面必须包含以下 YAML 头部：
---
title: "页面标题"
type: tool | concept | entity | source | workflow
tags: [知识标签, 可选工具名]  # 标签不能包含空格，多个单词用连字符连接
tools: [关联的工具名]  # 仅当 type 为 concept/workflow/source 且关联特定工具时填写
sources: [关联的raw文件相对路径]
last_updated: YYYY-MM-DD
---