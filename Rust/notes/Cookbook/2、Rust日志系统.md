# 一、概述

## 1、日志概念

日志，简单来说就是在某个时间点向指定的地方输出一条信息，记录着重要程度、时间、位置和发生的事件等。它是开发者了解程序运行状态、排查问题的关键工具。

- **开发调试阶段**：记录程序执行流程、变量值。通过查看日志可快速定位错误，例如函数调用是否成功、条件判断是否符合预期。复杂算法中，在关键步骤记日志能清晰看到每一步执行结果。
- **生产环境**：帮助运维实时监控系统运行状况。性能瓶颈时，日志可记录各模块响应时间、资源使用情况；还可用于安全审计，记录各种操作和事件以便追溯。

## 2、日志级别

日志级别是日志记录的重要属性，决定该条记录的重要性/严重程序。

Rust 的 `log`/`tracing`生态只有5个级别（从高到低）：

| 级别      | 语义                    | 典型场景                          |
| ------- | --------------------- | ----------------------------- |
| `Error` | 发生错误，某项功能失败，但系统整体仍可运行 | 数据库写入失败、外部库调用失败               |
| `Warn`  | 潜在问题，不影响系统正常运行，但需要关注  | 配置缺失但有默认值、触发重试                |
| `Info`  | 关键流程信息，确认程序运行状态       | 服务器启动成功、用户登录成功、关键任务完成（生产环境常开） |
| `Debug` | 详细调试信息，开发阶段定位问题       | 变量值、流程状态（生产常关，避免日志量过大）        |
| `Trace` | 最细粒度，跟踪程序每一步执行        | 调试底层逻辑（生产不开）                  |
在 Rust 的 `log` crate 中，对应`Level`枚举：

```rust
pub enum Level {
	Error = 1,
	Warn,
	Info,
	Debug,
	Trace,
}
```

程序产生的日志量非常大，生产环境全部开启将是"灾难"。因此需要控制日志输出的级别——设置一个**最低级别**后，只有该级别及更高的日志才会输出。例如最低级别设为 `Info`，则只有 Info / Warn / Error 输出，Debug / Trace 被过滤。

## 2、日志输出位置

通常日志可输出到两个地方：终端控制台和文件。

- **终端控制台**（标准输出 stdout、标准错误 stderr）：`println!`就是打印到 stdout。若日志没有持久化需求、只为调试，直接输出到控制台即可。
- **文件**：可以将日志持久化到磁盘文件中。还可以进一步为不同级别指定不同输出位置。

> 日志持久化不单指写磁盘文件，输出到控制台也能持久化：用一个日志采集工具从控制台标准输出中读取日志，发送到日志存储平台集中存储。


# 二、log crate

## 1、简介

`log`是 Rust 的日志门面库。它本身不输出任何日志，只提供统一的 API（各种宏）。

引入依赖：

```toml
[dependencies]
log = "0.4.33"
```

## 2、日志宏

`log`提供五个等级的宏（从高到低）：`error!`、`warn!`、`info!`、`debug!`、`trace!`，用法类似`println!`：

```rust
use log::{error, warn, info, debug, trace};

error!("Something really bad happened: {}", err);
warn!("Something might be wrong: {reason}");
info!("User {} logged in", user_id);
debug!("Request payload = {:?}", payload);
trace!("Loop index = {}", i);

```

此外还有一个通用日志宏`log!`。上面五个宏的级别是**编译期定死**的；当级别需要**运行时确定**（例如来自配置、命令行）时，就要用 `log!`。五个级别宏可理解为 `log!` 固定 level 的便捷封装：

```rust
use log::{Level, log};

let msg = String::from("Hello");
log!(Level::Info, "info log: {}", msg);
log!(target: "http", Level::Debug, "debug log: {}", msg);
```

- **`Level`**：枚举，变体 `Error`/`Warn`/`Info`/`Debug`/`Trace`。
- **`target`**：这条日志的分类标签/来源标识。不写时默认用当前模块路径作为 target；手动指定 target 可把某类日志归到更短、更语义化的分类中，方便过滤。

还有一个`log_enabled!`宏，用于判断在当前配置下的某个级别（及可选 traget）的日志是否会被记录——常用于避免构造昂贵日志参数**的开销：

```rust
use log::Level::Debug;
use log::{debug, log_enabled};

if log_enabled!(target: "http", log::Level::Debug) {
    let trace = build_http_trace(); // 仅在确实会记录时才构造
    debug!(target: "http", "trace = {}", trace);
}
```

## 3、门面与实现的分工

`log` crate 本身只是门面库，不负责把日志输出到终端/文件，只定义统一的日志 API（宏与 Trait ）。因此，Rust 日志生态遵循如下分工：

- **库开发者**：只依赖并使用`log`记录日志，不绑定任何具体实现，也不负责初始化日志系统
- **应用开发者**：选择并初始化一个具体的日志实现（后端 logger），如`env_logger`、`log4rs`等，真正处理和输出日志

`log`提供底层全局接口`set_logger`/`set_max_level`用于安装日志实现并设置全局级别。但大多数具体日志库都封装了更高层的初始化 API (如`init()`/`try_init()`)，内部完成这些调用，应用开发者只需调用一次初始化函数。

## 三、env_logger crate

`env_logger`是`log`的一个具体实现（`logger`），它实现`log::Log`，并用环境变量（`RUST_LOG`）控制过滤规则和日志级别。

引入依赖：

```toml
[dependencies]
log = "0.4.33"
env_logger = "0.11.10"
```