# 一、Tokio Runtime 概述

## 1、为什么需要 Runtime

Rust 语言本身提供了 `async` / `.await`、`Future`、`Waker` 等异步基础设施，但标准库并不内置完整的异步运行时。

也就是说，下面这个异步函数只是在语言层面定义了一个 `Future`：

```rust
async fn hello() {
    println!("hello");
}
```

调用 `hello()` 时，函数体不会立刻执行，而是返回一个 `Future`。这个 `Future` 必须被某个执行器不断 `poll`，才会真正向前推进，因此需要 Runtime 提供执行器。

Tokio Runtime 就是 Rust 生态中最主流的异步运行时之一。它负责提供：

| 组成     | 作用                                     |
| ------ | -------------------------------------- |
| 任务调度器  | 管理异步任务，决定什么时候 `poll` 哪个任务              |
| I/O 驱动 | 监听操作系统 I/O 事件，例如 socket 可读、可写          |
| 时间驱动   | 支持 `sleep`、`timeout`、`interval` 等定时能力  |
| 任务系统   | 支持 `tokio::spawn`、`JoinHandle`、任务取消等能力 |
| 阻塞线程池  | 承载无法异步化的同步阻塞代码                         |

核心关系如下：

> `async/.await` 让代码可以暂停和恢复，Tokio Runtime 负责真正调度和推进这些异步代码。

## 2、Tokio 适合什么场景

Tokio 最适合大量 I/O 并发场景，例如：

- Web 服务
- TCP / UDP 网络程序
- 数据库访问
- RPC 客户端和服务端
- 消息队列
- 定时任务
- 大量并发请求的爬虫或代理程序

这些场景的共同特点是：任务大部分时间不是在消耗 CPU，而是在等待外部 I/O。Tokio 可以在某个任务等待 I/O 时，把线程让给其他已经就绪的任务，从而用较少线程承载大量并发连接。

Tokio 不适合把所有问题都异步化。对于长时间 CPU 密集计算，或者必须调用同步阻塞库的场景，不能直接放在普通异步任务里长时间运行，否则会卡住 runtime 的工作线程。此时可以使用 `spawn_blocking` 把阻塞逻辑移到专门的阻塞线程池，也可以使用普通 OS 线程或独立计算线程池。

## 3、引入 Tokio 依赖

学习阶段通常可以直接启用 `full` feature：

```toml
[dependencies]
tokio = { version = "1", features = ["full"] }
```

也可以使用命令：

```bash
cargo add tokio --features full
```

官方文档也建议应用程序在不确定 feature 选择时使用 `full`，这样可以一次启用常用模块，减少学习过程中的 feature 缺失问题。

不过在实际库开发中，不应一律启用 `full`。库应该只启用自己真正需要的 feature，避免把不必要的编译成本和依赖传递给使用者。例如只需要运行时和 TCP 能力时，可以更精确地写：

```toml
tokio = { version = "1", features = ["rt", "net"] }
```

常见 feature 如下：

| feature | 作用 |
| --- | --- |
| `rt` | 当前线程 runtime、任务系统等基础能力 |
| `rt-multi-thread` | 多线程 runtime |
| `macros` | `#[tokio::main]`、`#[tokio::test]` |
| `time` | `tokio::time` 定时器相关能力 |
| `net` | TCP、UDP、Unix socket 等网络 I/O |
| `fs` | 异步文件 API |
| `sync` | channel、Mutex、Semaphore 等同步原语 |
| `process` | 异步进程管理 |
| `signal` | 信号处理 |
| `full` | 启用大部分常用 Tokio 功能 |

# 二、创建 Runtime

## 1、手动创建 Runtime

最直接的方式，是在普通 `main` 函数中手动创建一个 `Runtime`，然后用它执行异步代码。

如果只需要默认多线程 runtime，可以使用 `Runtime::new()`：

