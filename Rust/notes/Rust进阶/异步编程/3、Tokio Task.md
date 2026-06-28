# 一、从 Future 到 Task

## 1、Future 只是异步计算

调用异步函数不会立即执行函数体，而是返回一个 `Future`。

```rust
async fn work() -> i32 {
    println!("working");
    10
}

let future = work();
```

此时只创建了一个惰性的异步计算。它必须被执行器不断 `poll`，才会向前推进。

推进 Future 常见有三种方式：

```rust
// 方式一：在当前 Task 中等待
let value = work().await;

// 方式二：作为根 Future 交给 Runtime 驱动
let value = runtime.block_on(work());

// 方式三：创建独立的 Tokio Task
let handle = tokio::spawn(work());
let value = handle.await.unwrap();
```

需要准确区分：

- `future.await` 只是由**当前 Task** 继续轮询这个 Future，不会创建新的 Task
- `tokio::spawn(future)` 才会把 Future 包装成一个可独立调度的 Tokio Task
- `Runtime::block_on(future)` 驱动的是 Runtime 的根 Future；根 Future 完成并不意味着所有 spawn 出来的 Task 都已完成

## 2、Tokio Task

Tokio Task 是由 Tokio Runtime 调度的一段异步执行单元。每个 Task 内部持有一个顶层 Future，Runtime 通过反复调用它的 `poll` 来推进任务。

可以把关系理解为：

![[tokio-task-from-future.png|400]]

Task 和 OS 线程都能表示一段独立推进的执行逻辑，但它们不是同一层次的概念：

| 对比项  | Tokio Task               | OS 线程            |
| ---- | ------------------------ | ---------------- |
| 调度者  | Tokio Runtime            | 操作系统             |
| 数量   | 通常可以创建很多                 | 数量受系统资源约束更明显     |
| 切换方式 | 在 `.await` 等位置协作式让出      | 除了主动让出，操作系统可抢占调度 |
| 栈    | 编译器生成的状态机保存跨 `.await` 状态 | 通常拥有独立线程栈        |
| 适合场景 | 大量 I/O 并发                | 阻塞代码、CPU 计算、少量并发 |

Tokio 官方文档把 Task 类比为异步的 green thread。这个类比强调它是轻量并发单元，但不能据此认为 Task 就是一个更小的 OS 线程。

## 3、Task 如何被推进

一个 Task 的典型生命周期如下：

![[Pasted image 20260627150931.png|600]]

Task 使用==协作式调度==。它必须执行到能返回控制权的位置，Runtime 才能调度其他 Task。最常见的位置是一个尚未就绪的 `.await`；也可以显式调用 `tokio::task::yield_now().await`。


# 二、使用 spawn 创建 Task

## 1、tokio::spawn

`tokio::spawn` 把一个 Future 提交给当前 Runtime，并立即返回 `JoinHandle<T>`：

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

`tokio::spawn()`有如下特点：

- 创建一个独立的 Task，Future 不再只是当前 Task 的一个子 Future。
- 立即返回一个句柄，该句柄可用于等待结果、观察 panic 或请求取消
- 只负责“提交 + 排队”，不会在当前这一行调用栈里立刻去 poll 那个 Future。 真正的 poll 由 Runtime 调度器稍后另找时机执行
- 它必须在 Tokio Runtime 上下文中调用，否则会 panic

> [!note] 并发不等于并行
> `spawn` 创建的是并发 Task。它们可能在同一线程上交替运行；只有在多线程 Runtime 上，才可能同时运行在不同 worker thread 上。

## 2、spawn 不会等待 Task 完成

下面的程序通常看不到输出：

```rust
#[tokio::main]
async fn main() {
    tokio::spawn(async {
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
        println!("child done");
    });
}
```

`main` 的根 Future 很快完成，随后 Runtime 被关闭，尚未完成的 Task 会被取消。

如果结果或副作用不能丢失，就必须管理 Task 的生命周期：

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

`tokio::spawn()`返回一个句柄`JoinHandle<T>`，其中`T`是异步任务的返回值。

对句柄`.await`，返回`Result<T>`，`T`正是异步任务的返回值。

`handle.await` 挂起的是当前 Task，不会像 `std::thread::JoinHandle::join()` 那样阻塞 worker thread。

## 3、Runtime::spawn
如果显式持有 Runtime，也可以直接向它提交 Task：

```rust
use tokio::runtime::Runtime;  
  
  
fn main() {  
  
    let rt = Runtime::new().unwrap();  
  
    let handle = rt.spawn(async {  
        tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;  
        println!("child done");  
        10  
    });  
  
    let v = rt.block_on(handle).unwrap();  
    println!("value: {}", v);  
}
```

