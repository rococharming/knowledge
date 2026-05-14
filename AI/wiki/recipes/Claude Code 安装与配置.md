---
title: Claude Code 安装与配置
date: 2026-05-14
tags: [coding-tool, workflow]
source_count: 1
---

# Claude Code 安装与配置

本页介绍 [[Claude Code]] 的安装方式和接入国内第三方模型的详细配置。

## 安装

### macOS（原生安装）

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

此方式支持后台自动更新 Claude Code。如果后续设置了 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`，则不会自动更新。

验证安装：

```bash
claude --version
```

手动更新：

```bash
claude update
```

## 配置接入第三方模型

### 基本原理

Claude Code 默认向 Anthropic 官方接口发送请求。通过配置环境变量，可以将请求转发到国内第三方提供的 Anthropic 兼容接口。

需要配置三个核心要素：

- **Base URL**：替换默认的 Anthropic API 地址
- **Auth**：API Key（部分平台用 `ANTHROPIC_AUTH_TOKEN`，部分用 `ANTHROPIC_API_KEY`）
- **Model 映射**：将 Claude Code 的档位名映射到第三方模型标识符

配置文件位置：`~/.claude/settings.json`

### 通用配置字段说明

| 环境变量 | 说明 |
|---|---|
| `ANTHROPIC_BASE_URL` | 第三方网关的 Anthropic 兼容接口地址 |
| `ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_API_KEY` | API Key（平台决定使用哪个字段名） |
| `ANTHROPIC_MODEL` | 默认主模型 |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | `sonnet` 档位映射的模型 |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | `opus` 档位映射的模型 |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | `haiku` 档位映射的模型 |
| `API_TIMEOUT_MS` | API 请求超时（毫秒） |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | 设为 `1` 关闭自动更新、反馈、错误上报等非必要流量 |

### 接入 MiniMax

1. 进入 [MiniMax 开放平台](https://platform.minimaxi.com) 注册并购买 Token Plan
2. 复制 API Key
3. 编辑 `~/.claude/settings.json`：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "Your MINIMAX KEY",
    "ANTHROPIC_BASE_URL": "https://api.minimaxi.com/anthropic",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "MiniMax-M2.7",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "MiniMax-M2.7",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "MiniMax-M2.7",
    "ANTHROPIC_MODEL": "MiniMax-M2.7",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```

注意：Claude Code 会自动在 `ANTHROPIC_AUTH_TOKEN` 前加上 `Bearer`，因此直接填入 API Key 即可。

### 接入 Kimi

1. 访问 [Kimi Code 官网](https://www.kimi.com/code) 购买会员订阅计划
2. 在会员控制台创建 API Key（以 `sk-kimi-` 开头）
3. 编辑 `~/.claude/settings.json`：

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "Your Kimi Code KEY",
    "ANTHROPIC_BASE_URL": "https://api.kimi.com/coding/",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "kimi-for-coding",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "kimi-for-coding",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "kimi-for-coding",
    "ANTHROPIC_MODEL": "kimi-for-coding",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```

注意：

- Kimi k2.6 在 API 层面的内部模型标识符为 `kimi-for-coding`
- 也可以不设置模型字段，Kimi Code 后端会自动映射到 `kimi-for-coding`
- 这里使用的是 `ANTHROPIC_API_KEY` 而非 `ANTHROPIC_AUTH_TOKEN`

### 接入 DeepSeek

1. 进入 [DeepSeek 开放平台](https://platform.deepseek.com/) 注册账号
2. 在侧边栏找到 API Keys，点击「创建 API key」
3. 编辑 `~/.claude/settings.json`：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "Your DeepSeek KEY",
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-v4-pro",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-v4-pro",
    "ANTHROPIC_MODEL": "deepseek-v4-pro",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```

注意：DeepSeek 支持不同档位映射到不同模型（如 `haiku` → `deepseek-v4-flash`，`sonnet`/`opus` → `deepseek-v4-pro`）。

## 验证配置

配置完成后，进入项目目录启动 Claude Code：

```bash
cd path/to/project
claude
```

启动后输入：

```
/doctor
```

检查配置是否正确，也可以直接询问模型当前使用的模型名称来验证。

## 安全提醒

- API Key 不要分享给他人，泄漏后应立即重新生成
- 配置文件中包含敏感信息，注意文件权限（建议 `chmod 600 ~/.claude/settings.json`）

## 来源

- [[Claude Code入门]]
