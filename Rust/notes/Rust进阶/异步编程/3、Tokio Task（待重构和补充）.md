# 一、Task 概述

Tokio Task 是 Tokio Runtime 管理的异步执行单元。它可以理解为：**被 Tokio 调度器接管并推进的 `Future`**。

先看一个普通异步函数：

```rust
async fn work() {
    println!("working");
}
```

调用 `work()` 时，函数体不会立刻执行，而是返回一个 `Future`：

```rust
let future = work();
```

这个 `Future` 只是一个还没有被推进的异步计算。只有当它被 `.await`、被 `Runtime::block_on(...)` 驱动，或者被 `tokio::spawn(...)` 提交给 Tokio Runtime 后，它才会真正执行。

当一个 `Future` 被提交给 Tokio 调度器后，就成为一个 Tokio Task。Runtime 会在合适的时候调用它的 `poll` 方法，推进任务向前执行。

Task 的核心特点如下：

| 特点 | 含义 |
| --- | --- |
| 轻量 | 创建和切换 task 的成本远低于 OS 线程 |
| 非阻塞 | task 等待 I/O 时挂起，而不是阻塞 worker thread |
| 协作式调度 | task 需要在 `.await` 或 `yield_now().await` 等位置让出执行权 |
| 由 runtime 管理 | task 不是 OS 线程，不由操作系统直接调度 |
| 可以有返回值 | `JoinHandle<T>` 可以等待 task 返回 `T` |

Tokio 官方文档把 task 称为异步 green thread。它和 OS 线程相似，都表示一段可以独立推进的执行逻辑；但 OS 线程由操作系统调度，而 Tokio Task 由 Tokio Runtime 调度。


# 二、创建 Task

## 1、tokio::spawn

`tokio::spawn(...)` 用于创建普通异步 task。它接收一个 `Future`，把这个 `Future` 提交给当前 Tokio Runtime，并返回一个 `JoinHandle<T>`。

```rust
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        sleep(Duration::from_secs(1)).await;
        10
    });

    let value = handle.await.unwrap();
    println!("{value}");
}
```

`tokio::spawn(...)` 有几个关键语义：

| 语义 | 说明 |
| --- | --- |
| 提交到 runtime | 调用 `spawn` 后，task 会交给当前 runtime 调度 |
| 后台运行 | 即使不立刻 `.await` 返回的 `JoinHandle`，task 也可以开始运行 |
| 返回句柄 | 返回 `JoinHandle<T>`，用于等待结果或取消任务 |
| 不同步 poll | `spawn` 调用本身不会立刻同步 `poll` 传入的 future |
| 需要 runtime 上下文 | 必须在 Tokio Runtime 上下文中调用 |
| 不保证完成 | runtime 关闭时，尚未完成的 task 会被取消或丢弃 |

需要注意：`tokio::spawn` 创建的是**并发任务**，不是简单函数调用。它不会阻塞当前 task 等子 task 完成。

## 2、task 启动和等待

`spawn` 只是创建并提交 task，不代表当前 task 会等待它完成。

下面的代码可能看不到 `"child done"`：

```rust
#[tokio::main]
async fn main() {
    tokio::spawn(async {
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
        println!("child done");
    });
}
```

原因是：`main` 这个根 Future 很快结束，runtime 随后关闭，子 task 还没来得及完成就被取消。

如果结果很重要，需要保存并等待 `JoinHandle`：

```rust
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
        println!("child done");
        10
    });

    let value = handle.await.unwrap();
    println!("{value}");
}
```

这里的 `handle.await` 是异步等待。当前 task 会挂起，不会像 `std::thread::join()` 那样阻塞 worker thread。

## 3、Runtime::spawn

如果手上已经有一个 `Runtime`，也可以使用 `rt.spawn(...)` 创建 task：

```rust
use tokio::runtime::Runtime;

fn main() {
    let rt = Runtime::new().unwrap();

    let handle = rt.spawn(async {
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
        10
    });

    let value = rt.block_on(handle).unwrap();
    println!("{value}");
}
```

两种写法的选择：

| 写法 | 适合位置 |
| --- | --- |
| `tokio::spawn(...)` | 已经处于 Tokio Runtime 上下文的 async 代码 |
| `rt.spawn(...)` | 同步代码中明确持有某个 `Runtime` 值 |

在 `#[tokio::main]` 或 `rt.block_on(async { ... })` 内部，通常直接使用 `tokio::spawn`。

