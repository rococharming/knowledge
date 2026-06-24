# Rust 日志系统入门笔记

> 本文覆盖 `log`、`env_logger`、`tracing`、`tracing-subscriber`、`tracing-appender` 这条主流日志链路。
> 所有代码示例均基于实测验证（截至 2026-06，各 crate 最新稳定版本见各节）。

---

## 一、日志概述

### 1.1 日志是什么

日志，简单来说就是在某个时间点向指定的地方输出一条信息，记录着**重要程度、时间、位置和发生的事件**等。它是开发者了解程序运行状态、排查问题的关键工具。

- **开发调试阶段**：记录程序执行流程、变量值。通过查看日志可快速定位错误，例如函数调用是否成功、条件判断是否符合预期。复杂算法中，在关键步骤记日志能清晰看到每一步执行结果。
- **生产环境**：帮助运维实时监控系统运行状况。性能瓶颈时，日志可记录各模块响应时间、资源使用情况；还可用于安全审计，记录各种操作和事件以便追溯。

### 1.2 日志级别

日志级别是日志记录的重要属性，决定该条记录的重要性/严重程度。**Rust 的 `log` / `tracing` 生态只有 5 个级别**（从高到低），没有 `Fatal`：

| 级别      | 语义                    | 典型场景                          |
| ------- | --------------------- | ----------------------------- |
| `Error` | 发生错误，某项功能失败，但系统整体仍可运行 | 数据库写入失败、外部库调用失败               |
| `Warn`  | 潜在问题，不影响系统正常运行，但需要关注  | 配置缺失但有默认值、触发重试                |
| `Info`  | 关键流程信息，确认程序运行状态       | 服务器启动成功、用户登录成功、关键任务完成（生产环境常开） |
| `Debug` | 详细调试信息，开发阶段定位问题       | 变量值、流程状态（生产常关，避免日志量过大）        |
| `Trace` | 最细粒度，跟踪程序每一步执行        | 调试底层逻辑（生产不开）                  |

`log` crate 的 `Level` 枚举及数值（重要程度越高数值越小）：

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

### 1.3 日志输出位置

通常日志可输出到两个地方：终端控制台和文件。

- **终端控制台**（标准输出 stdout / 标准错误 stderr）：`println!` 就是打印到 stdout。若没有日志持久化需求、只为调试，直接输出控制台即可。
- **文件**：可进一步为不同级别指定不同输出位置——Debug 输出到控制台（方便开发且不占磁盘），Info/Warn 输出到 `info.log`，Error 输出到 `err.log`。

> 日志持久化不单指写磁盘文件，输出到控制台也能持久化：用一个日志采集工具从控制台标准输出读取日志，发送到日志存储平台集中存储。最典型的就是容器/容器云环境——容器进程把日志写到标准输出，一个单独的采集服务读取标准输出，经网络发送到日志处理和存储平台。

---

## 二、log crate（日志门面）

### 2.1 简介

`log` 是 Rust 的**日志门面库（logging facade）**。它本身不输出任何日志，只提供统一的 API（各种宏）。

```toml
[dependencies]
log = "0.4.33"
```

### 2.2 日志宏

`log` 提供五个等级的宏（从高到低）：`error!`、`warn!`、`info!`、`debug!`、`trace!`，用法类似 `println!`：

```rust
use log::{error, warn, info, debug, trace};

error!("Something really bad happened: {}", err);
warn!("Something might be wrong: {reason}");
info!("User {} logged in", user_id);
debug!("Request payload = {:?}", payload);
trace!("Loop index = {}", i);
```

此外还有一个通用日志宏 `log!`。上面五个宏的级别是**编译期定死**的；当级别需要**运行时确定**（例如来自配置、命令行）时，就要用 `log!`。五个级别宏可理解为 `log!` 固定 level 的便捷封装：

```rust
use log::{Level, log};

let msg = String::from("Hello");
log!(Level::Info, "info log: {}", msg);
log!(target: "http", Level::Debug, "debug log: {}", msg);
```

