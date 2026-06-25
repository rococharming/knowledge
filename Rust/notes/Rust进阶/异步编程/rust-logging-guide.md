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
- `env_logger`和`tracing-subscriber`负责过滤、格式化和输出
- `tracing-appender`负责文件滚动和非阻塞写入

它们都采用“记录接口”和“输出实现”分离的设计。库通常只记录日志，不负责初始化全局日志系统；最终的二进制程序负责选择输出方式并完成初始化。

## 2、日志级别

`log`和`tracing`都提供五个日志级别：

| 级别      | 含义             | 常见场景             |
| ------- | -------------- | ---------------- |
| `ERROR` | 当前操作失败，需要处理    | 数据写入失败、服务依赖不可用   |
| `WARN`  | 出现异常情况，但程序仍能继续 | 请求重试、使用默认配置      |
| `INFO`  | 重要的业务和生命周期信息   | 服务启动、任务完成、请求结果   |
| `DEBUG` | 开发和排查问题需要的细节   | 参数、分支、内部状态       |
| `TRACE` | 最细粒度的执行过程      | 底层协议、循环步骤、频繁状态变化 |

过滤级别表示允许输出的最低严重程度。例如设置为`INFO`时，会输出`INFO`、`WARN`和`ERROR`，不会输出`DEBUG`和`TRACE`。

生产环境通常以`INFO`为默认级别，再针对特定模块临时开启`DEBUG`。如果长期全量开启`TRACE`，不仅会产生大量日志，还可能明显增加格式化、I/O和存储开销。

## 3、如何选择

如果只是编写简单命令行工具，或者只需要普通文本日志，可以使用：

```text
log + env_logger
```

如果程序使用 Tokio、Axum、Tonic 等异步框架，通常优先使用：

```text
tracing + tracing-subscriber
```

`tracing`不仅能记录“发生了什么”，还可以记录事件所属的请求、任务或函数调用上下文。在多个异步任务交错执行时，这种上下文信息比单独的文本日志更重要。


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

不设置`RUST_LOG`，直接运行：

```shell
cargo run
```

默认只会看到`ERROR`日志，输出的关键部分类似：

```text
ERROR ... database connection failed
```

这是因为`env_logger`在没有读取到过滤规则时，默认过滤级别是`ERROR`。`WARN`、`INFO`、`DEBUG`和`TRACE`的级别都低于`ERROR`，因此会被过滤。

如果设置：

```shell
RUST_LOG=debug cargo run
```

则会输出`DEBUG`及以上级别：

```text
ERROR ... database connection failed
WARN  ... retrying request
INFO  ... server started
DEBUG ... configuration loaded
```

`TRACE`仍然不会输出，因为它低于当前设置的`DEBUG`级别。如果使用`RUST_LOG=trace`，五个级别才会全部输出。

> 实际输出通常还包含时间、日志来源和颜色。其中“日志来源”就是后文介绍的`target`，默认值通常是产生日志的 Rust 模块路径，例如`my_app::network`。这里及后文只展示与当前知识点有关的关键内容。

如果没有初始化`env_logger`等具体实现，`log`产生的记录没有接收者，通常不会看到任何输出。

## 3、库和应用的职责

库代码通常只依赖`log`，负责记录对调用者有价值的信息：

```rust
pub fn parse_config(input: &str) {
    log::debug!("parsing config, length = {}", input.len());
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
RUST_LOG=warn,my_app::network=debug cargo run
```

这表示：

- 默认只输出`WARN`及以上
- `my_app::network`模块输出`DEBUG`及以上

如果希望环境变量未设置时使用默认级别，可以使用`Builder`：

```rust
fn main() {
    env_logger::Builder::from_env(
        env_logger::Env::default().default_filter_or("info"),
    )
    .init();

    log::info!("server started");
}
```

这段配置仍然优先读取`RUST_LOG`。如果没有设置环境变量，则使用`INFO`作为默认级别，因此上面的`server started`会正常输出：

```text
INFO ... server started
```

`default_filter_or("info")`的作用不是覆盖环境变量，而是只在环境变量没有提供有效规则时设置默认值。

默认情况下，`env_logger`将日志写入`stderr`。如果需要输出到`stdout`：

