# Query Transcript (Old Skill): CAP定理和分布式共识之间有什么关系？

## 1. 问题解析
- **问题核心**: CAP定理与分布式共识的关系
- **涉及领域**: TestLarge
- **问题类型**: 综合查询

## 2. 规模判断
- TestLarge wiki 有 318 个页面
- 远超 200 页阈值，使用 qmd 大规模检索模式
- qmd 已安装

## 3. BM25 搜索
```bash
qmd search "CAP" --json -n 20 -c knowledge-testlarge
```
结果：CAP (0.89), log.md (0.85), 分布式事务 (0.85), DistributedSystems (0.82), Consensus (0.78)

```bash
qmd search "consensus" --json -n 20 -c knowledge-testlarge
```
结果：Consensus (0.9), CacheCoherence (0.85), DistributedSystems (0.85)

BM25 返回了相关结果，直接进入内容读取。

## 4. 读取具体内容
通过 qmd get 和直接 Read 读取：
- CAP.md — 简略内容
- Consensus.md — 简略内容
- DistributedSystems.md — 简略内容
- 分布式事务.md — 有实质内容
- 两阶段提交.md — 有实质内容

## 5. 综合回答
基于读取的内容组织答案。

**注意**: 旧 skill 没有 qmd update 步骤，没有 collection 检查，也没有 embed lazy-load 机制。
