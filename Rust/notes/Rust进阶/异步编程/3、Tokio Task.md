# 一、Tokio Task概述

## 1、简介

在学习 Tokio 时， **task（任务）** 是最核心的概念之一。因为 Tokio 本质上就是一个异步运行时，而异步运行时最重要的工作，就是 **调度和推进异步任务执行** 。

Tokio 官方文档通常把 task 描述为 **asynchronous green-thread（异步绿色线程）** 。这个说法有助于初学者建立直觉，但Tokio task 不是操作系统线程，而是一种 **由 Tokio 运行时在用户态调度的轻量级执行单元** 。

不过，从Rust异步模型的角度，更准确地说：task是被运行时驱动执行的 `Future` 。也就是说：

`async fn` 或 `async {...}` 会产生一个 `Future`

当这个 `Future` 被Tokio Runtime调度、poll、推进时，它就表现为一个Tokio Task。

## 2、Task与线程的区别

### （1）OS线程

Rust标准库 `std::thread::spawn()` 创建的是OS线程。每一个Rust原生线程，都对应一个 **真正的操作系统线程** ， **由操作系统内核负责调度** 。

这类线程的优点是功能完整、真正并行；缺点是创建和切换成本相对较高，因为涉及操作系统内核调度。

### （2）绿色线程

所谓绿色线程（green thread），通常是指由 **用户程序自己管理和调度的轻量执行单元，而不是操作系统直接调度** 。

由于切换发生在用户态，不需要频繁陷入内核，因此切换成本通常更低，可以更轻量地支持大规模并发。

### （3）Tokio Task

Tokio Task可以视为绿色线程，因为：

它由Tokio Runtime调度，而不是由OS直接调度

它比OS线程轻量得多

一个worker thread上可以轮流推进多个task

## 3、Future和Task

`Future` 表示一个将来才能完成的计算，更像待执行的任务说明书。而Task表示这个 `Future` 已经被运行时纳入调度并开始推进。

例如：

```rust
async fn do_work() {

println!("working...");

}
```
上述这是定义了一个异步函数。调用 `do_work()` 后，会得到一个 `Future` ，但它还没有被真正执行。

只要在以下几种情况下，它才会被推进，才称为Task：

被`.await`

被 `tokio::spawn(...)`

被 `join!`、 `select!`等机制驱动

被runtime的 `block_on(...)` 驱动
## 4、Tokio Task的调度方式

Tokio对Task的调度，不是抢占式的，而是协作式调度。 **所谓协作式调度，就是在任务在执行过程中，需要在合适的时候主动把执行权交还给调度器，让别的任务也有机会运行** 。

在Tokio中，常见的“让出执行权”的方式有：

执行到某个`.await` ，并且该异步操作当前还没准备好

显式调用 `tokio::task::yield_now().await`

这和OS线程的抢占式不同。OS线程可能会被操作系统强制切走，而 Tokio task 通常依赖 Future 自己在合适的位置暂停。

不过这里有个代价是如果某个task长时间不让出执行权，它就可能让同线程上的其他任务饥饿。

## 5、异步挂起和线程阻塞的区别

学习Tokio必须建立的第一层区分就是异步挂起和线程阻塞的区别，以 `tokio::time::sleep(...).await` 和 `std::thread::sleep(...)` 为例：

`tokio::time::sleep(...).await` ：挂起当前 task，不阻塞线程

`std::thread::sleep(...)` ：直接阻塞当前线程

也就是说：

异步挂起：当前任务先暂停，线程去做别的事情

线程阻塞：线程本身停住，这个线程上的其他任务也无法推进

因此，如果在Tokio异步代码中需要编写阻塞代码，需要把阻塞逻辑移到 `blocking thread` 中执行。

# 二、tokio::task模块

`tokio::task` 模块提供了多种和任务相关的能力，常见：

`spawn` ：创建普通异步任务

`spawn_blocking` ：把阻塞代码放到阻塞线程池执行

`yield_now` ：主动让出执行权

`JoinHandle` ：等待任务完成，或取消任务

`tokio::join!`和 `tokio::try_join!`：并发等待多个 `Future` 完成

# 三、创建异步任务

## 1、基本使用

通过 `tokio::task::spawn(...)` 用于把一个 `Future` 提交给当前runtime，生成一个新的异步任务，并交给Tokio调度执行。这是Tokio中最常见、最基础的任务创建方式。

此外，tokio对 `spawn` 进行了重导出，因此可以直接用 `tokio::spawn()` 。