在普通同步代码中，如果明确持有一个 `Runtime` 值，可以用 `rt.spawn` 把任务提交给这个 runtime。


# 三、JoinHandle

## 1、基本含义

`JoinHandle<T>` 是 task 的控制句柄。它可以等待 task 完成，并取得 task 的输出。

如果 task 返回 `i32`，句柄类型就是 `JoinHandle<i32>`：

```rust
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        5 + 3
    });

    let value = handle.await.unwrap();
    println!("{value}");
}
```

如果 task 没有显式返回值，句柄类型就是 `JoinHandle<()>`。

```rust
let handle = tokio::spawn(async {
    println!("I return nothing.");
});
```

需要注意：`handle.await` 的结果不是直接的 `T`，而是：

```rust
Result<T, tokio::task::JoinError>
```

因为 task 可能正常结束，也可能被取消或发生 panic。

| 结果 | 含义 |
| --- | --- |
| `Ok(value)` | task 正常完成，返回 `value` |
| `Err(err)` 且 `err.is_cancelled()` | task 被取消 |
| `Err(err)` 且 `err.is_panic()` | task 内部发生 panic |

## 2、返回 Result 的 task

如果 task 自己也返回 `Result<T, E>`，那么 `handle.await` 会形成两层 `Result`：

```rust
use std::io;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let handle = tokio::spawn(async {
        Ok::<i32, io::Error>(8)
    });

    let value = handle.await??;
    println!("{value}");

    Ok(())
}
```

这里的两层含义是：

| 写法 | 处理对象 |
| --- | --- |
| 第一个 `?` | 处理 `JoinError` |
| 第二个 `?` | 处理 task 自己返回的 `io::Error` |

## 3、丢弃 JoinHandle

丢弃 `JoinHandle` 不会取消 task，而是让 task 和句柄分离。

```rust
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
        println!("still running");
    });

    drop(handle);

    tokio::time::sleep(std::time::Duration::from_secs(2)).await;
}
```

`drop(handle)` 后，task 仍然可以继续在后台运行，但已经没有句柄可以等待它的返回值。这个返回值会被丢弃。

这和调用 `abort()` 不同：

| 操作 | 结果 |
| --- | --- |
| `drop(handle)` | 分离 task，不等待结果，不取消 task |
| `handle.abort()` | 请求取消 task |

## 4、JoinHandle 的取消安全

`&mut JoinHandle<T>` 是 cancel safe 的。也就是说，把同一个 `JoinHandle` 放进 `tokio::select!` 中等待时，如果本轮 `select!` 是其他分支先完成，task 的返回值不会因此丢失。

```rust
#[tokio::main]
async fn main() {
    let mut handle = tokio::spawn(async {
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
        10
    });

    tokio::select! {
        value = &mut handle => {
            println!("task finished: {:?}", value);
        }
        _ = tokio::time::sleep(std::time::Duration::from_millis(100)) => {
            println!("timeout first");
        }
    }

    let value = handle.await.unwrap();
    println!("{value}");
}
```

这里第一次 `select!` 中超时分支先完成，但 `handle` 仍然可以继续被等待。


# 四、Task 取消

## 1、abort

可以通过 `JoinHandle::abort()` 请求取消 task：

```rust
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        loop {
            tokio::time::sleep(std::time::Duration::from_secs(1)).await;
            println!("tick");
        }
    });

    tokio::time::sleep(std::time::Duration::from_millis(100)).await;
    handle.abort();

    match handle.await {
        Ok(_) => println!("finished"),
        Err(err) if err.is_cancelled() => println!("cancelled"),
        Err(err) => println!("task failed: {err}"),
    }
}
```

可能输出：

```shell
cancelled
```

`abort()` 的含义不是在任意机器指令处强行杀掉 task。它会通知 runtime 取消这个 task：

- 如果 task 已经在 `.await` 处挂起，runtime 可以尽快停止它
- 如果 task 正在一次 `poll` 调用中运行，需要等它把执行权还给 runtime

task 被取消时，已经创建的局部变量会被 drop。等待被取消的 `JoinHandle`，通常会得到 `JoinError`。

`abort()` 只是发出取消请求。要确认取消已经完成，需要继续等待 `handle.await`。

## 2、取消和正常完成

调用 `abort()` 后，不保证 `JoinHandle` 一定返回 cancelled 错误。因为 task 可能在取消生效前已经正常完成。

