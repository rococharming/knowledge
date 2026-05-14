---
title: Claude Code
date: 2026-05-14
tags: [coding-tool, agent]
source_count: 1
---

# Claude Code

**Claude Code** 是 Anthropic 推出的 AI 代码工具，能够在终端或 IDE 中理解代码库、编辑文件、执行命令，并与开发工具协同工作。

## 核心能力

- **代码理解**：读取和分析项目代码库结构
- **文件编辑**：自动创建、修改、删除文件
- **命令执行**：在终端执行 shell 命令
- **自然语言交互**：通过对话完成代码阅读、开发、调试、重构、测试等任务

## 安装

以 macOS 为例，在终端执行：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

安装后验证：

```bash
claude --version
```

手动更新：

```bash
claude update
```

## 基本使用

### 启动会话

```bash
cd path/to/project
claude
```

### 常用 Slash Commands

| 命令 | 别名 | 作用 |
|---|---|---|
| `/usage` | `/cost` | 查看当前会话成本和用量概览 |
| `/doctor` | — | 诊断安装、配置和环境问题 |
| `/status` | — | 查看环境状态（版本、模型、连接等） |
| `/clear` | `/new`, `/reset` | 清空当前上下文，开始新对话 |
| `/compact` | — | 压缩历史上下文，腾出空间 |
| `/model` | — | 切换当前会话使用的模型 |
| `/effort` | — | 切换 effort level（适用于支持的模型） |
| `/resume` | `/continue` | 恢复或切换到之前的会话 |
| `/exit` | `/quit` | 退出会话 |

### /usage 输出说明

- **Total cost**：会话的本地估算费用（接入第三方模型时不准确）
- **Total duration (API)**：API 调用累计耗时
- **Total duration (wall)**：会话经过的现实时间
- **Total code changes**：会话跟踪到的变更行数
- **Usage by model**：按模型统计 input、output、cache read、cache write

### 会话管理技巧

- `/clear` 适合任务边界切换，但不会删除旧会话，后续仍可通过 `/resume` 恢复
- `/compact [instructions]` 可在长任务中压缩上下文，保留重点信息
- 使用 `/rename` 为会话命名，便于后续通过名称识别和恢复

## 权限模式

详见 [[Claude Code 权限模式]]。支持四种模式：

- `default`：保守模式，编辑和执行前逐一确认
- `acceptEdits`：自动批准工作目录内的文件编辑和常见文件系统命令
- `plan`：只读分析模式，出方案但不动代码
- `bypassPermissions`：跳过权限检查，风险最高

按 `Shift + Tab` 在模式间循环切换。

## 实用快捷键

| 快捷键 | 功能 |
|---|---|
| `!` | 进入 Bash 执行命令 |
| `Option + Shift` | 换行（macOS） |
| `Ctrl + G` | 打开默认编辑器编辑对话内容 |
| `Ctrl + O` | 查看 compact 压缩详情 |
| `Shift + Tab` | 切换权限模式 |

## 模型配置

Claude Code 默认调用 Anthropic 官方接口，但可通过配置 `base URL + auth + model` 映射接入国内第三方模型。详见 [[Claude Code 安装与配置]]。

> 注意：接入第三方模型时，界面中显示的 `Sonnet`、`Opus`、`Haiku` 等名称只是档位标识，实际请求会被转发到配置的第三方模型。

## 来源

- [[Claude Code入门]]