```rust
fn main() {
    env_logger::Builder::from_env(
        env_logger::Env::default().default_filter_or("info"),
    )
    .target(env_logger::Target::Stdout)
    .init();
}
```

修改输出流不会改变过滤规则和日志内容，只是把日志从标准错误流改为标准输出。这个差异在终端里通常看不出来，但会影响 shell 重定向、管道和容器日志采集。

> 这里`Target::Stdout`中的 Target 表示**输出目标**，与下一节表示**日志来源或分类**的日志`target`不是同一个概念。

## 5、日志target

每条日志记录都有一个`target`，用于表示这条日志来自哪里，或者属于哪一类。它主要用于显示日志来源和配置过滤规则。

默认情况下，target 是日志宏所在的 Rust 模块路径。例如下面的日志写在`my_app::network`模块中：

```rust
mod network {
    pub fn connect() {
        log::info!("connected");
    }
}
```

它的输出可能类似：

```text
INFO my_app::network ... connected
```

其中`my_app::network`就是这条日志的 target。

也可以在日志宏中手动指定 target：

```rust
log::info!(target: "http_request", "request completed");
```

可以通过 target 单独过滤：

```shell
RUST_LOG=warn,http_request=info cargo run
```

在这个规则下，默认只允许`WARN`及以上，但 target 为`http_request`的日志允许`INFO`及以上，因此前面的`request completed`仍然会输出：

```text
INFO http_request ... request completed
```

如果去掉`http_request=info`，这条`INFO`日志就会被默认的`WARN`规则过滤。

对于普通日志，模块路径通常已经足够。只有在需要按业务类别过滤，而模块边界又不能表达这种分类时，才需要自定义 target。

## 6、log与env_logger的局限

传统日志记录通常是一条独立文本：

```rust
log::info!("request {} completed with status {}", request_id, status);
```

在高并发异步程序中，不同请求可能在同一线程上交错执行。为了关联同一请求的日志，只能在每一条日志中重复添加`request_id`等上下文。

`tracing`通过结构化字段和 Span 解决了这个问题。


# 三、tracing核心模型

## 1、tracing与tracing-subscriber的职责

`tracing`生态同样把“记录”和“处理”分开：

| Crate                | 职责                        |
| -------------------- | ------------------------- |
| `tracing`            | 提供 Event、Span、日志宏和插桩接口    |
| `tracing-subscriber` | 收集、过滤、格式化并输出 Event 与 Span |

如果只依赖`tracing`并调用`info!`等宏，却没有安装 Subscriber，产生的 Event 和 Span 就没有接收者，通常不会看到任何输出。

## 2、Event、Span和Subscriber

`tracing`有三个核心概念：

| 概念 | 含义 |
| --- | --- |
| Event | 某个时间点发生的事件，类似一条日志 |
| Span | 一段有开始和结束的执行上下文 |
| Subscriber | 收集、过滤、格式化和输出 Event 与 Span |

例如，一次 HTTP 请求可以表示为一个 Span：

```text
http_request{request_id=42 method=GET path=/users}
├── 开始校验身份
├── 查询数据库
└── 返回响应
```

Span 保存请求级上下文，内部产生的 Event 自动归属于这个 Span，不需要每一条日志都重复拼接请求信息。

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

下面逐步拆解这段代码。

首先导入五个日志宏：

```rust
use tracing::{debug, error, info, trace, warn};
```

这些宏用于产生不同级别的 Event。它们只负责记录事件，不负责过滤、格式化和输出：

| 宏 | 级别 | 常见用途 |
| --- | --- | --- |
| `error!` | `ERROR` | 当前操作已经失败 |
| `warn!` | `WARN` | 出现异常，但程序仍可继续 |
| `info!` | `INFO` | 重要的运行状态和业务事件 |
| `debug!` | `DEBUG` | 开发和排查问题需要的细节 |
| `trace!` | `TRACE` | 最细粒度的执行过程 |

然后导入环境变量过滤器：

```rust
use tracing_subscriber::EnvFilter;
```

`EnvFilter`属于`tracing-subscriber`，负责根据类似`info`、`debug`或`my_app::network=trace`的规则判断哪些 Event 和 Span 可以继续交给 Subscriber 处理。

接下来创建过滤器：

