# 一、概述

## 1、Rust日志生态

日志用于记录程序运行过程中发生的事件，例如服务启动、请求完成、重试、错误和性能异常。

在 Rust 中，日志通常分为两套生态：

| 方案                               | 核心能力             | 适合场景                 |
| -------------------------------- | ---------------- | -------------------- |
| `log` + `env_logger`             | 传统文本日志           | 小型程序、同步程序、库的通用日志接口   |
| `tracing` + `tracing-subscriber` | 结构化事件、Span、上下文传播 | Tokio、Web 服务、高并发异步程序 |
其中：

- `log`和`tracing`负责在代码中记录事件
- `env-logger`和`tracing-subscriber`负责过滤、格式化和输出

它们都采用“记录接口”+“输出实现”的分离设计。

- 库通常只记录日志，不负责初始化，因此之需要依赖`log`或`tracing`。
- 最终二进制程序负责选择输出方式并完成初始化

## 2、日志级别

`log`和`tracing`都提供五个日志级别（从高到低）：

| 级别      | 含义             | 常见场景             |
| ------- | -------------- | ---------------- |
| `ERROR` | 当前操作失败，需要处理    | 数据写入失败、服务依赖不可用   |
| `WARN`  | 出现异常情况，但程序仍能继续 | 请求重试、使用默认配置      |
| `INFO`  | 重要的业务和生命周期信息   | 服务启动、任务完成、请求结果   |
| `DEBUG` | 开发和排查问题需要的细节   | 参数、分支、内部状态       |
| `TRACE` | 最细粒度的执行过程      | 底层协议、循环步骤、频繁状态变化 |

**过滤级别**表示允许输出的最低严重程度。例如，当设置过滤级别为`INFO`时，会输出`INFO`及`INFO`以上的日志事件，而不会输出`DEBUG`和`TRACE`。

生产环境通常以`INFO`为默认级别，再针对特定模块临时开启`DEBUG`。如果长期全量开启`TRACE`，不仅会产生大量日志，还可能明显增加格式化、I/O和存储开销。


## 3、如何选择

如果只是编写简单命令行工具，或者只需要普通文本日志，可以使用：

```
log + env_logger
```

如果程序使用 Tokio 等异步框架，通常优先使用：

```
tracing + tracing-subscriber
```

`tracing`不仅能记录发生了什么，还可以记录事件所属的请求、任务或函数调用上下文。在多个异步任务交错执行时，这种上下文信息要比单独的文本日志更重要。


# 二、log与env_logger

## 1、log与env_logger的职责

`log`和`env_logger`不是两个功能重复的日志库，而是分别负责日志系统的不同部分：

| Crate        | 职责                   |
| ------------ | -------------------- |
| `log`        | 提供统一的日志宏和接口，负责产生日志记录 |
| `env_logger` | 接收`log`产生的记录，过滤并输出   |

`log`是一个日志门面库。代码通过`error!`、`warn!`、`info!`、`debug!`和`trace!`等宏记录日志，但`log`本身不负责输出。

`env_logger`是`log`的一种具体实现。应用程序调用`env_logger::init()`后，它会注册为全局 logger，接收`log`产生的日志记录，并根据`RUST_LOG`等环境变量配置决定是否输出。

两者的关系可以简单理解为：

```text
业务代码
   │
   │ 调用 log 宏
   ▼
log 日志门面
   │
   │ 转交日志记录
   ▼
env_logger
   │
   ▼
终端
```

## 2、基本使用

```toml
[dependencies]
log = "0.4"
env_logger = "0.11"
```

`log`提供五个常用宏：

```rust
use log::{debug, error, info, trace, warn};

fn main() {
    // 初始化日志实现。应该在程序入口尽早调用，并且只调用一次。
    env_logger::init();

    error!("database connection failed");
    warn!("retrying request");
    info!("server started");
    debug!("configuration loaded");
    trace!("polling connection");
}
```

不设置`RUST_LOG`，直接运行`cargo run`：

![[Pasted image 20260625001329.png|500]]

默认只会看到`ERROR`日志。

这是因为`env_logger`在没有读取到过滤规则时，默认过滤级别是`ERROR`。`WARN`、`INFO`、`DEBUG`和`TRACE`的级别都低于`ERROR`，因此会被过滤。

如果设置`RUST_LOG`，例如：

```shell
RUST_LOG=debug cargo run
```

则会输出`DEBUG`及以上级别：

![[Pasted image 20260625002111.png|500]]

`TRACE`仍然不会输出，因为它低于当前设置的`DEBUG`级别。如果使用`RUST_LOG=trace`，五个级别才会全部输出。

除了输出日志内容，每条日志记录还带有如下格式：

```
[2026-06-24T16:21:02Z ERROR hello_cargo]
```

表示时间、日志级别和 target。其中 target 表示日志来源和分类，默认通常是日志宏所在的模块路径。

