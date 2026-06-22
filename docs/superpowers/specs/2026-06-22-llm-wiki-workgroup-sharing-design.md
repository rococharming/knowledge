---
title: LLM Wiki 工作小组分享 HTML PPT 设计
date: 2026-06-22
tags: [llm-wiki, obsidian, knowledge-management, presentation]
---

# LLM Wiki 工作小组分享 HTML PPT 设计

## 目标

为工作小组制作一份 30 分钟、15 页的中文 HTML 演示文稿。核心目标是让听众理解：LLM Wiki 不是“把资料交给 AI 问答”，而是一套将原始素材持续编译为可浏览、可审阅、可演进知识库的工作方式；Obsidian 是其中面向人的浏览与审阅层；Web Clipper 是高效的素材入口。

## 受众与范围

- 受众：需要共建或维护技术知识资产的工作小组成员。
- 主要依据：`AI/notes/llm-wiki/1、LLM Wiki介绍.md`、`Obsidian/notes/1、Obsidian安装与配置.md`、`Obsidian/notes/2、Obsidian Web Clipper.md`。
- 内容重点：LLM Wiki 的价值、三层结构和 Ingest → Query → Lint 闭环；Obsidian 与 Clipper 仅服务于这个叙事主线。
- 不包含：Obsidian 插件安装的逐步屏幕操作、具体 AI 产品选型或团队权限治理细节。

## 叙事方案

采用“闭环优先”而非概念堆叠或工具教学：从团队知识散落、重复研究的问题进入，依次建立 LLM Wiki 的心智模型、展示其架构和维护循环，再把 Obsidian 定位为人类协作界面、把 Web Clipper 定位为原料入口，最后收束为一条小组可立即试行的最小路径。

## 视觉与交互

- 模板：`presenter-mode-reveal`，提供演讲者视图、当前/下一页预览、计时与逐字稿。
- 主题：`obsidian-claude-gradient`，以深色蓝紫渐变呼应 Obsidian 与 AI 协作。
- 输出：独立的静态 HTML deck；键盘支持翻页、总览、全屏和演讲者模式。
- 每页保留 150–300 字中文口语化逐字稿，仅置于隐藏的 `.notes` 区域，不污染观众视图。

## 15 页结构

| 页码 | 页面目的 | 观众可见核心信息 |
| --- | --- | --- |
| 1 | 开场 | 从“知识为什么总在聊天记录里消失？”切入。 |
| 2 | 问题 | 传统文件问答/RAG 的重复理解与无法沉淀。 |
| 3 | 定义 | LLM Wiki = 原始资料 + 持续整理 + 结构化 Markdown Wiki。 |
| 4 | 转变 | LLM 从临时答题者变为长期知识库维护者。 |
| 5 | 架构 | raw、wiki、schema 三层及职责边界。 |
| 6 | 维护闭环 | Ingest → Query → Lint 如何让知识持续演进。 |
| 7 | 导航与演进 | index.md 和 log.md 分别解决“找内容”与“看变化”。 |
| 8 | Obsidian 的角色 | 本地 Markdown、双向链接、关系图谱与 Git 审阅。 |
| 9 | 人机协作入口 | Obsidian CLI/Agent 如何减少结构化操作失误。 |
| 10 | 素材入口 | Web Clipper 把网页正文与元数据保存为 Markdown。 |
| 11 | 剪藏质量 | 模板与变量、图片本地化和 raw 不可变原则。 |
| 12 | 端到端示例 | 一篇文章从网页到 raw、wiki 页面和可引用答案。 |
| 13 | 小组最小实践 | 一套 vault、一个领域、三条操作规则。 |
| 14 | 成功标准 | 可浏览、可追溯、可复用、可持续维护。 |
| 15 | 收束与行动 | 本周可完成的第一个 ingest 与后续讨论。 |

## 验收与验证

1. 15 张幻灯片均可通过左右方向键与 URL 深链访问。
2. 所有页面可见内容只面向听众；逐字稿只出现在 `.notes`。
3. 每页渲染为 PNG 后不存在文字溢出、遮挡或低对比度。
4. 叙事中 LLM Wiki 占主要篇幅，Obsidian 与 Clipper 作为支撑环节出现。
5. 演讲者模式可从观众页面以 `S` 键打开。

## 风险与处理

- 30 分钟内内容可能偏密：每页只保留一个结论，安装界面细节移入逐字稿或会后资料。
- 参考笔记含截图：演示不直接依赖截图，以结构图、流程图和简洁示意替代，避免画面碎片化。
- 本地浏览器环境差异：交付前用 headless Chrome 逐页渲染验证。