```rust
use tokio::runtime::Runtime;

fn main() {
    let rt = Runtime::new().unwrap();

    rt.block_on(async {
        println!("run async code");
    });
}
```

`Runtime::new()` 创建的是多线程 runtime。它要求启用 `rt-multi-thread` feature，并会启用 I/O 和时间驱动。

`Runtime` 本身只是运行时环境。真正把异步代码交给 runtime 执行的是 `block_on`：

```rust
fn main() {
    let rt = tokio::runtime::Runtime::new().unwrap();

    rt.block_on(async {
        println!("hello from async block");
    });
}
```

这里可以分成两步理解：

- `Runtime::new()` 创建运行时
- `rt.block_on(...)` 把一个根 `Future` 放进运行时，并阻塞当前线程直到它完成

如果需要更细粒度配置，可以使用 `Builder`。

创建当前线程 runtime：

```rust
use tokio::runtime::Builder;

fn main() {
    let rt = Builder::new_current_thread()
        .enable_all()
        .build()
        .unwrap();

    rt.block_on(async {
        println!("current thread runtime");
    });
}
```

创建多线程 runtime：

```rust
use tokio::runtime::Builder;

fn main() {
    let rt = Builder::new_multi_thread()
        .worker_threads(4)
        .enable_all()
        .build()
        .unwrap();

    rt.block_on(async {
        println!("multi thread runtime");
    });
}
```

`enable_all()` 会启用 I/O 驱动和时间驱动。手动用 `Builder` 创建 runtime 时，如果没有启用这些驱动，使用 `tokio::net` 或 `tokio::time` 时可能会在运行时报错。

也可以只启用某一类驱动：

```rust
let rt = tokio::runtime::Builder::new_multi_thread()
    .enable_io()
    .enable_time()
    .build()
    .unwrap();
```

学习和多数应用场景下，使用 `enable_all()` 可以减少遗漏驱动配置的问题。

## 2、使用 #[tokio::main]

手动创建 runtime 能清楚展示运行时的创建和驱动过程。实际应用程序入口通常会写得更简洁，Tokio 提供了 `#[tokio::main]` 宏：

```rust
#[tokio::main]
async fn main() {
    println!("hello tokio");
}
```

这个宏会把 `async fn main()` 包装成一个普通 `fn main()`，在里面创建 Tokio Runtime，然后调用 `block_on` 驱动原来的异步主函数。

结合前面手动创建 runtime 的写法，`#[tokio::main]` 大致等价于：

```rust
fn main() {
    tokio::runtime::Builder::new_multi_thread()
        .enable_all()
        .build()
        .unwrap()
        .block_on(async {
            println!("hello tokio");
        });
}
```

默认情况下，`#[tokio::main]` 使用多线程 runtime。它会创建一组 worker thread 来调度异步任务。

也可以显式指定 worker 线程数：

```rust
#[tokio::main(worker_threads = 4)]
async fn main() {
    println!("multi-thread runtime");
}
```

如果希望只在当前线程上运行异步任务，可以使用 current-thread runtime：

```rust
#[tokio::main(flavor = "current_thread")]
async fn main() {
    println!("current-thread runtime");
}
```

需要注意：

- `current_thread` 不是“额外创建一个单独线程”
- 它表示所有异步任务都在当前线程上被驱动
- 如果这个线程被阻塞，整个 current-thread runtime 就无法继续推进其他任务

## 3、多线程和当前线程 runtime 的区别

Tokio 常见 runtime flavor 有两种：

| 类型 | 创建方式 | 特点 | 适合场景 |
| --- | --- | --- | --- |
| 多线程 runtime | `new_multi_thread()` / 默认 `#[tokio::main]` | 多个 worker 线程，使用 work-stealing 调度 | 大多数服务端应用 |
| 当前线程 runtime | `new_current_thread()` / `flavor = "current_thread"` | 不创建 worker 线程，所有任务在当前线程上推进 | 嵌入同步程序、测试、小工具、需要单线程约束的场景 |

