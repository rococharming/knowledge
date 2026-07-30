---
title: Codex接入第三方模型
date: 2026-06-22
tags: [AI, Codex]
aliases:
  - Codex接入第三方模型
---

# 一、为什么不能直接改个baseurl + API key

Codex CLI 或 Codex App 使用的是 Response API，大多数第三方模型使用的是 OpenAI-compatiable Chat Completions，协议不完全匹配。

要解决：让 Codex 发出的请求 -> 被第三方模型理解 -> 返回内容转换为 Codex 可识别形式

因此，Codex 接入第三方模型真正要解决的不是把 API Key 填进去，而是让 Codex 发出的请求能被第三方模型理解，再把第三方模型返回的内容转换成 Codex 能识别的形式。

![](https://picx.zhimg.com/v2-109619f080977edd107d28285a5912dd_r.jpg)

如何解决：

CC-Switch：本地代理  协议转换，代理层将 Response API 和 Chat Completions 进行互转
Codex++：桌面端增强 配置注入 桌面端配置和UI层做增强



# 二、CC-Switch

CC-Switch 类似于一个多 Agent Coding 工具的配置中心和本地路由代理。它最早为 Claude Code 设计，后来扩展到了 Codex，Gemini CLI、OpenCode、OpenClaw等工具。

在 Codex 场景，它主要做两件事：

- **配置切换**：把不同编码工具的配置统一管理起来，自持一键切换预设、导入模板、切换供应商
- **本机代理**：本机启动一个HTTP服务，将 Codex 的请求做协议转换和路由分发，再转发给第三方模型

核心：不动 Codex 本身，只改配置，再起一个代理。

设置之前，建议先确认 Codex 当前走的是 API Key / 本地配置路线，而不是 ChatGPT 登录路线。两种模式混在一起时，请求路径容易变得不明确，最后报错也不好判断。另外，Codex 至少需要运行一次，让配置文件初始化好，便于后续路由配置。


https://zhuanlan.zhihu.com/p/2045207013248995839
