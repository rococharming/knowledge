---
title: Claude Code 入门
date: 2026-05-14
tags: [coding-tool, agent, workflow]
source_count: 1
---

# Claude Code 入门

本文是 Anthropic 推出的 AI 代码工具 **Claude Code** 的入门指南，涵盖安装、第三方模型接入、基本命令、权限模式和简单实战。

## 核心内容

### 1. 工具定位

Claude Code 是一款基于终端/IDE 的 AI 编程助手，能够理解代码库、编辑文件、执行命令，并通过自然语言交互完成代码阅读、开发、调试、重构和测试等任务。它建立在 Claude 模型之上，但支持通过配置接入国内第三方模型。

### 2. 安装与配置

支持 macOS 原生安装（`curl | bash`），也支持手动更新（`claude update`）。由于官方接口需要国外手机号且存在封号风险，更推荐通过配置 `base URL + auth + model` 映射接入国内第三方模型（MiniMax、Kimi、DeepSeek）。详见 [[Claude Code 安装与配置]]。

### 3. 基本命令

Claude Code 提供丰富的 Slash Command 用于会话管理：

| 命令 | 作用 |
|---|---|
| `/usage` | 查看当前会话成本与用量概览 |
| `/doctor` | 诊断安装、配置和环境问题 |
| `/status` | 查看当前环境状态（版本、模型、连接等） |
| `/clear` | 清空当前上下文，开始新对话 |
| `/compact` | 压缩历史上下文，腾出空间 |
| `/model` | 切换当前会话使用的模型 |
| `/resume` | 恢复或切换到之前的会话 |
| `/exit` | 退出会话 |

详见 [[Claude Code]] 实体页面的基本使用部分。

### 4. 权限模式

Claude Code 提供四种 [[Claude Code 权限模式|权限模式]] 控制自主程度：

- `default`：最保守，编辑/执行前逐一确认
- `acceptEdits`：自动批准工作目录内的文件编辑和常见文件系统命令
- `plan`：只读分析模式，不出方案不动代码
- `bypassPermissions`（Yolo 模式）：跳过权限检查，直接执行，风险最大

### 5. 核心机制：Prompt Caching

Claude Code 在每次请求中会发送大量上下文（系统提示词、CLAUDE.md、Skill 描述、历史对话等）。Prompt Caching 将这些稳定上下文写入缓存，后续请求命中时可大幅降低费用（cache read 约为普通 input 的 10%）。

### 6. 实战示例

素材中包含一个完整实战：通过 `plan` 模式设计需求和技术方案，再让 Claude Code 自动执行，最终实现一个 HTML + CSS + JavaScript 的网页版 TodoList 应用。

## 关键要点

- 接入第三方模型时，`Sonnet`/`Opus`/`Haiku` 等档位名称只是界面显示，实际请求会被映射到配置的第三方模型
- 按 `Shift + Tab` 可在权限模式间循环切换
- 按 `Ctrl + G` 可打开默认编辑器编辑对话内容
- 对话框支持直接拖入图片

## 来源

- [[Claude Code入门]]