这里需要注意，`Runtime::block_on()`传入的是`JoinHandle<T>`句柄，`JoinHandle<T>`本身是实现了`Future`的值，即`Future<Output = Result<T, JoinError>>`。

## 4、Handle::spawn
Handle 是对 Runtime 的一个轻量句柄，可以`clone()`；而 Runtime 本身是**独占**的，不能 clone。

最典型的就是将句柄送到一个同步线程：

```rust
use std::thread;
use tokio::runtime::Runtime;
use tokio::time::{sleep, Duration};

fn main() {
    let rt = Runtime::new().unwrap();

    // 只把提交 Task 的能力交给同步线程，Runtime 仍由 main 持有。
    let runtime_handle = rt.handle().clone();

    let submitter = thread::spawn(move || {
        println!("submit task from sync thread");

        runtime_handle.spawn(async {
            sleep(Duration::from_secs(1)).await;
            println!("async task done");
            10
        })
    });

    // 第一次 join 等待同步线程完成“提交 Task”，得到 Tokio JoinHandle。
    let task_handle = submitter.join().unwrap();

    // 再由 Runtime 驱动并等待异步 Task 完成。
    let value = rt.block_on(task_handle).unwrap();
    println!("value: {value}");
}
```

这里有两个不同体系的句柄：

- `submitter` 是 `std::thread::JoinHandle`，`join()` 会阻塞 `main` 线程，直到同步线程完成 Task 的提交
- `task_handle` 是 `tokio::task::JoinHandle<i32>`，它实现了 `Future`，可以传给 `rt.block_on()` 等待异步 Task 的结果

同步线程不在 Tokio Runtime 的异步上下文中，因此不能直接调用 `tokio::spawn()`；但它持有与特定 Runtime 关联的 `Handle`，所以可以通过 `runtime_handle.spawn()` 向该 Runtime 提交 Task。整个过程中，`Runtime` 的所有权始终留在 `main` 线程。

总结：

| 写法 | 典型位置 |
| --- | --- |
| `tokio::spawn(...)` | 已处于 Tokio Runtime 上下文的异步代码 |
| `runtime.spawn(...)` | 同步代码明确持有某个 `Runtime` |
| `handle.spawn(...)` | 只需要提交 Task，不需要持有整个 `Runtime` |

# 三、JoinHandle：结果、错误与分离

## 1、等待 Task 的结果

如果 Task 的输出是 `T`，`spawn` 返回 `JoinHandle<T>`。等待句柄得到的不是直接的 `T`，而是：

```rust
Result<T, tokio::task::JoinError>
```

因为 Task 可能正常结束，也可能被取消或 panic：

| 结果                                | 含义            |
| --------------------------------- | ------------- |
| `Ok(value)`                       | Task 正常完成     |
| `Err(err)` 且 `err.is_cancelled()` | Task 被取消      |
| `Err(err)` 且 `err.is_panic()`     | Task 内部 panic |
| `Err(err)`                        | 其他错误          |

```rust
let handle = tokio::spawn(async { 5 + 3 });

match handle.await {
    Ok(value) => println!("result: {value}"),
    Err(err) if err.is_cancelled() => println!("cancelled"),
    Err(err) if err.is_panic() => println!("panicked"),
    Err(err) => println!("join failed: {err}"),
}
```

Task 内部的 panic 不会直接变成当前 Task 的 panic，而是由 `JoinHandle` 以 `JoinError` 报告。如果丢弃句柄，这个错误也会失去常规的观察渠道。

## 2、Task 自己返回 Result

如果 Task 输出本身是 `Result<T, E>`，等待句柄会得到两层 `Result`：

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

两个 `?` 分别处理：

1. 外层 `JoinError`：Task 是否执行到正常返回
2. 内层业务错误：Task 自己的操作是否成功

## 3、丢弃 JoinHandle 会分离 Task

`JoinHandle` 被 drop 时，Task **不会被取消**，而是与句柄分离并继续运行：

```rust
let handle = tokio::spawn(async {
    do_work().await;
});

drop(handle); // Task 仍然运行，但无法再等待结果
```

总结：

| 操作 | Task 是否继续 | 能否再等待结果 |
| --- | --- | --- |
| `handle.await` | 运行到完成 | 可以取得结果 |
| `drop(handle)` | 是 | 不可以 |
| `handle.abort()` | 请求取消 | 仍可 await 确认终止 |

# 四、所有权、Send 与 'static

## 1、spawn 的类型约束

`tokio::spawn` 的签名可以简化为：

```rust
pub fn spawn<F>(future: F) -> JoinHandle<F::Output> 
where
	F: Future + Send + 'static
	F::Output: Send + 'static
```

