---
title: 日志分析 CLI 项目目标
date: 2026-07-20
tags: [Rust, 项目, CLI, 日志分析]
aliases:
  - rlog 项目目标
  - 日志分析 CLI
  - Rust 日志分析项目
---

# 一、项目目标

本项目实现一个日志分析命令行工具，命名为 `rlog`。

`rlog` 的基本目标是：

> 从日志文件中按行读取内容，根据级别或关键词筛选日志，并能统计不同日志级别的数量。

它可以看作是 [[Rust/notes/项目/01_minigrep/1、minigrep 项目目标|minigrep]] 之后的第二个 Rust CLI 练习项目。`minigrep` 主要练习“从文件中搜索文本”，而 `rlog` 会在这个基础上继续加入子命令、日志级别、过滤条件、统计结果和模块拆分。

第一版命令设计如下：

```shell
rlog view full_log.txt
rlog view full_log.txt --level error
rlog view full_log.txt --contains connection
rlog stats full_log.txt
```

其中：

- `view` 用于查看日志，可以结合过滤条件只输出匹配行。
- `stats` 用于统计日志级别数量，例如 `TRACE`、`DEBUG`、`INFO`、`WARN`、`ERROR`。
- `full_log.txt` 是要分析的日志文件路径。
- `--level` 用于按日志级别过滤。
- `--contains` 用于按关键词过滤。

第一版处理常见的五种日志级别：

| 级别 | 含义 | 示例场景 |
|---|---|---|
| `TRACE` | 最细粒度的追踪信息 | 函数入口、循环细节、协议帧 |
| `DEBUG` | 调试信息 | 中间变量、分支选择、配置详情 |
| `INFO` | 普通运行信息 | 程序启动、请求完成 |
| `WARN` | 警告信息 | 请求变慢、配置缺失但仍可运行 |
| `ERROR` | 错误信息 | 连接失败、文件读取失败 |

为了让第一版范围足够清晰，本项目先约定使用类似下面的日志格式：

```text
[2026-07-20T09:29:50Z TRACE rlog::app] entering startup sequence
```

可以在 `rlog/` 项目根目录创建一个测试日志文件 `full_log.txt`：

```text
[2026-07-20T09:29:50Z TRACE rlog::app] entering startup sequence
[2026-07-20T09:30:00Z INFO rlog::app] application started
[2026-07-20T09:30:30Z DEBUG rlog::config] resolved config path rlog.toml
[2026-07-20T09:31:12Z INFO rlog::app] loaded configuration from rlog.toml
[2026-07-20T09:32:05Z WARN rlog::network] connection is slow
[2026-07-20T09:32:45Z ERROR rlog::network] connection failed
[2026-07-20T09:32:50Z DEBUG rlog::retry] connection retry backoff set to 200ms
[2026-07-20T09:33:10Z INFO rlog::retry] retrying connection
[2026-07-20T09:33:40Z INFO rlog::network] connection established
[2026-07-20T09:34:01Z WARN rlog::parser] skipped malformed log line
[2026-07-20T09:35:22Z ERROR rlog::storage] failed to write archive file
[2026-07-20T09:35:40Z TRACE rlog::storage] closing archive writer
[2026-07-20T09:36:00Z INFO rlog::app] shutdown requested
```

第一版主要完成以下能力：

| 能力 | 用途 |
|---|---|
| 命令行参数解析 | 接收子命令、文件路径、级别过滤和关键词过滤 |
| 按行读取文件 | 支持处理较大的日志文件，不一次性读完整个文件 |
| 日志级别解析 | 从每一行日志中识别 `TRACE`、`DEBUG`、`INFO`、`WARN`、`ERROR` |
| 日志过滤 | 根据 `--level` 和 `--contains` 判断是否输出当前行 |
| 统计汇总 | 计算不同日志级别分别出现了多少次 |
| 错误处理 | 处理文件不存在、参数错误等可预期问题 |
| 测试 | 验证解析、过滤和统计逻辑是否正确 |

这个项目会用到几个重要的 Rust 知识点：

| 知识点 | 在项目中的用途 |
|---|---|
| `PathBuf` | 表示日志文件路径 |
| `BufReader` | 按行读取日志文件 |
| `Result` 和 `?` | 传播文件读取、解析和运行错误 |
| `enum` | 表示 `TRACE`、`DEBUG`、`INFO`、`WARN`、`ERROR` 等日志级别 |
| `struct` | 表示命令行参数、日志记录和统计结果 |
| `Option` | 表示可选过滤条件 |
| `match` | 根据子命令或日志级别执行不同逻辑 |
| 迭代器 | 对日志行进行过滤、映射和统计 |
| 模块拆分 | 将 CLI、解析、过滤和统计逻辑分开 |
| 单元测试 | 单独验证日志解析、过滤和统计函数 |

第一版推荐的项目结构是：

```shell
src/
├── main.rs
├── cli.rs
├── log_entry.rs
├── filter.rs
└── stats.rs
```

各文件职责如下：

| 文件 | 职责 |
|---|---|
| `main.rs` | 程序入口，负责调用 CLI 解析和运行逻辑 |
| `cli.rs` | 定义命令行参数、子命令和选项 |
| `log_entry.rs` | 定义日志级别和日志行解析逻辑 |
| `filter.rs` | 根据级别和关键词判断日志行是否匹配 |
| `stats.rs` | 统计 `TRACE`、`DEBUG`、`INFO`、`WARN`、`ERROR` 数量 |

后续第二版可以在第一版基础上继续扩展：

| 功能 | 说明 |
|---|---|
| 解析时间 | 从日志行中提取时间字段 |
| 解析模块 | 提取 `rlog::app`、`rlog::network` 等模块名 |
| 时间范围过滤 | 只查看某个时间段内的日志 |
| JSON 输出 | 使用 `serde` 和 `serde_json` 输出结构化结果 |

因此，本项目的学习重点不是一次性写出复杂工具，而是按真实软件开发流程逐步推进：

1. 明确需求和第一版边界。
2. 设计命令行接口。
3. 拆分模块和数据结构。
4. 实现文件读取、过滤和统计。
5. 编写测试保护核心逻辑。
6. 生成 release 二进制。

下一步进入 [[Rust/notes/项目/02_rlog/2、命令行参数设计|命令行参数设计]]，使用 `clap` 定义 `view` 和 `stats` 两个子命令。
