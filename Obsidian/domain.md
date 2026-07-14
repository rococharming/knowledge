---
title: Obsidian 领域规则
date: 2026-06-21
domain: Obsidian
---

# Obsidian 领域规则

## 领域概述

聚焦 Obsidian 工具与插件生态，包括核心功能、社区插件、主题、CSS 片段、工作流设计，以及基于 Obsidian 搭建 llm-wiki 知识库的方法与最佳实践。

## 分类体系

wiki 页面按以下子目录组织：

- `summaries/` — 单篇文章、教程、官方文档或视频的要点摘要
- `entities/` — Obsidian 相关实体：插件、主题、开发者、核心团队、第三方工具
- `concepts/` — 核心概念：双向链接、图谱视图、Dataview、MOC、Zettelkasten、原子笔记
- `comparisons/` — 对比分析：Obsidian 与其他笔记工具、插件方案对比、工作流对比
- `overviews/` — 领域概览：Obsidian 插件生态、核心功能、笔记方法论地图
- `syntheses/` — 综合结论：Obsidian 使用最佳实践、知识库搭建总结
- `recipes/` — 可复用配方：模板、CSS snippets、Dataview 查询、快捷键方案、自动化脚本

## 标签体系

领域初始标签（统一使用英文，便于检索和 Dataview 查询）。标签是动态扩展的——以下只是种子标签，LLM 在 ingest 时会根据素材内容自动补充：

- `#obsidian` — Obsidian 工具本身、核心功能与版本动态
- `#plugins` — 插件的安装、配置、推荐与开发
- `#note-taking` — 笔记记录方法与写作流程
- `#knowledge-management` — 知识管理理论与实践
- `#markdown` — Markdown 语法、Obsidian 扩展语法与格式规范
- `#workflow` — 个人工作流、自动化与日常使用方法
- `#zettelkasten` — 卡片盒笔记法及其在 Obsidian 中的实践
- `#pkm` — Personal Knowledge Management，个人知识管理体系

**标签添加原则**：
- 初始标签作为 ingest 时的参考基准
- 当素材涉及新的子主题时，自动创建新标签
- 定期 review 标签使用情况，合并过于细分的标签

## qmd 配置

- collection 名称：`knowledge-obsidian`
- collection root：`Obsidian/wiki`
- collection 注册：由 `qmd_sync.py` 根据 Git 根目录与 collection root 幂等同步；本机配置不写入仓库

## 特殊约定

- 插件页面需标注：核心插件 / 社区插件、支持平台、是否需要网络同步或第三方服务
- 涉及具体插件时，优先给出官方 GitHub 仓库或 Obsidian 社区插件市场链接
- 知识库搭建相关页面需说明适用场景：个人学习 / 团队协作文档 / LLM 知识库
