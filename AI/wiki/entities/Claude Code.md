---
title: Claude Code
date: 2026-07-17
tags: [llm, agent, coding-tool]
source_count: 1
---

# Claude Code

Claude Code 是 Anthropic 推出的 AI 编程工具，可在终端或 IDE 中理解代码库、编辑文件、执行命令，并与本地开发工具协同工作。它适合用于代码阅读、开发、调试、重构、测试和项目内问答等任务。

Claude Code 的能力建立在 Claude 模型之上，但也可以通过配置 Anthropic 兼容接口接入第三方模型。第三方接入的关键是配置 `ANTHROPIC_BASE_URL`、密钥变量和模型别名映射，具体流程见 [[Claude Code 第三方模型接入]]。

## 安装与更新

macOS 原生安装方式：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

安装完成后可检查版本：

```bash
claude --version
```

原生安装方式支持后台自动更新。若配置了 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`，自动更新会被关闭。也可以手动执行：

```bash
claude update
```

## 基本使用入口

进入项目目录后运行：

```bash
claude
```

进入会话后，可以使用 `/` 开头的 slash command 操作当前会话，例如查看状态、切换模型、压缩上下文、恢复历史会话等。常用命令见 [[Claude Code 常用命令]]。

## 权限控制

Claude Code 的工作方式受 Permission Mode 影响。常见模式包括 `default`、`acceptEdits`、`plan` 和 `bypassPermissions`，分别对应不同的读写权限与确认策略。更详细的使用场景见 [[Claude Code 权限模式]]。

## 入门实践

一种稳妥的入门方式是先在 `plan` 模式中让 Claude Code 产出需求和技术方案，确认后再切换到可编辑模式执行。例如先让它规划一个 HTML、CSS、JavaScript 实现的 todo 应用，再根据计划逐步落地。

## 相关页面

- [[Claude Code 第三方模型接入]]
- [[Claude Code 常用命令]]
- [[Claude Code 权限模式]]
- [[Claude Code 入门指南]]
- [[Claude Code 入门实战流程]]

## 来源

- [[Claude Code入门]]