- **`Level`**：枚举，变体 `Error`/`Warn`/`Info`/`Debug`/`Trace`。
- **`target`**：这条日志的分类标签/来源标识。不写时默认用当前模块路径作为 target；手动指定 target 可把某类日志归到更短、更语义化的分类中，方便过滤。

还有一个 `log_enabled!` 宏，用于判断在当前配置下某个级别（及可选 target）的日志是否会被记录——常用于**避免构造昂贵日志参数**的开销：

```rust
use log::Level::Debug;
use log::{debug, log_enabled};

if log_enabled!(target: "http", log::Level::Debug) {
    let trace = build_http_trace(); // 仅在确实会记录时才构造
    debug!(target: "http", "trace = {}", trace);
}
```

### 2.3 门面与实现的分工

`log` crate 本身只是门面库，不负责把日志输出到终端/文件，只定义统一的日志 API（宏与 trait）。Rust 日志生态遵循以下分工：

- **库开发者**：只依赖并使用 `log` 记录日志，不绑定任何具体实现，也不负责初始化日志系统。
- **应用开发者**：选择并初始化一个具体的日志实现（后端 logger），如 `env_logger`、`log4rs`、`simple_logger` 等，真正处理和输出日志。

`log` 提供底层全局接口 `set_logger` / `set_max_level` 用于安装日志实现并设置全局级别。但大多数具体日志库都封装了更高层的初始化 API（如 `init()` / `try_init()`），内部完成这些调用，应用开发者通常只需调用一次初始化函数。

> **注意**：全局 logger 只能初始化一次，因此库代码不应主动初始化日志系统，以免干扰应用层的日志配置。

---

## 三、env_logger crate（log 的具体实现）

`env_logger` 是 `log` 的一个具体实现（logger），它实现 `log::Log`，并**用环境变量（通常是 `RUST_LOG`）控制过滤规则和日志级别**。

```toml
[dependencies]
log = "0.4.33"
env_logger = "0.11.10"
```

### 3.1 最小示例

```rust
use log::{trace, debug, info, warn, error};

fn main() {
    // 尽量放在最早位置
    env_logger::init();

    trace!("This is a trace message");
    debug!("This is a debug message");
    info!("This is a info message");
    warn!("This is a warn message");
    error!("This is a error message");
}
```

默认情况下，`env_logger` 除 `error` 外其他级别都被禁用，因此上面只显示 ERROR。此外**默认输出到 stderr 而非 stdout**。

### 3.2 运行时设置 RUST_LOG

这是 `env_logger` 的典型用法。例如设置 info 及以上输出：

```shell
# Linux/macOS
RUST_LOG=info cargo run
# Windows PowerShell
$env:RUST_LOG="info"; cargo run
```

`log` 的默认 target 是模块路径，`env_logger` 的过滤规则按 **target 前缀匹配**，可在 `RUST_LOG` 里增加模块规则：

```rust
use log::{trace, debug, info, warn, error};

mod http {
    pub mod client {
        use log::{debug, info, warn};
        pub fn run() {
            warn!("client warn");
            info!("client info");
            debug!("client debug");
        }
    }
}

fn main() {
    env_logger::init();

    trace!("This is a trace message");
    debug!("This is a debug message");
    info!("This is a info message");
    warn!("This is a warn message");
    error!("This is a error message");

    http::client::run();
}
```

根（root）只打印 warn 及以上，但 http 模块打印 debug 及以上：

```shell
# 假设包名为 myapp
RUST_LOG=warn,myapp::http=debug cargo run
```

### 3.3 代码中设置默认级别

用 `env_logger::Builder` 可在代码里指定默认过滤级别（环境变量没配时生效）：

```rust
use log::{trace, debug, info, warn, error};

mod http {
    pub mod client {
        use log::{debug, info, warn};
        pub fn run() {
            warn!("client warn");
            info!("client info");
            debug!("client debug");
        }
    }
}

fn main() {
    // 从环境变量读取（RUST_LOG），若没配置则使用默认规则 "info"
    env_logger::Builder::from_env(
        env_logger::Env::default().default_filter_or("info")
    ).init();

    trace!("This is a trace message");
    debug!("This is a debug message");
    info!("This is a info message");
    warn!("This is a warn message");
    error!("This is a error message");

    http::client::run();
}
```

