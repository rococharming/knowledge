---
title: ChatGPT App 基本组成
date: 2026-07-30
tags:
  - AI
  - ChatGPT
  - ChatGPT-App
aliases:
  - ChatGPT App界面
  - ChatGPT App组成
---

# 一、整体界面

ChatGPT App 的界面主要分为四个部分：

| 区域 | 主要用途 |
|---|---|
| 产品选择器 | 在 ChatGPT 和 Codex 工作区之间切换 |
| 侧边栏 | 新建、查找和组织项目、对话及功能入口 |
| 主工作区 | 显示对话、任务过程和生成结果 |
| 输入区 | 描述任务、提供上下文并选择执行方式 |


![[assets/Pasted image 20260730181124.png|600]]

界面中出现的入口会受到操作系统、客户端版本、账号套餐和工作区策略影响，因此实际显示内容可能略有不同。

除了上述四个主要部分，App 还提供两个按需展开的辅助区域：

- **右侧边栏**：辅助工具的统一入口，可以打开 **Review**、**Terminal**、**Browser**、**Files** 和 **Side chat** 等面板。在不离开当前主任务的情况下，可以审阅变更、运行命令、浏览网页、查看文件或发起侧边对话；不同工作模式下可用的入口可能不同。
- **底部栏（Bottom Panel）**：用于承载终端等辅助工具。Codex 的集成终端会继承当前 Project 或 Worktree 的工作目录，可在这里运行命令、查看构建和测试输出，并让 ChatGPT 读取终端结果继续分析。

![[assets/Pasted image 20260730183633.png|600]]

右侧边栏和底部栏都不是固定显示的主区域，可以根据任务需要打开、调整大小或隐藏，避免挤占主工作区。

## 1、产品选择器

左上角的产品选择器用于切换 **ChatGPT** 和 **Codex**：

- **ChatGPT** 工作区包含 Chat 和 Work，适合对话、研究、分析和创建交付物。
- **Codex** 工作区面向软件开发，提供代码库、终端、Git、Diff 和代码审查等开发能力。

Chat 和 Work 的对话显示在 ChatGPT 工作区中：

![[assets/Pasted image 20260730181249.png|600]]

Codex 对话及开发项目保留在 Codex 工作区中。

![[assets/Pasted image 20260730181406.png|600]]

处于 Codex 工作区时，可以点击 **New chat** 右侧的 `Quick chat` 图标快速发起普通 ChatGPT 对话。

![[assets/Pasted image 20260730181503.png|600]]

`Quick chat`可用于快速提问。

![[assets/Pasted image 20260730181525.png|600]]

## 2、侧边栏

侧边栏用于进入主要功能和管理最近的工作。以 Codex 工作区为例，通常可以看到：

- **New chat**：新建对话
- **Pull requests**：查看和处理 Pull Request
- **Sites**：查看创建的网站
- **Scheduled**：管理定时任务及其运行结果
- **Plugins**：浏览和管理插件
- **Projects**：查看 ChatGPT Project 和本地 Project
- **Recents**：继续最近的对话

Project 和 Chat 都可以固定、重命名或归档。固定只会改变它们在侧边栏中的显示位置，不会增加 ChatGPT 可以访问的上下文。

## 3、主工作区

主工作区用于显示当前对话、任务过程和结果。根据任务类型，它可能包含：

- 用户消息和 ChatGPT 回复
- 计划、进度和工具调用
- 权限确认或待回答的问题
- 文件、图片、网页或交付物预览
- 代码 Diff、终端输出和测试结果
- 长期任务或子任务状态


## 4、输入区

输入区用于描述任务、补充上下文并设置本次任务的执行方式。

以 Codex 输入区为例，底部控件从左到右分别是：

![[assets/Pasted image 20260730183947.png|600]]

- `+`：附加文件、图片或当前模式支持的其他上下文。
- 手掌图标：查看或调整权限模式，决定哪些操作可以直接执行，哪些操作需要先确认。
- 模型名称与推理强度：选择本次任务使用的模型及思考级别。可用选项会随账号和产品更新而变化。
- 麦克风：使用语音输入提示词。
- 向上箭头：发送任务。


