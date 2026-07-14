---
title: Claude Code 配置第三方模型
date: 2026-07-14
tags: [coding-tool, configuration, workflow]
source_count: 1
---

# Claude Code 配置第三方模型

这个配方用于在用户级配置文件中为 [[Claude Code]] 接入第三方模型。它适用于目标平台提供 Anthropic 兼容接口，并明确说明应使用 API Key 还是 Bearer Token 鉴权的场景。

## 前置条件

1. 已安装 Claude Code，并能运行 `claude --version`。
2. 已在目标平台生成 API Key 或 Token。
3. 已确认目标平台的 Anthropic 兼容接口地址、鉴权方式和可用模型 ID。

## 配置位置

常见做法是在用户级配置文件中写入环境变量：

```text
~/.claude/settings.json
```

基本结构如下：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://example.com/anthropic",
    "ANTHROPIC_API_KEY": "YOUR_API_KEY",
    "ANTHROPIC_MODEL": "provider-model-id",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "provider-model-id",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "provider-model-id",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "provider-model-id"
  }
}
```

如果平台要求 Bearer Token 鉴权，则通常使用 `ANTHROPIC_AUTH_TOKEN` 替代 `ANTHROPIC_API_KEY`：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://example.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
    "ANTHROPIC_MODEL": "provider-model-id"
  }
}
```

## 配置步骤

1. 打开目标平台控制台，创建并复制 API Key 或 Token。
2. 打开 `~/.claude/settings.json`。
3. 在 `env` 中设置 `ANTHROPIC_BASE_URL`。
4. 按平台要求设置 `ANTHROPIC_API_KEY` 或 `ANTHROPIC_AUTH_TOKEN`。
5. 设置 `ANTHROPIC_MODEL` 作为默认模型。
6. 根据需要补充 `ANTHROPIC_DEFAULT_SONNET_MODEL`、`ANTHROPIC_DEFAULT_OPUS_MODEL`、`ANTHROPIC_DEFAULT_HAIKU_MODEL` 和 `ANTHROPIC_DEFAULT_FABLE_MODEL` 等别名映射。
7. 重新启动 `claude`，用 `/status` 或 `claude doctor` 检查配置是否生效。

## 安全注意

- 不要把真实 API Key 写入项目仓库。
- 不要把包含密钥的截图、日志或配置片段公开分享。
- 如果密钥泄漏，应立即在平台后台删除或重新生成。
- 第三方平台的模型 ID、上下文长度和计费策略可能变化，更新配置前应以平台当前文档为准。

## 相关页面

- [[Claude Code]]
- [[Claude Code 第三方模型接入]]
- [[Claude Code 入门指南]]

## 来源

- [[Claude Code入门]]
