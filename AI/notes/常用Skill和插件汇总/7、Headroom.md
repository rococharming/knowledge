---
title: Headroom
date: 2026-07-20
tags: [AI, coding-tool, context-engineering, token-optimization]
aliases:
  - Headroom AI
  - Headroom 上下文压缩
  - AI Agent 上下文优化层
---

# 一、概述

`headroomlabs-ai/headroom` 是一个放在 AI Agent 或应用与大模型服务之间的 **上下文优化层**。它会在请求到达模型前，压缩工具输出、日志、搜索结果、JSON、文件和对话内容，减少实际发送给模型的输入 token；模型响应则原样返回。

它不是大模型、Skill 或新的 Agent 框架，而是一层可插拔的本地中间件。核心目标是：让模型看到更少但更有用的上下文，同时在需要时仍能取回原始内容。

> [!summary] 核心价值
> Headroom 解决的是“Agent 工作越久，工具结果和历史内容越多，输入成本、延迟和上下文压力越高”的问题。它通过内容识别、专用压缩器、提示词缓存优化和可逆检索，尽量避免简单截断带来的信息丢失。

Headroom 提供五种主要入口：

| 入口 | 作用 | 适合场景 |
|---|---|---|
| Python Library | 调用 `compress(messages)` 后再请求模型 | 希望在代码里精确控制压缩参数 |
| TypeScript SDK | 通过本地 Headroom Proxy 调用同一压缩链路 | Node.js、Vercel AI SDK、OpenAI 或 Anthropic SDK 项目 |
| Proxy | 在客户端和模型服务之间运行本地 HTTP 代理 | 不想改业务逻辑，只想改模型服务地址 |
| Agent Wrap | 启动代理、配置接入并运行 Codex、Claude Code 等工具 | 日常使用 Coding Agent |
| MCP Server | 暴露压缩、原文检索和统计工具 | 只想让支持 MCP 的 Agent 按需压缩 |

MCP（Model Context Protocol，模型上下文协议）是一种让 Agent 以统一方式调用外部工具的协议。Headroom 提供的主要 MCP 工具有：

- `headroom_compress`：按需压缩一段内容。
- `headroom_retrieve`：按哈希值取回原始内容。
- `headroom_stats`：查看本次会话的压缩与节省统计。

除了核心压缩链路，项目还包含跨 Agent 记忆、`headroom learn` 失败经验提取和输出长度控制等功能。这些属于相邻能力，不是理解 Headroom 压缩机制的前提。

截至 2026-07-20，核对的 `main` 提交为 `fd0e1a8`，项目版本为 `0.32.0`，使用 Apache 2.0 许可证，Python 要求为 3.10 及以上；TypeScript SDK 要求 Node.js 18 及以上。

# 二、安装

## 1、安装命令行工具

官方推荐把 CLI 安装为独立的 `uv` 工具，避免污染项目环境：

```shell
uv tool install --python 3.13 "headroom-ai[all]"
```

如果是在 Python 项目的虚拟环境中使用：

```shell
pip install "headroom-ai[all]"
```

需要注意：

- PyPI 包 `headroom-ai` 才会提供 `headroom` 命令。
- npm 包 `headroom-ai` 只是 TypeScript SDK，不会提供 CLI。
- TypeScript SDK 会调用本地 Headroom Proxy，因此仍需通过 Python 包启动代理。
- `[all]` 包含核心常用能力，但不会包含所有框架适配器，也不包含需要 C++ 工具链的可选 HNSW 向量后端。

## 2、在 Codex 中使用

最短路径是直接包装一次 Codex 会话：

```shell
headroom wrap codex
```

这条命令会启动或复用本地代理，将当前 Codex 会话指向 `http://127.0.0.1:8787/v1`，配置相关上下文工具和 MCP，然后启动 Codex。它不是简单地给 Codex 增加一个提示词，而是实际接管请求转发路径。

如果需要撤销 Headroom 管理的持久配置，可使用：

```shell
headroom unwrap codex
```

Headroom 会用带标记的配置块和备份恢复 Codex 配置；即使如此，首次在重要环境启用前，仍应检查 `~/.codex/config.toml` 的变化。

## 3、单独启动 Proxy 或 MCP

只使用代理：

```shell
headroom proxy --port 8787
```

然后让 OpenAI 兼容客户端指向：

```text
http://127.0.0.1:8787/v1
```

只安装 MCP 能力：

```shell
pip install "headroom-ai[mcp]"
headroom mcp serve
```

Codex 等桌面应用不一定继承交互式 Shell 的 `PATH`。如果 MCP 启动失败，应先执行：

```shell
command -v headroom
```

再把返回的绝对路径写入 MCP 配置，而不是只写 `command = "headroom"`。

## 4、验证安装

```shell
headroom doctor
headroom perf
```

- `headroom doctor` 检查代理、路由和依赖是否正常。
- `headroom perf` 展示当前环境中的压缩效果。
- 代理运行时可使用 `headroom dashboard` 查看实时统计。

安装成功不等于压缩一定有收益。还需要用自己的真实任务对比 token、延迟、回答正确率和原文检索情况。

# 三、工作原理

