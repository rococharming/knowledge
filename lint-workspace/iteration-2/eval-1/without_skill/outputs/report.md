# AI 领域 Wiki Lint 报告

**检查时间**: 2026-05-09
**检查范围**: /Users/songpengfei/knowledge/AI/wiki/
**文件总数**: 7 个 .md 文件

---

## 一、死链检查

死链定义：页面中 `[[链接]]` 指向的文件不存在。

### 发现 1 个死链

| 来源页面 | 死链 | 说明 |
|---------|------|------|
| `/Users/songpengfei/knowledge/AI/wiki/concepts/RAG.md` | `[[不存在的页面]]` | RAG.md 的"相关页面"部分引用了该链接，但 wiki 中无对应文件 |

**建议**: 删除该死链，或创建对应的 wiki 页面。

---

## 二、孤立页面检查

孤立页面定义：没有被其他任何 wiki 页面中的 `[[链接]]` 指向的页面。

### 发现 1 个孤立页面

| 页面路径 | 页面标题 | 说明 |
|---------|---------|------|
| `/Users/songpengfei/knowledge/AI/wiki/summaries/孤立文章.md` | 孤立文章 | 该页面在 index.md 中被列出，但没有被任何其他页面通过 `[[链接]]` 引用 |

**说明**: index.md 中的列表项 `[[孤立文章]]` 不计入"被其他页面链接"，因为 index.md 是目录文件，此处统计的是内容页面之间的交叉引用。

**建议**: 考虑在相关概念页面中添加对该页面的引用，或评估是否需要保留。

---

## 三、Frontmatter 问题检查

### 发现 1 个 frontmatter 缺失

| 页面路径 | 问题 | 说明 |
|---------|------|------|
| `/Users/songpengfei/knowledge/AI/wiki/summaries/缺 frontmatter.md` | 缺少 frontmatter | 该页面完全没有 YAML frontmatter，缺少 `title`、`date` 等必需字段 |

### Frontmatter 完整度统计

| 页面 | title | date | source_count | tags |
|------|:-----:|:----:|:------------:|:----:|
| `index.md` | ✓ | ✓ | - | - |
| `log.md` | ✗ | ✗ | - | - |
| `concepts/RAG.md` | ✓ | ✓ | ✓ | ✓ |
| `concepts/旧概念.md` | ✓ | ✓ | ✓ | ✓ |
| `entities/Claude Code.md` | ✓ | ✓ | ✓ | ✓ |
| `summaries/孤立文章.md` | ✓ | ✓ | ✓ | ✓ |
| `summaries/缺 frontmatter.md` | ✗ | ✗ | ✗ | ✗ |

**说明**: `log.md` 作为操作日志，通常不需要标准 frontmatter，此处不视为问题。

**建议**: 为 `summaries/缺 frontmatter.md` 添加标准 frontmatter：

```yaml
---
title: 缺 frontmatter
date: 2026-05-09
source_count: 0
tags: []
---
```

---

## 四、陈旧内容检查

陈旧定义：`date` 超过 6 个月（即早于 2025-11-09）。

### 发现 1 个陈旧页面

| 页面路径 | 页面标题 | 当前 date | 距今天数 |
|---------|---------|----------|---------|
| `/Users/songpengfei/knowledge/AI/wiki/concepts/旧概念.md` | 旧概念 | 2024-01-01 | ~494 天 |

**建议**: 审阅该页面内容，确认信息是否仍然准确，更新后刷新 `date` 字段。

---

## 五、空分类检查

空分类定义：`index.md` 中列出但没有任何页面的分类。

### 发现 4 个空分类

| 分类 | 状态 |
|------|------|
| Comparisons | （暂无） |
| Overviews | （暂无） |
| Syntheses | （暂无） |
| Recipes | （暂无） |

**建议**: 可以保留这些空分类作为占位，等待后续内容填充；或暂时从 index.md 中移除，等有内容时再添加。

---

## 六、问题汇总

| 问题类型 | 数量 | 严重程度 |
|---------|------|---------|
| 死链 | 1 | 中 |
| 孤立页面 | 1 | 低 |
| Frontmatter 缺失 | 1 | 中 |
| 陈旧内容 | 1 | 低 |
| 空分类 | 4 | 低 |

---

## 七、修复建议优先级

1. **高优先级**：修复 `RAG.md` 中的死链 `[[不存在的页面]]`
2. **中优先级**：为 `summaries/缺 frontmatter.md` 添加标准 frontmatter
3. **低优先级**：审阅 `concepts/旧概念.md` 内容并更新日期
4. **低优先级**：评估孤立页面 `summaries/孤立文章.md` 的去留
5. **可选**：清理或保留 index.md 中的 4 个空分类
