# 一、概述


Rust 语言本身以及标准库提供了 `async` / `.await`、`Future`、`Waker` 等异步基础设施，但并没有内置完整的异步运行时。

下面这个异步函数只是在语言层面定义了一个 `Future`：

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

Tokio 最适合大量 I/O 并发场景，例如：

- Web 服务
- TCP / UDP 网络程序
- 数据库访问
- RPC 客户端和服务端
- 消息队列
- 定时任务
- 大量并发请求的爬虫或代理程序

这些场景的共同特点是：任务大部分时间不是在消耗 CPU，而是在等待外部 I/O。Tokio 可以在某个任务等待 I/O 时，把线程让给其他已经就绪的任务，从而用较少线程承载大量并发连接。

不过，Tokio 不适合把所有问题都异步化。对于长时间的 CPU 密集计算任务，或者必须调用同步阻塞库的场景，不能直接放在普通异步任务中长时间执行，否则会卡住 runtime 的工作线程。此时可以使用 Tokio 提供的 `spawn_blocking` 把阻塞逻辑移到专门的阻塞线程池中，或者使用 OS 线程或独立计算线程池。

学习阶段引入 Tokio 依赖通常可以直接启用 `full` feature：

```toml
[dependencies]
tokio = { version = "1", features = ["full"] }
```

也可以使用命令：

```shell
cargo add tokio --features full
```

官方文档也建议应用程序在不确定 feature 选择时使用 `full`，这样可以一次启用常用模块，减少学习过程中的 feature 缺失问题。