### 3.4 设置输出位置

默认 `env_logger` 输出到 stderr。

**(1) 输出到 stdout**：用 `Builder::target()` 改变输出目标：

```rust
env_logger::Builder::from_env(
    env_logger::Env::default().default_filter_or("info")
).target(env_logger::Target::Stdout).init();
```

**(2) 输出到文件**：`env_logger` 没有直接传文件名写入的 API，但允许自定义 writer，打开文件并写进去：

```rust
use log::{trace, debug, info, warn, error};
use std::io::Write;

mod http {
    pub mod client {
        use log::{debug, info, warn};
        pub fn run() {
            warn!("client warn");
            info!("client info");
            debug!("client debug");
        }
    }
}

fn main() {
    let file = std::fs::OpenOptions::new()
        .create(true)
        .write(true)
        .append(true)
        .open("log.txt")
        .unwrap();

    // 文件加锁：logger 全局共享，可能在多线程里并发写日志
    let file = std::sync::Mutex::new(file);

    env_logger::Builder::from_env(
        env_logger::Env::default().default_filter_or("info")
    ).format(move |buf, record| {
        let mut f = file.lock().unwrap();
        writeln!(f, "{} [{}] {}", record.level(), record.target(), record.args()).unwrap();
        Ok(())
    }).init();

    trace!("This is a trace message");
    debug!("This is a debug message");
    info!("This is a info message");
    warn!("This is a warn message");
    error!("This is a error message");

    http::client::run();
}
```

> 这里 `use std::io::Write;` 是必须的——`writeln!` 写入文件需要 `Write` trait 在作用域内。

---

## 四、tracing（异步可观测性框架）

### 4.1 简介

`tracing` 是 Rust 生态面向**异步/并发程序可观测性**的诊断框架。它不仅能像 `log` 一样记一条条日志事件（event），更重要的是引入了 **span（跨度/作用域）** 的概念。

- 可用 span 表示一次请求 / 一次任务 / 一次函数调用的执行上下文，并在 span 内持续产生事件。
- 这些 span 能**跨越 `await` 自动传播**，形成一棵结构化的调用树。
- 事件可携带键值字段（结构化日志），方便过滤、聚合、输出 JSON 等。

传统的 `log` 只是按级别输出文本信息（level + target + message），缺少 span 这种天然的上下文关联能力。在 Tokio 这类高并发异步场景，`tracing` 更容易把同一条请求链路上的日志串起来，而 `log` 往往只能靠手动打印 `request_id`、线程名拼上下文。

```toml
[dependencies]
tracing = "0.1.44"
tracing-subscriber = "0.3.23"
```

### 4.2 结构化事件 event

对 `log` 来说：

```rust
log::info!("user {} login from {}", user_id, ip);
```

这条日志最终就是一段文本（message），加上 level + target + 时间戳。但 `user_id`、`ip` 对系统来说只是字符串的一部分，很难做机器化分析。

在 `tracing` 中通常写：

```rust
tracing::info!(user_id = 42, ip = "1.2.3.4", "user login");
```

这条日志不是"拼出来的一行字符串"，而是一个 **Event**，包含：

- message：`"user login"`
- fields（结构化字段）：`user_id=42`、`ip="1.2.3.4"`

输出为 JSON 时概念上像这样：

```json
{
    "level": "INFO",
    "message": "user login",
    "user_id": 42,
    "ip": "1.2.3.4"
}
```

之后可方便统计：哪个用户请求最多、聚合某个 ip 的错误率，在 ELK/ClickHouse/Datadog 里按字段筛选。

### 4.3 跨度 span

span 代表一个范围或一段过程的上下文，例如：

- 一次 HTTP 请求：进来 → 处理 → 返回响应
- 一次数据库查询：发起 → 等待 → 拿到结果
- 一个异步任务：spawn 之后 → 完成之前

span 最关键的是可携带**上下文字段**（如 `request_id`、`user_id`、`method`、`path`）。一个函数就是一个 span 单元。

