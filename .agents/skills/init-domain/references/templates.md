# Init-Domain 模板参考

## 领域 CLAUDE.md 模板

```markdown
---
title: <领域> 领域规则
date: <YYYY-MM-DD>
domain: <领域>
---

# <领域> 领域规则

## 领域概述

<1-2 句话描述核心主题和边界>

## 分类体系

wiki 页面按以下子目录组织：

- `summaries/` — 单个来源的摘要
- `entities/` — 实体页面（人、产品、公司、框架）
- `concepts/` — 概念页面（技术、方法论、理论）
- `comparisons/` — 对比分析
- `overviews/` — 领域概览
- `syntheses/` — 综合结论
- `recipes/` — 实操方法/可复用配方
<用户自定义的额外分类>

## 标签体系

领域初始标签（统一使用英文，便于检索和 Dataview 查询）。标签是动态扩展的——以下只是种子标签，LLM 在 ingest 时会根据素材内容自动补充：

- `#tag1` — 标签说明
- `#tag2` — 标签说明

**标签添加原则**：
- 初始标签作为 ingest 时的参考基准
- 当素材涉及新的子主题时，自动创建新标签
- 定期 review 标签使用情况，合并过于细分的标签

## qmd 配置

- collection 名称：`knowledge-<领域小写>`
- 索引路径：`./wiki/`

## 特殊约定

<基于领域特点的额外规则>
```

## wiki/index.md 模板

```markdown
---
title: <领域> Wiki 索引
date: <YYYY-MM-DD>
---

# <领域> Wiki 索引

## Summaries

_（暂无）_

## Entities

_（暂无）_

## Concepts

_（暂无）_

## Comparisons

_（暂无）_

## Overviews

_（暂无）_

## Syntheses

_（暂无）_

## Recipes

_（暂无）_
```

## wiki/log.md 模板

```markdown
# <领域> Wiki 操作日志

## [<YYYY-MM-DD>] init-domain | 领域初始化
- 创建领域目录结构
- 生成领域 CLAUDE.md
```