如果没有初始化`env_logger`等具体实现，`log`产生的记录没有接收者，通常不会看到任何输出。例如这里的`hello_cargo`就是 target。

## 3、库和应用的职责

库代码通常只依赖`log`，负责记录对调用者有价值的信息：

```rust
pub fn parse_config(input: &str) {  
    log::debug!("parsing config: {}", input); 
}
```

最终的应用程序同时依赖`log`和某个日志实现，并负责初始化：

```rust
fn main() {
	env_logger::init();

    my_library::run();
}
```

全局 logger 只能成功初始化一次。库如果主动调用`env_logger::init()`，会剥夺应用程序选择日志格式、过滤规则和输出位置的权利，因此初始化逻辑应该放在二进制入口。

## 4、RUST_LOG过滤

`env_logger`通常通过`RUST_LOG`环境变量控制日志级别：

```shell
RUST_LOG=info cargo run
```

只为某个模块开启更详细的日志：

```shell
RUST_LOG=info, my_app::network=debug cargo run
```

这表示：

- 默认只输出`WARN`及以上
- `myapp:network`模块输出`DEBUG`及以上

如果希望环境变量未设置时使用默认级别，可以使用`Builder`：

```rust
use log::{error, warn, info, debug, trace};  
  
  
fn main() {  
  
    env_logger::Builder::from_env(env_logger::Env::default().default_filter_or("info"))  
        .init();  
  
    error!("database connection failed");  
    warn!("retrying request");  
    info!("server started");  
    debug!("configuration loaded");  
    trace!("polling connection");  
  
}
```

这段配置仍然优先读取`RUST_LOG`。如果没有设置环境变量，则使用`INFO`作为默认级别，因此上面的`server started`会正常输出。

`default_filter_or("info")`的作用不是覆盖环境变量，而是只在环境变量没有提供有效规则时设置默认值。

默认情况下，`env_logger`将日志写入`stderr`。如果需要输出到`stdout`：

```rust
use log::{error, warn, info, debug, trace};  
  
  
fn main() {  
  
    env_logger::Builder::from_env(env_logger::Env::default().default_filter_or("info"))  
        .target(env_logger::Target::Stdout)  
        .init();  
  
    error!("database connection failed");  
    warn!("retrying request");  
    info!("server started");  
    debug!("configuration loaded");  
    trace!("polling connection");  
  
}
```

修改输出流不会改变过滤规则和日志内容，只是把日志从标准错误流改为标准输出。这个差异在终端里通常看不出来，但会影响 shell 重定向、管道和容器日志采集。

## 5、日志target

每条日志记录都有一个 target，用于表示这条日志来自哪里，或者属于哪一类。它主要用于显示日志来源和配置过滤规则。

默认情况下，target 是日志宏所在Rust 模块路径。例如下面的日志写在`hello_cargo::network`模块中：

```rust
use log::{error, warn, info, debug, trace};  
  
mod network {  
    use log::info;  
  
    pub fn connect() {  
        info!("Connecting to server");  
    }  
}  
  
fn main() {  
  
    env_logger::init();  
  
    network::connect();  
  
}
```

执行：

```shell
RUST_LOG=info cargo run
```

结果：

```text
[2026-06-24T17:06:45Z INFO  hello_cargo::network] Connecting to server
```

其中`hello_cargo::network`就是这条日志的 target。

也可以在日志宏里手动指定`target`：

```rust
info!(target: "net", "Connecting to server");
```

可以通过 target 单独过滤：

```shell
RUST_LOG=warn,net=info cargo run
```

在这个规则下，默认只允许`WARN`及以上，但 target 为`net`的日志允许`INFO`及以上。

对于普通日志，模块路径已经足够。只有在需要按业务类别过滤，而模块边界又不能表达这种分类时，才自定义`target`。


## 6、log与env-logger的局限

传统日志记录通常是一条独立文本：

```rust
log::info!("request {} completed with status {}", request_id, status);
```

在高并发异步程序中，不同请求可能在同一线程上交错执行。为了关联同一请求的日志，只能在每一条日志中重复添加`request_id`等上下文。

`tracing`通过结构化字段和 Span 解决了这个问题。


# 三、tracing 核心模型

## 1、tracing与tracing-subscriber的职责

`tracing`生态同样把“记录”和“处理”分开：

| Crate                | 职责                        |
| -------------------- | ------------------------- |
| `tracing`            | 提供 Event、Span、日志宏和插桩接口    |
| `tracing-subscriber` | 收集、过滤、格式化并输出 Event 与 Span |
如果只依赖`tracing`并调用`info!`等宏，却没有安装 Subscriber，产生的 Event 和 Span 就没有接收者，就看到任何输出。

## 2、Event、Span和Subscriber

`tracing`有三个核心概念：