通过 `span!` 宏或 `info_span!` 等宏创建 span 区间。`span!` 是通用宏，需自己指定 level；`info_span!`、`debug_span!` 固定级别，是 `span!` 的便捷版本：

```rust
let span = tracing::span!(
    tracing::Level::INFO,
    "http_request",
    request_id = %req_id,
    method = %method,
    path = %path,
);
```

其中 `"http_request"` 是 span 名，`%value` 表示以 `Display` 格式输出，`?value` 表示以 `Debug` 格式输出。

通过 `enter()` 方法进入 span 区间：

```rust
let _enter = span.enter();
```

当 `_enter` 离开作用域时被 drop，即退出 span。之后在里面打的所有事件：

```rust
tracing::info!("do auth");
tracing::warn!("slow query");
```

都会自动携带这次请求的上下文 `request_id`、`method`、`path`。启用日志输出后端（`tracing_subscriber`）后，控制台可能看到类似：

```
INFO  http_request{request_id=1001 method=GET path=/api/user}: do auth
WARN  http_request{request_id=1001 method=GET path=/api/user}: slow query
```

### 4.4 订阅者 Subscriber

`tracing` 只是把"发生了什么（event）"以及"发生在什么上下文（span）"发出来，本身不会自动打印或写入文件。只有在二进制程序启动时安装一个全局 subscriber（最常见的就是 `tracing_subscriber`），这些 event/span 才会被收集并按规则处理——决定哪些级别输出、按 target/字段过滤、用文本还是 JSON 格式化、输出到控制台还是转发到文件/采集系统。

`tracing_subscriber::fmt` 提供的全局订阅者会把格式化后的日志写到 **stdout**。若想写文件，通常用 `tracing_appender::non_blocking` 做异步落盘——它会返回一个 `WorkerGuard`，**必须在 main 里把 guard 留住**，否则 guard 被提前丢弃会导致后台线程停止、缓冲日志刷不出去，看起来就像"没有写入"（详见 5.2 节实测）。

---

## 五、tracing_subscriber 基本使用

### 5.1 使用全局默认订阅者初始化

```rust
use tracing::{trace, debug, info, warn, error};

mod http {
    pub mod client {
        use tracing::{debug, info, warn};
        pub fn run() {
            warn!("client warn");
            info!("client info");
            debug!("client debug");
        }
    }
}

fn main() {
    // 安装默认的全局订阅者。默认级别与是否读 RUST_LOG 取决于 env-filter feature，
    // 详见下方对照表：未启用 feature 时默认 INFO 且不读 RUST_LOG。
    tracing_subscriber::fmt::init();

    trace!("This is a trace message");
    debug!("This is a debug message");
    info!("This is a info message");
    warn!("This is a warn message");
    error!("This is a error message");

    http::client::run();
}
```

说明：

- `fmt::init()` 等价于创建一个默认的 fmt subscriber 并设为全局默认 subscriber。
- **默认输出到 stdout**。
- **默认过滤级别与 `RUST_LOG` 是否生效，取决于是否启用 `env-filter` feature**——这是最容易踩的坑：

| `tracing-subscriber` feature | `RUST_LOG` 未设置时默认级别 | `RUST_LOG` 是否生效 |
|------------------------------|---------------------------|-------------------|
| 默认（**未**启用 `env-filter`） | **INFO 及以上** | ❌ 不生效 |
| 启用 `env-filter` | **ERROR** | ✅ 生效 |

  - **未启用 `env-filter`** 时，`fmt::init()` 不挂 `EnvFilter`，用一个静态的 `LevelFilter::INFO` 兜底，且**完全不读 `RUST_LOG`**——即使设了 `RUST_LOG=trace` 也仍是 INFO 及以上。
  - **启用 `env-filter`** 时，`fmt::init()` 才等价于 `fmt().with_env_filter(EnvFilter::from_default_env()).init()`，读取 `RUST_LOG`；`RUST_LOG` 未设置时 `from_default_env()` 的默认 directive 是 `LevelFilter::ERROR`，只输出 ERROR。

  > 因此原笔记"默认 INFO"在默认配置下成立，"读 RUST_LOG"则只有启用 `env-filter` 才成立；二者不能同时无条件为真。