```rust
let filter = EnvFilter::try_from_default_env()
    .unwrap_or_else(|_| EnvFilter::new("info"));
```

这一段可以拆成两步理解。

第一步：

```rust
EnvFilter::try_from_default_env()
```

它尝试从默认环境变量`RUST_LOG`读取过滤规则，返回一个`Result<EnvFilter, _>`：

- 设置了有效的`RUST_LOG`：返回`Ok(filter)`
- 没有设置或规则无效：返回`Err(...)`

例如：

```shell
RUST_LOG=debug cargo run
```

会创建允许`DEBUG`及以上级别通过的过滤器。

第二步：

```rust
.unwrap_or_else(|_| EnvFilter::new("info"))
```

`unwrap_or_else`是`Result`的方法：

- 如果前一步是`Ok(filter)`，直接取出其中的`filter`
- 如果前一步是`Err(...)`，执行闭包`|_| EnvFilter::new("info")`

闭包参数`_`表示忽略具体错误，`EnvFilter::new("info")`则创建一个默认允许`INFO`及以上级别的过滤器。

因此，这两行代码表达的是：

```text
优先使用 RUST_LOG
        │
        ├── 读取成功 → 使用环境变量中的规则
        │
        └── 读取失败 → 使用默认规则 info
```

得到过滤器后，创建并初始化 Subscriber：

```rust
tracing_subscriber::fmt()
    .with_env_filter(filter)
    .init();
```

这条调用链包含三个步骤：

| 调用                          | 作用                                   |
| --------------------------- | ------------------------------------ |
| `tracing_subscriber::fmt()` | 创建一个用于格式化日志并写入终端的 Subscriber builder |
| `.with_env_filter(filter)`  | 把前面创建的`EnvFilter`安装到 Subscriber 上    |
| `.init()`                   | 构建 Subscriber，并注册为全局默认 Subscriber    |

`fmt()`返回的是 builder，因此可以通过链式方法继续配置时间、target、线程 ID、JSON 格式和输出位置。

`init()`完成后，后续`error!`、`info!`等宏产生的 Event 才会进入这套处理流程：

```text
tracing日志宏
      │
      ▼
EnvFilter判断是否保留
      │
      ▼
fmt Subscriber格式化
      │
      ▼
终端输出
```

全局 Subscriber 通常只能初始化一次。如果重复调用`init()`，程序会发生 panic。因此，初始化代码一般集中放在`main`函数开头。

不设置`RUST_LOG`时，输出的关键部分类似：

```text
ERROR ... database connection failed
WARN  ... retrying request
INFO  ... server started
```

`DEBUG`和`TRACE`不会输出。原因不是`tracing`自身存在固定的默认级别，而是这段代码通过`unwrap_or_else`显式把默认过滤规则设置成了`INFO`。

如果运行：

```shell
RUST_LOG=debug cargo run
```

则`EnvFilter::try_from_default_env()`会成功读取环境变量，`DEBUG`日志也会输出。过滤和格式化的更多配置会在后文介绍。

## 4、记录结构化Event

`tracing`的宏不仅能记录消息，还能记录独立字段：

```rust
let user_id = 42;
let status = 200;
let elapsed_ms = 18;

tracing::info!(
    user_id,
    status,
    elapsed_ms,
    "request completed"
);
```

使用默认文本格式时，输出的关键部分类似：

```text
INFO ... request completed user_id=42 status=200 elapsed_ms=18
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

不要只记录：

```rust
tracing::error!("{err}");
```

只有错误文本时，很难知道错误发生在哪个操作、影响了哪个对象。

## 6、Span

可以使用`info_span!`等宏创建 Span：

```rust
use tracing::info_span;