多线程 runtime 默认按系统可用 CPU 并行度创建 worker 线程，也可以通过 `worker_threads(...)` 或 `TOKIO_WORKER_THREADS` 调整。

当前线程 runtime 不会创建 worker 线程，它直接使用当前线程运行异步执行器，并阻塞调用者直到 Future 完成。

例如：

```rust
use tokio::runtime::Builder;

fn main() {
    let rt = Builder::new_current_thread()
        .enable_all()
        .build()
        .unwrap();

    rt.block_on(async {
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
        println!("done");
    });
}
```

这里的 `sleep` 并没有阻塞 OS 线程，但整个 current-thread runtime 只有主线程可以推进任务。如果主线程没有进入 `block_on`，任务就不会继续运行。

## 4、是否应该创建多个 Runtime

一个程序可以创建多个 Tokio Runtime。例如在不同 OS 线程中分别创建 runtime：

```rust
fn main() {
    let t1 = std::thread::spawn(|| {
        let rt = tokio::runtime::Runtime::new().unwrap();
        rt.block_on(async {
            println!("runtime 1");
        });
    });

    let t2 = std::thread::spawn(|| {
        let rt = tokio::runtime::Runtime::new().unwrap();
        rt.block_on(async {
            println!("runtime 2");
        });
    });

    t1.join().unwrap();
    t2.join().unwrap();
}
```

但大多数应用不应该随意创建多个 runtime。因为每个 runtime 都有自己的调度器、I/O 驱动、时间驱动、worker 线程和阻塞线程池。多个 runtime 会增加资源占用，也会让任务、句柄、关闭流程变复杂。


# 三、Runtime 如何执行异步代码

## 1、block_on 的含义

`Runtime::block_on` 是同步代码进入异步运行时的入口。它会在当前线程上驱动一个 `Future`，并阻塞同步调用者，直到这个 `Future` 完成：

```rust
use tokio::runtime::Runtime;

fn main() {
    let rt = Runtime::new().unwrap();

    let value = rt.block_on(async {
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
        42
    });

    println!("{value}");
}
```

这里要区分两层含义：

- 对同步调用者来说，`block_on` 返回前，后面的同步代码不会继续执行
- 对 runtime 来说，调用 `block_on` 的线程会进入执行循环，负责 `poll` 传入的 `Future`；当某个任务在 `.await` 处挂起时，这个线程可以继续推进其他已经就绪的任务

`block_on` 的返回值就是被驱动的 `Future` 的输出值。上面例子中，`value` 的值就是 `42`。

## 2、std::thread::sleep 和 tokio::time::sleep

学习 Tokio 时必须区分线程阻塞和任务挂起。

| 写法 | 影响 |
| --- | --- |
| `std::thread::sleep(...)` | 阻塞当前 OS 线程 |
| `tokio::time::sleep(...).await` | 挂起当前异步任务，不阻塞 worker 线程 |

示例：

```rust
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    sleep(Duration::from_secs(1)).await;
    println!("done");
}
```

`tokio::time::sleep` 返回的是一个 `Future`。当它还没到期时，当前任务会返回 `Pending`，runtime 可以去调度其他任务。时间到期后，时间驱动会唤醒这个任务，之后它会被再次 `poll` 并继续执行。

而下面这种写法会直接阻塞 worker 线程：

```rust
#[tokio::main]
async fn main() {
    std::thread::sleep(std::time::Duration::from_secs(1));
    println!("done");
}
```

如果很多异步任务都这样写，就会让 Tokio 失去高并发优势。

## 3、spawn 只是提交任务

在 runtime 上下文中，可以使用 `tokio::spawn` 创建新的异步任务：

```rust
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        sleep(Duration::from_secs(1)).await;
        println!("child task done");
    });

    handle.await.unwrap();
}
```

`tokio::spawn` 的作用是把一个 `Future` 提交给当前 runtime 调度。它会立即返回一个 `JoinHandle<T>`，不会等子任务执行完成。