```rust
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        10
    });

    tokio::time::sleep(tokio::time::Duration::from_millis(1)).await;
    handle.abort();

    match handle.await {
        Ok(value) => println!("finished: {value}"),
        Err(err) if err.is_cancelled() => println!("cancelled"),
        Err(err) => println!("failed: {err}"),
    }
}
```

如果 task 在 `abort()` 之前已经完成，那么最终会得到 `Ok(value)`。

## 3、runtime 关闭

Runtime 关闭时，尚未完成的普通异步 task 会被取消。

```rust
#[tokio::main]
async fn main() {
    tokio::spawn(async {
        tokio::time::sleep(std::time::Duration::from_secs(10)).await;
        println!("will not print");
    });
}
```

上面代码中，外层 `main` 很快结束，runtime 被关闭，未完成的子 task 不会继续执行。


# 五、Send、'static 和所有权

## 1、spawn 的类型约束

`tokio::spawn` 的核心签名可以简化为：

```rust
pub fn spawn<F>(future: F) -> JoinHandle<F::Output>
where
    F: Future + Send + 'static,
    F::Output: Send + 'static,
```

这表示：

| 约束 | 含义 |
| --- | --- |
| `F: Send` | task 可以在线程之间安全移动 |
| `F: 'static` | task 不能持有可能提前失效的短生命周期引用 |
| `F::Output: Send` | task 的输出可以在线程之间安全移动 |
| `F::Output: 'static` | task 的输出不能依赖短生命周期引用 |

这些约束和 Tokio 的多线程调度有关。一个 task 在 `.await` 处挂起后，下一次被唤醒时，可能会被另一个 worker thread 继续 `poll`。

`'static` 不表示 task 一定活到程序结束，也不表示内存泄漏。它表示从类型上看，这个 task 不借用某个可能提前失效的局部变量。

## 2、捕获局部变量

示例：

```rust
#[tokio::main]
async fn main() {
    let s = String::from("hello");

    tokio::spawn(async {
        println!("{}", s);
    });
}
```

这段代码会编译报错。`tokio::spawn` 创建的异步任务不能借用局部变量，因为 spawn 出来的任务不保证一定在 `main` 结束前执行完。

更常见的写法是把所有权移动进 task：

```rust
#[tokio::main]
async fn main() {
    let s = String::from("hello");

    tokio::spawn(async move {
        println!("{s}");
    })
    .await
    .unwrap();
}
```

这里 `async move` 会把 `s` 的所有权移动进异步块。task 不再借用外部局部变量，因此满足 `'static` 要求。

如果多个 task 都需要访问同一份数据，通常使用 `Arc<T>` 共享所有权：

```rust
use std::sync::Arc;

#[tokio::main]
async fn main() {
    let data = Arc::new(String::from("hello"));

    let h1 = {
        let data = Arc::clone(&data);
        tokio::spawn(async move {
            println!("task1: {data}");
        })
    };

    let h2 = {
        let data = Arc::clone(&data);
        tokio::spawn(async move {
            println!("task2: {data}");
        })
    };

    h1.await.unwrap();
    h2.await.unwrap();
}
```

## 3、!Send 值

`tokio::spawn` 要求整个 task 是 `Send`，但这不表示 task 内部完全不能出现 `!Send` 值。

如果 `!Send` 值只存在于两个 `.await` 之间，不跨越 `.await`，通常可以通过编译：

```rust
use std::rc::Rc;

#[tokio::main]
async fn main() {
    tokio::spawn(async {
        {
            let value = Rc::new(1);
            println!("{value}");
        }

        tokio::task::yield_now().await;
    })
    .await
    .unwrap();
}
```

这里的内部代码块是有意义的：

```rust
{
    let value = Rc::new(1);
    println!("{value}");
}
```

`value` 在 `.await` 之前离开作用域并被释放，因此没有 `Rc<T>` 跨越 `.await`。

但如果 `Rc<T>` 跨越 `.await`，整个 future 就不是 `Send`：

```rust
use std::rc::Rc;

#[tokio::main]
async fn main() {
    tokio::spawn(async {
        let value = Rc::new(10);

        tokio::task::yield_now().await;

        println!("{value}");
    });
}
```

这类代码应该改用 `Arc<T>`，或者使用 `LocalSet` / `spawn_local` 在单线程本地任务集中运行。


# 六、本地任务

## 1、LocalSet 和 spawn_local