`F: Future`很显然，要求传入一个`Future`。

| 约束                   | 含义                     |
| -------------------- | ---------------------- |
| `F: Send`            | 挂起的`Future`可以在线程间安全地移动 |
| `F: 'static`         | `Future`不持有可能提前失效的借用   |
| `F::Output: Send`    | 输出可以安全地在线程间传递          |
| `F::Output: 'static` | 输出不依赖可能提前失效的借用         |

多线程 Runtime 可能在一个 worker thread 上挂起 Task，又在另一个 worker thread 上继续轮询它，所以普通 spawn Task 必须是 `Send`。

`'static` 不表示 Task 一定运行到程序结束，也不表示数据必须是全局变量。它表示 Task 持有的数据不包含短于 `'static` 的借用；拥有所有权的 `String`、`Vec<T>` 等通常都满足这个要求。

## 2、使用 async move 转移所有权

下面的 Task 借用了局部变量，无法满足 `'static`：

```rust
let text = String::from("hello");

tokio::spawn(async {
    println!("{text}");
}).await.unwarp();
```

通常使用 `async move` 把所有权移入 Future：

```rust
let text = String::from("hello");

tokio::spawn(async move {
    println!("{text}");
})
.await
.unwrap();
```

多个 Task 共享只读或线程安全的可变状态时，通常使用 `Arc<T>`：

```rust
use std::sync::Arc;

#[tokio::main]
async fn main() {
    let data = Arc::new(String::from("hello"));

    let h1 = {
        let data = Arc::clone(&data);
        tokio::spawn(async move {
            println!("task 1: {data}");
        })
    };

    let h2 = {
        let data = Arc::clone(&data);
        tokio::spawn(async move {
            println!("task 2: {data}");
        })
    };

    h1.await.unwrap();
    h2.await.unwrap();

    // main 仍然持有一个 Arc，底层 String 不会被提前释放。
    println!("main: {data}");
}
```

`Arc::clone()` 只增加原子引用计数，不会复制底层 `String`。三个 `Arc` 共同拥有同一个值，因此两个 Task 和 `main` 都能安全读取它。

### （1）共享可变状态：Arc\<Mutex\<T>>

`Arc` 只解决**谁拥有数据**的问题，不允许直接通过共享引用修改内部数据。如果多个 Task 需要修改同一份状态，通常把 `Mutex<T>` 放进 `Arc`：

```rust
use std::sync::{Arc, Mutex};

#[tokio::main]
async fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = Vec::new();

    for _ in 0..10 {
        let counter = Arc::clone(&counter);

        handles.push(tokio::spawn(async move {
            // 临界区很短，并且其中没有 .await。
            {
                let mut value = counter.lock().unwrap();
                *value += 1;
            } // MutexGuard 在 .await 之前释放

            tokio::task::yield_now().await;
        }));
    }

    for handle in handles {
        handle.await.unwrap();
    }

    println!("counter: {}", *counter.lock().unwrap());
}
```

这里使用 `std::sync::Mutex` 是合适的，因为锁只保护一次很短的同步操作，`MutexGuard` 不会跨越 `.await`。同步 Mutex 等锁时会阻塞当前线程，所以临界区必须足够短，并且不能在持锁期间执行阻塞操作。

### （2）锁必须跨越 await：tokio::sync::Mutex

如果业务逻辑确实要求在持锁期间等待异步操作，应使用 `tokio::sync::Mutex`。它的 `lock()` 本身是异步的，等待锁时会挂起当前 Task，而不是阻塞 worker thread：

```rust
use std::sync::Arc;
use tokio::{
    sync::Mutex,
    time::{sleep, Duration},
};

#[tokio::main]
async fn main() {
    let value = Arc::new(Mutex::new(0));

    let h1 = {
        let value = Arc::clone(&value);
        tokio::spawn(async move {
            let mut value = value.lock().await;
            sleep(Duration::from_millis(100)).await;
            *value += 1;
        })
    };

    let h2 = {
        let value = Arc::clone(&value);
        tokio::spawn(async move {
            let mut value = value.lock().await;
            sleep(Duration::from_millis(100)).await;
            *value += 1;
        })
    };

    h1.await.unwrap();
    h2.await.unwrap();

    println!("value: {}", *value.lock().await);
}
```

这个例子中，锁保护范围包含 `sleep(...).await`，所以另一个 Task 必须等前一个 Task 释放锁后才能进入临界区。虽然 Tokio Mutex 允许这样写，但持锁跨越 `.await` 会降低并发度；如果不需要维持某个跨异步操作的不变量，应尽早释放锁。

选择原则可以概括为：

