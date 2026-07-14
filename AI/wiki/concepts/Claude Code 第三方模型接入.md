---
title: Claude Code 第三方模型接入
date: 2026-07-14
tags: [coding-tool, llm, configuration]
source_count: 1
---

# Claude Code 第三方模型接入

Claude Code 第三方模型接入，是指让 [[Claude Code]] 不直接请求 Anthropic 官方 API，而是把请求转发到兼容 Anthropic API 的第三方平台、模型网关或云平台。

## 核心配置要素

第三方模型接入通常由三类配置共同完成：

| 配置 | 含义 |
|---|---|
| `ANTHROPIC_BASE_URL` | 覆盖默认 API 地址，把请求路由到第三方平台或网关的 Anthropic 兼容接口 |
| `ANTHROPIC_API_KEY` 或 `ANTHROPIC_AUTH_TOKEN` | 鉴权密钥，分别对应 `X-Api-Key` 和 Bearer Token 一类的鉴权方式 |
| 模型与别名映射 | 把 Claude Code 内部使用的模型别名映射到第三方平台真实存在的模型 ID |

`ANTHROPIC_API_KEY` 和 `ANTHROPIC_AUTH_TOKEN` 不应随意混用，应以目标平台文档或示例为准。密钥必须视为敏感信息，不能提交到 Git 仓库或公开分享。

## 模型别名映射

Claude Code 内部会使用 `sonnet`、`opus`、`haiku`、`fable` 等模型别名。接入第三方模型时，需要把这些别名映射到平台支持的具体模型，例如：

- `ANTHROPIC_MODEL`：当前会话默认模型。
- `ANTHROPIC_DEFAULT_SONNET_MODEL`：`sonnet` 别名实际调用的模型。
- `ANTHROPIC_DEFAULT_OPUS_MODEL`：`opus` 别名实际调用的模型。
- `ANTHROPIC_DEFAULT_HAIKU_MODEL`：`haiku` 别名实际调用的模型。
- `ANTHROPIC_DEFAULT_FABLE_MODEL`：`fable` 别名实际调用的模型。

带 `_NAME` 后缀的变量主要影响模型选择器中的显示名称，不等同于实际发送给接口的模型 ID。

## 非必要流量

部分第三方网关或受限网络环境会同时配置 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`，用于减少自动更新、反馈、错误报告和遥测等非必要流量。关闭非必要流量会改变更新和诊断行为，因此应和安装方式、团队策略一起考虑。

## 使用约束

第三方接入的稳定性取决于平台对 Anthropic 兼容协议、上下文长度、工具调用、模型别名和鉴权方式的支持程度。配置时要优先查看平台官方文档，并在 `claude doctor`、`/status` 和实际任务中验证连接状态。

## 相关页面

- [[Claude Code]]
- [[Claude Code 配置第三方模型]]
- [[Claude Code 入门指南]]

## 来源

- [[Claude Code入门]]
