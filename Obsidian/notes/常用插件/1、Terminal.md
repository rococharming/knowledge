---
title: Terminal 插件
date: 2026-07-13
tags: [Obsidian, Obsidian插件, 插件, Terminal]
aliases:
  - Obsidian Terminal
  - Terminal 插件
  - Terminal
---

# 一、概述

Terminal 是一个 Obsidian 社区插件，用于在 Obsidian 内部打开终端面板。它适合在不离开 Obsidian 的情况下执行 shell 命令、运行脚本、调用 AI Agent 或处理当前仓库里的 Markdown 文件。

如果已经习惯在外部终端中操作 Obsidian 仓库，Terminal 插件并不是必需品。它的价值在于把“阅读笔记”和“执行命令”放到同一个工作空间里，减少在 Obsidian、终端和 AI Agent 应用之间来回切换。

在 AI 工作流中，Terminal 插件常和 [[Obsidian/notes/6、Obsidian CLI|Obsidian CLI]]、Claude Code、Codex 等命令行工具配合使用。它提供的是终端入口，真正执行仓库操作的仍然是 shell 命令、CLI 工具或 Agent。

# 二、安装 Terminal 插件

## 1、开启社区插件

Terminal 属于社区插件，因此需要先开启 Obsidian 的社区插件功能。进入 **设置 -> 第三方插件**，关闭安全模式。

关闭安全模式后，进入社区插件市场，点击浏览。

## 2、搜索并安装

在社区插件市场中搜索 `Terminal`。

![[assets/Pasted image 20260622003725.png|600]]

打开插件详情页后，点击安装。

![[assets/Pasted image 20260622003738.png|600]]

安装完成后，点击启用。

![[assets/Pasted image 20260622003754.png|600]]

启用后，Obsidian 左侧功能区会出现 `Terminal` 图标。

![[assets/Pasted image 20260713015649.png|200]]

# 三、打开内嵌终端

## 1、选择打开方式

点击左侧功能区的 `Terminal` 图标后，会出现终端打开方式选择界面。

![[assets/Pasted image 20260622003840.png|600]]

如果目标是在 Obsidian 内部直接使用终端，应选择 **整合式**。整合式会把终端作为 Obsidian 内部面板打开，而不是额外弹出独立窗口。

![[assets/Pasted image 20260622003919.png|600]]

打开后，窗口下方会出现终端面板。默认情况下，它会使用系统配置的 shell，例如 macOS 上常见的 `zsh`。

## 2、适合使用整合式的场景

整合式终端适合这些任务：

- **快速运行命令**：例如查看当前目录、执行 Git 状态检查或运行本地脚本。
- **操作当前仓库**：例如配合 `rg` 搜索笔记内容，或执行 Markdown 批量处理命令。
- **调用 AI Agent**：例如在 Obsidian 内部启动命令行 Agent，让它读取和修改当前仓库。
- **验证工具输出**：例如运行 [[Obsidian/notes/6、Obsidian CLI|Obsidian CLI]] 命令后直接查看结果。

> 注意：Terminal 插件只是把系统终端嵌入 Obsidian。命令能否运行，仍然取决于本机是否已经安装对应工具，以及 shell 环境变量是否配置正确。

# 四、配置默认终端

## 1、进入插件设置

如果希望以后点击 Terminal 图标时直接打开整合式终端，可以进入 **设置 -> 第三方插件 -> 已安装插件**，找到 `Terminal` 插件。

![[assets/Pasted image 20260622004001.png|600]]

点击插件设置。

![[assets/Pasted image 20260622004020.png|600]]

在默认设置中选择 **整合式**，这样后续打开插件时会默认使用内嵌终端。

## 2、编辑整合式配置

在 **配置** 中找到整合式对应的配置，点击编辑。

![[assets/Pasted image 20260622004041.png|300]]

这里可以修改终端使用的 shell、启动目录和其他运行选项。常见需求是把默认 shell 从系统默认值改成自己常用的 shell。

## 3、切换到 fish shell

例如想使用 `fish` shell，可以把 shell 配置改为 `fish` 可执行文件的路径。

![[assets/Pasted image 20260622004129.png|400]]

设置完成后，再从左侧功能区点击 `Terminal` 按钮，就可以直接打开 `fish shell`。

# 五、小结

Terminal 插件把系统终端嵌入 Obsidian，使用户可以在阅读和管理笔记时直接运行命令。它特别适合 AI Agent、Obsidian CLI、Git 和本地脚本等工作流，但它本质上仍然是终端入口。

更完整的插件安装、启用和选择原则，可以参考 [[Obsidian/notes/3、Obsidian 插件|Obsidian 插件]]；如果重点是让 AI 通过 Obsidian 官方接口操作仓库，则继续阅读 [[Obsidian/notes/6、Obsidian CLI|Obsidian CLI]]。