`LocalSet` 用来运行 `!Send` 的本地 task。这些 task 会在同一个线程上执行，不会被移动到其他 worker thread。

典型场景是使用 `Rc<T>`、`RefCell<T>` 等不能跨线程移动的类型。

`LocalSet` 本身不是 runtime，它只是一个本地任务集合，真正驱动任务运行的仍然是 Tokio Runtime。

示例：

```rust
use std::rc::Rc;
use tokio::runtime::Runtime;
use tokio::task::LocalSet;

fn main() {
    let rt = Runtime::new().unwrap();
    let local = LocalSet::new();

    rt.block_on(local.run_until(async {
        let handle = tokio::task::spawn_local(async {
            let n = Rc::new(10);

            tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
            println!("{n}");
        });

        handle.await.unwrap();
    }));
}
```

这段代码虽然使用的是多线程 runtime，但 `Rc<T>` 所在的任务是通过 `spawn_local` 放进 `LocalSet` 运行的，因此它被限制在创建 `LocalSet` 的线程上，不会跨线程迁移。

`LocalSet::run_until(future)` 用于在当前线程进入这个 `LocalSet` 的本地任务上下文，驱动其中的 `spawn_local` 任务，并一直运行到传入的 `future` 完成。

在 `LocalSet` 本地任务上下文中，仍然可以通过 `tokio::spawn` 创建普通 `Send` task：

```rust
use tokio::runtime::Runtime;
use tokio::task::LocalSet;

fn main() {
    let rt = Runtime::new().unwrap();
    let local = LocalSet::new();

    rt.block_on(local.run_until(async {
        let handle1 = tokio::task::spawn_local(async {
            tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
            println!("local task done");
        });

        let handle2 = tokio::spawn(async {
            tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
            println!("send task done");
        });

        handle1.await.unwrap();
        handle2.await.unwrap();
    }));
}
```


# 七、阻塞任务

## 1、worker thread 和 blocking thread

Tokio runtime 中常见两类线程：

| 线程类型 | 作用 |
| --- | --- |
| worker thread | 执行普通异步任务，负责调度和 `poll` |
| blocking thread | 执行通过 `spawn_blocking` 提交的同步阻塞代码 |

普通异步 task 运行在 worker thread 上。worker thread 不适合长期阻塞，因为它还要负责调度其他异步任务。

下面这种写法会直接卡住 worker thread：

```rust
#[tokio::main]
async fn main() {
    std::thread::sleep(std::time::Duration::from_secs(10));
}
```

如果 runtime 只有少量 worker thread，而这些线程都被阻塞，其他异步任务就无法及时被调度。

## 2、spawn_blocking

`tokio::task::spawn_blocking(...)` 用于把同步阻塞闭包放到 Tokio 的阻塞线程池执行。

```rust
#[tokio::main]
async fn main() {
    let handle = tokio::task::spawn_blocking(|| {
        let mut sum = 0;

        for i in 0..100 {
            std::thread::sleep(std::time::Duration::from_millis(10));
            sum += i;
        }

        sum
    });

    let value = handle.await.unwrap();
    println!("{value}");
}
```

在这里，传入 `spawn_blocking` 的闭包可以运行同步阻塞代码，因为它在 Tokio 的阻塞线程池中运行，而不是在普通 worker thread 上运行。

它和 `tokio::spawn` 的区别如下：

| 写法 | 参数 | 执行位置 | 是否被反复 `poll` |
| --- | --- | --- | --- |
| `tokio::spawn` | `Future` | worker thread | 是 |
| `tokio::task::spawn_blocking` | 同步闭包 | blocking thread pool | 否 |

`spawn_blocking` 适合：

- 调用同步阻塞库
- 执行同步文件、压缩、解析等操作
- 桥接无法改成 async 的旧代码
- 执行少量或可控时长的 CPU 计算

对于长期、密集、可并行的 CPU 计算，更常见的做法是使用专门的计算线程池，例如 `rayon`，避免把 Tokio 的阻塞线程池当成通用 CPU 计算池。

## 3、block_in_place

`tokio::task::block_in_place(...)` 也可以在异步上下文中运行同步阻塞代码，但它和 `spawn_blocking` 的执行模型不同。

`block_in_place` 会告诉多线程 runtime：当前 task 接下来要阻塞当前 worker thread。Runtime 可以先把这个 worker thread 上的其他任务转移给其他 worker thread，然后在当前线程上执行传入的阻塞闭包。

