---
title: Claude Code 入门指南
date: 2026-07-17
tags: [llm, coding-tool, workflow]
source_count: 1
---

# Claude Code 入门指南

这篇素材是一份 Claude Code 入门教程，覆盖工具定位、安装、第三方模型配置、常用命令、权限模式和一个 todo 应用实战。它适合作为 [[Claude Code]] 的来源级入口。

## 核心内容

1. Claude Code 是 Anthropic 推出的 AI 编程工具，能在终端或 IDE 中理解代码库、编辑文件、执行命令，并辅助开发者完成阅读、开发、调试、重构和测试。
2. macOS 可通过官方安装脚本安装，并使用 `claude --version` 验证安装结果。
3. Claude Code 可通过 Anthropic 兼容接口接入第三方模型，关键是配置 `ANTHROPIC_BASE_URL`、密钥变量和模型别名映射。
4. 日常会话依赖 `/usage`、`/doctor`、`/status`、`/clear`、`/compact`、`/model`、`/resume` 等命令完成状态查看、上下文管理、模型切换和历史恢复。
5. Permission Mode 决定 Claude Code 是否在编辑、命令执行或网络请求前询问用户，常见模式包括 `default`、`acceptEdits`、`plan` 和 `bypassPermissions`。
6. 入门实战建议先用 plan 模式生成方案，再确认需求并执行实现。

## 拆分页面

- [[Claude Code]]：工具定位、安装、基础入口和相关页面。
- [[Claude Code 第三方模型接入]]：第三方模型配置变量、密钥形式、平台示例和操作流程。
- [[Claude Code 常用命令]]：slash command、上下文管理、模型切换和输入技巧。
- [[Claude Code 权限模式]]：Permission Mode 的类型、风险和选择建议。

## 来源价值

素材按“安装 -> 配置 -> 使用 -> 权限 -> 实战”的顺序组织，保留 summary 页面有助于按原教程顺序回读。教程型连续截图不在概念页中机械继承，其中第三方模型接入截图保留在 [[Claude Code 第三方模型接入]]，todo 应用实战截图保留在 [[Claude Code 入门实战流程]]。

## 来源

- [[Claude Code入门]]
