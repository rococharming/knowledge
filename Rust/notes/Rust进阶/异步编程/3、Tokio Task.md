# 一、Task 概述

Tokio Task 是 Tokio 运行时调度的异步执行单元。它可以理解为“被 Tokio Runtime 管理并推进的 `Future`”。

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

Task 的核心特点如下：

| 特点           | 含义                                               |
| ------------ | ------------------------------------------------ |
| 轻量           | 创建和切换 task 的成本远低于 OS 线程                          |
| 非阻塞          | task 等待 I/O 时挂起，而不是阻塞 worker 线程                  |
| 协作式调度        | task 需要在 `.await` 或 `yield_now().await` 等位置让出执行权 |
| 由 runtime 管理 | task 不是 OS 线程，不由操作系统直接调度                         |
| 可以有返回值       | `JoinHandle<T>` 可以等待 task 返回 `T`                 |

# 二、创建 Task

## 1、tokio::spawn

`tokio::spawn(...)` 用于创建普通异步 task。它接收一个 `Future`，把它提交给当前 Tokio Runtime，并返回一个 `JoinHandle<T>`。

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
| 立即提交 | 调用 `spawn` 后，task 会被提交给 runtime |
| 返回句柄 | 返回 `JoinHandle<T>`，用于等待结果或取消任务 |
| 不同步 poll | `spawn` 调用本身不会立刻同步 `poll` 传入的 task |
| 需要 runtime 上下文 | 必须在 Tokio Runtime 上下文中调用 |
| 不保证完成 | runtime 关闭时，尚未完成的 task 会被取消 |

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

`drop(handle)` 后，task 仍然可以继续在后台运行，但已经没有句柄可以等待它的返回值。

这和调用 `abort()` 不同：

| 操作 | 结果 |
| --- | --- |
| `drop(handle)` | 分离 task，不等待结果，不取消 task |
| `handle.abort()` | 请求取消 task |

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

输出：

```shell
cancelled
```

`abort()` 的含义不是在任意机器指令处强行杀掉 task。它会通知 runtime 取消这个 task：

- 如果 task 已经在 `.await` 处挂起，runtime 可以尽快停止它
- 如果 task 正在一次 `poll` 调用中运行，需要等它把执行权还给 runtime

task 被取消时，已经持有的局部变量会被 drop。等待被取消的 `JoinHandle`，通常会得到 `JoinError`

`abort()` 只是发出取消请求。要确认取消已经完成，需要继续等待 `handle.await`。

## 2、取消和正常完成

调用 `abort()` 后，不保证 `JoinHandle` 一定返回 cancelled 错误。因为 task 可能在取消生效前已经正常完成。

```rust
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        10
    });
    
    // 故意 sleep
    tokio::time::sleep(tokio::time::Duration::from_millis(1)).await;

    handle.abort();

    match handle.await {
        Ok(value) => println!("finished: {value}"),
        Err(err) if err.is_cancelled() => println!("cancelled"),
        Err(err) => println!("failed: {err}"),
    }
}
```


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

上面代码中，外层 `block_on` 很快结束，`main` 结束后 runtime 被 drop，未完成的子 task 不会继续执行。

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

下面代码会出错：

```rust
#[tokio::main]
async fn main() {
    let s = String::from("hello");
    let r = &s;

    tokio::spawn(async move {
        println!("{r}");
    });
}
```

`r` 借用了局部变量 `s`，而 `tokio::spawn` 创建的 task 可能在当前作用域结束后仍然存在，因此这个引用不满足 `'static`。

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
  
    });  
  
    tokio::time::sleep(tokio::time::Duration::from_secs(10)).await;  
}
```

这里的：

```rust
{  
	let value = Rc::new(1);  
	println!("{value}");  
}  
```

代码块`{}`是必须的，这样会让`value`离开作用域被释放。

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

## 1、LocalSet

`LocalSet` 用来运行 `!Send` 的本地 task。这些 task 会在同一个线程上执行，不会被移动到其他 worker thread。

典型场景是使用 `Rc<T>`、`RefCell<T>` 等不能跨线程移动的类型。

示例：

```rust
use std::rc::Rc;
use tokio::task::LocalSet;