```rust
#[tokio::main]
async fn main() {
    let value = tokio::task::block_in_place(|| {
        std::thread::sleep(std::time::Duration::from_millis(100));
        10
    });

    println!("{value}");
}
```

`block_in_place` 和 `spawn_blocking` 的区别如下：

| 写法 | 执行方式 | 返回方式 |
| --- | --- | --- |
| `spawn_blocking` | 把闭包提交到 blocking thread pool | 返回 `JoinHandle<R>`，需要 `.await` |
| `block_in_place` | 在当前 worker thread 上切换为阻塞模式运行闭包 | 直接返回 `R` |

使用 `block_in_place` 时要注意：

- 只能在多线程 runtime 中使用，不能在 current-thread runtime 中使用
- 它会阻塞当前 task 内部的其他并发分支，例如同一个 `join!` 中的其他 future
- 闭包一旦开始执行，也不能被异步取消
- 多数情况下，`spawn_blocking` 更容易控制阻塞代码和异步代码之间的边界

因此，学习和业务代码中优先使用 `spawn_blocking`。只有在确实希望避免额外提交到 blocking thread pool，并且清楚当前 runtime 是多线程 runtime 时，再考虑 `block_in_place`。

## 4、blocking 任务取消

已经开始执行的 `spawn_blocking` 任务通常不能被 `abort()` 取消，因为它不是异步 task，执行过程中没有 `.await` 边界可以让 runtime 停止继续 `poll`。

```rust
#[tokio::main]
async fn main() {
    let handle = tokio::task::spawn_blocking(|| {
        std::thread::sleep(std::time::Duration::from_secs(3));
        println!("blocking done");
    });

    handle.abort();

    let _ = handle.await;
}
```

如果 blocking 任务还没开始运行，`abort()` 可能阻止它启动；如果已经开始运行，闭包通常会继续执行到结束。


# 八、多个任务的管理

## 1、Vec<JoinHandle<T>>

如果任务数量较少，并且需要按创建顺序收集结果，可以把 `JoinHandle` 放进 `Vec`：

```rust
#[tokio::main]
async fn main() {
    let mut handles = Vec::new();

    for i in 0..3 {
        handles.push(tokio::spawn(async move {
            i * 2
        }));
    }

    for handle in handles {
        let value = handle.await.unwrap();
        println!("{value}");
    }
}
```

这个写法会按 `Vec` 中的顺序等待结果，不一定按任务完成顺序处理结果。

## 2、JoinSet

`JoinSet<T>` 用于管理一组同类型 task，并按完成顺序取回结果。

```rust
use tokio::task::JoinSet;

#[tokio::main]
async fn main() {
    let mut set = JoinSet::new();

    for i in 0..3 {
        set.spawn(async move {
            tokio::time::sleep(tokio::time::Duration::from_secs(3 - i)).await;
            i * 2
        });
    }

    while let Some(res) = set.join_next().await {
        let value = res.unwrap();
        println!("{value}");
    }
}
```

当不关心创建顺序，只想哪个任务先完成就先处理哪个结果时，`JoinSet` 比 `Vec<JoinHandle<T>>` 更自然。

`JoinSet` 适合：

- 动态创建一批同类型 task
- 按完成顺序处理结果
- 在循环中持续加入和回收任务

如果 task 的返回类型不同，通常需要拆分多个 `JoinSet`，或者把返回值统一成同一个 enum。

需要注意：`JoinSet` 被 drop 时，会立即 abort 它内部仍在运行的所有 task。如果只是想放弃继续管理这些 task，但允许它们在后台继续运行，可以使用 `detach_all()`。


# 九、协作式调度和 yield_now

## 1、协作式调度

Tokio task 使用协作式调度。它的意思是：

> 一个异步任务需要在合适的位置主动让出执行权，Tokio 才能去调度其他任务。

在 Rust async 里，最常见的让出执行权的位置就是 `.await`：

```rust
async fn task_a() {
    println!("A start");

    tokio::time::sleep(std::time::Duration::from_secs(1)).await;

    println!("A end");
}
```

执行到 `tokio::time::sleep(...).await` 时，如果定时器还没到，当前任务会返回 `Poll::Pending`，相当于告诉 Tokio：我现在不能继续了，你可以先去运行别的任务。