## 1、当前请求链路

当前 `main` 的核心链路可以概括为：

```text
Agent / 应用
  ↓ 请求消息、工具输出、日志、文件
可选工具结果拦截器
  ↓
CacheAligner
  ↓
ContentRouter
  ↓
CCR 保存原文并写入检索标记
  ↓
大模型服务
  ↓
原样返回模型响应
```

这里有一个容易被旧文档误导的变化：当前代码已经移除 `IntelligentContextManager / RollingWindow`，不会再通过丢弃旧消息来管理上下文。现在的主策略是 **live-zone-only compression**，即只处理尚未被上游缓存固定的活跃内容，不修改已经冻结的历史前缀。

> [!warning] 以当前代码为准
> 仓库中的 `architecture.mdx` 仍保留“第三阶段会删除旧消息”的旧描述，但当前 `TransformPipeline`、README 和 CCR 文档都已说明该阶段被移除。理解架构时应以当前代码的 `CacheAligner → ContentRouter` 两段主链路为准。

## 2、CacheAligner：保护提示词缓存

大模型服务通常会缓存重复的提示词前缀。这里的提示词缓存也叫 KV Cache（Key-Value Cache，模型对已处理前缀的中间计算结果）。只要前缀字节稳定，后续请求就能复用计算，降低延迟或费用。

`CacheAligner` 负责识别日期、会话 ID 等容易变化的内容，帮助调用方把稳定前缀与动态内容分开。代理还会把已经被上游缓存的消息标记为冻结前缀，后续压缩不会改写这些字节，避免为了少量压缩破坏更大的缓存收益。

## 3、ContentRouter：按内容类型选择压缩器

`ContentRouter` 不会用一种算法处理所有输入，而是先识别内容类型，再路由到合适的压缩器。

| 内容类型 | 主要处理方式 | 保留重点 |
|---|---|---|
| JSON 数组 | `SmartCrusher` 统计抽样与去重 | 字段结构、异常项、首尾信息和分布特征 |
| 源代码 | AST 感知的 `CodeCompressor` | import、类型、函数与类签名；默认有较强保护 |
| 搜索结果 | `SearchCompressor` | 文件、位置和相关匹配 |
| 构建与测试日志 | `LogCompressor` | 错误、堆栈和关键状态变化 |
| Git Diff | `DiffCompressor` | 变更结构和关键差异 |
| HTML | 正文提取 | 去除标签、导航和页面噪声 |
| 表格与配置 | 结构化压缩 | 列、键和高信息量值 |
| 普通文本 | `Kompress-v2-base` 或轻量文本压缩 | 标题、高信息量 token 和与问题相关的内容 |

AST（Abstract Syntax Tree，抽象语法树）是源代码的结构化表示。按 AST 压缩比按行截断更容易保留程序骨架，但函数体细节仍可能是当前任务所需信息，因此 Headroom 默认保护最近代码，以及处于分析、修复、调试语境中的代码。

如果压缩器不可用、解析失败、内容过短或压缩后反而更大，Headroom 会直接返回原内容。连续失败还会触发短暂熔断，在冷却时间内跳过压缩，避免代理反复拖慢每个请求。

## 4、SmartCrusher：压缩结构化工具输出

Headroom 最擅长的是较大的 JSON 数组，例如 API 响应、数据库行和结构化日志。

`SmartCrusher` 会：

1. 解析数组和字段结构。
2. 识别重复项、常量字段、数值分布和变化点。
3. 保留开头的结构样本、末尾的最新样本和重要性更高的项目。
4. 额外保留错误、异常值和突变项，即使它们超过原定样本预算。
5. 将原始内容写入 CCR，并在压缩结果中留下可检索的哈希标记。

因此，它不是无条件“取前 15 条”，也不是简单删除重复行，而是在缩小数据规模的同时保留结构和异常信号。

## 5、CCR：压缩后仍可取回原文

CCR 是 Compress-Cache-Retrieve（压缩、缓存、检索）的缩写。它把有损压缩变成可恢复流程：

```text
1000 条工具结果
  ↓ 压缩
20 条代表性结果 + hash
  ↓ 模型发现信息不足
headroom_retrieve(hash)
  ↓
返回本地缓存中的原始 1000 条结果
```

在 Anthropic 与 OpenAI 代理路径中，Headroom 可以拦截 `headroom_retrieve` 调用、读取本地缓存并自动继续模型请求。单独使用 MCP 时，则由 Agent 显式调用检索工具。

> [!warning] “可逆”不等于永久保存
> Proxy 的 CCR 原文默认 TTL（Time To Live，存活时间）是 30 分钟，MCP 本地存储默认是 1 小时。进程退出、缓存清理或 TTL 到期后，哈希可能无法继续检索；长时间任务应调大 `HEADROOM_CCR_TTL_SECONDS`，并保留重新读取原始来源的能力。

## 6、默认安全边界

当前代码包含多层保护：

- 默认不压缩用户消息。
- 默认保护最后 4 条消息中的代码。
- 用户提出分析、审查、解释、修复或调试代码时，保护相关代码内容。
- 文件读取结果、失败的工具调用和错误输出存在额外保护逻辑。
- 小于阈值的内容直接透传，不承担无意义的压缩开销。
- 压缩结果变大时回退原文。
- 工具输出只有在可通过 CCR 恢复时，才允许采用有损结果。