因此下面这段代码通常看不到子任务输出：

```rust
use tokio::runtime::Runtime;
use tokio::time::{sleep, Duration};

fn main() {
    let rt = Runtime::new().unwrap();

    rt.block_on(async {
        tokio::spawn(async {
            sleep(Duration::from_secs(1)).await;
            println!("child task done");
        });
    });
}
```

原因是：外层 `block_on` 驱动的 `Future` 很快结束，`main` 函数随后结束，runtime 被 drop，尚未完成的子任务也就不会继续推进。

正确做法是等待 `JoinHandle`：

```rust
use tokio::runtime::Runtime;
use tokio::time::{sleep, Duration};

fn main() {
    let rt = Runtime::new().unwrap();

    rt.block_on(async {
        let handle = tokio::spawn(async {
            sleep(Duration::from_secs(1)).await;
            println!("child task done");
            10
        });

        let value = handle.await.unwrap();
        println!("{value}");
    });
}
```

`JoinHandle.await` 等待的是任务结果，它不会像 `std::thread::join()` 那样阻塞 worker 线程，而是挂起当前异步任务，让 runtime 继续调度其他任务。

## 4、Runtime::spawn 和 tokio::spawn

除了 `tokio::spawn`，`Runtime` 本身也提供 `spawn` 方法：

```rust
use tokio::runtime::Runtime;
use tokio::time::{sleep, Duration};

fn main() {
    let rt = Runtime::new().unwrap();

    let handle = rt.spawn(async {
        sleep(Duration::from_secs(1)).await;
        100
    });

    let value = rt.block_on(handle).unwrap();
    println!("{value}");
}
```

两者区别如下：

| 写法 | 使用前提 |
| --- | --- |
| `tokio::spawn(...)` | 当前线程已经处于 Tokio runtime 上下文 |
| `rt.spawn(...)` | 手上明确持有某个 `Runtime` 值 |

在 `#[tokio::main]` 或 `rt.block_on(async { ... })` 内部，通常直接使用 `tokio::spawn`。

在同步代码中，如果手上有 `Runtime`，可以使用 `rt.spawn` 把任务提交给这个 runtime。

## 5、enter 只进入上下文，不驱动任务

`Runtime::enter` 可以把当前线程临时标记为处于某个 Tokio runtime 上下文中。

它常用于让依赖“当前 runtime 上下文”的 API 可以工作，例如 `tokio::spawn`：

```rust
use tokio::runtime::Runtime;
use tokio::time::{sleep, Duration};

fn main() {
    let rt = Runtime::new().unwrap();

    let _guard = rt.enter();

    let handle = tokio::spawn(async {
        sleep(Duration::from_secs(1)).await;
        println!("done");
    });

    rt.block_on(handle).unwrap();
}
```

这里要特别注意：

> `enter` 只是进入 runtime 上下文，不会主动驱动任何 `Future`。

真正让任务向前运行的，仍然是 `block_on`、worker 线程或其他 runtime 驱动机制。

如果只调用 `enter`，然后不调用 `block_on`，current-thread runtime 中的任务不会自己运行。

# 四、Runtime 的调度模型

## 1、Future、Task 和 Poll

`async fn` 或 `async { ... }` 会创建 `Future`。当这个 `Future` 被 runtime 纳入调度，它就成为一个 Tokio task。

runtime 调度任务的核心动作是调用 `poll`：

```rust
trait Future {
    type Output;

    fn poll(
        self: std::pin::Pin<&mut Self>,
        cx: &mut std::task::Context<'_>,
    ) -> std::task::Poll<Self::Output>;
}
```

`poll` 有两种结果：

| 结果 | 含义 |
| --- | --- |
| `Poll::Ready(value)` | 任务完成，返回结果 |
| `Poll::Pending` | 任务暂时不能继续，需要以后被唤醒 |