- **Event**：某个时间点发生的事件，类似一条日志
- **Span**：一条有开始和结束的执行上下文
- **Subscriber**：收集、过滤、格式化输出 Event 和 Span

普通日志描述的是某个瞬间发生的事情：

```rust
info!("开始查询用户");  
error!("数据库连接失败");
```

这种记录在`tracing`中通常叫`Event`，即某一事件点发生的一件事。

而`Span`不是某一条日志，而是一个有开始、有结束、内部还包含其他日志和子过程的范围。

例如：

```rust
let span = tracing::info_span!("handle_request", request_id = 42)'
let _guard = span.enter();  // 进入上下文

tracing::info!("开始处理请求");
do_something();
tracing::info!("请求处理完成")；
```

这里的`handle_request`就是一个`Span`，可理解为：

```
handle_request(request_id = 42)  
├── 开始处理请求  
├── do_something  
└── 请求处理完成
```

`Span`为内部所有事情提供了共同上下文：`request_id = 42`。


## 3、基本使用

添加依赖：

```toml
[dependencies]
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

在程序入口初始化 Subscriber 后，就可以使用`tracing`提供的日志宏：

```rust
use tracing::{debug, error, info, trace, warn};
use tracing_subscriber::EnvFilter;

fn main() {
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info"));

    tracing_subscriber::fmt()
        .with_env_filter(filter)
        .init();

    error!("database connection failed");
    warn!("retrying request");
    info!("server started");
    debug!("configuration loaded");
    trace!("polling connection");
}
```

输出：

![[Pasted image 20260625020433.png|600]]

`EnvFilter`为过滤器，负责根据规则过滤`Event`和`Span`，判断哪些可以交给 Subscriber 处理。

`EnvFilter::try_from_default_env()`尝试从默认环境变量`RUST_LOG`读取过滤规则，返回一个`Result<EnvFilter, _>`：

- 设置了有效的`RUST_LOG`：返回`Ok(filter)`
- 如果没有设置或规则无效：返回`Err(...)`

如果没有设置或规则无效，则默认使用`EnvFilter::new("info")`指定默认过滤级别为`INFO`。

`tracing_subscriber::fmt()`创建一个用于格式化日志并写入终端的`SubscriberBuilder`。

`.with_env_filter`则用于把前面创建的`EnvFilter`安装到 Subscriber 上。

`.init`构建 Subscriber，并注册为全局默认Subscriber。

`fmt()`返回的是 builder，因此可以通过链式方法继续配置时间、target、线程 ID、JSON 格式和输出位置。

`init()`完成后，后续`error!`、`info!`等宏产生的 Event 才真正写入目标。

全局 Subscriber 通常只能初始化一次。如果重复调用`init()`，程序会发生 panic。因此，初始化代码一般集中放在`main`函数开头。

`tracing_subscriber`默认过滤规则是`INFO`。

如果运行：

```shell
RUST_LOG=debug cargo run
```

则`EnvFilter::try_from_default_env()`会成功读取环境变量，`DEBUG`日志也会输出。


## 4、结构化日志

`tracing`的宏不仅可以能记录消息，还能独立记录字段：

```rust
use tracing_subscriber::EnvFilter;  
use tracing::{error, warn, info, debug, trace};  
  
fn main() {  
  
    let filter = EnvFilter::try_from_default_env()  
        .unwrap_or_else(|_| EnvFilter::new("info"));  
  
    tracing_subscriber::fmt()  
        .with_env_filter(filter)  
        .init();  
  
    let user_id = 42;  
    let status = 200;  
    let elapsed_ms = 18;  
  
    info!(user_id, status, elapsed_ms, "request completed");  
  
}
```

输出：

```text
2026-06-24T18:16:31.455166Z  INFO hello_cargo: request completed user_id=42 status=200 elapsed_ms=18
```

这里的`user_id`、`status`和`elapsed_ms`是独立的结构化字段，不只是消息字符串的一部分。文本输出会把字段格式化到同一行；如果改用 JSON 输出，日志平台就可以直接按这些字段查询和聚合。

## 5、字段记录方式

字段常见写法如下：

```rust
tracing::info!(
    user_id = 42,
    success = true,
    method = "GET",
    "request completed"
);
```

如果字段名和变量名相同，可以简写：

```rust
let user_id = 42;
let status = 200;

tracing::info!(user_id, status, "request completed");
```

`?`表示使用`Debug`格式，`%`表示使用`Display`格式：

```rust
tracing::debug!(request = ?request, "received request");
tracing::warn!(error = %error, "request failed");
```

常见选择：

- 普通数字、布尔值和字符串：直接记录
- 自定义结构体：使用`?value`
- 错误、URL、ID等实现了`Display`的值：使用`%value`

错误日志应该同时包含稳定的事件描述和错误字段：

```rust
tracing::error!(
    error = %err,
    user_id,
    "failed to update user"
);
```