如果一个 task 长时间执行 CPU 计算，并且中间没有 `.await`，Tokio 就没有机会在同一个 worker thread 上切换到其他 task：

```rust
async fn bad_task() {
    loop {
        // 长时间 CPU 计算，没有 .await
    }
}
```

这类代码会影响同一 worker thread 上其他异步任务的调度。

## 2、yield_now

`tokio::task::yield_now()` 用来让当前 Tokio task 主动让出一次执行机会，把控制权交还给 Runtime 调度器。

它本身是一个异步函数，只有写成下面这样才真正发生让出：

```rust
tokio::task::yield_now().await;
```

调用后，当前 task 会被重新放回调度队列，Runtime 可以先调度其他已经就绪的 task。当当前 task 再次被调度时，会从 `yield_now().await` 后面继续执行。

示例：

```rust
use tokio::task;

#[tokio::main]
async fn main() {
    task::spawn(async {
        println!("spawned task done!");
    });

    task::yield_now().await;

    println!("main task done!");
}
```

需要注意：`yield_now()` **不保证调度顺序**。即使当前 task 主动 yield，下一轮调度也可能仍然继续调度当前 task。不能依赖它来实现严格的任务执行顺序。

它适合在较长的异步计算循环中偶尔让出执行权，避免一个 task 长时间占用 worker thread：

```rust
async fn better_task() {
    loop {
        // 做一小段计算

        tokio::task::yield_now().await;
    }
}
```


# 十、spawn、join! 和 select! 的关系

## 1、spawn 和 join! 的区别

`tokio::spawn` 会创建新的 task。新 task 被提交给 runtime 调度，可能和当前 task 在同一个线程上交替执行，也可能在多线程 runtime 中被移动到其他 worker thread 上执行。

`tokio::join!` 不会创建新的 task。它只是在**当前 task 内部**同时等待多个 `Future`，由当前 task 轮流 `poll` 这些 future。

示例：

```rust
async fn fetch_user() -> String {
    tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
    "user".to_string()
}

async fn fetch_order() -> String {
    tokio::time::sleep(tokio::time::Duration::from_secs(3)).await;
    "order".to_string()
}

#[tokio::main]
async fn main() {
    let (user, order) = tokio::join!(fetch_user(), fetch_order());

    println!("{user}");
    println!("{order}");
}
```

`join!` 返回的是一个元组，顺序和传入的 `Future` 顺序一致：

```rust
let (a, b, c) = tokio::join!(fa(), fb(), fc());
```

如果这些 Future 返回的是 `Result`，`join!` 仍然会等待所有分支完成，即使其中某个分支已经返回 `Err`。

## 2、try_join!

`tokio::try_join!` 适合多个 Future 都返回 `Result` 的场景。

它也会在同一个异步 task 中并发等待多个 `Future`：

- 如果所有 `Future` 都返回 `Ok(_)`，最终返回 `Ok((...))`
- 如果任意 `Future` 返回 `Err(_)`，立即返回这个错误，不再继续等待其他分支完成

```rust
use tokio::time::{sleep, Duration};

async fn fetch_user() -> Result<String, &'static str> {
    sleep(Duration::from_secs(1)).await;
    Ok("user".to_string())
}

async fn fetch_order() -> Result<String, &'static str> {
    sleep(Duration::from_secs(1)).await;
    Ok("order".to_string())
}

#[tokio::main]
async fn main() -> Result<(), &'static str> {
    let (user, order) = tokio::try_join!(
        fetch_user(),
        fetch_order()
    )?;

    println!("{user}, {order}");

    Ok(())
}
```

对比关系如下：

| 写法 | 是否创建新 task | 完成条件 | 返回值 |
| --- | --- | --- | --- |
| `tokio::spawn` | 是 | 被 spawn 的 task 自己完成 | `JoinHandle<T>` |
| `tokio::join!` | 否 | 所有分支完成 | `(A, B, ...)` |
| `tokio::try_join!` | 否 | 全部 `Ok`，或第一个 `Err` | `Result<(A, B, ...), E>` |

## 3、select!

`tokio::select!` 用来同时等待多个异步分支，哪个分支先完成，就执行哪个分支对应的处理逻辑，然后整个 `select!` 表达式结束。

基本形式如下：

```rust
tokio::select! {
    result = future_a() => {
        // future_a 先完成的处理逻辑
    }
    result = future_b() => {
        // future_b 先完成的处理逻辑
    }
}
```

例如，同时等待一个任务完成或一个超时事件：

