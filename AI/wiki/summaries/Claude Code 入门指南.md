---
title: Claude Code 入门指南
date: 2026-07-14
tags: [coding-tool, workflow, agent]
source_count: 1
---

# Claude Code 入门指南

这篇素材介绍了 [[Claude Code]] 的定位、安装方式、第三方模型接入、常用斜杠命令、权限模式和一个简单的实战流程。它适合作为第一次配置和使用 Claude Code 的入口。

## 核心内容

- [[Claude Code]] 是面向终端和 IDE 的 AI 编程工具，可以理解代码库、编辑文件、执行命令，并配合开发工具完成阅读、开发、调试、重构和测试。
- 安装流程以 macOS 为例：使用官方安装脚本安装，执行 `claude --version` 验证，必要时用 `claude update` 手动更新。
- [[Claude Code 第三方模型接入]] 的核心是配置兼容 Anthropic API 的 `BASE_URL`、密钥变量和模型别名映射。
- [[Claude Code 配置第三方模型]] 总结了用户级 `~/.claude/settings.json` 的常见配置结构，以及 MiniMax、Kimi、DeepSeek、智谱 GLM 等平台的接入思路。
- 基本使用围绕 `/usage`、`/doctor`、`/status`、`/clear`、`/compact`、`/model`、`/effort`、`/resume` 和 `/exit` 等命令展开。
- 权限模式用于控制 Claude Code 在编辑文件、执行命令和发起外部访问前是否需要确认，常见模式包括 `default`、`acceptEdits`、`plan` 和高风险的 `bypassPermissions`。

## 使用路径

第一次使用时，可以先按安装、验证、登录或第三方模型配置的顺序完成环境准备；进入项目目录后运行 `claude` 开始会话。熟悉基础命令后，再根据任务风险选择权限模式：探索代码时可用 `plan`，需要高效编辑时可用 `acceptEdits`，不应在不可信项目中轻易使用 `bypassPermissions`。

## 关联页面

- [[Claude Code]]
- [[Claude Code 第三方模型接入]]
- [[Claude Code 配置第三方模型]]

## 来源

- [[Claude Code入门]]