当任务等待 socket、定时器、channel 等异步资源时，通常会返回 `Pending`，并通过 `Waker` 安排唤醒。等资源就绪后，runtime 再把任务放回可调度队列。

## 2、协作式调度

Tokio task 不是由操作系统抢占式调度的线程，而是由 Tokio 在用户态调度的轻量级任务。

Tokio 能在少量线程上运行大量任务，是因为任务会在 `.await` 处主动让出执行权：

```rust
async fn read_and_process() {
    let data = read_from_socket().await;
    process(data);
}
```

当 `read_from_socket().await` 暂时无法完成时，当前 task 会挂起，worker 线程可以去推进其他 task。

但如果某个 task 长时间不 `.await`，也不主动让出执行权，它就会长期占住当前 worker 线程，影响其他任务：

```rust
#[tokio::main]
async fn main() {
    tokio::spawn(async {
        loop {
            // 长时间 CPU 循环，没有 .await
        }
    });
}
```

对于这类情况，可以考虑：

- 把 CPU 密集任务放到专门线程池
- 使用 `spawn_blocking`
- 在确实合适的位置调用 `tokio::task::yield_now().await`
- 把大计算拆分成更小的可让出步骤

## 3、多线程 runtime 的任务迁移

在多线程 runtime 中，`tokio::spawn` 创建的任务可能在不同 worker 线程之间迁移。

因此，普通 `tokio::spawn` 要求被提交的 Future 及其输出都满足：

```rust
Send + 'static
```

这两个约束的含义是：

- `Send`：任务可以安全地移动到其他线程执行
- `'static`：任务不能持有可能提前失效的短生命周期引用

这并不表示任务一定会活到程序结束，也不表示内存泄漏。它表示这个任务从类型上看不依赖某个临时借用，因此 runtime 可以安全地管理它的生命周期。

如果需要运行 `!Send` 的 future，不能直接丢给普通 `tokio::spawn`。这类内容通常要配合 `LocalSet` 和 `spawn_local` 使用，后续学习 task 和局部任务时再展开。

# 五、阻塞代码和 spawn_blocking

## 1、worker thread 和 blocking thread

Tokio runtime 中常见两类线程：

| 线程类型 | 作用 |
| --- | --- |
| worker thread | 执行普通异步任务，负责调度和 `poll` |
| blocking thread | 执行通过 `spawn_blocking` 提交的同步阻塞代码 |

worker thread 不适合长期阻塞。下面这种写法会直接卡住 worker 线程：

```rust
#[tokio::main]
async fn main() {
    std::thread::sleep(std::time::Duration::from_secs(10));
}
```

如果 runtime 只有少量 worker 线程，而这些线程都被阻塞，其他异步任务就无法及时被调度。

## 2、使用 spawn_blocking

Tokio 提供 `tokio::task::spawn_blocking` 来运行阻塞代码：

```rust
#[tokio::main]
async fn main() {
    let result = tokio::task::spawn_blocking(|| {
        let mut sum = 0;

        for i in 0..1_000_000 {
            sum += i;
        }

        sum
    })
    .await
    .unwrap();

    println!("{result}");
}
```

`spawn_blocking` 会把闭包提交到 Tokio 管理的阻塞线程池中执行。它不是普通异步任务，不会在 worker thread 上被反复 `poll`。

它适合：

- 调用同步文件、压缩、加密、解析等阻塞库
- 执行少量或可控时长的 CPU 计算
- 临时桥接无法改写为 async 的旧代码

但它不适合无限循环或不可控的长期任务。对于大量 CPU 密集计算，专门的计算线程池通常更清晰，例如使用 Rayon 这类面向 CPU 并行计算的线程池。

## 3、blocking 任务不容易取消

普通异步任务可以通过 `JoinHandle::abort` 取消：

```rust
let handle = tokio::spawn(async {
    tokio::time::sleep(std::time::Duration::from_secs(60)).await;
});

handle.abort();
```

