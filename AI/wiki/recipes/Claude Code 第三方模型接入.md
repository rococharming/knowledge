---
title: Claude Code 第三方模型接入
date: 2026-07-17
tags: [llm, coding-tool, workflow]
source_count: 1
---

# Claude Code 第三方模型接入

Claude Code 默认面向 Anthropic 官方服务，但也可以通过 Anthropic 兼容接口接入第三方模型。核心配置是 `BASE_URL + API_KEY + model` 映射。

## 核心变量

| 配置 | 作用 |
|---|---|
| `ANTHROPIC_BASE_URL` | 覆盖默认 Anthropic API 地址，把请求发送到第三方平台或网关。 |
| `ANTHROPIC_API_KEY` | API Key 形式的密钥，通常作为 `X-Api-Key` 请求头发送。 |
| `ANTHROPIC_AUTH_TOKEN` | Bearer Token 形式的密钥，通常作为 `Authorization: Bearer ...` 请求头发送。 |
| `ANTHROPIC_MODEL` | 当前会话默认模型。 |
| `ANTHROPIC_DEFAULT_*_MODEL` | 把 Claude Code 内部模型别名映射到第三方平台真实模型 ID。 |
| `ANTHROPIC_DEFAULT_*_MODEL_NAME` | 控制模型选择器里的显示名称。 |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | 关闭非必要流量，包括自动更新、反馈、错误上报和遥测。 |

`ANTHROPIC_API_KEY` 和 `ANTHROPIC_AUTH_TOKEN` 都是密钥配置，区别主要在 HTTP 请求头形式。实际使用时应以第三方平台文档或示例为准，不要随意混用。

> [!warning]
> API Key 或 Token 类似密码，不应公开、提交到 Git 仓库或发给别人；泄漏后应在平台后台删除或重新生成。

## 配置位置

常见配置位置是用户级文件 `~/.claude/settings.json`，通过 `env` 字段为 Claude Code 会话注入环境变量：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://example.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "YOUR API KEY",
    "ANTHROPIC_MODEL": "provider-model-id"
  }
}
```

## 常见平台示例

素材记录了 MiniMax、Kimi、DeepSeek、智谱 GLM 等平台的示例配置。由于第三方模型名称、上下文长度、接口路径和计费计划可能变化，实际落地前应以平台当前文档为准。

| 平台 | 素材中的接口形态 | 密钥变量倾向 |
|---|---|---|
| MiniMax | `https://api.minimaxi.com/anthropic` | `ANTHROPIC_API_KEY` |
| Kimi | `https://api.moonshot.cn/anthropic` | `ANTHROPIC_AUTH_TOKEN` |
| DeepSeek | `https://api.deepseek.com/anthropic` | `ANTHROPIC_AUTH_TOKEN` |
| 智谱 GLM | `https://open.bigmodel.cn/api/anthropic` | `ANTHROPIC_API_KEY` |

## 操作流程

1. 在第三方平台创建 API Key 或 Token。
2. 确认平台提供的是 Anthropic 兼容接口，并记录 base URL。
3. 在 `~/.claude/settings.json` 的 `env` 中配置 base URL、密钥和默认模型。
4. 按需配置 `sonnet`、`opus`、`haiku`、`fable` 等模型别名映射。
5. 进入项目目录运行 `claude`，再用 `/status` 或 `/doctor` 检查当前模型、连接状态和配置来源。

![[Pasted image 20260514142220.png|600]]

上图是素材中 DeepSeek 开放平台创建 API Key 的入口截图，保留它是为了帮助定位关键配置前置步骤；具体按钮位置和平台界面可能变化，实际操作仍以平台当前页面为准。

## 相关页面

- [[Claude Code]]
- [[Claude Code 常用命令]]
- [[Claude Code 权限模式]]

## 来源

- [[Claude Code入门]]