# 二、对话与项目

Chat 是一次独立工作的记录，Project 则用于组织一组相关 Chat 及其共享上下文。当前 ChatGPT App 的 Project 视图同时包含 ChatGPT Project 和连接本地文件夹的本地 Project。

## 1、独立 Chat

任务不依赖共享文件、指令或本地目录时，可以直接选择 **New chat**。此时 该 Chat 会和 ChatGPT 网页端的 Chat 一起出现在`Recents`下：

![[assets/Pasted image 20260730184405.png|600]]

适合的场景包括：

- 临时提问或解释概念
- 改写一段文字
- 比较几个方案
- 完成一次性的小任务

## 2、ChatGPT Project

ChatGPT Project 用于让多次对话共享一组资料和规则，可以包含：

- Chat 和 Work 对话
- 上传的文件
- 连接的外部来源
- 项目级指令

同一个 Project 中可以为不同结果分别创建 Chat，例如把资料收集、报告起草和内容审阅拆成三个 Chat，避免所有内容堆在一条对话中。

## 3、本地 Project

需要读取或修改电脑中的文件时，可以创建本地 Project 并关联文件夹。

本地 Project 不局限于单个文件夹：

- 一个 Project 可以添加多个相关文件夹。
- 主文件夹是新 Chat 的默认工作目录。
- Codex 在主文件夹中执行 Git 操作，并自动发现 `AGENTS.md`、Skill 和 `config.toml`等。
- 其他文件夹仍可用于搜索、读取和编辑，但不会自动参与上述项目配置发现。

例如，一个 Project 可以同时关联前端、后端和文档目录；不相关或权限边界不同的工作则应拆成不同 Project。

选中某个本地 `Project`，选择**Edit project**：

![[assets/Pasted image 20260730184734.png]]

可以增加其他文件夹：

![[assets/Pasted image 20260730184908.png|400]]

增加其他文件夹后，还可以选择哪一个作为主文件夹。

Project 负责组织工作，实际能否读取、修改文件或访问网络，仍由权限模式和沙盒共同决定。

## 4、管理 Chat 与 Project

常见管理动作包括：

- **Pin**：把常用 Chat 或 Project 固定在侧边栏顶部
- **Rename**：用结果导向的名称重命名任务
- **Search**：按标题、对话内容或 Git 分支查找历史 Chat
- **Archive**：收起已经结束但仍需保留的对话

被归档的对话可以在 **Settings > Archived chats** 中恢复。

# 三、扩展能力入口

## 1、Plugins 与 Skills

Plugins 把可复用的工作流和外部能力安装到 ChatGPT 或 Codex 中。一个 Plugin 可以包含 Skill、Connector、MCP Server、浏览器扩展、Hook 或定时任务模板。

在桌面 App 中，可以在 Work 或 Codex 工作区打开 **Plugins**：

![[assets/Pasted image 20260730185251.png|600]]

在顶部有**Plugins**和**Skills**切换按钮。

对于**Plugins**，可以：

1. 浏览或搜索 Plugin。
2. 查看它包含的能力和需要的权限。
3. 安装并完成必要的外部服务授权。
4. 新建 Chat 后描述任务，或在输入区显式选择对应 Plugin 或 Skill。

安装 Plugin 不代表它拥有无限权限。外部服务仍使用各自的账号授权；本地工具仍受到当前沙盒和审批策略限制。

## 2、Scheduled

Scheduled 用于查看定时任务、最近运行结果以及需要处理的异常。定时任务可以：

- 在指定时间或周期运行
- 回到已有 Chat 继续工作
- 每次创建独立运行记录
- 使用 Project、Skill 或 Plugin
- 在 Git Project 中选择本地目录或独立 Worktree

需要本地文件的定时任务运行时，电脑必须开机、ChatGPT App 必须保持运行，并且相关 Project 仍可访问。

MCP、Hook 和 Plugin 可以为任务提供工具或流程，但它们本身不等于定时任务。定时与运行记录统一由 Scheduled 管理。

# 四、设置与快捷操作

## 1、Settings