fn main() {
    let rt = tokio::runtime::Builder::new_current_thread()
        .enable_all()
        .build()
        .unwrap();

    let local = LocalSet::new();

    rt.block_on(local.run_until(async {
        let value = Rc::new(10);

        tokio::task::spawn_local(async move {
            println!("{value}");
        })
        .await
        .unwrap();
    }));
}
```

`spawn_local` 创建的是本地 task。它不要求 future 是 `Send`，但必须运行在 `LocalSet` 或支持本地任务的 runtime 上下文中。

## 2、spawn 和 spawn_local

| 写法 | task 是否需要 `Send` | 运行位置 |
| --- | --- | --- |
| `tokio::spawn(...)` | 需要 | Tokio Runtime，可跨 worker thread 移动 |
| `tokio::task::spawn_local(...)` | 不需要 | 当前 `LocalSet` 或本地 runtime |

选择标准：

- task 需要跨线程调度：使用 `tokio::spawn`
- task 内部持有 `Rc<T>`、`RefCell<T>` 等 `!Send` 值并跨 `.await`：使用 `LocalSet` + `spawn_local`
- 能改成 `Arc<T>` / `Mutex<T>` 等线程安全类型：优先考虑普通 `tokio::spawn`

# 八、协作式调度

## 1、让出执行权

Tokio task 使用协作式调度。一个 task 只有在合适的位置让出执行权，runtime 才有机会调度同一 worker thread 上的其他 task。

常见让出位置：

- `.await` 一个尚未就绪的异步操作
- 显式调用 `tokio::task::yield_now().await`

示例：

```rust
async fn work() {
    for _ in 0..100 {
        // 做一小段计算

        tokio::task::yield_now().await;
    }
}
```

`yield_now().await` 会把执行权交还给 Tokio 调度器，让其他 task 有机会运行。之后当前 task 仍然会再次被调度。

## 2、长时间计算

下面的 task 会长时间占住 worker thread：

```rust
async fn bad_task() {
    loop {
        // 长时间 CPU 计算，没有 .await
    }
}
```

问题不在于它是循环，而在于它没有 `.await`，也没有其他让出执行权的位置。Tokio 无法在一次 `poll` 调用内部强行抢占这个 task。

处理方式：

- 把计算拆小，在合适位置调用 `yield_now().await`
- 使用 `spawn_blocking` 执行少量或可控时长的阻塞/计算逻辑
- 对大量 CPU 密集计算，使用专门的计算线程池，例如 Rayon
- 对长期运行的同步后台逻辑，使用专门 OS 线程

# 九、阻塞任务

## 1、spawn_blocking

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

它和 `tokio::spawn` 的区别如下：

| 写法 | 参数 | 执行位置 | 是否被反复 `poll` |
| --- | --- | --- | --- |
| `tokio::spawn` | `Future` | worker thread | 是 |
| `tokio::task::spawn_blocking` | 同步闭包 | blocking thread pool | 否 |

`spawn_blocking` 适合：

- 调用同步阻塞库
- 执行同步文件、压缩、解析等操作
- 执行少量或可控时长的 CPU 计算

不适合：

- 无限循环
- 长期后台 worker
- 大量 CPU 密集计算且没有并发限制

## 2、blocking 任务取消

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

因此，提交给 `spawn_blocking` 的任务应该有明确结束条件。长期运行的同步逻辑更适合使用 `std::thread::spawn` 创建专门线程。

# 十、多个任务的管理

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
            i * 2
        });
    }

    while let Some(result) = set.join_next().await {
        let value = result.unwrap();
        println!("{value}");
    }
}
```

当不关心创建顺序，只想哪个任务先完成就先处理哪个结果时，`JoinSet` 比 `Vec<JoinHandle<T>>` 更自然。

# 十一、常见错误

## 1、没有 Runtime 上下文

`tokio::spawn` 必须在 Tokio Runtime 上下文中调用。

错误示例：

```rust
fn main() {
    tokio::spawn(async {
        println!("hello");
    });
}
```

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

## 2、误以为 JoinHandle drop 会取消任务

`drop(handle)` 不会取消 task：

```rust
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
        println!("done");
    });

    drop(handle);

    tokio::time::sleep(std::time::Duration::from_secs(2)).await;
}
```

如果需要取消，要调用 `abort()`：

```rust
handle.abort();
```

## 3、在 task 中执行阻塞操作

错误示例：

```rust
#[tokio::main]
async fn main() {
    tokio::spawn(async {
        std::thread::sleep(std::time::Duration::from_secs(10));
    });
}
```

这会阻塞当前 worker thread。异步等待应该使用 `tokio::time::sleep(...).await`：

```rust
#[tokio::main]
async fn main() {
    tokio::spawn(async {
        tokio::time::sleep(std::time::Duration::from_secs(10)).await;
    })
    .await
    .unwrap();
}
```

必须调用同步阻塞代码时，使用 `spawn_blocking`：

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

## 4、把 join! 当成 spawn

`tokio::join!` 不会自动创建新 task。它会在当前 task 中并发推进多个 `Future`。

```rust
#[tokio::main]
async fn main() {
    let a = async { 1 };
    let b = async { 2 };

    let (x, y) = tokio::join!(a, b);
    println!("{x}, {y}");
}
```

如果希望两个工作成为独立 task，需要使用 `tokio::spawn`：

```rust
#[tokio::main]
async fn main() {
    let a = tokio::spawn(async { 1 });
    let b = tokio::spawn(async { 2 });

    let (x, y) = tokio::join!(a, b);

    println!("{}, {}", x.unwrap(), y.unwrap());
}
```

# 十二、整体理解

Tokio Task 可以按下面这条线理解：

1. `async fn` / `async { ... }` 产生 `Future`
2. `tokio::spawn(...)` 把 `Future` 注册成 runtime 管理的 task
3. task 在 worker thread 上被 `poll`
4. task 在 `.await` 处挂起，让出 worker thread
5. 等待的资源就绪后，runtime 重新调度 task
6. `JoinHandle<T>` 可以等待 task 完成并取得结果
7. `abort()` 可以请求取消普通异步 task
8. `spawn_blocking` 用于把同步阻塞闭包放到阻塞线程池

一句话总结：

> Tokio Task 是 Rust async 代码进入 Tokio 调度系统后的执行单元；它不是 OS 线程，而是由 runtime 在 worker thread 上协作式推进的轻量任务。

# 参考资料

- [Tokio task module documentation](https://docs.rs/tokio/latest/tokio/task/)
- [Tokio `spawn` documentation](https://docs.rs/tokio/latest/tokio/task/fn.spawn.html)
- [Tokio `JoinHandle` documentation](https://docs.rs/tokio/latest/tokio/task/struct.JoinHandle.html)
- [Tokio `spawn_blocking` documentation](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html)
- [Tokio `LocalSet` documentation](https://docs.rs/tokio/latest/tokio/task/struct.LocalSet.html)