示例：

```rust
use tokio::time::{sleep, Duration};

#[tokio::main]

async fn main() {

let t = tokio::spawn(async {

sleep(Duration::from_secs(1)).await;

println!("child task done");

});

t.await.unwrap();

}
```
说明：

`async { ... }` 产生一个 `Future`

`tokio::spawn(...)` 把它注册到runtime中

runtime开始调度这个 `Future`

`t.await` 等待这个任务完成

这里 `t` 的类型是 `JoinHandle<()>` 。调用`.await` 后，得到的是任务执行结果。如果任务正常结束，则返回 `Ok(...)` ，如果任务被取消或 `panic` ，则返回 `Err(...)` 。

这里 `spawn()` 不会像普通函数顺序执行完再返回，它只是把任务提交给调度器，然后立刻返回一个句柄。这意味着新任务和当前任务可以被runtime交替推进。
## 2、常见错误

**（1）任务刚创建，runtime就结束了**

```rust
use tokio::runtime::Runtime;

use tokio::time::{sleep, Duration};

fn main() {

let rt = Runtime::new().unwrap();

rt.block_on(async {

tokio::spawn(async {

sleep(Duration::from_secs(1)).await;

println!("done");

});

});

}
```
这段代码看不到"done"输出，因为 `spawn()` 只是提交任务就返回，因此外层的 `block_on(...)` 很快结束，于是main函数随即结束，runtime被销毁，尚未完成的任务来不及继续执行。

修改后的代码：
```rust
use tokio::runtime::Runtime;

use tokio::time::{sleep, Duration};

fn main() {

let rt = Runtime::new().unwrap();

rt.block_on(async {

let t = tokio::spawn(async {

sleep(Duration::from_secs(1)).await;

println!("done");

});

t.await.unwrap();

});

}
```
通过对任务句柄 `JoinHandle<T>` 进行`.await` ，等待任务完成。

**（2）在异步任务中捕获非'static引用**

`tokio::spawn()` 往往要求任务可以安全地被runtime管理并可能跨线程移动，因此通常要求任务满足 ``Send + `static`` 。如果在任务中捕获短生命周期引用，通常会报错。

错误示例：
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
这里 `r` 借用了局部变量 `s` ，而任务可能活得比当前作用域更久，因此不满足要求。

正确写法：
```rust
#[tokio::main]

async fn main() {

let s = String::from("hello");

tokio::spawn(async move {

println!("{s}");

}).await.unwrap();

}
```
## 3、任务句柄

`spawn(...)` 、 `spawn_blocking()` 、 `spawn_local()` 等创建任务的方法，都会返回一个 `JoinHandle<T>` 。可以将其理解为任务在runtime中运行后的控制句柄。

常见用途如下：

等待任务完成

```rust
use tokio::time::{sleep, Duration};

#[tokio::main]

async fn main() {

let task = tokio::spawn(async {

sleep(Duration::from_secs(1)).await;

10

});

let result = task.await.unwrap();

println!("result = {}", result);

}
```
这里 `result` 的值就是10。

需要注意的是， `JoinHandle.await` 等待的是任务结果，不是阻塞OS线程。 **它表示当前异步任务先暂停，等目标任务完成后再继续，而runtime仍然可以去调度其他任务** 。

检查任务是否完成
```rust
use tokio::time::{sleep, Duration};

#[tokio::main]

async fn main() {

let task = tokio::spawn(async {

sleep(Duration::from_secs(2)).await;

});

println!("finished? {}", task.is_finished());

sleep(Duration::from_secs(3)).await;

println!("finished? {}", task.is_finished());

}
```
第一次通常输出 `false` ，第二次通常输出 `true` 。
# 四、执行阻塞代码

## 1、基本使用

Tokio的 `worker thread` 主要用于轮询和推进异步任务。如果把 **长时间同步计算、旧版阻塞库、文件压缩、复杂解析等** 逻辑直接写进普通异步任务中，就会长时间占用worker thread，影响其他异步任务执行。

因此，Tokio提供了 `spawn_blocking()` ，专门把这类工作提交到 **blocking thread pool（阻塞线程池）** 中执行。

示例代码：

```rust
use tokio::task;

#[tokio::main]

