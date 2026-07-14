---
title: Claude Code
date: 2026-07-14
tags: [coding-tool, agent, workflow]
source_count: 1
---

# Claude Code

Claude Code 是 Anthropic 推出的 AI 编程工具，面向终端、IDE 和代码库工作流。它基于 Claude 模型能力运行，也可以通过兼容 Anthropic API 的网关或第三方平台接入其他模型。

## 定位

Claude Code 的核心价值是把自然语言任务转化为代码库内的实际操作。它可以阅读项目结构、理解上下文、编辑文件、运行命令、执行测试，并在必要时和用户确认风险较高的动作。

## 安装与验证

macOS、Linux 和 WSL 可使用官方安装脚本安装：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

安装后用以下命令验证：

```bash
claude --version
```

更完整的环境检查可以运行：

```bash
claude doctor
```

原生安装通常支持后台自动更新；需要立即更新时可执行：

```bash
claude update
```

## 常用命令

| 命令 | 用途 |
|---|---|
| `/usage` 或 `/cost` | 查看当前会话的费用、耗时和模型用量估算 |
| `/doctor` | 打开诊断检查，查看安装、更新、后台服务、MCP、技能和版本锁等状态 |
| `/status` | 查看当前会话、模型、账号、连接和配置来源等状态 |
| `/clear` | 清空当前上下文，开始新的任务上下文 |
| `/compact` | 压缩当前会话上下文，保留后续任务所需摘要 |
| `/model` | 查看或切换当前模型 |
| `/effort` | 调整支持推理强度设置的模型的 effort level |
| `/resume` 或 `/continue` | 恢复或切换到历史会话 |
| `/exit` 或 `/quit` | 退出当前会话 |

## 权限模式

Claude Code 的权限模式决定它在编辑文件、运行命令或执行潜在高风险操作前是否需要用户确认。

| 模式 | 适用场景 |
|---|---|
| `default` | 默认监督模式，适合日常使用和不确定任务 |
| `acceptEdits` | 自动批准工作目录内的编辑，适合边界明确的开发任务 |
| `plan` | 只读规划和分析，适合先探索代码库或制定方案 |
| `bypassPermissions` | 跳过权限检查，风险最高，只适合完全可信且边界清晰的环境 |

可以用 <kbd>Shift</kbd> + <kbd>Tab</kbd> 在可用模式之间切换。`bypassPermissions` 也可以通过 `--dangerously-skip-permissions` 或 `--permission-mode bypassPermissions` 启动，但应谨慎使用。

## 相关页面

- [[Claude Code 入门指南]]
- [[Claude Code 第三方模型接入]]
- [[Claude Code 配置第三方模型]]

## 来源

- [[Claude Code入门]]