本项目 `Cargo.toml` 里 `tracing-subscriber = "0.3.23"` 未启用 `env-filter`，故 `cargo run` 默认就输出 INFO。要让 `RUST_LOG` 生效，需在依赖里开 feature：

```toml
tracing-subscriber = { version = "0.3.23", features = ["env-filter"] }
```

实测对照（包名 `probe`，5 条 trace/debug/info/warn/error）：

```
# 未启用 env-filter，env -i 清空环境 → INFO 及以上
INFO  probe: info msg
WARN  probe: warn msg
ERROR probe: error msg

# 启用 env-filter，env -i 清空环境 → 仅 ERROR
ERROR probe: error msg

# 启用 env-filter，RUST_LOG=trace → 全部
TRACE probe: trace msg
DEBUG probe: debug msg
INFO  probe: info msg
WARN  probe: warn msg
ERROR probe: error msg
```

想在代码里**显式**控制级别（不依赖 feature 与环境变量），用 builder 链：

```rust
tracing_subscriber::fmt()
    .with_max_level(tracing::Level::INFO)   // 静态级别，不读 RUST_LOG
    .init();
```

### 5.2 输出日志到文件

```rust
use tracing::info;

fn main() {
    // 1. 创建日志文件
    let file = std::fs::OpenOptions::new()
        .create(true)
        .write(true)
        .truncate(true)
        .open("log.txt")
        .unwrap();

    // 2. 创建异步写入器：日志先写入内部队列，由后台线程刷入文件。
    //    _guard 是 WorkerGuard，主线程必须持有它，
    //    确保程序结束前把缓冲日志全部 flush。
    let (non_blocking, _guard) = tracing_appender::non_blocking(file);

    tracing_subscriber::fmt()
        .with_writer(non_blocking)  // 指定输出位置
        .with_ansi(false)            // 写文件不需要颜色
        .init();

    info!("This is an info message");
    info!("This is another info message");
}
```

> 需要额外依赖 `tracing-appender = "0.2.5"`。

**实测：WorkerGuard 提前丢弃会丢日志。** 若把 `drop(_guard);` 放在 `.init()` 之前，guard 一旦 drop 后台刷盘线程即停止，上面两条 info 全部丢失——`log.txt` 为 **0 字节**。因此 `_guard` 必须在 `main` 作用域里一直存活到程序结束。

### 5.3 滚动策略 + 自定义格式

可按天/小时/大小切分文件，避免单文件无限增长；也可自定义格式（时间戳、是否打印 target/level/span 等）。

```rust
use tracing::info;
use tracing_subscriber::fmt::time::FormatTime;
use tracing_subscriber::fmt::format::Writer;

// 自定义时间格式器（需额外依赖 chrono）
struct LocalTimer;

impl FormatTime for LocalTimer {
    fn format_time(&self, w: &mut Writer<'_>) -> std::fmt::Result {
        write!(w, "{}", chrono::Local::now().format("%F %T %.3f"))
    }
}

fn main() {
    // 按天滚动的文件 appender，文件放在当前目录，前缀 tracing.log
    let file_appender = tracing_appender::rolling::daily("./", "tracing.log");
    let (non_blocking, _guard) = tracing_appender::non_blocking(file_appender);

    let format = tracing_subscriber::fmt::format()
        .with_level(true)
        .with_target(true)
        .with_timer(LocalTimer);

    tracing_subscriber::fmt()
        .with_max_level(tracing::Level::TRACE)
        .with_writer(non_blocking)
        .with_ansi(false)
        .event_format(format)  // 设置事件格式
        .init();

    info!("This is an info message");
}
```

> 需额外依赖：`tracing-appender = "0.2.5"`、`chrono = "0.4"`。
>
> **避免使用 `tracing_subscriber::fmt::time::LocalTime`**：它需要启用 `local-time` feature 才能编译，且该 feature 依赖 `unsound_local_offset`，存在已知的非安全性问题。上面用 `chrono` + 自定义 `FormatTime` 是更稳妥的本地时间方案。

