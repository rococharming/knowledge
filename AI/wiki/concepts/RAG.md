---
title: "RAG"
date: 2026-05-09
source_count: 1
tags: [llm, rag, knowledge-retrieval, concept]
---

# RAG（Retrieval-Augmented Generation）

## 定义

RAG（检索增强生成）是一种将外部知识检索与大语言模型生成能力结合的技术范式。通过将文档切分成小块，在查询时检索相关片段并注入模型上下文，从而扩展模型的知识边界。

## 关键信息

### 核心机制
- 文档切分（Chunking）
- 向量检索（Vector Search）
- 重排序（Reranking）
- 上下文注入

### 局限性
1. **片段化问题**
   - 上下文断裂：无法看到完整的论证链条
   - 重复检索：相同的问题每次都要重新搜索
   - 知识不积累：检索结果不会随时间改善

2. **检索质量瓶颈**
   - 即使使用向量搜索 + 重排序，检索准确率也存在上限
   - 复杂查询需要综合多份文档时，效果会显著下降

### 与 Prompt Caching 的对比
- RAG 强调"按需检索片段"
- Prompt Caching 强调"一次性加载完整上下文并复用"

## 相关素材

- [[从RAG到PromptCaching知识检索范式的演进]]