```rust
async fn do_work() -> &'static str {
    tokio::time::sleep(tokio::time::Duration::from_secs(3)).await;
    "work done!"
}

#[tokio::main]
async fn main() {
    tokio::select! {
        result = do_work() => {
            println!("任务完成：{result}");
        }

        _ = tokio::time::sleep(tokio::time::Duration::from_secs(1)) => {
            println!("超时!");
        }
    }
}
```

输出：

```shell
超时!
```

没有被选中的分支会被取消。因此，`select!` 里的 future 如果持有资源或有副作用，要确认取消语义是可以接受的。

`select!` 也常用于事件循环中，例如同时监听消息和退出信号：

```rust
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel::<String>(8);

    tokio::spawn(async move {
        for i in 0..10 {
            tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
            tx.send(format!("message {i}")).await.unwrap();
        }
    });

    loop {
        tokio::select! {
            msg = rx.recv() => {
                match msg {
                    Some(msg) => println!("收到消息：{msg}"),
                    None => break,
                }
            }

            _ = tokio::signal::ctrl_c() => {
                println!("收到 Ctrl+C，退出");
                break;
            }
        }
    }
}
```

默认情况下，`select!` 会随机选择检查分支的顺序，这样在循环中多个分支总是 ready 时，可以提供一定公平性。也可以使用 `biased;` 改成从上到下固定顺序轮询。

```rust
tokio::select! {
    biased;

    _ = future_a() => {
        println!("A");
    }
    _ = future_b() => {
        println!("B");
    }
}
```

使用 `biased;` 后，分支顺序就由你自己负责。如果前面的分支经常 ready，后面的分支可能长期得不到机会，因此一般只有在确实需要固定优先级时才使用。


# 十一、常见使用建议

## 1、什么时候使用 spawn

适合使用 `tokio::spawn` 的场景：

- 每个连接、请求、订阅或后台任务都有相对独立的生命周期
- 当前 task 不需要立即等待结果
- 任务之间需要并发推进
- 需要把一批任务交给 runtime 调度

典型例子是网络服务中为每个连接创建一个 task：

```rust
use tokio::net::{TcpListener, TcpStream};

async fn process(socket: TcpStream) {
    // 处理连接
}

#[tokio::main]
async fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:8080").await?;

    loop {
        let (socket, _) = listener.accept().await?;

        tokio::spawn(async move {
            process(socket).await;
        });
    }
}
```

## 2、什么时候不需要 spawn

如果只是想在当前 async 函数里同时等待几个 `Future`，通常不需要 `spawn`，直接用 `join!` / `try_join!` 更简单。

```rust
let (a, b) = tokio::join!(future_a(), future_b());
```

如果只是调用一个异步函数并等待它完成，直接 `.await` 就够了：

```rust
let value = compute().await;
```

过度使用 `spawn` 会让生命周期、取消、错误处理和结果收集都更复杂。

## 3、不要在普通 task 中长时间阻塞

普通 `tokio::spawn` 里的代码运行在 worker thread 上。不要在里面长时间调用：

- `std::thread::sleep`
- 阻塞式文件或网络 I/O
- 长时间 CPU 密集循环
- 长时间持有同步锁

对应处理方式如下：

| 问题 | 更合适的方式 |
| --- | --- |
| 异步等待时间 | `tokio::time::sleep(...).await` |
| 同步阻塞库 | `tokio::task::spawn_blocking(...)` |
| 长时间 CPU 计算 | 独立线程池或 `rayon` |
| 循环中偶尔计算较久 | 拆小批次，并适当 `yield_now().await` |


# 十二、参考资料

- [Tokio 官方文档：tokio::task 模块](https://docs.rs/tokio/latest/tokio/task/index.html)
- [Tokio 官方教程：Spawning](https://tokio.rs/tokio/tutorial/spawning)
- [Tokio API 文档：tokio::task::spawn](https://docs.rs/tokio/latest/tokio/task/fn.spawn.html)
- [Tokio API 文档：JoinHandle](https://docs.rs/tokio/latest/tokio/task/struct.JoinHandle.html)
- [Tokio API 文档：LocalSet](https://docs.rs/tokio/latest/tokio/task/struct.LocalSet.html)
- [Tokio API 文档：spawn_blocking](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html)
- [Tokio API 文档：block_in_place](https://docs.rs/tokio/latest/tokio/task/fn.block_in_place.html)