fn handle_request(request_id: u64) {
    let span = info_span!("http_request", request_id);
    let _guard = span.enter();

    tracing::info!("validating request");
    tracing::info!("request completed");
}
```

`enter()`返回一个 guard。guard 存活期间，当前执行流位于该 Span 中；guard 被丢弃时退出 Span。

假设程序已经初始化格式化 Subscriber，输出的关键部分类似：

```text
INFO http_request{request_id=42}: validating request
INFO http_request{request_id=42}: request completed
```

两条 Event 都包含`http_request`及其`request_id`字段，因为它们发生在同一个 Span 中。这正是 Span 相比重复手写`request_id`的价值。

这种写法适合同步代码，但不能直接照搬到异步函数中。

## 7、异步代码不能跨await持有EnterGuard

下面的写法是错误的：

```rust
async fn handle_request(request_id: u64) {
    let span = tracing::info_span!("http_request", request_id);
    let _guard = span.enter();

    load_user().await;
    save_record().await;
}
```

异步任务在`.await`处可能暂停，运行时线程会继续执行其他任务。此时`_guard`仍然存活，可能让同一线程上其他任务产生的事件错误地进入当前 Span。

因此，`Span::enter()`的 guard 不应该跨越`.await`。

异步函数优先使用`#[instrument]`：

```rust
use tracing::instrument;

#[instrument]
async fn handle_request(request_id: u64) {
    tracing::info!("validating request");

    load_user().await;

    tracing::info!("request completed");
}
```

`#[instrument]`会为每次函数调用创建 Span，并在 Future 每次被轮询时进入对应 Span，能够正确适配异步任务的暂停和恢复。

输出效果与同步 Span 类似：

```text
INFO handle_request{request_id=42}: validating request
INFO handle_request{request_id=42}: request completed
```

区别在于 Span 会随着 Future 的每次轮询正确进入和退出，不会因为任务在`.await`处暂停而污染同一线程上其他任务的上下文。

## 8、instrument属性

默认情况下，`#[instrument]`会：

- 使用函数名作为 Span 名
- 使用`Debug`记录函数参数
- 让函数内部的 Event 继承这个 Span

```rust
#[tracing::instrument]
async fn find_user(user_id: u64) -> Result<User, AppError> {
    tracing::debug!("querying database");

    database_find_user(user_id).await
}
```

对于大型对象、敏感信息或没有实现`Debug`的参数，使用`skip`：

```rust
#[tracing::instrument(skip(db, password))]
async fn login(
    db: &Database,
    user_id: u64,
    password: &str,
) -> Result<User, AppError> {
    authenticate(db, user_id, password).await
}
```

常用配置：

```rust
#[tracing::instrument(
    name = "create_order",
    level = "info",
    skip(db, request),
    fields(
        user_id = request.user_id,
        order_id = tracing::field::Empty,
    ),
    err
)]
async fn create_order(
    db: &Database,
    request: CreateOrder,
) -> Result<Order, AppError> {
    let order = db.insert_order(request).await?;

    tracing::Span::current().record("order_id", order.id);

    Ok(order)
}
```

当函数成功返回时，`order_id`会在数据库写入完成后补充到当前 Span。返回`Err`时，`err`会自动生成一条错误事件。

概念上的输出可能类似：

```text
ERROR create_order{user_id=42}: error=database unavailable
```

因为数据库写入失败时还没有获得订单 ID，所以`order_id`仍为空，不会显示具体值。具体格式由 Subscriber 决定。使用`err`后，上层通常不应再无差别地记录一次同样的错误，否则容易产生重复日志。

其中：

- `name`：自定义 Span 名
- `level`：设置 Span 级别
- `skip`：不自动记录指定参数
- `fields`：添加自定义字段
- `err`：返回`Err`时记录错误
- `ret`：记录返回值，通常只适合小而安全的值

敏感信息、认证令牌、密码、完整请求体不应该写入日志。

## 9、为Future附加Span

无法直接在函数上使用`#[instrument]`时，可以通过`Instrument`为 Future 附加 Span：

```rust
use tracing::Instrument;

async fn spawn_job(job_id: u64) {
    let span = tracing::info_span!("background_job", job_id);

    tokio::spawn(
        async move {
            tracing::info!("job started");
            run_job(job_id).await;
            tracing::info!("job completed");
        }
        .instrument(span),
    );
}
```

如果希望新任务继承当前 Span，可以使用：

```rust
use tracing::Instrument;

tokio::spawn(
    async move {
        run_child_task().await;
    }
    .in_current_span(),
);
```

是否继承当前 Span 应根据语义决定：

- 当前请求的一部分：继承当前 Span
- 与当前请求解耦的后台任务：创建新的顶层 Span


# 四、tracing-subscriber

## 1、初始化Subscriber