### 5.4 `#[instrument]` 为函数设置 span

`#[instrument]` 标记函数，让整个函数进入 span：

```rust
use tracing::{event, instrument, Level};

#[instrument]
fn hello() {
    event!(Level::INFO, val = 3, "Hello");
}
```

- 进入函数时创建 span（默认 span 名 = 函数名）。
- **默认把函数参数记录成字段**。
- 函数内部的事件自动带上该 span 上下文（span 名、字段）。

实测输出（`RUST_LOG=trace`）：

```
INFO hello{name="world"}: Hello world
```

可见 `hello` 函数的 `name` 参数被自动记录为 span 字段。

常用配置：

```rust
// 跳过大对象/敏感参数（避免日志过大或泄密）
#[instrument(skip(req, body))]
fn handler(req: Request, body: Bytes) { ... }

// 自定义 span 名
#[instrument(name = "hello_span")]
fn hello() { ... }

// 记录返回值错误（需配合 Result）：
//   返回 Err(e) 时自动把 e 记录到 span；
//   返回 Ok(v) 时自动把 v 记录到 span。
#[instrument(err, ret)]
fn do_work() -> Result<u32, MyErr> { ... }
```

完整示例：

```rust
use tracing::{trace, debug, info, warn, error, instrument, event, Level};

#[instrument]
fn hello(name: String) {
    event!(Level::INFO, "Hello {}", name);
}

mod http {
    pub mod client {
        use tracing::{debug, info, instrument, warn};

        #[instrument]
        pub fn run() {
            warn!("client warn");
            info!("client info");
            debug!("client debug");
        }
    }
}

fn main() {
    tracing_subscriber::fmt::init();

    trace!("This is a trace message");
    debug!("This is a debug message");
    info!("This is a info message");
    warn!("This is a warn message");
    error!("This is a error message");

    http::client::run();
    hello("world".to_string());
}
```

### 5.5 配置 layer 层 + 日志级别过滤

想把日志同时输出到多个位置，可通过多个 fmt layer + registry：

```rust
use std::fs::OpenOptions;
use tracing::{trace, debug, info, warn, error, instrument};
use tracing_subscriber::EnvFilter;
use tracing_subscriber::filter::LevelFilter;
use tracing_subscriber::layer::SubscriberExt;
use tracing_subscriber::util::SubscriberInitExt;

#[instrument]
fn hello(name: String) {
    info!("Hello {}", name);
}

mod http {
    pub mod client {
        use tracing::{debug, info, instrument, warn};

        #[instrument]
        pub fn run() {
            warn!("client warn");
            info!("client info");
            debug!("client debug");
        }
    }
}

fn main() {
    // 1. 打开日志文件
    let file = OpenOptions::new()
        .create(true)
        .write(true)
        .truncate(true)
        .open("tracing.log")
        .unwrap();

    // 2. 异步写入缓冲
    let (non_blocking, _guard) = tracing_appender::non_blocking(file);

    // 3. 文件 layer
    let file_layer = tracing_subscriber::fmt::layer()
        .with_writer(non_blocking)
        .with_ansi(false);

    // 4. stdout layer
    let stdout_layer = tracing_subscriber::fmt::layer()
        .with_writer(std::io::stdout)
        .with_ansi(true);

    tracing_subscriber::registry()
        .with(stdout_layer)
        .with(file_layer)
        .with(if cfg!(debug_assertions) {
            LevelFilter::TRACE
        } else {
            LevelFilter::OFF
        })
        .with(EnvFilter::try_from_default_env().unwrap_or_else(|_| EnvFilter::new("info")))
        .init();

    trace!("This is a trace message");
    debug!("This is a debug message");
    info!("This is a info message");
    warn!("This is a warn message");
    error!("This is a error message");

    http::client::run();
    hello("world".to_string());
}
```

> 需额外依赖 `tracing-appender = "0.2.5"`，且 `tracing-subscriber` 要启用 `env-filter` feature：
> `tracing-subscriber = { version = "0.3.23", features = ["env-filter"] }`

上述例子有两类过滤：

