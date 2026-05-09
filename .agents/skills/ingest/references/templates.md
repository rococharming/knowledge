# Wiki 页面模板

Ingest 时根据素材内容选择合适的模板创建页面。

## Summary 模板（单篇素材摘要）

```markdown
---
title: "素材标题"
date: 2026-05-09
source_count: 1
tags: [tag1, tag2]
---

# 素材标题

来源：[[原始文件名]]

## 核心观点

...

## 关键要点

...

## 相关页面

- [[相关实体 1]]
- [[相关概念 2]]
```

## Entity 模板（实体：人、产品、框架、公司）

```markdown
---
title: "实体名称"
date: 2026-05-09
source_count: 1
tags: [entity, 领域标签]
---

# 实体名称

## 定义

...

## 关键信息

...

## 相关素材

- [[某篇文章摘要]]
```

## Concept 模板（概念：方法论、技术、理论）

```markdown
---
title: "概念名称"
date: 2026-05-09
source_count: 1
tags: [concept, 领域标签]
---

# 概念名称

## 定义

...

## 关键信息

...

## 相关素材

- [[某篇文章摘要]]
```

## Comparison 模板（对比分析）

```markdown
---
title: "A vs B"
date: 2026-05-09
source_count: 1
tags: [comparison, 领域标签]
---

# A vs B

## 结论

...

## 全维度对比

| 特性 | A | B |
|------|---|---|
| ... | ... | ... |

## 详细分析

...

## 相关素材

- [[某篇文章摘要]]
```

## Overview 模板（领域概览）

```markdown
---
title: "xxx 概览"
date: 2026-05-09
source_count: N
tags: [overview, 领域标签]
---

# xxx 概览

## 概述

...

## 主要组成部分

...

## 相关页面

- [[子主题 1]]
- [[子主题 2]]
```

## Synthesis 模板（综合结论）

```markdown
---
title: "xxx 最佳实践"
date: 2026-05-09
source_count: N
tags: [synthesis, 领域标签]
---

# xxx 最佳实践

## 核心结论

...

## 具体建议

...

## 相关素材

- [[某篇文章摘要]]
```

## Recipe 模板（实操配方）

```markdown
---
title: "如何 xxx"
date: 2026-05-09
source_count: 1
tags: [recipe, 领域标签]
---

# 如何 xxx

## 前置条件

...

## 步骤

1. ...
2. ...

## 相关素材

- [[某篇文章摘要]]
```
