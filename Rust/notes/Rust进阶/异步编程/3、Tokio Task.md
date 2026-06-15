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

| 约束                   | 含义                      |
| -------------------- | ----------------------- |
| `F: Send`            | task 可以在线程之间安全移动        |
| `F: 'static`         | task 不能持有可能提前失效的短生命周期引用 |
| `F::Output: Send`    | task 的输出可以在线程之间安全移动     |
| `F::Output: 'static` | task 的输出不能依赖短生命周期引用     |

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

这段代码会编译报错：

![[Pasted image 20260615093802.png|500]]

`tokio::spawn`创建的异步任务不能借用局部变量。因为`tokio::spawn` 出来的任务不保证一定在 `main` 结束前执行完。

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

`LocalSet`本身不是 runtime，它只是一个本地任务集合，真正驱动任务运行的仍然是 Tokio Runtime。

示例：

```rust
use tokio::runtime::Runtime;  
use tokio::task::LocalSet;  
use std::rc::Rc;  
  
fn main() {  
    let rt = Runtime::new().unwrap();  
  
    let local = LocalSet::new();  
  
    rt.block_on(local.run_until(async {  
        let handle = tokio::task::spawn_local(async {  
            let n = Rc::new(10);  
  
            tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;  
  
            println!("{}", n);  
        });  
  
        handle.await.unwrap();   
    }));  
}
```

这段代码虽然使用的是多线程 runtime，但`Rc<T>`所在的任务是通过`spawn_local`放进`LocalSet`运行的，因此它被限制在`main`线程（创建`LocalSet`的线程），不会跨线程迁移。

`LocalSet::run_until(future)`用于在当前线程进入这个 `LocalSet` 的本地任务上下文，驱动其中的 `spawn_local` 任务，并一直运行到传入的 `future` 完成。

在`LocalSet`本地任务上下文中，仍然可以通过`tokio::spawn`创建跨线程的异步任务：

```rust
use tokio::runtime::Runtime;  
use tokio::task::LocalSet;  
  
fn main() {  
    let rt = Runtime::new().unwrap();  
  
    let local = LocalSet::new();  
  
    rt.block_on(local.run_until(async {  
        let handle1 = tokio::task::spawn_local(async {  
            tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;  
            println!("task 1 done");  
        });  
  
        let handle2 = tokio::spawn(async {  
            tokio::time::sleep(tokio::time::Duration::from_secs(3)).await;  
            println!("task 2 done");  
        });  
  
        handle1.await.unwrap();  
        handle2.await.unwrap();  
    }));  
}
```

# 七、spawn_blocking和阻塞任务

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

在这里，`tokio::task::spawn_blocking(...)` 传入的闭包可以运行同步阻塞代码，因为它在 Tokio 的阻塞线程池中运行而非 worker thread。

它和 `tokio::spawn` 的区别如下：

| 写法 | 参数 | 执行位置 | 是否被反复 `poll` |
| --- | --- | --- | --- |
| `tokio::spawn` | `Future` | worker thread | 是 |
| `tokio::task::spawn_blocking` | 同步闭包 | blocking thread pool | 否 |

`spawn_blocking` 适合：

- 调用同步阻塞库
- 执行同步文件、压缩、解析等操作
- 执行少量或可控时长的 CPU 计算


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


# 八、多个任务的管理

## 1、Vec<JoinHandle\<T>>

如果任务数量较少，并且需要按创建顺序收集结果，可以把 `JoinHandle` 放进 `Vec`：

```rust
#[tokio::main]  
async fn main() {  
    let mut handles = Vec::new();  
  
    for i in 0..3 {  
        handles.push(tokio::spawn(async move {  
            i * 2  
        }))  
    }  
  
    for handle in handles {  
        let value = handle.await.unwrap();  
        println!("{}", value);  
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
            tokio::time::sleep(tokio::time::Duration::from_secs(i + 1)).await;  
            i * 2  
        });  
    }  
  
    while let Some(res) = set.join_next().await {  
        let value = res.unwrap();  
        println!("{}", value);  
    }  
  
}
```

当不关心创建顺序，只想哪个任务先完成就先处理哪个结果时，`JoinSet` 比 `Vec<JoinHandle<T>>` 更自然。

# 九、tokio::task::yield_now

`tokio::task::yield_now()`用来让当前 Tokio 任务主动让出一次执行机会，把控制权交还给 Runtime 执行器。

它本身是一个异步函数，只有写成下面这样才真正发生让出：

```rust
tokio::task::yield_now().await;
```

调用后，当前任务会被重新放回调度队列，Runtime 可以先调度其他已经就绪的任务。当当前任务再次被调度时，会从`yield_now().await` 后面继续执行。`yield_now()` 完成时没有返回值。

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

结果：

![[Pasted image 20260615104000.png|100]]

结果并不是我们所预期的，尽管 main 任务在 spawn 之后主动通过`task::yield_now().await`让出了一次执行机会，但可以看到还是`main task done`先打印。

因为`yield_now()` **不保证调度顺序**。即使当前任务主动 yield，下一轮调度也可能仍然继续调度当前任务。不能依赖它来实现严格的任务执行顺序。它适合在较长的异步计算循环中偶尔让出执行权，避免一个任务长时间占用 worker thread。


# 十、join!和try_join!

## 1、join!

`tokio::join!`用来在同一个异步任务中并发等待多个`Future`，直到所有分支都完成后，再一次性返回它们的结果。

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
    println!("{}", user);  
    println!("{}", order);  
}
```

`join!`返回的是一个元组，顺序和传入的`Future`顺序一致：

```rust
let (a, b, c) = tokio::join!(fa(), fb(), fc());
```

> `join!`不是并发，也不是并行运行每个 Future。它等待的多个 Future 会放在当前的 Tokio Task 中，由当前 Task 所在的线程轮流 poll。

如果这些 Future 返回的是 `Result`，`join!` 仍然会等待所有分支完成，即使其中某个分支已经返回 `Err`：

```rust
async fn a() -> Result<i32, &'static str> {
    Ok(1)
}

async fn b() -> Result<i32, &'static str> {
    Err("failed")
}

#[tokio::main]
async fn main() {
    let (ra, rb) = tokio::join!(a(), b());

    println!("{ra:?}, {rb:?}");
}
```


## 2、try_join!

`tokio::try_join!` 适合多个 Future 都返回 `Result` 的场景。

它也会在同一个异步任务中并发等待多个`Future`：

- 如果所有`Future`都返回`Ok(_)`，最终返回`Ok((...))`
- 如果任意`Future`返回`Er(_)`，立即返回这个错误，不再继续等待其他分支完成

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

`try_join!` 的返回值也是按传入顺序组成的元组，只是外面包了一层 `Result`：

```rust
let result: Result<(A, B), E> = tokio::try_join!(fa(), fb());
```

## 3、对比关系

|写法|分支返回类型|完成条件|返回值|
|---|---|---|---|
|`tokio::join!`|任意类型|所有分支完成|`(A, B, ...)`|
|`tokio::try_join!`|`Result<T, E>`|全部 `Ok`，或第一个 `Err`|`Result<(A, B, ...), E>`|


# 十一、select!

`tokio::select!`用来同时等待多个异步分支