- **`LevelFilter`（编译构建差异）**
  ```rust
  .with(if cfg!(debug_assertions) { LevelFilter::TRACE } else { LevelFilter::OFF })
  ```
  Debug 构建允许 TRACE..ERROR，Release 构建则全部关闭。

- **`EnvFilter`（运行时环境变量）**
  ```rust
  .with(EnvFilter::try_from_default_env().unwrap_or_else(|_| EnvFilter::new("info")))
  ```
  从 `RUST_LOG` 读取过滤规则，没设置则默认 info 及以上。

**最终生效规则取两类过滤的交集**。实测（Debug 构建、`RUST_LOG` 未设置）：`LevelFilter::TRACE` ∩ `EnvFilter("info")` = info 及以上输出，trace/debug 被过滤——stdout 与 `tracing.log` 同时输出 info/warn/error 三条。

---

## 六、常见坑

1. **`tracing` 不初始化 subscriber 就没有输出**。`tracing::info!` 只是发布事件，没有 subscriber 收集就不会被处理。本项目 `examples/fundamentals.rs` 就没初始化 subscriber，运行后看不到任何 tracing 输出——必须先 `tracing_subscriber::fmt::init()`（或手动 `set_global_default`）。

2. **`fmt::init()` 的默认级别和 `RUST_LOG` 是否生效，取决于 `env-filter` feature**。未启用时默认 INFO 且不读 `RUST_LOG`；启用时默认 ERROR 且读 `RUST_LOG`。不要想当然地认为"默认 INFO"或"默认 ERROR"，先确认依赖里是否开了 `features = ["env-filter"]`。详见 5.1 节对照表。

3. **`WorkerGuard` 必须持有到 main 结束**。`tracing_appender::non_blocking` 返回的 `_guard` 一旦提前 drop，后台刷盘线程停止，缓冲中的日志会全部丢失（实测文件 0 字节）。不要把它放进会提前结束的子作用域。

4. **`tracing::log::LevelFilter` 是内部 API**。该模块被 `#[cfg(feature = "log")]` 门控且 `#[doc(hidden)]`，是 `tracing` 内部桥接用，不应在应用代码里 import。需要 `LevelFilter` 时直接用 `tracing_subscriber::filter::LevelFilter`。

5. **`LocalTime` 需要 `local-time` feature 且 `unsound`**。`tracing_subscriber::fmt::time::LocalTime` 在未启用 `local-time` feature 时**编译不过**，且该 feature 依赖 `unsound_local_offset` 有非安全性争议。需要本地时间用 `chrono` + 自定义 `FormatTime`（见 5.3）。

6. **不要引入用不到的依赖**。本项目曾引入 `tracing-flame` 但代码无任何引用，徒增编译开销。`cargo machete` 或人工核查可发现这类废弃依赖。

7. **库代码不要初始化全局 logger**。全局 logger/subscriber 只能初始化一次，库主动初始化会干扰应用层配置。库只管用宏记日志，初始化交给最终二进制。

8. **包名与目录名不一致**会带来混淆。本项目曾出现包名 `rust-tracing-guide` 与目录名 `rust-tracing-primer` 不一致，已统一为 `rust-tracing-primer`。

---

## 七、参考资源

官方文档：

- [tracing crate 文档](https://docs.rs/tracing/latest/tracing/)
- [tracing-subscriber 文档](https://docs.rs/tracing-subscriber/latest/tracing_subscriber/)
- [log crate 文档](https://docs.rs/log/latest/log/)
- [env_logger 文档](https://docs.rs/env_logger/latest/env_logger/)

社区资源：

- [Decrusting the tracing crate（视频）](https://www.youtube.com/watch?v=21rtHinFA40)
- [Are we observable yet? An introduction to Rust telemetry](https://www.lpalmieri.com/posts/2020-09-27-zero-to-production-4-are-we-observable-yet/)
- [Get started with Tracing in Rust](https://www.shuttle.rs/blog/2024/01/09/getting-started-tracing-rust)
- [Tokio 官方 tracing 介绍博客](https://tokio.rs/blog/2019-08-tracing)