async fn main() {

let t = task::spawn_blocking(|| {

let mut sum = 0;

for i in 0..1_000_000 {

sum += i;

}

sum

});

let res = t.await.unwrap();

println!("res = {}", res);

}
```
说明：这里闭包中的计算是同步执行的，但不会占用普通 worker thread。Tokio 会把它安排到阻塞线程池中执行，而当前 runtime仍可继续推进其它异步任务。
## 2、spawn_blocking()与std::thread::spawn()的区别

二者都能执行同步代码，但语义不同。

（1） `std::thread::spawn()`

创建标准库线程（OS线程）

返回 `std::thread::JoinHandle`

使用`.join()` 等待

不属于Tokio的任务体系

（2） `tokio::task::spawn_blocking()`

任务交给Tokio的阻塞线程池

返回 `tokio::task::JoinHandle`

可以在async环境下直接`.await`

更适合作为同步代码和异步世界之间的桥梁

## 3、blocking任务的取消问题

通过 `spawn_blocking()` 创建的任务，一旦已经开始执行，就不能像普通异步任务那样可靠取消。

示例：

```rust
use tokio::task;

#[tokio::main]

async fn main() {

let h = task::spawn_blocking(|| {

for i in 0..5 {

println!("blocking: {}", i);

std::thread::sleep(std::time::Duration::from_secs(1));

}

});

tokio::time::sleep(tokio::time::Duration::from_millis(200)).await;

h.abort(); // 尝试取消

match h.await {

Ok(_) => println!("finished normally"),

Err(e) => println!("cancelled with error {:?}", e),

}

}
```
如果 blocking 任务已经启动， `abort()` 往往无法像普通异步任务那样立刻停止它。  
因此， `spawn_blocking()` 更适合用于：

有明确结束条件的同步逻辑

时长可控的阻塞计算

同步世界与异步世界之间的桥接

不适合用于“永不结束的死循环阻塞任务”。
## 4、与async世界交换数据

### （1）简单返回值

```rust
#[tokio::main]

async fn main() {

let t = tokio::task::spawn_blocking(|| {

let mut sum = 0;

for i in 0..1000 {

sum += i;

}

sum

});

let res = t.await.unwrap();

println!("res = {}", res);

}
```
### （2）通过通道流式发送数据

```rust
use tokio::task;

use tokio::sync::mpsc;

#[tokio::main]

async fn main() {

let (tx, mut rx) = mpsc::channel::<String>(10);

let t = task::spawn_blocking(move || {

for i in 0..5 {

tx.blocking_send(format!("line: {}", i)).unwrap();

}

});

while let Some(msg) = rx.recv().await {

println!("{}", msg);

}

t.await.unwrap();

}
```
在阻塞上下文中，应使用 `blocking_send()` 、 `blocking_recv()` 这类专门为同步阻塞环境准备的方法，
# 五、主动让出执行权

## 1、基本使用

`task::yield_now()` 用于让当前异步任务主动放弃本轮执行机会，把线程交还给调度器，让其他任务有机会先运行。

示例：

```rust
use tokio::task;

#[tokio::main]

async fn main() {

let t1 = tokio::spawn(async {

for i in 1..=5 {

println!("task A -> {}", i);

task::yield_now().await;

}

});

let t2 = tokio::spawn(async {

for i in 1..=5 {

println!("task B -> {}", i);

task::yield_now().await;

}

});

t1.await.unwrap();

t2.await.unwrap();

}
```
这里的两个异步任务打印一次后都会通过 `yield_now().await` 让当前任务主动停一次，从而使得另一个任务有机会运行。因此，这样输出的结果交替打印的概率更大。
## 2、注意事项

`yield_now()` 本身返回 Future，必须`.await`

它不是睡眠，不表示等待固定时间

它也不保证严格顺序，只是“给其他任务一个机会”

# 六、取消异步任务

## 1、基本使用

通过 `tokio::spawn()` 创建的任务，可以使用 `JoinHandle.abort()` 取消。

示例：

```rust
use tokio::time::{sleep, Duration};

use tokio::task::JoinError;

#[tokio::main]

async fn main() {

let t = tokio::spawn(async {

sleep(Duration::from_secs(10)).await;

});

t.abort();

let err: JoinError = t.await.unwrap_err();

println!("{}", err.is_cancelled());

}
```
说明：这里任务原本要睡眠 10 秒，但主任务在 10 毫秒后调用了 `abort()` 。因此该任务不会正常完成， `task.await` 得到的是 `JoinError` ，并且 `is_cancelled()` 为 `true` 。
## 2、取消的真实含义

`abort()` 的含义不是“强行回滚任务已经做过的事情”，它表示请求 `Runtime` 不再继续推进这个任务。

如果任务已经做过部分副作用，例如：

已经发送了一部分数据

已经改写了一部分状态

已经打印了若干内容

这些副作用通常不会自动撤销。

如果任务已经结束再 `abort()` ，则此时 `abort()` 不会有任何效果。此时 `await` 得到的仍然是正常结果，而不是取消错误。

# 七、等待多个任务

## 1、tokio::join!

`tokio::join!`用于并发等待多个 `Future` 全部完成。

示例：

```rust
use tokio::join;