`tracing`只负责产生 Event 和 Span。程序必须初始化 Subscriber，日志才会被处理。

推荐显式配置默认过滤级别：

```rust
use tracing_subscriber::EnvFilter;

fn main() {
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info"));

    tracing_subscriber::fmt()
        .with_env_filter(filter)
        .init();

    tracing::info!("server started");
}
```

这样：

- 设置了`RUST_LOG`时使用环境变量
- 未设置时默认输出`INFO`及以上

因此直接运行时，`server started`会输出；如果设置`RUST_LOG=warn`，这条`INFO`日志会被过滤。

相比直接调用`tracing_subscriber::fmt::init()`，显式配置默认规则更容易理解，也不会让行为依赖隐含的 feature 和默认值。

全局 Subscriber 只能初始化一次。在测试或可能重复初始化的环境中，可以使用`try_init()`：

```rust
let _ = tracing_subscriber::fmt()
    .with_env_filter("info")
    .try_init();
```

正式应用启动时通常不应静默忽略初始化失败，而应该让配置冲突尽早暴露。

## 2、RUST_LOG规则

全局设置日志级别：

```shell
RUST_LOG=debug cargo run
```

默认`INFO`，只为当前应用的数据库模块开启`DEBUG`：

```shell
RUST_LOG=info,my_app::database=debug cargo run
```

关闭依赖库的噪声：

```shell
RUST_LOG=info,hyper=warn,h2=warn cargo run
```

多个规则之间使用逗号分隔。模块名通常来自 Event 或 Span 的 target，默认 target 是代码所在的模块路径。

## 3、文本格式

可以控制是否显示 target、线程信息、文件和行号：

```rust
use tracing_subscriber::EnvFilter;

fn main() {
    tracing_subscriber::fmt()
        .with_env_filter(
            EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| EnvFilter::new("info")),
        )
        .with_target(true)
        .with_thread_ids(true)
        .with_file(true)
        .with_line_number(true)
        .compact()
        .init();
}
```

这段配置不会改变 Event 本身，只会丰富文本输出的元数据。输出的关键部分可能类似：

```text
INFO ThreadId(01) my_app::server src/main.rs:18 server started
```

其中 target、线程 ID、文件路径和行号分别来自`with_target`、`with_thread_ids`、`with_file`和`with_line_number`。

开发环境可以保留较多定位信息。生产环境是否记录文件、行号和线程 ID，需要根据日志量和排障需求决定。

在异步程序中，线程 ID 只能说明当前由哪个运行时线程执行，不能稳定标识一个异步任务。请求和任务应该使用 Span 字段标识。

## 4、JSON格式

结构化日志平台通常更适合接收 JSON：

```rust
use tracing_subscriber::EnvFilter;

fn main() {
    tracing_subscriber::fmt()
        .with_env_filter(
            EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| EnvFilter::new("info")),
        )
        .json()
        .flatten_event(true)
        .with_current_span(true)
        .with_span_list(true)
        .init();
}
```

使用`.json()`需要为`tracing-subscriber`启用`json` feature：

```toml
[dependencies]
tracing-subscriber = {
    version = "0.3",
    features = ["env-filter", "json"],
}
```

假设记录：

```rust
tracing::info!(user_id = 42, "user logged in");
```

输出会变成单行 JSON，结构大致如下：

```json
{
  "level": "INFO",
  "message": "user logged in",
  "user_id": 42
}
```

实际 JSON 还可能包含时间戳、target和 Span 信息。`.flatten_event(true)`会把`message`和`user_id`等 Event 字段提升到 JSON 顶层；如果不启用，它们通常位于`fields`对象中。`.with_current_span(true)`和`.with_span_list(true)`则会附加当前 Span及完整 Span 路径。

容器环境通常直接把 JSON 日志写到`stdout`，再由日志采集系统负责持久化、检索和归档。应用程序不一定需要自己写日志文件。


# 五、输出到文件

## 1、非阻塞写入

同步写文件会让记录日志的线程直接参与 I/O。异步服务通常使用`tracing-appender`提供的非阻塞写入器：

```toml
[dependencies]
tracing = "0.1"
tracing-appender = "0.2"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

示例：

```rust
use tracing_subscriber::EnvFilter;