不过在实际开发中，不应一律启用 `full`。应该只启用自己真正需要的 feature，避免把不必要的编译成本和依赖传递给使用者。

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
       println!("Hello, world!");  
    });  
}
```

`Runtime::new()` 创建的是多线程 runtime。它要求启用 `rt-multi-thread` feature，并会启用 I/O 和时间驱动。

`Runtime` 本身只是运行时环境。真正把异步代码交给 runtime 执行的是 `block_on`：

```rust
rt.block_on(async {  
   println!("Hello, world!");  
});  
```

如果需要更细粒度配置，可以使用 `Builder`。

创建多线程 runtime：

```rust
use tokio::runtime::Builder;  
  
  
fn main() {  
    let rt = Builder::new_multi_thread()  
        .enable_all()  
        .build()  
        .unwrap();  
  
    rt.block_on(async {  
        println!("Hello, world!");  
    })  
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

创建多线程 runtime 时，默认 worker 线程数按系统可用 CPU 并行度确定，也可以通过 `worker_threads(n)` 指定 worker 线程数量：

```rust
let rt = Builder::new_multi_thread()  
    .worker_threads(4)  
    .enable_all()  
    .build()  
    .unwrap();
```

除了使用 `Builder::new_multi_thread()` 创建多线程 runtime，也可以使用 `Builder::new_current_thread()` 创建当前线程 runtime：

```rust
use tokio::runtime::Builder;

fn main() {
    let rt = Builder::new_current_thread()
        .enable_all()
        .build()
        .unwrap();

    rt.block_on(async {
        println!("Hello, world!");
    });
}
```

## 2、多线程 Runtime 和 当前线程 Runtime 的区别

Tokio 常见 runtime flavor 有两种：

| 类型           | 创建方式                                           | 特点                               | 适合场景                     |
| ------------ | ---------------------------------------------- | -------------------------------- | ------------------------ |
| 多线程 runtime  | `Builder::new_multi_thread()` 或默认 `Runtime::new()` | 多个 worker 线程，使用 work-stealing 调度 | 大多数服务端应用                 |
| 当前线程 runtime | `Builder::new_current_thread()`                  | 不创建 worker 线程，所有任务在当前线程上推进       | 嵌入同步程序、测试、小工具、需要单线程约束的场景 |

多线程 runtime 默认按系统可用 CPU 并行度创建 worker 线程，也可以通过 `worker_threads(...)` 调整。

当前线程 runtime 不会创建 worker 线程，它直接使用调用 `rt.block_on(...)` 的线程运行异步执行器。`block_on` 返回前，后面的同步代码不会继续执行；但在 `block_on` 内部，这个线程会负责 `poll` Future 并推进已经就绪的任务。

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

## 3、使用 \#\[tokio::main]

手动创建 runtime 能清楚展示运行时的创建和驱动过程。实际应用程序入口通常会写得更简洁，Tokio 提供了 `#[tokio::main]` 宏：

```rust
#[tokio::main]  
async fn main() {  
    println!("Hello, world!");  
}
```

它本质上还是普通的 `fn main()`，在里面创建 Tokio Runtime，然后调用 `block_on` 驱动原来的异步主函数。大致等价于：

```rust
use tokio::runtime::Runtime;  
  
fn main() {  
    let rt = Runtime::new().unwrap();  
      
    rt.block_on(async {  
        println!("Hello, world!");  
    })  
}
```

默认情况下，`#[tokio::main]` 使用多线程 runtime。它会创建一组 worker thread 来调度异步任务。

也可以显式指定 worker 线程数：

```rust
#[tokio::main(worker_threads = 4)]  
async fn main() {  
    println!("Hello, world!");  
}
```

如果希望只在当前线程上运行异步任务，可以使用 current-thread runtime：

```rust
#[tokio::main(flavor = "current_thread")]  
async fn main() {  
    println!("Hello, world!");  
}
```

## 4、创建多个 Runtime

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

# 三、Runtime 执行异步代码

## 1、block_on 的含义

`Runtime::block_on` 是同步代码进入异步运行时的入口。它会在当前线程上驱动一个 `Future`，并阻塞同步调用者，直到这个 `Future` 完成：

```rust
use tokio::runtime::Runtime;

fn main() {
    let rt = Runtime::new().unwrap();

    let value = rt.block_on(async {
        tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
        42
    });

    println!("{value}");
}
```

这里要区分两层含义：

- 对同步调用者来说，`block_on` 返回前，后面的同步代码不会继续执行
- 对 runtime 来说，调用 `block_on` 的线程会进入执行循环，负责 `poll` 传入的 `Future`；当某个任务在 `.await` 处挂起时，这个线程可以继续推进其他已经就绪的任务

`block_on` 的返回值就是被驱动的 `Future` 的输出值。上面例子中，`value` 的值就是 `42`。

## 2、std::thread::sleep 和 tokio::time::sleep 的区别

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

因此，在异步任务中要避免误用标准库的 `std::thread::sleep`，它会直接阻塞当前工作线程，使得异步运行时无法去调度其他就绪任务。

## 3、tokio::spawn

在 runtime 上下文中，可以使用 `tokio::spawn` 创建新的异步任务：

```rust
use tokio::runtime::Runtime;  
  
  
fn main() {  
  
    let rt = Runtime::new().unwrap();  
  
    rt.block_on(async {  
        let handle = tokio::spawn(async {  
            tokio::time::sleep(tokio::time::Duration::from_secs(3)).await;  
            println!("child task done!");  
        });  
  
        handle.await.unwrap();  
    });  
}
```

`tokio::spawn` 的作用是把一个 `Future` 提交给当前 runtime 调度。它会立即返回一个 `JoinHandle<T>`，不会等子任务执行完成。

通过对 `handle.await` 可以等待该任务完成。这里等待的是异步任务的结果，当前异步任务会挂起，不会像 `std::thread::join()` 那样阻塞 worker 线程。

下面这段代码看不到子任务输出：

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

原因是外层 `block_on` 驱动的 `Future` 很快结束，`main` 函数随后结束，runtime 被 drop，尚未完成的子任务也就不会继续推进。

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

## 4、Runtime::spawn

除了 `tokio::spawn`，`Runtime` 本身也提供 `spawn` 方法：

```rust
use tokio::runtime::Runtime;  
  
  
fn main() {  
  
    let rt = Runtime::new().unwrap();  
  
    let handle1 = rt.spawn(async {  
        tokio::time::sleep(tokio::time::Duration::from_secs(3)).await;  
        println!("child task 1 done!");  
        10  
    });  
  
    let handle2 = rt.spawn(async {  
        tokio::time::sleep(tokio::time::Duration::from_secs(2)).await;  
        println!("child task 2 done!");  
        20  
    });  
  
    rt.block_on(async {  
        let value1 = handle1.await.unwrap();  
        let value2 = handle2.await.unwrap();  
        println!("value1: {}, value2: {}", value1, value2);  
    });  
}
```

两者区别如下：

| 写法 | 使用前提 |
| --- | --- |
| `tokio::spawn(...)` | 当前线程已经处于 Tokio runtime 上下文 |
| `rt.spawn(...)` | 手上明确持有某个 `Runtime` 值 |

在 `#[tokio::main]` 或 `rt.block_on(async { ... })` 内部，通常直接使用 `tokio::spawn`。

在同步代码中，如果手上有 `Runtime`，可以使用 `rt.spawn` 把任务提交给这个 runtime。

## 5、Runtime::enter

`Runtime::enter` 的作用是让当前线程进入某个 Tokio Runtime 的上下文，使得当前线程的代码能够感知这个 Runtime。它不会运行 Future，也不会等待 Future 完成。

它常用于让依赖“当前 runtime 上下文”的 API 可以工作，例如 `tokio::spawn`：

```rust
use tokio::runtime::Runtime;
use std::time::Duration;

fn main() {
    let rt = Runtime::new().unwrap();

    let _guard = rt.enter();

    tokio::spawn(async {
        tokio::time::sleep(Duration::from_secs(1)).await;
        println!("task done");
    });
}
```

这里：

```rust
let _guard = rt.enter();
```

表示当前线程进入 `rt` 的上下文。

所以后面的：

```rust
tokio::spawn(...)
```

就知道应该把任务提交到哪个 runtime。

但是要注意：`enter` 只是“设置上下文”，不是“驱动运行时”。

上面的代码中，任务被 `spawn` 进 runtime 了，但如果程序马上退出，任务可能根本来不及执行。真正驱动 Future 执行的仍然需要 `block_on`。

更典型的例子是：

```rust
use tokio::runtime::Runtime;
use std::time::Duration;

fn main() {
    let rt = Runtime::new().unwrap();

    {
        let _guard = rt.enter();

        tokio::spawn(async {
            tokio::time::sleep(Duration::from_secs(1)).await;
            println!("task done");
        });
    }

    rt.block_on(async {
        tokio::time::sleep(Duration::from_secs(2)).await;
    });
}
```

这里分成两步：

- `rt.enter()` 只负责把当前线程标记为“处于 rt 的上下文中”，让 `tokio::spawn` / `tokio::time::sleep` 这类 API 能找到 runtime
- `rt.block_on(...)` 负责真正驱动 Future，并阻塞同步调用者直到入口 Future 完成

`enter` 返回的是一个 guard。只要这个 guard 还活着，当前线程就处在该 runtime 上下文中；guard 被 drop 后，就退出这个上下文。

```rust
let guard = rt.enter();

// 这里处于 Tokio runtime 上下文中

drop(guard);

// 这里已经离开 Tokio runtime 上下文
```

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

## 2、操作系统抢占式调度和 Tokio 协作式调度

### （1）抢占式调度

操作系统调度的是线程。抢占式调度的意思是：

> 一个线程运行一段时间后，即使自己不主动让出 CPU，操作系统也可以强制暂停它，然后切换到另一个线程运行。

例如有两个线程：

- 线程 A：while 循环计算
- 线程 B：处理网络请求

即使线程 A 一直在计算，没有主动停下来，操作系统也会通过时间片机制把 CPU 从线程 A 手里“抢回来”，再分配给线程 B。

![[Pasted image 20260613174430.png|300]]

### （2）Tokio 协作式调度

Tokio 调度的是异步任务，也就是`Future`，它属于用户态调度的轻量级任务。协作式调度的意思：

> 一个异步任务需要在合适的位置主动让出执行权，Tokio 才能去调度其他任务。

在 Rust async 里，最常见的让出执行权的位置就是`.await`：

```rust
async fn task_a() {
    println!("A start");

    tokio::time::sleep(std::time::Duration::from_secs(1)).await;

    println!("A end");
}
```

执行到 `tokio::time::sleep(...).await` 时，如果定时器还没到，当前任务会返回 `Poll::Pending`，相当于告诉 Tokio 我现在不能继续了，你可以先去运行别的任务。

![[Pasted image 20260613175906.png|300]]

### （3）核心区别

- 操作系统抢占式调度：线程不想停，OS 也能强制它停。
- Tokio 协作式调度：任务不主动让出，Tokio 不能在一次 `poll` 调用中强行抢占它

例如：

```rust
async fn bad_task() {
    loop {
        // 长时间 CPU 计算，没有 .await
    }
}
```

因为它内部没有 `.await`，也没有返回 `Poll::Pending`，Tokio 就没有机会切换到同一个 worker 线程上的其他异步任务。

此时解决办法可以使用：

- `tokio::task::yield_now()` 主动让出

```rust
async fn better_task() {
    loop {
        // 做一小段计算

        tokio::task::yield_now().await;
    }
}
```

- `tokio::task::spawn_blocking` 将少量或可控时长的 CPU 计算放到阻塞线程池

```rust
tokio::task::spawn_blocking(|| {
    // 少量 CPU 计算或阻塞 I/O
});
```

### （4）线程调度和任务调度的关系

Tokio 并不是替换操作系统调度。更准确地说：

- 操作系统调度 Tokio 的 worker 线程
- Tokio 的 worker 线程内部调度异步任务

可以这样理解：

```text
操作系统
  │
  ├─ 调度线程 1
  │     └─ Tokio 调度 task A / task B / task C
  │
  ├─ 调度线程 2
  │     └─ Tokio 调度 task D / task E / task F
  │
  └─ 调度线程 3
        └─ Tokio 调度 task G / task H
```

所以它们不是同一层的调度：

| 层级              | 调度者       | 被调度对象 |
| --------------- | --------- | ----- |
| 操作系统层           | OS 内核     | 线程    |
| Tokio runtime 层 | Tokio 调度器 | 异步任务  |

即使某个 Tokio 任务不 `.await`，操作系统仍然可以抢占运行它的线程，切换到其他线程。

## 3、多线程 runtime 的任务迁移

多线程 runtime 的任务迁移是指：

> 一个 `tokio::spawn` 出来的异步任务，不一定一直在同一个 worker thread 上执行。它每次 `.await` 让出执行权后，下一次被唤醒时，可能会被别的 worker thread 继续 `poll`。

因此，`tokio::spawn` 要求被提交的 `Future` 及其输出都满足 `Send + 'static`：

```rust
tokio::spawn(async move {
	// ...
})
```

这两个约束的含义是：

- `Send`：任务可以安全地移动到其他线程执行
- `'static`：任务不能持有可能提前失效的短生命周期引用

这并不表示任务一定会活到程序结束，也不表示内存泄漏。它表示这个任务从类型上看不依赖某个临时借用，因此 runtime 可以安全地管理它的生命周期。

# 五、阻塞代码和 spawn_blocking

## 1、worker thread 和 blocking thread

Tokio runtime 中常见两类线程：

| 线程类型            | 作用                              |
| --------------- | ------------------------------- |
| worker thread   | 执行普通异步任务，负责调度和 `poll`           |
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
use tokio::runtime::Runtime;  
  
fn main() {  
    let rt = Runtime::new().unwrap();  
	  
	// tokio::task::spawn_blocking 需要能找到当前 runtime
    let _guard = rt.enter();  
  
    let handle = tokio::task::spawn_blocking(|| {  
       let mut sum = 0;  
  
        for i in 0..100 {  
		    // 故意 sleep 模拟同步阻塞代码
            std::thread::sleep(std::time::Duration::from_millis(100));  
            sum += i;  
        }  
  
        sum  
    });  
  
    rt.block_on(async {  
        let res = handle.await.unwrap();  
        println!("{}", res);  
    });  
  
}
```

`spawn_blocking` 会把闭包提交到 Tokio 管理的阻塞线程池中执行。它不是普通异步任务，不会在 worker thread 上被反复 `poll`。

它适合：

- 调用同步文件、压缩、加密、解析等阻塞库
- 执行少量或可控时长的 CPU 计算
- 临时桥接无法改写为 async 的旧代码

## 3、blocking 任务不容易取消

普通异步任务可以通过 `JoinHandle::abort` 取消：

```rust
use tokio::runtime::Runtime;  
  
fn main() {  
    let rt = Runtime::new().unwrap();  
  
    rt.block_on(async {  
        let handle = tokio::spawn(async {  
           for i in 1..=10 {  
               tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;  
               println!("Sleeping for {:?}", i);  
           }  
        });  
  
        handle.abort();  
  
        match handle.await {  
            Ok(_) => println!("Done!"),  
            Err(e) if e.is_cancelled() => println!("Cancelled!"),  
            Err(e) => println!("Error: {:?}", e),  
        }  
    })  
  
}
```

输出：

```shell
Cancelled!
```

取消异步任务的本质是：runtime 不再继续 `poll` 这个任务，并丢弃它保存的状态。

但 `spawn_blocking` 不同。一旦阻塞闭包已经在线程中开始执行，Tokio 不能安全地强行杀掉这个 OS 线程。因此：

- 如果 blocking 任务还没开始，`abort` 可能阻止它运行
- 如果 blocking 任务已经开始，`abort` 通常不能让它立刻停止
- runtime 关闭时，也可能需要等待已经开始的 blocking 任务结束

```rust
use tokio::runtime::Runtime;  
  
fn main() {  
    let rt = Runtime::new().unwrap();  
  
    rt.block_on(async {  
        let handle = tokio::task::spawn_blocking(||  {  
           for i in 1..=10 {  
                std::thread::sleep(std::time::Duration::from_secs(1));  
               println!("Hello, {}!", i);  
           }  
        });  
  
        // 故意 sleep，让 blocking 开始  
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;  
  
        handle.abort();  
  
        handle.await.unwrap();  
    })  
  
}
```

可以看到 blocking 任务并不会取消：

```shell
Hello, 1!
Hello, 2!
Hello, 3!
Hello, 4!
Hello, 5!
Hello, 6!
Hello, 7!
Hello, 8!
Hello, 9!
Hello, 10!
```

所以提交给 `spawn_blocking` 的代码应该有明确结束条件。

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

## 1、drop Runtime 

`Runtime` 是一个普通 Rust 值。当它离开作用域时，runtime 会进入关闭流程：

```rust
use tokio::runtime::Runtime;

fn main() {
    let rt = Runtime::new().unwrap();

    rt.block_on(async {
        println!("runtime running");
    });

} // rt 在这里被 drop，Runtime 关闭
```

也可以显式调用 `drop()`：

```rust
drop(rt);
```

如果 Runtime 关闭时，还有 `tokio::spawn` 创建的异步任务没有完成，这些任务会被直接丢弃，不会继续执行。

```rust
use tokio::runtime::Runtime;  
  
  
fn main() {  
    let rt = Runtime::new().unwrap();  
  
    rt.block_on(async {  
        tokio::spawn(async{  
            for i in 0..10 {  
                tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;  
                println!("{}", i);  
            }  
        });  
    });  
    // Runtime 关闭，任务还没完成，会被取消  
}
```

这里 `tokio::spawn` 创建了子任务，但由于 `tokio::spawn` 会直接返回，`block_on` 驱动的外层 `Future` 结束，`main` 函数结束，`rt` 会被 `drop`，此时任务就不会继续被执行。

**但 Runtime 关闭时，已经开始执行的 `spawn_blocking` 任务不能被强行取消，Runtime 默认会等待它们结束**。如果 `spawn_blocking` 任务存在死循环，则进程无法结束。

示例：

```rust
use tokio::runtime::Runtime;  
use std::time::Duration;  
  
fn main() {  
    let rt = Runtime::new().unwrap();  
  
    rt.block_on(async {  
        tokio::task::spawn_blocking(|| {  
            for i in 0..10 {  
                println!("{}", i);  
                std::thread::sleep(Duration::from_secs(1));  
            }  
        });  
  
    })  
  
}
```

原因是普通线程里的同步代码没有 `.await` 边界，Tokio 不能安全地把它中途停掉。

![[Pasted image 20260614010843.png|50]]

## 2、shutdown_timeout

如果不想无限等待阻塞任务，可以用`shutdown_timeout()`。它会等待一段时间，超过时间后返回，不再继续等待。

示例：

```rust
use tokio::runtime::Runtime;  
use tokio::time::Duration;  
  
fn main() {  
    let rt = Runtime::new().unwrap();  
  
    rt.block_on(async {  
        tokio::task::spawn_blocking(|| {  
            for i in 0..10 {  
                println!("{}", i);  
                std::thread::sleep(Duration::from_secs(1));  
            }  
        });  
    });  
  
    rt.shutdown_timeout(tokio::time::Duration::from_secs(5));  
}
```

结果：

![[Pasted image 20260614010808.png|100]]

但注意，`shutdown_timeout` 不会强杀已经运行的 blocking task。超过时间后，runtime 不再等待这些任务结束；已经开始执行的 blocking task 可能继续运行，直到闭包自己返回或进程结束。

## 3、shutdown_background

`shutdown_background()` 在后台关闭，不在当前线程等待完整关闭。它适合“不想在当前线程等待 Runtime 完全关闭”的场景。

示例：

```rust
use tokio::runtime::Runtime;  
use tokio::time::Duration;  
  
fn main() {  
    let rt = Runtime::new().unwrap();  
  
    rt.block_on(async {  
        tokio::task::spawn_blocking(|| {  
            for i in 0..10 {  
                println!("{}", i);  
                std::thread::sleep(Duration::from_secs(1));  
            }  
        });  
    });  
  
    rt.shutdown_background();  
}
```

和 `shutdown_timeout` 一样，`shutdown_background` 不会强行杀掉已经开始执行的 blocking 任务。它们改变的是当前线程等待 runtime 关闭的方式。

因此，在设计阻塞任务时，尽量不要把无限循环放进 `spawn_blocking`，或者给阻塞任务设计退出条件，在关闭前通知阻塞任务停止。


# 七、常见错误

## 1、在没有 Runtime 的地方调用 Tokio API

某些 Tokio API 依赖当前 runtime 上下文。例如：

```rust
fn main() {
    tokio::spawn(async {
        println!("hello");
    });
}
```

这段代码运行会`panic`：

![[Pasted image 20260614011824.png|400]]

因为普通 `main` 函数中没有进入 Tokio runtime，无法调用 `tokio::spawn`。

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