use tokio::time::{sleep, Duration};

async fn do_one() -> i32 {

println!("do one begin");

sleep(Duration::from_secs(1)).await;

println!("do one end");

10

}

async fn do_two() -> i32 {

println!("do two begin");

sleep(Duration::from_secs(2)).await;

println!("do two end");

20

}

#[tokio::main]

async fn main() {

let (r1, r2) = join!(do_one(), do_two());

println!("r1: {}, r2: {}", r1, r2);

println!("all done");

}
```
说明：这里 `do_one()` 和 `do_two()` 会被并发推进，但 `join!` 会一直等到 **所有分支都完成** 之后，才继续执行后面的代码。
## 2、try_join!

`tokio::try_join!`常用于多个返回 `Result` 的 `Future` 。它的语义是：

如果所有任务都返回 `Ok((...))` ，则整体返回 `Ok((...))`

如果有任意一个任务先返回 `Err(...)` ，则整体提前返回该错误

示例：

```rust
use tokio::try_join;

use tokio::time::{sleep, Duration};

async fn do_one() -> Result<i32, &'static str> {

println!("do one begin");

sleep(Duration::from_secs(1)).await;

println!("do one end");

Ok(10)

}

async fn do_two() -> Result<i32, &'static str> {

println!("do two begin");

sleep(Duration::from_secs(2)).await;

println!("do two end");

// Ok(20)

Err("error")

}

#[tokio::main]

async fn main() {

match try_join!(do_one(), do_two()) {

Ok((r1, r2)) => {

println!("result 1: {}", r1);

println!("result 2: {}", r2);

}

Err(e) => {

println!("error: {:?}", e);

}

}

println!("all done");

}
```
# 八、等待最先完成的任务

`tokio::select!`用于同时等待多个异步分支，当其中某个分支最先完成时，执行它对应的处理逻辑，并取消其他尚未完成的分支。

## 1、最简形式

```rust
use tokio::select;

use tokio::time::{sleep, Duration};

async fn sleep_n(n: u64) -> u64 {

sleep(Duration::from_secs(n)).await;

n

}

#[tokio::main]

async fn main() {

select! {

v = sleep_n(5) => println!("branch 1 done: {}", v),

v = sleep_n(3) => println!("branch 2 done: {}", v),

}

}
```
这里两个分支都会被并发推进，但 `sleep_n(3)` 更早完成，因此第二个分支先被选中。而另一个分支会被取消。

`select!` 会让 **当前async控制流** 停在这里等待，但它不会阻塞 OS线程，runtime 仍可以在这个线程上运行别的 task。
## 2、带if条件分支

每个分支可以加上if条件，在一次 `select!`的执行过程中，如果条件为 `false` ，这个分支在本轮不参与选择。

示例：

```rust
use tokio::select;

use tokio::time::{sleep, Duration};

async fn sleep_n(n: u64) -> u64 {

sleep(Duration::from_secs(n)).await;

n

}

#[tokio::main]

async fn main() {

let mut flag = false;

for _ in 0..2 {

select! {

v = sleep_n(5) => {

println!("branch 1 done: {}", v);

flag = true;

}

v = sleep_n(3), if flag => println!("branch 2 done: {}", v),

}

}

}
```
说明：第一轮select!因为flag为false，所以分支2不参与；第二轮flag为true，分支2参与。
## 3、biased模式

默认情况下， `select!`会尽量伪随机公平地轮询各个分支。如果想按照书写顺序优先选择分支，可以使用 `biase;`。

示例：

```rust
#[tokio::main]

async fn main() {

let mut count = 0u8;

loop {

tokio::select! {

biased;

_ = async {}, if count < 1 => { count += 1; println!("first"); }

_ = async {}, if count < 2 => { count += 1; println!("second"); }

else => { break; }

}

}

}
```
说明：

由于第一轮两个分支都满足条件，但由于设置了biased，因此第一轮必定是第一个分支被选择。

当所有分支都不可用时，可以执行 `else` 。如果所有分支都被禁用，但没有 `else` ，则 `select!`会panic。
