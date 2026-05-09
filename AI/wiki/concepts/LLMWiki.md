---
title: "LLM Wiki"
date: 2026-05-09
source_count: 1
tags: [llm, knowledge-retrieval, concept, workflow]
---

# LLM Wiki

## 定义

LLM Wiki 是由 Karpathy 提出的一种知识管理概念，核心思想是：让 LLM 主动维护一个结构化的知识库，而不是被动地响应检索请求。

## 关键信息

### 核心理念
- 知识被"编译"一次，然后持续维护
- 交叉引用在编译阶段就建立好了
- 矛盾和新信息在 ingest 时就被标记和处理

### 与 RAG 的区别
- RAG：被动检索，每次查询时动态搜索
- LLM Wiki：主动维护，知识被结构化存储和持续更新

### 与 Prompt Caching 的关系
LLM Wiki 可被视为 Prompt Caching 思想的进一步扩展：
- Prompt Caching 解决的是"如何高效加载上下文"
- LLM Wiki 解决的是"如何主动维护和结构化知识"

### 关键特征
1. **结构化**：知识按类别组织（实体、概念、对比等）
2. **交叉引用**：页面间通过链接相互关联
3. **持续维护**：新信息通过 ingest 流程整合，矛盾被显式标记
4. **复合增长**：每次探索的成果都沉淀为可复用的知识资产

## 相关素材

- [[从RAG到PromptCaching知识检索范式的演进]]
