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

ChatGPT App 的界面可以分为四个部分：

| 区域 | 主要用途 |
|---|---|
| 产品选择器 | 在 ChatGPT 和 Codex 工作区之间切换 |
| 侧边栏 | 新建、查找和组织项目、对话及功能入口 |
| 主工作区 | 显示对话、任务过程和生成结果 |
| 输入区 | 描述任务、提供上下文并选择执行方式 |

![[assets/Pasted image 20260730180007.png|800]]

界面中出现的入口会受到操作系统、客户端版本、账号套餐和工作区策略影响，因此实际显示内容可能略有不同。

## 1、产品选择器

左上角的产品选择器用于切换 **ChatGPT** 和 **Codex**：

- **ChatGPT** 工作区包含 Chat 和 Work，适合对话、研究、分析和创建交付物。
- **Codex** 工作区面向软件开发，提供代码库、终端、Git、Diff 和代码审查等开发能力。

Chat 和 Work 的对话显示在 ChatGPT 工作区中；Codex 对话及开发项目保留在 Codex 工作区中。处于 Codex 工作区时，可以点击 **New chat** 右侧的 `Quick chat` 图标快速发起普通 ChatGPT 对话。

> [!todo] 待补截图
> 分别截取 ChatGPT 和 Codex 工作区，标出产品选择器以及 Chat / Work 切换位置。

## 2、侧边栏

侧边栏用于进入主要功能和管理最近的工作。以 Codex 工作区为例，通常可以看到：

- **New chat**：新建对话
- **Pull requests**：查看和处理 Pull Request
- **Sites**：查看创建的网站
- **Scheduled**：管理定时任务及其运行结果
- **Plugins**：浏览和管理插件
- **Projects**：查看 ChatGPT Project 和本地 Project
- **Recents**：继续最近的对话

Project 和 Chat 都可以固定、重命名或归档。固定只会改变它们在侧边栏中的显示位置，不会增加 ChatGPT 可以访问的上下文。搜索与归档的具体方法参考 [[4、对话与 Projects]]。

## 3、主工作区

主工作区用于显示当前对话、任务过程和结果。根据任务类型，它可能包含：

- 用户消息和 ChatGPT 回复
- 计划、进度和工具调用
- 权限确认或待回答的问题
- 文件、图片、网页或交付物预览
- 代码 Diff、终端输出和测试结果
- 长期任务或子任务状态

右侧或底部面板会按需出现。例如，Codex 修改代码后可以打开 Review Pane 检查 Diff；Work 创建文档或演示文稿后，可以在预览区检查结果。它们不是每次对话都会同时显示。

## 4、输入区

输入区不仅用于输入文字，还用于确定本次任务的上下文和执行方式。根据当前工作区和功能权限，可能包含：

- 附加文件、图片或其他上下文
- 选择当前 Project 或本地目录
- 选择 Chat、Work 或 Codex
- 选择本地或云端执行
- 选择模型和推理强度
- 选择权限模式
- 调用 Plugin、Skill 或其他工具
- 使用语音输入

不同模式不会显示完全相同的控件。例如，Work 可以选择 `Work locally` 或 `Cloud`；Codex 会显示开发相关的权限、目录和模型设置。

> 不要把模型选择当作输入区最重要的功能。明确目标、提供正确上下文并选择合适的工作方式，通常比频繁切换模型更重要。

# 二、对话与项目