取消异步任务的本质是：runtime 不再继续 `poll` 这个任务，并丢弃它保存的状态。

但 `spawn_blocking` 不同。一旦阻塞闭包已经在线程中开始执行，Tokio 不能安全地强行杀掉这个 OS 线程。因此：

- 如果 blocking 任务还没开始，`abort` 可能阻止它运行
- 如果 blocking 任务已经开始，`abort` 通常不能让它立刻停止
- runtime 关闭时，也可能需要等待已经开始的 blocking 任务结束

所以提交给 `spawn_blocking` 的代码应该有明确结束条件。

如果需要可取消的阻塞任务，应该自己设计取消机制，例如共享一个 `AtomicBool`：

```rust
use std::sync::{
    atomic::{AtomicBool, Ordering},
    Arc,
};

#[tokio::main]
async fn main() {
    let cancelled = Arc::new(AtomicBool::new(false));
    let flag = Arc::clone(&cancelled);

    let handle = tokio::task::spawn_blocking(move || {
        while !flag.load(Ordering::Relaxed) {
            std::thread::sleep(std::time::Duration::from_millis(100));
            println!("working");
        }
    });

    tokio::time::sleep(std::time::Duration::from_secs(1)).await;
    cancelled.store(true, Ordering::Relaxed);

    handle.await.unwrap();
}
```

## 4、阻塞代码和异步代码通信

如果阻塞代码只需要返回最终结果，直接让闭包返回即可：

```rust
let value = tokio::task::spawn_blocking(|| {
    1 + 2
})
.await
.unwrap();
```

如果阻塞代码需要不断把中间结果传给异步任务，可以使用 channel。Tokio 的部分 channel 提供了 `blocking_send` / `blocking_recv`，方便在同步阻塞上下文中使用。

```rust
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel::<String>(8);

    let handle = tokio::task::spawn_blocking(move || {
        for i in 0..5 {
            tx.blocking_send(format!("line {i}")).unwrap();
        }
    });

    while let Some(line) = rx.recv().await {
        println!("{line}");
    }

    handle.await.unwrap();
}
```

这样可以让阻塞世界和 async 世界保持清晰边界。

# 六、Runtime 关闭

## 1、drop Runtime 会发生什么

`Runtime` 是一个普通 Rust 值。当它离开作用域或被 `drop(rt)` 时，runtime 会进入关闭流程。

可以从几个方面理解：

- 不再接受新的任务
- 未完成的普通异步任务不再继续被 `poll`
- I/O 驱动和时间驱动被关闭
- worker 线程退出调度循环
- 已经开始执行的 blocking 任务可能会被等待

示例：

```rust
use tokio::runtime::Runtime;

fn main() {
    let rt = Runtime::new().unwrap();

    rt.block_on(async {
        tokio::spawn(async {
            tokio::time::sleep(std::time::Duration::from_secs(60)).await;
            println!("will not print");
        });
    });

    drop(rt);
}
```

这里子任务还没完成，runtime 就被关闭了，所以它不会继续执行。

## 2、shutdown_timeout 和 shutdown_background

如果 runtime 中存在已经开始运行的 `spawn_blocking` 任务，普通 drop 可能会等待很久。

Tokio 提供了两个常见关闭方法：

| 方法 | 含义 |
| --- | --- |
| `shutdown_timeout(duration)` | 等待一段时间，超过时间后返回 |
| `shutdown_background()` | 在后台关闭，不在当前线程等待完整关闭 |

示例：

```rust
fn main() {
    let rt = tokio::runtime::Runtime::new().unwrap();

    rt.spawn_blocking(|| {
        loop {
            std::thread::sleep(std::time::Duration::from_secs(1));
        }
    });

    rt.shutdown_timeout(std::time::Duration::from_millis(100));
}
```

需要注意：这些方法不会强行杀掉已经开始执行的 blocking 任务。它们只是改变当前线程等待 runtime 关闭的方式。

因此，真正可靠的做法仍然是：

