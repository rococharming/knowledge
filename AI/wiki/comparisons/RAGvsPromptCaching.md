---
title: "RAG vs Prompt Caching"
date: 2026-05-09
source_count: 1
tags: [llm, rag, prompt-caching, comparison, knowledge-retrieval]
---

# RAG vs Prompt Caching

## 对比

| 维度 | RAG | Prompt Caching |
|------|-----|----------------|
| 知识组织 | 文档切分成小块，按需检索 | 完整上下文一次性加载 |
| 上下文完整性 | 片段化，论证链条可能断裂 | 完整，保持全局关联 |
| 重复查询 | 每次重新检索 | 复用缓存，成本大幅降低 |
| 知识积累 | 不自动积累，检索质量不变 | 缓存可复用，知识持续可用 |
| 适用窗口 | 不受上下文长度限制 | 需要大上下文窗口（200K+） |
| 复杂查询 | 多文档综合时效果下降 | 天然支持多文档综合理解 |

## 核心判断

RAG 和 Prompt Caching 代表了两种不同的知识检索哲学：

- **RAG**："需要时再找"——适合超大规模文档库，上下文窗口有限
- **Prompt Caching**："一次性备齐"——适合中等规模知识库，上下文窗口充足

随着上下文窗口不断扩大（4K → 200K+），Prompt Caching 的适用场景正在快速扩展。

## 未来趋势

Prompt Caching 和 LLM Wiki 代表了从"即时检索"到"持久知识"的范式转变。随着上下文窗口继续扩大和缓存成本下降，这种趋势将越来越明显。

## 相关页面

- [[RAG]]
- [[Prompt Caching]]
- [[LLM Wiki]]