fn main() {
    std::fs::create_dir_all("./logs").unwrap();

    let file_appender = tracing_appender::rolling::daily(
        "./logs",
        "app.log",
    );

    let (writer, _guard) = tracing_appender::non_blocking(file_appender);

    tracing_subscriber::fmt()
        .with_env_filter(
            EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| EnvFilter::new("info")),
        )
        .with_writer(writer)
        .with_ansi(false)
        .init();

    tracing::info!("server started");
}
```

`non_blocking`会创建后台工作线程。日志先进入队列，再由后台线程写入文件。

运行后，`./logs`目录中会生成按天滚动的日志文件，文件内容包含：

```text
INFO ... server started
```

终端不会再显示这条日志，因为`.with_writer(writer)`已经把当前格式化 Subscriber 的输出目标改成了文件 writer。

这里的`_guard`必须保留在`main`作用域中。程序退出时，它会负责等待后台线程刷新尚未写完的日志。下一节会详细说明它的生命周期。

## 2、WorkerGuard生命周期

`tracing_appender::non_blocking`返回：

```rust
(NonBlocking, WorkerGuard)
```

`WorkerGuard`负责在程序退出时等待后台线程刷新缓冲数据。它必须在日志系统的整个生命周期内保持存活。

下面的封装方式是错误的：

```rust
fn init_tracing() {
    let (writer, _guard) = tracing_appender::non_blocking(std::io::stdout());

    tracing_subscriber::fmt()
        .with_writer(writer)
        .init();
}
```

函数返回后，`_guard`立即被丢弃，后续日志可能无法正常写入。

应该把 guard 返回给`main`：

```rust
fn init_tracing() -> tracing_appender::non_blocking::WorkerGuard {
    std::fs::create_dir_all("./logs").unwrap();

    let file_appender = tracing_appender::rolling::daily(
        "./logs",
        "app.log",
    );

    let (writer, guard) = tracing_appender::non_blocking(file_appender);

    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| tracing_subscriber::EnvFilter::new("info")),
        )
        .with_writer(writer)
        .with_ansi(false)
        .init();

    guard
}

fn main() {
    let _guard = init_tracing();

    tracing::info!("server started");
}
```

变量名以`_`开头只会关闭“未使用变量”警告，不会让变量提前释放。`_guard`仍然会存活到当前作用域结束。

## 3、同时输出到终端和文件

如果不同输出目标需要不同格式或过滤规则，可以使用 Layer 组合。

Layer 可以理解为附加在 Subscriber 上的一层处理逻辑。每个 Layer 可以独立完成过滤、格式化或输出，`registry()`则负责把多个 Layer 组合成一个完整的 Subscriber。

下面的配置分别创建终端 Layer 和文件 Layer：

```rust
use tracing_subscriber::{
    filter::LevelFilter,
    layer::SubscriberExt,
    util::SubscriberInitExt,
    Layer,
};

fn init_tracing() -> tracing_appender::non_blocking::WorkerGuard {
    std::fs::create_dir_all("./logs").unwrap();

    let file_appender = tracing_appender::rolling::daily(
        "./logs",
        "app.log",
    );
    let (file_writer, guard) =
        tracing_appender::non_blocking(file_appender);

    let stdout_layer = tracing_subscriber::fmt::layer()
        .with_writer(std::io::stdout)
        .with_filter(LevelFilter::INFO);

    let file_layer = tracing_subscriber::fmt::layer()
        .with_writer(file_writer)
        .with_ansi(false)
        .with_filter(LevelFilter::DEBUG);

    tracing_subscriber::registry()
        .with(stdout_layer)
        .with(file_layer)
        .init();

    guard
}
```

这个配置会：

- 终端输出`INFO`及以上
- 文件输出`DEBUG`及以上

例如程序依次记录`DEBUG`和`INFO`：

```rust
tracing::debug!("configuration loaded");
tracing::info!("server started");
```

终端只会看到：

```text
INFO ... server started
```

日志文件则会同时包含：

```text
DEBUG ... configuration loaded
INFO  ... server started
```

这是因为两个 Layer 分别拥有自己的`LevelFilter`，同一条 Event 可以被不同 Layer 以不同规则处理。

如果还需要使用`RUST_LOG`，可以继续组合`EnvFilter`。过滤器放在整个 Subscriber 上时，会影响所有 Layer；放在单个 Layer 上时，只影响该输出目标。


# 六、异步程序完整示例

下面是一个适合 Tokio 应用的最小完整示例：

```toml
[dependencies]
tokio = { version = "1", features = ["macros", "rt-multi-thread", "time"] }
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

