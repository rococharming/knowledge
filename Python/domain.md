---
title: Python 领域规则
date: 2026-05-27
domain: Python
---

# Python 领域规则

## 领域概述

Python 编程语言语法、标准库、工程实践与生态

## 分类体系

wiki 页面按以下子目录组织：

- `summaries/` — 单篇文章、教程、文档的摘要
- `entities/` — 实体页面：库/框架（如 Django、Pandas）、工具（如 Pytest）、PEP、重要人物
- `concepts/` — 概念页面：语言特性（如 GIL、装饰器、生成器）、设计模式、编程范式
- `comparisons/` — 对比分析：库选型、Python 2 vs 3、同步 vs 异步、不同 Web 框架对比
- `overviews/` — 领域概览：Python 生态地图、Web 开发技术栈、数据科学工具链
- `syntheses/` — 综合结论与最佳实践：代码风格指南、项目结构设计、性能优化策略
- `recipes/` — 可复用方法：虚拟环境搭建、打包发布流程、Docker 化部署、常见数据处理模式

## 标签体系

领域初始标签（统一使用英文，便于检索和 Dataview 查询）。标签是动态扩展的——以下只是种子标签，LLM 在 ingest 时会根据素材内容自动补充：

- `#python` — Python 语言核心语法与特性
- `#stdlib` — 标准库模块与用法
- `#data-science` — 数据分析、机器学习相关库与实践
- `#web-dev` — Web 开发框架与相关技术
- `#testing` — 测试框架、测试策略与代码质量
- `#performance` — 性能优化、Profiling、内存管理
- `#best-practices` — 工程实践、代码风格、项目结构

**标签添加原则**：
- 初始标签作为 ingest 时的参考基准
- 当素材涉及新的子主题时，自动创建新标签
- 定期 review 标签使用情况，合并过于细分的标签

## qmd 配置

- collection 名称：`knowledge-python`
- 索引路径：`./wiki/`

## 特殊约定

- **模块导入标注**：涉及标准库模块时，在页面中显式标注 `import` 语句或模块路径，便于检索
- **Python 版本标注**：涉及版本差异的特性（如 `|` 联合类型运算符 3.10+），必须标注最低支持版本
- **类型提示优先**：代码示例尽量包含类型注解，符合现代 Python 工程实践