- 不把无限循环放进 `spawn_blocking`
- 给阻塞任务设计退出条件
- 在关闭前通知后台任务停止
- 等待关键任务正常收尾

# 七、常见错误和判断标准

## 1、在没有 Runtime 的地方调用 Tokio API

某些 Tokio API 依赖当前 runtime 上下文。例如：

```rust
fn main() {
    tokio::spawn(async {
        println!("hello");
    });
}
```

这段代码会出错，因为普通 `main` 函数中没有进入 Tokio runtime。

修复方式：

```rust
#[tokio::main]
async fn main() {
    tokio::spawn(async {
        println!("hello");
    })
    .await
    .unwrap();
}
```

或者手动创建 runtime：

```rust
fn main() {
    let rt = tokio::runtime::Runtime::new().unwrap();

    rt.block_on(async {
        tokio::spawn(async {
            println!("hello");
        })
        .await
        .unwrap();
    });
}
```

## 2、在 async 代码中直接调用阻塞函数

错误倾向：

```rust
#[tokio::main]
async fn main() {
    std::thread::sleep(std::time::Duration::from_secs(10));
}
```

更合适：

```rust
#[tokio::main]
async fn main() {
    tokio::time::sleep(std::time::Duration::from_secs(10)).await;
}
```

如果必须调用阻塞函数：

```rust
#[tokio::main]
async fn main() {
    tokio::task::spawn_blocking(|| {
        std::thread::sleep(std::time::Duration::from_secs(10));
    })
    .await
    .unwrap();
}
```

## 3、创建任务后不等待结果

`spawn` 只是提交任务，不代表任务一定能在程序退出前完成。

```rust
#[tokio::main]
async fn main() {
    tokio::spawn(async {
        println!("maybe lost");
    });
}
```

如果任务结果很重要，应该保存并等待 `JoinHandle`：

```rust
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        println!("done");
        1
    });

    let value = handle.await.unwrap();
    println!("{value}");
}
```

如果任务是后台任务，也应该明确设计它的生命周期和关闭方式，不能只依赖 `spawn` 后由 runtime 自行处理。

## 4、在异步函数中频繁创建 Runtime

错误倾向：

```rust
async fn do_work() {
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async {
        println!("nested");
    });
}
```

在已经处于 Tokio runtime 内部时，再创建 runtime 并调用 `block_on` 往往会造成复杂问题。更好的方式通常是直接 `.await`：

```rust
async fn do_work() {
    println!("work");
}
```

如果确实需要从同步代码调用异步代码，应当把 runtime 放在同步边界处创建和复用，而不是在业务函数里到处创建。

# 八、整体理解

可以把 Tokio Runtime 理解成异步程序的“执行环境”：

1. `async fn` 产生 `Future`
2. `#[tokio::main]` 或 `Runtime::new()` 创建 runtime
3. `block_on` 把根 Future 放进 runtime 并等待它完成
4. `tokio::spawn` 把更多 Future 变成 task，交给 runtime 调度
5. task 在 `.await` 处挂起，让 worker thread 去执行其他任务
6. I/O 或定时器就绪后，runtime 唤醒对应 task
7. 阻塞代码用 `spawn_blocking` 放到 blocking thread，避免卡住 worker thread
8. runtime 关闭时，未完成异步任务会停止推进，blocking 任务需要额外注意退出条件

一句话总结：

> Tokio Runtime 不是语法糖，而是 Rust async 真正跑起来所依赖的调度、I/O、定时器和线程资源管理层。

# 参考资料

- [Tokio crate documentation](https://docs.rs/tokio/latest/tokio/)
- [Tokio runtime module documentation](https://docs.rs/tokio/latest/tokio/runtime/)
- [Tokio `#[main]` macro documentation](https://docs.rs/tokio/latest/tokio/attr.main.html)
- [Tokio tutorial: spawning](https://tokio.rs/tokio/tutorial/spawning)