| 场景 | 建议 |
| --- | --- |
| 临界区很短，且不跨 `.await` | 优先考虑 `std::sync::Mutex` |
| 必须在持锁期间 `.await` | 使用 `tokio::sync::Mutex` |
| 数据可以由单个 Task 独占 | 优先考虑 channel，通过消息修改状态 |

## 3、Task 中能否使用 !Send 值

普通 spawn Task 可以临时使用 `Rc<T>` 等 `!Send` 值，只要它不跨越 `.await` 存活：

```rust
use std::rc::Rc;

tokio::spawn(async {
    {
        let value = Rc::new(1);
        println!("{value}");
    } // Rc 在 await 前离开作用域

    tokio::task::yield_now().await;
});
```

如果 `Rc<T>` 跨越 `.await`，生成的 Future 就不是 `Send`：

```rust
use std::rc::Rc;

tokio::spawn(async {
    let value = Rc::new(1);
    tokio::task::yield_now().await;
    println!("{value}");
});
```

这时可以改用 `Arc<T>`，也可以明确选择只能在本地线程运行的 Task。


# 五、本地 Task：LocalSet 与 spawn_local

## 1、为什么需要本地 Task

普通的 `tokio::spawn` 要求 Future 满足 `Send`。原因是多线程 Runtime 可以把挂起的 Task 移到另一个 worker thread 上继续执行。如果 Future 持有跨越 `.await` 的 `Rc<T>`、`RefCell<T>` 或线程绑定资源，它就不能在线程之间安全移动，也就不能交给 `tokio::spawn`。

`spawn_local` 用于创建不要求 `Send` 的本地 Task。作为代价，这个 Task 被限制在驱动本地执行环境的线程上：它可以在该线程上多次挂起、恢复，但不能被 Runtime 迁移到其他 worker thread。

Tokio 通常使用 `LocalSet` 提供这个本地执行环境。下面的程序同时创建：

- 一个通过 `spawn_local` 创建的 `!Send` Task，持有跨越 `.await` 的 `Rc`
- 一个通过 `tokio::spawn` 创建的普通 `Send` Task，持有跨越 `.await` 的 `Arc`

```rust
use std::{
    rc::Rc,
    sync::Arc,
    thread,
};
use tokio::{
    runtime::Builder,
    task::LocalSet,
    time::{sleep, Duration},
};

fn main() {
    let rt = Builder::new_multi_thread()
        .worker_threads(2)
        .enable_all()
        .build()
        .unwrap();

    let local = LocalSet::new();
    let local_thread = thread::current().id();

    println!("run_until thread: {local_thread:?}");

    rt.block_on(local.run_until(async move {
        // Rc 会跨越 await，因此这个 Future 是 !Send。
        let local_data = Rc::new(String::from("local data"));

        let local_handle = tokio::task::spawn_local(async move {
            let before = thread::current().id();
            println!("local task before await: {before:?}");

            sleep(Duration::from_millis(100)).await;

            let after = thread::current().id();
            println!("local task after await:  {after:?}");
            println!("local_data: {local_data}");

            // 本地 Task 始终由运行 LocalSet 的线程推进。
            assert_eq!(before, local_thread);
            assert_eq!(after, local_thread);
        });

        // LocalSet 内也能创建普通的 Send Task。
        let send_data = Arc::new(String::from("send data"));

        let send_handle = tokio::spawn(async move {
            println!(
                "Send task before await: {:?}",
                thread::current().id()
            );

            sleep(Duration::from_millis(100)).await;

            println!(
                "Send task after await:  {:?}",
                thread::current().id()
            );
            println!("Send data: {send_data}");
        });

        local_handle.await.unwrap();
        send_handle.await.unwrap();
    }));
}
```

结果；

```
run until thread: ThreadId(1)
local task before await: ThreadId(1)
Send task before await: ThreadId(2)
Send task after await: ThreadId(3)
Send data: send data
local task after await: ThreadId(1)
local data: local data
```

这个例子中的执行关系是：

```text
main 线程
  └─ Runtime::block_on(...)
       └─ LocalSet::run_until(...)
            ├─ spawn_local：!Send Task，只在 main 线程上执行
            └─ tokio::spawn：Send Task，由 Runtime 正常调度
```

本地 Task 在 `sleep(...).await` 前后的线程 ID 必定与调用 `run_until` 的线程相同，因此可以安全地让 `Rc` 跨越 `.await`。普通 `Send` Task 则不属于 `LocalSet`，它由多线程 Runtime 正常调度；它可能在任意可用的 worker thread 上执行，也可能在挂起后由另一个线程继续执行。线程 ID 的具体输出不能作为固定调度顺序来依赖。

### （1）LocalSet 的职责

