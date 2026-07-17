---
title: Claude Code 常用命令
date: 2026-07-17
tags: [coding-tool, workflow]
source_count: 1
---

# Claude Code 常用命令

Claude Code 会话中可以通过 `/` 开头的 slash command 管理上下文、模型、状态和历史会话。这些命令是日常使用 [[Claude Code]] 的主要控制面。

## `/usage`

`/usage` 用于查看当前会话的成本和用量概览，也可以使用别名 `/cost`。

常见字段包括：

- `Total cost`：当前会话的本地估算费用。接入第三方模型时可能不准确。
- `Total duration (API)`：API 调用累计耗时。
- `Total duration (wall)`：会话从开始到现在经过的现实时间。
- `Total code changes`：会话跟踪到的变更行数，不一定等同于完整 `git diff`。
- `Usage by model`：按模型统计 input、output、cache read、cache write。

## `/doctor`

`/doctor` 是自诊断命令，用于检查安装、更新、后台服务、远程控制、MCP、Skills 和版本锁等状态。

它适合在模型连接异常、MCP 不可用、自动更新状态不明确或版本冲突时作为第一轮排查入口。

## `/status`

`/status` 打开设置界面的 Status 页面，用于查看版本、当前模型、账号状态、连接状态、会话名称、会话 ID、`cwd` 和配置来源。

`Setting sources` 能帮助判断当前生效配置来自用户级配置、项目级配置还是其他来源。

## `/clear` 与 `/compact`

`/clear` 用于清空当前上下文并开始新上下文，适合任务边界明确、旧上下文开始干扰新问题或前面探索方向错误时使用。它不会删除旧会话，后续仍可通过 `/resume` 找回。

`/compact` 用于压缩当前会话上下文，适合长任务还没结束但上下文过长时使用。可以附带压缩重点：

```text
/compact 保留数据库结构、接口变更和未完成 TODO
```

## `/model` 与 `/effort`

`/model` 用于切换当前会话模型。不带模型名时打开模型选择器，带模型名时直接切换。

对于支持 effort level 的模型，还可以用 `/effort` 调整推理强度。

## `/resume` 与 `/exit`

`/resume` 用于恢复或切换历史会话，可通过会话 ID、会话名称恢复，也可以不带参数打开会话选择器。`/continue` 是它的别名。

`/exit` 用于退出当前 Claude Code 会话并返回 shell，别名是 `/quit`。

## 输入技巧

- 在对话框中按 <kbd>!</kbd> 可进入 Bash 执行命令。
- macOS 下换行通常是 <kbd>Option</kbd> + <kbd>Enter</kbd>；Windows 下是 <kbd>Shift</kbd> + <kbd>Enter</kbd>。
- 按 <kbd>Ctrl</kbd> + <kbd>G</kbd> 可以打开默认编辑器编辑对话内容。
- 对话框支持图片输入，可拖入图片或用 <kbd>Ctrl</kbd> + <kbd>V</kbd> 粘贴。

## 相关页面

- [[Claude Code]]
- [[Claude Code 权限模式]]
- [[Claude Code 第三方模型接入]]
- [[Claude Code 入门实战流程]]

## 来源

- [[Claude Code入门]]
