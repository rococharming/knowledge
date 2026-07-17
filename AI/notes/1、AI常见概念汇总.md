---
title: AI 常见概念汇总
date: 2026-07-09
tags: [AI, LLM, token]
aliases:
  - AI 常见概念汇总
  - AI常见概念汇总
source_count: 0
---

# 二、Token

## 1、概念

**Token** 是大语言模型处理文本时的基本单位，可以简单理解为模型“阅读”和“生成”时的最小粒度。

- 一个 token 通常对应约 **0.75 个英文单词**，或 **0.5 个左右汉字**（具体比例因模型分词器不同而异）。
- 模型的上下文长度、计费、速度等通常都按 token 计算。

> [!tip]
> 估算成本时，不要直接按“字数”算，而要按 token 数算。中文密度高，同样的字数通常比英文消耗更多 token。

## 2、Input

**Input** 指模型在一次请求中接收到的全部输入 token。

- 它不只是你当前输入的那句话，通常还包括：系统提示词、历史对话、上下文文件、Skill 描述、工具返回结果等。
- Input 是计费的主要部分之一，通常单价低于 output，但总量往往很大。
- 在 `Claude Code` 的 `/usage` 中，`input` 列表示当前会话中按模型累积的普通输入 token，即**未命中缓存、也未写入缓存**的输入部分。

## 3、Output

**Output** 指模型生成的输出 token。

- 包括模型返回给你的可见回答，也可能包括模型内部的思考过程（如 Claude 的 extended thinking / thinking tokens）。
- Output 通常比 Input 单价更高，但总量通常小于 Input。
- 在 `Claude Code` 的 `/usage` 中，`output` 列统计当前会话按模型累积的输出 token。

## 4、Cache Read（缓存命中）

**Cache Read** 指本次请求中有一部分输入 token 没有按普通 input 计费，而是从 **prompt cache** 中读取命中。

- 命中缓存的 token 通常价格远低于普通 input，大约是普通 input 的 **10% 左右**（具体比例看模型和平台定价）。
- 它适合那些**多轮请求中重复出现**的内容，例如系统提示词、CLAUDE.md、项目结构说明、已读文件等。
- 在 `Claude Code` 的 `/usage` 中，`cache read` 列显示命中缓存的输入 token 数。

## 5、Cache Write（缓存写入）

**Cache Write** 指本次请求中把一部分输入 token 写入 prompt cache，以便后续请求复用。

- 缓存写入本身通常需要额外成本，比普通 input 更贵一些。
- 它的价值在于：第一次“投资”写入后，后续如果命中，就能以很低的 cache read 成本复用。
- 是否写入缓存、写入哪些部分，通常由模型平台或客户端自动管理，用户一般无需手动干预。
- 在 `Claude Code` 的 `/usage` 中，`cache write` 列显示写入缓存的输入 token 数。

## 6、Prompt Caching 的整体逻辑

Prompt Caching 的核心目的：

> 把稳定、重复的上下文缓存起来，避免每次请求都按全价重新发送。

典型流程：

```text
第一次请求：大量 input token 被写入 cache → 产生 cache write 费用
第二次请求：相同上下文命中 cache → 产生较低的 cache read 费用
未命中部分：仍按普通 input 计费
```

### 适合缓存的内容

- 系统提示词（system prompt）
- 项目规则文件（如 CLAUDE.md、AGENTS.md）
- 历史对话中重复出现的上下文
- 已读取的大文件内容

### 不一定适合缓存的内容

- 每次都不一样的用户新输入
- 工具返回的实时结果（如最新日志、命令输出）
- 一次性上下文

## 7、Claude Code /usage 中的指标关系

在 `/usage` 输出中，按模型统计的 token 大致关系如下：

```text
总输入相关 token ≈ input + cache read + cache write
```

但三者计费方式不同：

| 类型 | 含义 | 计费特点 |
| --- | --- | --- |
| `input` | 普通输入 token | 正常单价 |
| `cache read` | 从缓存命中读取的输入 token | 低价，通常约为 input 的 10% |
| `cache write` | 写入缓存的输入 token | 较贵，用于后续复用 |
| `output` | 模型生成的输出 token | 通常单价高于 input |