`LocalSet` 不是 Runtime，也不会自己创建线程。它是一个本地 Task 集合，负责保证其中的 Task 在同一线程上执行；I/O 驱动、定时器和实际的执行能力仍由 Runtime 提供。

`LocalSet` 本身也是 `!Send`、`!Sync` 的，不能把它随意移动或共享到其他线程。更准确地说，“本地 Task 固定在线程上”指的是：本地 Task 始终在运行并驱动这个 `LocalSet` 的线程上被轮询。

### （2）run_until 做了什么

```rust
rt.block_on(local.run_until(main_future));
```

这行代码可以分成两层理解：

1. `local.run_until(main_future)` 进入该 `LocalSet` 的上下文，使其中的 `spawn_local` 把 Task 加入这个本地集合
2. `rt.block_on(...)` 在当前线程上驱动这个组合 Future，同时推进 `main_future` 和已经加入 `LocalSet` 的本地 Task

`run_until` 的结束条件是传入的 `main_future` 完成，而不是自动等待 LocalSet 中所有 Task 完成。本例在 `main_future` 中等待了 `local_handle`，所以本地 Task 一定会在 `run_until` 返回前完成。

如果没有等待句柄：

```rust
local.run_until(async {
    tokio::task::spawn_local(async {
        do_work().await;
    });
}).await;
```

外层 Future 很快完成，尚未完成的本地 Task 会留在 `LocalSet` 中。它不会被自动转移到 Runtime 的普通任务队列，只有下一次调用 `run_until`，或者直接等待整个 `LocalSet` 时，才会继续被推进。

> [!warning]
> `run_until` 应直接用于 `Runtime::block_on`，或者用于 `#[tokio::main]` / `#[tokio::test]` 提供的根异步上下文，不能放进 `tokio::spawn` 创建的普通 Task 中运行。

## 2、spawn 与 spawn_local 的选择

| API | Future 是否要求 `Send` | Task 能否跨 worker thread |
| --- | --- | --- |
| `tokio::spawn` | 是 | 可以 |
| `tokio::task::spawn_local` | 否 | 不可以 |

在 `LocalSet` 内仍然可以调用 `tokio::spawn`。这样创建的是普通 `Send` Task，不受 `LocalSet` 的单线程约束。

> [!warning]
> `spawn_local` 必须在 `LocalSet` 或支持本地 Task 的运行环境中调用，否则会 panic。不能仅靠把 Runtime 配置为 current-thread 就推断任意位置都可调用它。


# 六、协作式调度与阻塞代码

## 1、Task 必须让出执行权

当一个 `.await` 对应的 Future 尚未就绪时，当前 Task 返回 `Poll::Pending`，Runtime 才有机会在该 worker thread 上推进其他 Task。

如果 Task 长时间计算且没有 `.await`，它就会长时间占用 worker thread：

```rust
async fn bad_task() {
    loop {
        // 长时间 CPU 计算，没有 await
    }
}
```

即使代码写在 `async fn` 中，也不会自动变成非阻塞代码。普通同步函数、析构函数以及 CPU 计算仍然会直接占用当前线程。

## 2、yield_now

`yield_now()` 让当前 Task 主动归还一次执行权：

```rust
async fn calculate_in_batches() {
    for batch in 0..100 {
        calculate_one_batch(batch);
        tokio::task::yield_now().await;
    }
}
```

它适合把可拆分的短计算分批执行，但有两个限制：

- 不保证另一个特定 Task 会紧接着运行
- 不能把真正耗时的 CPU 计算变成适合异步 Runtime 的工作负载

对于长时间 CPU 密集计算，应使用专门线程或 Rayon 等计算线程池。

## 3、spawn_blocking