Chat 是一次独立工作的记录，Project 则用于组织一组相关 Chat 及其共享上下文。当前 ChatGPT App 的 [Projects](https://learn.chatgpt.com/docs/projects) 视图同时包含 ChatGPT Project 和连接本地文件夹的本地 Project。

## 1、独立 Chat

任务不依赖共享文件、指令或本地目录时，可以直接选择 **New chat**。

适合的场景包括：

- 临时提问或解释概念
- 改写一段文字
- 比较几个方案
- 完成一次性的小任务

每个 Chat 保留自己的消息和任务结果。一个 Chat 中提供的临时文件或说明，不会自动成为其他 Chat 的上下文。

## 2、ChatGPT Project

ChatGPT Project 用于让多次对话共享一组资料和规则，可以包含：

- Chat 和 Work 对话
- 上传的文件
- 连接的外部来源
- 项目级指令

同一个 Project 中可以为不同结果分别创建 Chat，例如把资料收集、报告起草和内容审阅拆成三个 Chat，避免所有内容堆在一条对话中。

## 3、本地 Project

需要读取或修改电脑中的文件时，可以创建本地 Project 并关联文件夹。

本地 Project 不再局限于单个文件夹：

- 一个 Project 可以添加多个相关文件夹。
- 主文件夹是新 Chat 的默认工作目录。
- Codex 在主文件夹中执行 Git 操作，并自动发现 `AGENTS.md`、Skill 和 `config.toml`。
- 其他文件夹仍可用于搜索、读取和编辑，但不会自动参与上述项目配置发现。

例如，一个 Project 可以同时关联前端、后端和文档目录；不相关或权限边界不同的工作则应拆成不同 Project。

Project 负责组织工作，实际能否读取、修改文件或访问网络，仍由权限模式和沙盒共同决定。

## 4、管理 Chat 与 Project

常见管理动作包括：

- **Pin**：把常用 Chat 或 Project 固定在侧边栏顶部
- **Rename**：用结果导向的名称描述任务
- **Search**：按标题、对话内容或 Git 分支查找历史 Chat
- **Archive**：收起已经结束但仍需保留的对话

被归档的对话可以在 **Settings > Archived chats** 中恢复。

# 三、扩展能力入口

## 1、Plugins 与 Skills

[Plugin](https://learn.chatgpt.com/docs/plugins) 把可复用的工作流和外部能力安装到 ChatGPT 或 Codex 中。一个 Plugin 可以包含 Skill、Connector、MCP Server、浏览器扩展、Hook 或定时任务模板。

在桌面 App 中，可以在 Work 或 Codex 工作区打开 **Plugins**：

1. 浏览或搜索 Plugin。
2. 查看它包含的能力和需要的权限。
3. 安装并完成必要的外部服务授权。
4. 新建 Chat 后描述任务，或在输入区显式选择对应 Plugin 或 Skill。

安装 Plugin 不代表它拥有无限权限。外部服务仍使用各自的账号授权；本地工具仍受到当前沙盒和审批策略限制。详细用法参考 [[9、Plugins 与外部服务]]。

## 2、Scheduled

[Scheduled](https://learn.chatgpt.com/docs/automations) 用于查看定时任务、最近运行结果以及需要处理的异常。定时任务可以：

- 在指定时间或周期运行
- 回到已有 Chat 继续工作
- 每次创建独立运行记录
- 使用 Project、Skill 或 Plugin
- 在 Git Project 中选择本地目录或独立 Worktree

需要本地文件的定时任务运行时，电脑必须开机、ChatGPT App 必须保持运行，并且相关 Project 仍可访问。

MCP、Hook 和 Plugin 可以为任务提供工具或流程，但它们本身不等于定时任务。定时与运行记录统一由 Scheduled 管理。详细用法参考 [[11、长期任务与自动化]]。

# 四、设置与快捷操作

## 1、Settings

按 <kbd>Cmd</kbd> + <kbd>,</kbd>（macOS）或 <kbd>Ctrl</kbd> + <kbd>,</kbd>（Windows）打开 Settings。

首次使用时可以重点检查：

- **General**：多行提示发送方式、任务运行时防止电脑休眠、后续消息行为
- **Keyboard Shortcuts**：搜索、修改或恢复快捷键
- **Notifications**：任务完成、权限确认和问题提醒
- **Appearance**：主题、颜色和字体
- **Browser**：内置浏览器、Chrome 扩展和网站权限
- **Computer Use**：桌面应用访问权限
- **Personalization**：Personality、Custom Instructions 和 Memories
- **Archived chats**：恢复归档对话

Codex 还提供 Git、环境、Worktree、MCP Server 和配置文件等开发设置。首次使用时不需要逐项修改，遇到明确需求后再调整。权限与故障排查参考 [[12、权限、设置与故障排查]]。

## 2、常用快捷键

以下快捷键在 macOS 使用 <kbd>Cmd</kbd>，在 Windows 使用 <kbd>Ctrl</kbd>：

| 操作 | macOS | Windows |
|---|---|---|
| 打开命令菜单 | <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> | <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> |
| 打开 Settings | <kbd>Cmd</kbd> + <kbd>,</kbd> | <kbd>Ctrl</kbd> + <kbd>,</kbd> |
| 新建 Chat | <kbd>Cmd</kbd> + <kbd>N</kbd> | <kbd>Ctrl</kbd> + <kbd>N</kbd> |
| 打开 Quick chat | <kbd>Cmd</kbd> + <kbd>Option</kbd> + <kbd>N</kbd> | <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>N</kbd> |
| 搜索 Chat | <kbd>Cmd</kbd> + <kbd>G</kbd> | <kbd>Ctrl</kbd> + <kbd>G</kbd> |
| 当前 Chat 内查找 | <kbd>Cmd</kbd> + <kbd>F</kbd> | <kbd>Ctrl</kbd> + <kbd>F</kbd> |
| 打开文件夹 | <kbd>Cmd</kbd> + <kbd>O</kbd> | <kbd>Ctrl</kbd> + <kbd>O</kbd> |
| 显示或隐藏侧边栏 | <kbd>Cmd</kbd> + <kbd>B</kbd> | <kbd>Ctrl</kbd> + <kbd>B</kbd> |
| 打开快捷键列表 | <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>/</kbd> | <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>/</kbd> |

快捷键可能与系统或其他软件冲突，可以在 **Settings > Keyboard Shortcuts** 中搜索、修改或恢复。