```rust
use std::time::Duration;
use tracing::{info, instrument};
use tracing_subscriber::EnvFilter;

fn init_tracing() {
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info"));

    tracing_subscriber::fmt()
        .with_env_filter(filter)
        .with_target(false)
        .compact()
        .init();
}

#[instrument(
    name = "process_request",
    skip(body),
    fields(body_len = body.len())
)]
async fn process_request(
    request_id: u64,
    body: Vec<u8>,
) -> Result<(), &'static str> {
    info!("request received");

    tokio::time::sleep(Duration::from_millis(20)).await;

    if body.is_empty() {
        return Err("empty request body");
    }

    info!(status = 200, "request completed");

    Ok(())
}

#[tokio::main]
async fn main() {
    init_tracing();

    let first = tokio::spawn(process_request(1, vec![1, 2, 3]));
    let second = tokio::spawn(process_request(2, Vec::new()));

    let (first_result, second_result) = tokio::join!(first, second);

    for (task_name, result) in [
        ("first", first_result),
        ("second", second_result),
    ] {
        match result {
            Ok(Ok(())) => {}
            Ok(Err(error)) => {
                tracing::warn!(
                    task = task_name,
                    error = %error,
                    "request processing failed"
                );
            }
            Err(error) => {
                tracing::error!(
                    task = task_name,
                    error = %error,
                    "task failed to complete"
                );
            }
        }
    }
}
```

运行后，关键输出大致如下，具体先后顺序可能不同：

```text
INFO process_request{request_id=1 body_len=3}: request received
INFO process_request{request_id=2 body_len=0}: request received
INFO process_request{request_id=1 body_len=3}: request completed status=200
WARN request processing failed task="second" error=empty request body
```

两个请求由 Tokio 并发执行，因此前几条日志的顺序不能作为业务保证。不过，每条请求内部的日志都带有自己的`request_id`和`body_len`，即使交错输出也能区分所属请求。

第二个请求返回业务错误，但任务本身正常完成，所以匹配的是`Ok(Err(error))`分支；只有任务发生 panic、被取消或运行时关闭时，才会进入`Err(error)`分支并得到`JoinError`。

这个例子体现了几个关键原则：

- 在启动异步任务前初始化 Subscriber
- 使用`#[instrument]`建立请求级 Span
- 使用结构化字段记录 ID、长度和状态码
- 使用`skip`避免记录完整请求体
- 在任务汇总边界统一记录业务错误，避免同一个错误被重复记录
- 区分任务正常完成、业务函数返回`Err`和任务本身未正常完成


# 七、日志设计原则

## 1、记录有用的上下文

一条错误日志至少应该回答：

- 哪个操作失败
- 失败原因是什么
- 影响哪个请求、用户或任务
- 是否会重试

推荐：

```rust
tracing::warn!(
    request_id,
    attempt,
    error = %err,
    "request failed, retrying"
);
```

不推荐：

```rust
tracing::warn!("failed");
```

## 2、稳定字段比拼接文本更重要

推荐：

```rust
tracing::info!(
    request_id,
    status = 200,
    elapsed_ms,
    "request completed"
);
```

不推荐：

```rust
tracing::info!(
    "request {} completed: status={}, elapsed={}ms",
    request_id,
    200,
    elapsed_ms,
);
```

人可以阅读两种写法，但只有前者便于日志平台稳定提取和聚合字段。

## 3、不要泄露敏感信息

日志中不应该记录：

- 密码
- Token、Cookie、Authorization Header
- 私钥和密钥
- 完整银行卡号
- 未脱敏的个人隐私数据

使用`#[instrument]`时要特别注意：函数参数默认会通过`Debug`记录。敏感参数必须使用`skip`排除。

## 4、避免重复记录同一个错误

如果底层函数记录错误后又把`Err`返回，上层每传播一次都再记录一遍，最终会产生多条内容近似的错误日志。