需要特别注意：当前 Python `CompressConfig` 的 `compress_system_messages` 默认值是 `True`，与部分旧文档中“系统提示词不会被压缩”的说法不完全一致。如果系统或开发者提示词必须逐字保持，应显式设置：

```python
from headroom import CompressConfig, compress

result = compress(
    messages,
    model="gpt-4o",
    config=CompressConfig(compress_system_messages=False),
)
```

# 四、实践指南

## 1、如何选择接入方式

| 需求 | 推荐方式 |
|---|---|
| 直接优化日常 Codex 或 Claude Code 会话 | `headroom wrap codex` 或 `headroom wrap claude` |
| 已有 OpenAI 或 Anthropic 兼容应用，不想改代码 | Proxy |
| Python 应用需要逐次控制和读取压缩指标 | `compress(messages)` |
| TypeScript 应用 | npm SDK + 本地 Proxy |
| 只想让 Agent 自己决定何时压缩 | MCP Server |
| 团队共享、长期运行和集中治理 | 持久部署或团队版，而不是每人临时启动一个进程 |

第一次尝试时，优先从 `wrap` 或 Proxy 开始。它们最接近真实请求链路，也比同时启用记忆、失败学习、输出塑形和自定义压缩器更容易判断收益来自哪里。

## 2、推荐验证流程

```text
选择 5～10 个真实任务
  ↓
记录未启用 Headroom 的 token、耗时和结果
  ↓
只启用 wrap 或 Proxy
  ↓
检查 doctor、perf、dashboard 和 CCR 检索失败
  ↓
比较正确率、输入 token、总延迟和费用
  ↓
确认有稳定收益后，再调整压缩强度或启用附加能力
```

至少同时观察四项：

- **任务结果**：答案、代码和测试是否仍然正确。
- **输入节省**：真正发送给上游模型的 token 减少多少。
- **总延迟**：压缩耗时是否被更短的模型处理时间抵消。
- **检索可靠性**：是否出现 CCR 原文到期、哈希缺失或模型没有主动检索。

## 3、适合与不适合的场景

Headroom 更适合：

- 包含大量 JSON、数据库结果、搜索结果和构建日志的 Agent 工作流。
- 长时间、多工具调用的 Coding Agent 会话。
- 希望多个 Agent 共享本地上下文或统计的个人开发环境。
- 需要保留原始工具结果、又想降低常态上下文成本的任务。

Headroom 收益较小或不适合：

- 很短的单轮问答。
- 主要内容都是当前需要逐行修改的源码。
- 已经高度精简的命令输出。
- 无法运行本地进程的沙箱环境。
- 对每一个输入字节都要求模型立即可见、且不能依赖后续检索的高风险任务。

## 4、如何看待官方基准

README 给出的主张是：JSON 数据可减少约 60%～95% token，而 Coding Agent 的整体输入通常减少约 15%～20%。仓库还展示了代码搜索、事故排查、Issue 分流和代码库探索等任务中 47%～92% 的个别结果。

这些数字只能说明项目在特定数据集和任务上具有潜力，不能直接当作本地保证：

- 高压缩率主要来自大量结构化或重复工具输出，不代表普通对话。
- 仓库基准页仍包含基于旧版 `0.5.18` 的测试，而当前代码版本已经是 `0.32.0`。
- 官方生产遥测也显示，很多短请求的中位压缩率只有 4.8%。
- 正确率评估的样本量和任务覆盖有限，仍需用自己的任务验证。

> [!tip]
> 判断 Headroom 是否值得保留，不要只看“累计节省 token”。如果回答需要频繁回读原文、失败重试变多或延迟明显上升，表面上的压缩率可能没有转化为真实收益。

## 5、与其他工具的关系

- **模型原生 Compaction**：通常压缩长对话历史；Headroom 更关注发送前的工具输出和内容类型路由，并提供 CCR 原文检索。两者可以互补。
- **RTK / lean-ctx**：主要精简命令行工具输出；Headroom 的范围更大，还处理 API、日志、JSON、文本和代理请求。Headroom 默认会在 Agent Wrap 中配置 RTK，也可选择 lean-ctx。
- **[[6、Ponytail|Ponytail]]**：Ponytail 约束 Agent 的实现决策和输出行为，减少不必要代码；Headroom 压缩进入模型的上下文。前者解决“不要过度实现”，后者解决“不要把所有原始数据都塞给模型”，不能相互替代。

## 6、参考

- [Headroom GitHub 仓库](https://github.com/headroomlabs-ai/headroom)
- [Quickstart](https://headroom-docs.vercel.app/docs/quickstart)
- [How Compression Works](https://headroom-docs.vercel.app/docs/how-compression-works)
- [CCR 可逆压缩](https://headroom-docs.vercel.app/docs/ccr)
- [Limitations](https://headroom-docs.vercel.app/docs/limitations)
- [Benchmarks](https://headroom-docs.vercel.app/docs/benchmarks)