[[2、Tokio Runtime#五、阻塞代码和 spawn_blocking|Tokio Runtime 的阻塞代码章节]] 已经解释了 worker thread 和 blocking thread 的运行机制。这里从 Task 管理角度补充 API 的选择：同步阻塞代码不应直接放在普通 Task 中。

```rust
#[tokio::main]
async fn main() {
    std::thread::sleep(std::time::Duration::from_secs(10));
}
```

这会阻塞执行 `main` Future 的线程。Tokio 提供 `spawn_blocking`，把同步闭包提交给专门的阻塞线程池：

```rust
let handle = tokio::task::spawn_blocking(|| {
    std::thread::sleep(std::time::Duration::from_secs(1));
    10
});

let value = handle.await.unwrap();
println!("{value}");
```

| API | 接收对象 | 执行位置 | 执行模型 |
| --- | --- | --- | --- |
| `tokio::spawn` | Future | worker thread | 多次 `poll`，可挂起恢复 |
| `spawn_blocking` | 同步闭包 | blocking thread pool | 闭包开始后同步运行到返回 |

`spawn_blocking` 适合：

- 调用没有异步接口的阻塞库
- 同步文件操作、压缩、解析等有限时长操作
- 桥接旧的同步代码

Tokio 的 blocking 线程上限很高，以便容纳阻塞 I/O。大量 CPU 计算不应无限制地提交进去；应使用信号量限制并发，或改用专门计算线程池。

## 4、block_in_place

`block_in_place` 告诉多线程 Runtime：当前代码即将阻塞。Runtime 会把该 worker thread 上的其他 Task 转移出去，然后在当前线程执行闭包：

```rust
let value = tokio::task::block_in_place(|| {
    std::thread::sleep(std::time::Duration::from_millis(100));
    10
});
```

它与 `spawn_blocking` 的主要区别是：

| API | 执行方式 | 返回方式 |
| --- | --- | --- |
| `spawn_blocking` | 提交到 blocking 线程池 | 返回 `JoinHandle<R>`，异步等待 |
| `block_in_place` | 当前 worker thread 转入阻塞模式 | 直接返回 `R` |

使用 `block_in_place` 要注意：

- 在 current-thread Runtime 内调用会 panic；在 Runtime 外调用则只是直接执行闭包
- 同一 Task 内并发的其他分支也会暂停，例如同一个 `join!` 中的其他 Future
- 已开始执行的闭包不能被异步取消

多数业务代码优先使用边界更清晰的 `spawn_blocking`。

## 5、阻塞任务难以取消

`spawn_blocking` 闭包一旦开始运行，调用 `abort()` 通常无效；如果它仍在队列中尚未开始，取消才可能阻止其启动。

需要提前停止长时间阻塞操作时，应让闭包自己周期性检查停止标志：

```rust
use std::{
    sync::{
        Arc,
        atomic::{AtomicBool, Ordering},
    },
    thread,
    time::Duration,
};

fn do_one_bounded_step(step: usize) {
    println!("processing step {step}");

    // 模拟一个耗时有限、最终一定会返回的同步操作。
    thread::sleep(Duration::from_millis(200));
}

#[tokio::main]
async fn main() {
    let stop = Arc::new(AtomicBool::new(false));
    let worker_stop = Arc::clone(&stop);

    let handle = tokio::task::spawn_blocking(move || {
        let mut completed_steps = 0;

        while !worker_stop.load(Ordering::SeqCst) {
            do_one_bounded_step(completed_steps);
            completed_steps += 1;
        }

        println!("blocking task observed the stop flag");
        completed_steps
    });

    // 让阻塞任务先执行一段时间。这里挂起的是异步 Task，
    // 不会阻塞 Tokio 的 worker thread。
    tokio::time::sleep(Duration::from_millis(550)).await;

    println!("requesting stop");
    stop.store(true, Ordering::SeqCst);

    // 等待闭包观察停止标志并自行返回。
    let completed_steps = handle.await.unwrap();
    println!("completed {completed_steps} steps");
}
```

这里没有强制杀死 blocking thread。主异步 Task 只是把共享的原子标志设置为 `true`，阻塞闭包在下一轮循环开始时观察到它，然后主动退出。整个过程属于**协作式停止**。

`Ordering::SeqCst` 提供最强、最容易理解的内存顺序保证，适合这个教学示例。某些性能敏感场景可以根据同步关系改用 Acquire/Release，但需要单独证明其正确性，不能只为减少开销而随意替换。

停止响应速度取决于 `do_one_bounded_step()` 的最长执行时间。如果一个步骤可能永久阻塞或长时间不返回，闭包就没有机会再次检查停止标志，这种方式同样无法及时停止它。因此，每个步骤都必须是有界并且最终会返回的。


# 七、Task 的取消

## 1、强制取消：abort

`JoinHandle::abort()` 会请求 Runtime 取消 Task：

```rust
let handle = tokio::spawn(async {
    loop {
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
        println!("tick");
    }
});

handle.abort();

match handle.await {
    Err(err) if err.is_cancelled() => println!("cancelled"),
    Ok(_) => println!("completed before cancellation"),
    Err(err) => println!("task failed: {err}"),
}
```

取消不是在任意机器指令处强行杀死 Task：

1. `abort()` 只发出取消请求并立即返回
2. 如果 Task 正在一次 `poll` 中执行，要等它把控制权交还给 Runtime
3. Runtime 丢弃 Task 的 Future，运行其中局部变量的析构函数
4. `handle.await` 确认 Task 已终止，通常得到 cancelled `JoinError`

Task 可能在取消生效前正常完成，所以 `abort()` 后仍可能得到 `Ok(value)`。

> [!warning]
> Future 被 drop 时会运行 Rust 析构函数，但不会继续执行 `.await` 后面的异步清理逻辑。需要异步清理、提交事务或发送关闭消息时，应优先采用协作式取消。

## 2、协作式取消

协作式取消是由 Task 主动接收关闭信号、清理资源并正常返回。可以使用 channel、`Notify`，或者 `tokio-util` 的 `CancellationToken`：

```rust
use tokio_util::sync::CancellationToken;

let token = CancellationToken::new();
let child_token = token.clone();

let handle = tokio::spawn(async move {
    loop {
        tokio::select! {
            _ = child_token.cancelled() => {
                println!("cleaning up");
                break;
            }
            _ = do_one_job() => {}
        }
    }
});

token.cancel();
handle.await.unwrap();
```

| 方式 | 特点 | 适合场景 |
| --- | --- | --- |
| `abort()` | 简单直接，在下次让出后丢弃 Future | 无需异步清理、超时后的兜底终止 |
| 协作式信号 | Task 可完成清理并决定退出位置 | 服务关闭、写回状态、释放外部资源 |

常见的优雅关闭流程是：发送取消信号 → 停止接收新工作 → 等待在途 Task 清理退出 → 超时后再 `abort` 兜底。

## 3、select! 的取消语义

`tokio::select!` 在一个 Task 内同时等待多个 Future。某个分支完成后，其余分支会被 drop：

```rust
tokio::select! {
    value = operation() => println!("done: {value:?}"),
    _ = tokio::time::sleep(std::time::Duration::from_secs(1)) => {
        println!("timeout");
    }
}
```

这里超时后，`operation()` Future 会被 drop。因此在循环中使用 `select!` 前，要检查相关 API 是否 cancel safe，否则可能丢失部分进度或数据。

但是下面的语义不同：

```rust
let mut handle = tokio::spawn(operation());

tokio::select! {
    result = &mut handle => println!("done: {result:?}"),
    _ = tokio::time::sleep(std::time::Duration::from_secs(1)) => {
        println!("stop waiting");
    }
}
```

未选中的是“等待 `JoinHandle`”这个分支；独立 Task 不会自动取消。如需超时后终止它，要显式调用 `handle.abort()`，或发送协作式取消信号。

## 4、JoinHandle 的取消安全

`&mut JoinHandle<T>` 是 cancel safe 的。它在 `select!` 中未被选中时，结果不会凭空丢失：

```rust
let mut handle = tokio::spawn(async {
    tokio::time::sleep(std::time::Duration::from_secs(1)).await;
    10
});

tokio::select! {
    result = &mut handle => {
        println!("task finished: {result:?}");
        return;
    }
    _ = tokio::time::sleep(std::time::Duration::from_millis(100)) => {
        println!("not finished yet");
    }
}

let value = handle.await.unwrap();
println!("{value}");
```

这里超时分支先完成，只是停止等待 `JoinHandle`；已经 spawn 的 Task 仍在运行。


# 八、管理多个 Task

## 1、Vec\<JoinHandle\<T>>

任务数量固定、希望按创建顺序收集结果时，可以保存句柄：

```rust
let mut handles = Vec::new();

for i in 0..3 {
    handles.push(tokio::spawn(async move { i * 2 }));
}

for handle in handles {
    println!("{}", handle.await.unwrap());
}
```

Task 仍然是并发运行的，只是结果按 `Vec` 顺序取出。如果第一个 Task 很慢，已经完成的后续 Task 也要等它之后才被处理。

## 2、JoinSet

`JoinSet<T>` 管理一组输出类型相同的 Task，并按完成顺序取出结果：

```rust
use tokio::task::JoinSet;

let mut set = JoinSet::new();

for i in 0..3 {
    set.spawn(async move {
        tokio::time::sleep(std::time::Duration::from_secs(3 - i)).await;
        i * 2
    });
}

while let Some(result) = set.join_next().await {
    println!("{}", result.unwrap());
}
```

`JoinSet` 适合动态增加 Task、按完成顺序处理结果。其生命周期语义也更集中：

- `join_next()` 取出下一个完成结果
- `abort_all()` 请求取消所有 Task，但仍应继续 `join_next()` 回收结果并确认终止
- `shutdown().await` 取消全部 Task 并等待它们关闭，同时忽略 panic
- drop `JoinSet` 会立即 abort 仍在其中的 Task
- `detach_all()` 会移除并分离所有 Task，让它们继续后台运行

## 3、TaskTracker 与优雅关闭

`tokio-util` 的 `TaskTracker` 适合“只追踪 Task 是否退出，不需要保存每个返回值”的服务型场景。它通常与 `CancellationToken` 配合：

```rust
use tokio_util::{
    sync::CancellationToken,
    task::TaskTracker,
};

let token = CancellationToken::new();
let tracker = TaskTracker::new();

for _ in 0..3 {
    let token = token.clone();
    tracker.spawn(async move {
        token.cancelled().await;
        cleanup().await;
    });
}

token.cancel();
tracker.close();
tracker.wait().await;
```

`wait()` 只有在 Tracker 已关闭且已经为空时才完成。与 `JoinSet` 不同，drop `TaskTracker` 不会取消被追踪的 Task；Task 完成后也能立即释放，不会为了等待读取返回值而持续积累已完成结果。

## 4、避免无界 spawn

对每条输入都直接 `spawn` 可能导致 Task 数量、内存和下游请求数无限增长：

```rust
while let Some(job) = receive_job().await {
    tokio::spawn(process(job));
}
```

常见的背压手段包括：

- 使用有界 `mpsc` channel
- 使用 `Semaphore` 限制同时运行的 Task 数量
- 保持固定数量的 worker Task
- 使用 `JoinSet`，达到上限后先回收一个已完成 Task

Task 很轻量，但不是零成本；它仍然占用 Future 状态、调度信息以及捕获的数据。


# 九、spawn、join! 与 select! 的选择

## 1、直接 await

如果只是顺序调用一个异步操作，直接 `.await`：

```rust
let value = compute().await;
```

它不会增加独立 Task、句柄和生命周期管理成本。

## 2、join! 与 try_join!

`join!` 在**当前 Task 内**并发轮询多个 Future，不会创建新 Task：

```rust
let (user, order) = tokio::join!(fetch_user(), fetch_order());
```

所有分支共享当前 Task 的调度预算，并且总是在同一个线程上被轮询。某个分支如果同步阻塞或长时间不让出，会拖住其他分支。

`try_join!` 用于分支都返回 `Result` 的情况。遇到第一个 `Err` 时立即返回，其余 Future 被 drop：

```rust
let (user, order) = tokio::try_join!(fetch_user(), fetch_order())?;
```

## 3、select!

`select!` 等待第一个完成的分支，并取消当前 Task 内未选中的 Future：

```rust
tokio::select! {
    message = receiver.recv() => handle(message),
    _ = shutdown.cancelled() => return,
}
```

默认情况下，`select!` 会随机选择检查分支的起点，以提供一定公平性。加上 `biased;` 后按书写顺序检查，调用者要自己避免后面的分支饥饿。

## 4、选择总结

| 方式 | 创建新 Task | 生命周期 | 典型用途 |
| --- | --- | --- | --- |
| `.await` | 否 | 完全嵌套 | 顺序执行一个操作 |
| `join!` | 否 | 所有分支结束后返回 | 少量 Future 并发且全部都要结果 |
| `try_join!` | 否 | 首个错误时丢弃其他分支 | 少量可取消的 fallible Future |
| `select!` | 否 | 首个分支完成后丢弃其他分支 | 竞速、超时、事件循环、关闭信号 |
| `spawn` | 是 | 与创建者解耦，需自行管理 | 独立连接、后台工作、动态并发 |

能用 `.await` 或 `join!` 表达的嵌套并发，通常不必急着 `spawn`。`spawn` 带来真正独立的 Task，也同时带来所有权、错误传播、取消和关闭管理成本。


# 十、实践原则

## 1、明确每个 Task 的所有者

创建 Task 时应能回答：

- 谁保存或追踪它的句柄？
- 谁负责观察它的错误？
- 谁在服务关闭时通知它退出？
- 等待多久后需要强制取消？

如果这些问题都没有答案，Task 很可能会变成难以控制的后台工作。

## 2、让并发保持有界

不要因为 Task 轻量就无限 spawn。应根据连接数、内存、数据库容量和外部服务限流设置并发上限，并通过有界队列或 `Semaphore` 形成背压。

## 3、不要阻塞 worker thread

| 工作类型 | 建议方式 |
| --- | --- |
| 异步 I/O 或定时等待 | Tokio 异步 API + `.await` |
| 有限时长的同步阻塞调用 | `spawn_blocking` |
| 可拆分的少量计算 | 分批计算并适当 `yield_now().await` |
| 长时间 CPU 密集计算 | Rayon、专用线程池或 OS 线程 |

## 4、优先设计协作式关闭

需要资源清理的服务 Task，应监听取消信号并正常返回；`abort` 更适合作为无需清理的直接取消，或优雅关闭超时后的兜底。

## 5、不要忽略 JoinError

生产代码中直接 `.await.unwrap()` 只适合“子 Task panic 就应让当前流程失败”的明确场景。后台 Task 应记录或传播 panic、取消和业务错误，否则故障可能悄无声息。
