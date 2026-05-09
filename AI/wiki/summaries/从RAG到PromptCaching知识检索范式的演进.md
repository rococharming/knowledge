---
title: "从 RAG 到 Prompt Caching：知识检索范式的演进"
date: 2026-05-09
source_count: 1
tags: [llm, rag, prompt-caching, knowledge-retrieval]
---

# 从 RAG 到 Prompt Caching：知识检索范式的演进

来源：[[test-article-rag-vs-cache]]（`AI/raw/articles/test-article-rag-vs-cache.md`）

## 核心观点

随着大语言模型上下文窗口从 4K 扩展到 200K+，知识检索范式正从传统的 RAG 向 Prompt Caching 和 LLM Wiki 演进，标志着从"即时检索"到"持久知识"的根本转变。

## 关键要点

### RAG 的局限性

1. **片段化问题**
   - 上下文断裂：文档切分导致完整论证链条丢失
   - 重复检索：相同问题每次都要重新搜索
   - 知识不积累：检索结果不会随时间改善

2. **检索质量瓶颈**
   - 即使使用向量搜索 + 重排序，准确率仍有上限
   - 复杂查询需综合多份文档时效果显著下降

### Prompt Caching 的崛起

Anthropic 在 Claude 3.5 Sonnet 中引入的 Prompt Caching 机制代表新思路：

1. **完整性**：整个代码库或文档集作为完整上下文存在
2. **一致性**：不因分块策略不同而丢失关联
3. **效率**：复用缓存后，后续请求成本大幅降低

### LLM Wiki 的启示

Karpathy 提出的 LLM Wiki 概念进一步扩展了这一思路：

- 知识被"编译"一次，然后持续维护
- 交叉引用在编译阶段就建立好了
- 矛盾和新信息在 ingest 时就被标记和处理

## 未来展望

Prompt Caching 和 LLM Wiki 代表了从"即时检索"到"持久知识"的范式转变。随着上下文窗口继续扩大和缓存成本下降，这种趋势将越来越明显。

## 相关页面

- [[Prompt Caching]]
- [[RAG]]
- [[LLM Wiki]]
- [[Anthropic]]
- [[Karpathy]]