通常选择一个最有上下文的边界记录：

- 底层库：返回包含原因的错误
- 业务边界：补充业务上下文
- 请求入口：记录最终响应和状态

错误传播本身不需要每一层都打日志。

## 5、控制高频路径日志

循环、轮询、每条消息和每次网络读写都可能是高频路径。此类日志通常使用`DEBUG`或`TRACE`，并避免记录大型对象。

如果构造日志字段的成本很高，可以先判断该级别是否启用：

```rust
if tracing::enabled!(tracing::Level::DEBUG) {
    let snapshot = build_expensive_snapshot();
    tracing::debug!(snapshot = ?snapshot, "state snapshot");
}
```

## 6、日志不是指标和分布式追踪的替代品

日志适合记录离散事件和诊断上下文，但不适合替代所有可观测性工具：

| 需求 | 更合适的工具 |
| --- | --- |
| 查看单次请求发生了什么 | 日志、Span |
| 统计请求量和错误率 | Metrics |
| 查看跨服务调用链 | Distributed Tracing |
| 分析 CPU 和锁竞争 | Profiling |

`tracing`的 Span 可以进一步接入 OpenTelemetry，但本地 Span 不等于已经具备跨服务分布式追踪能力。


# 八、常见问题

## 1、调用tracing宏后没有输出

常见原因：

- 没有初始化 Subscriber
- 日志级别被过滤
- `RUST_LOG`中的模块名不正确
- Subscriber 已经在其他位置初始化

先使用最小配置验证：

```rust
tracing_subscriber::fmt()
    .with_max_level(tracing::Level::TRACE)
    .init();
```

## 2、RUST_LOG没有生效

确认`tracing-subscriber`启用了`env-filter`：

```toml
tracing-subscriber = {
    version = "0.3",
    features = ["env-filter"],
}
```

并且初始化时确实添加了`EnvFilter`：

```rust
tracing_subscriber::fmt()
    .with_env_filter(
        tracing_subscriber::EnvFilter::from_default_env(),
    )
    .init();
```

## 3、异步任务的Span上下文混乱

检查是否把`span.enter()`返回的 guard 跨`.await`持有。

异步代码应该改用：

- `#[instrument]`
- `Future::instrument(span)`
- `Future::in_current_span()`

## 4、文件末尾日志丢失

检查`tracing_appender::non_blocking`返回的`WorkerGuard`是否一直存活到程序结束。

## 5、初始化两次导致panic

`init()`在全局 Subscriber 已存在时会 panic。应用程序应该集中初始化；测试中可按场景使用`try_init()`或局部 Subscriber。

## 6、依赖库使用log，应用使用tracing

这是常见组合。`tracing-subscriber`的格式化 Subscriber 可以接收通过兼容层转换的`log`记录，因此应用通常不需要同时初始化`env_logger`。

不要在同一应用里无目的地分别初始化两套全局日志系统，否则容易出现重复输出或初始化冲突。


# 九、总结

Rust 日志生态可以概括为：

```text
log                    传统日志门面
env_logger             log的简单输出实现

tracing                结构化Event和Span
tracing-subscriber     过滤、格式化和输出
tracing-appender       文件滚动和非阻塞写入
```

对于异步程序，最重要的不是把`println!`替换成`info!`，而是建立清晰的上下文：

- 用 Span 表示一次请求、任务或操作
- 用 Event 表示 Span 内发生的关键事件
- 用结构化字段记录稳定、可查询的数据
- 用`#[instrument]`或`Instrument`正确传播异步上下文
- 在应用入口统一初始化 Subscriber
- 谨慎控制日志级别、敏感数据和高频日志

掌握这些原则后，日志才能在多个异步任务交错执行时仍然保持可读、可查和可定位。


# 十、参考资料

- [tracing文档](https://docs.rs/tracing/latest/tracing/)
- [tracing-subscriber文档](https://docs.rs/tracing-subscriber/latest/tracing_subscriber/)
- [tracing-appender文档](https://docs.rs/tracing-appender/latest/tracing_appender/)
- [log文档](https://docs.rs/log/latest/log/)
- [env_logger文档](https://docs.rs/env_logger/latest/env_logger/)
