---
title: 对话与 Projects
date: 2026-07-30
tags: [AI, ChatGPT, Project]
aliases:
  - ChatGPT Projects
  - ChatGPT项目
---

# 一、组织单位

ChatGPT App 使用 Chat 和 Project 组织工作：

- **Chat** 保存一次任务的消息、工具活动和结果。
- **Project** 把多个相关 Chat、文件、来源和指令放到一起。

Project 的作用不是让一个 Chat 无限变长，而是让多个目标明确的 Chat 共享同一组稳定背景。

| 工作情况 | 推荐组织方式 |
|---|---|
| 一次性问题，不依赖共享资料 | 独立 Chat |
| 同一主题需要多次对话和多个成果 | ChatGPT Project |
| ChatGPT 需要直接操作电脑中的文件夹 | 本地 Project |

# 二、独立 Chat

独立 Chat 适合边界清楚、完成后不需要长期复用上下文的任务，例如：

- 解释一个概念
- 改写一封邮件
- 查询一次最新信息
- 总结单个附件

从 Home 选择 **New chat** 即可开始。任务逐渐扩大后，可以把它移入 Project，再为不同成果拆分新的 Chat。

> 一个 Chat 最好围绕一个明确结果展开。如果调研、写作、审查和后续维护都混在同一条长对话中，历史上下文会逐渐变得难以管理。

# 三、ChatGPT Project

## 1、共享内容

ChatGPT Project 适合长期知识工作。它通常包含：

- **Chats**：属于该 Project 的对话。
- **Sources**：上传文件和已连接的资料来源。
- **Project Instructions**：对 Project 内所有 Chat 生效的指令。

同一个 Project 可以同时包含 Chat 和 Work 对话。新 Chat 会使用 Project 中共享的文件、来源和指令。

ChatGPT Project 不会自动获得电脑文件夹的直接访问权。需要通过上传文件、添加来源或安装 Plugin 提供资料。

## 2、拆分 Chat

Project 负责共享背景，Chat 负责一个具体成果。

以“AI 编程工具调研”为例，可以拆成：

- `收集产品能力`
- `比较 Claude Code 与 Codex`
- `生成汇报 PPT`
- `审查事实和引用`
- `整理后续行动`

这些 Chat 使用同一组资料和 Project Instructions，但每条对话的目标保持独立。

## 3、项目指令

Project Instructions 适合保存该项目长期有效的要求，例如：

```text
默认使用中文。
所有产品能力以官方文档为准。
区分已经发布的功能与设计中的功能。
生成报告时先给结论，再给证据。
```

一次性要求仍应写在当前 Chat 中，不要把临时任务塞进 Project Instructions。

# 四、本地 Project

## 1、本地目录

本地 Project 将一个或多个电脑文件夹附加到 Project。ChatGPT 可以在权限允许的范围内搜索、读取和修改这些文件。

适合的场景包括：

- 软件代码库
- 本地文档仓库
- 一组需要批量整理的素材
- 前端项目与后端项目共同组成的工作区

通过 Project 菜单中的 **Edit project** 可以添加文件夹，并指定 Primary Folder。

## 2、主目录

Primary Folder 是新 Chat 默认使用的工作目录。Codex 还会从这里自动发现：

- Git 仓库
- `AGENTS.md`
- Skills
- `.codex/config.toml`
- 本地环境配置

Secondary Folder 仍然可以用于搜索、读取和编辑，但不会作为 Git 操作和配置发现的默认根目录。

如果两个文件夹属于完全无关的任务，应创建不同 Project，避免扩大不必要的文件访问范围。

## 3、权限边界

Project 和文件夹决定 ChatGPT **从哪里工作**，Sandbox 和 Permission Mode 决定它 **实际能够做什么**。

即使文件夹已经附加，访问工作区外的文件、使用网络或执行高权限操作仍可能需要审批。相关规则参考 [[12、权限、设置与故障排查|权限、设置与故障排查]]。

# 五、管理方式

## 1、固定与命名

- Pin Project：把常用 Project 固定在侧边栏上方。
- Pin Chat：固定经常返回的 Chat。
- Rename Chat：用结果命名，例如“Q3 发布计划”或“登录页无障碍审查”。

固定只改变显示位置，不会改变上下文或权限。

## 2、搜索

使用 <kbd>Cmd</kbd> / <kbd>Ctrl</kbd> + <kbd>G</kbd> 搜索历史 Chat；打开 Chat 后，使用 <kbd>Cmd</kbd> / <kbd>Ctrl</kbd> + <kbd>F</kbd> 在当前对话中查找文字。

## 3、归档

任务结束后可以 Archive Chat，让活动区域保持清晰。已归档对话可以从 Settings 中恢复。

归档不同于删除：归档只是把 Chat 移出日常列表；删除则会移除内容，执行前应确认是否仍需保留。

# 六、实践

下面用“桌面端 AI 工具调研”建立知识工作 Project：

1. 新建 ChatGPT Project，命名为 `桌面端 AI 工具调研`。
2. 在 Sources 中加入需要长期复用的官方文档或资料文件。
3. 添加 Project Instructions，声明语言、事实来源和输出风格。
4. 创建 `梳理产品能力` Chat，使用 Chat 收集和讨论信息。
5. 创建 `生成比较报告` Chat，切换到 Work 生成可检查的文件。
6. 创建 `事实审查` Chat，专门检查日期、名称、数字和来源。
7. 将完成的 Chat 归档，保留 Project 供后续更新。

> [!todo] 待补截图
> 截取一个不含敏感信息的 Project，展示 Chats、Sources 与 Project Instructions 的位置。

如果资料只用于一次消息，直接附加到 Chat；如果需要跨多个 Chat 使用，再放入 Project。文件、图片和网页资料的选择方式参考 [[5、资料、搜索与多模态输入|资料、搜索与多模态输入]]。
