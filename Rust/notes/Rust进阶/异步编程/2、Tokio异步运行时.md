# 一、Tokio简介

Tokio是目前Rust生态最主流的异步运行时之一。它提供了异步任务调度、I/O驱动、定时器、同步原语等一整套基础设施，是Rust异步编程中最常见、也是最重要的运行时框架。

Tokio常见的模块包括：

`tokio` ：核心运行时，提供任务调度、任务生成、运行时管理等能力

`tokio::net` ：异步TCP/UDP等网络I/O

`tokio::fs` ：文件系统相关API

`tokio::time` ：定时器、超时等时间相关功能

`tokio::sync` ：互斥量、信号量、通道等同步原语

在使用 `tokio` 前，需要先在 `Cargo.toml` 中引入依赖，例如：

```toml
tokio = { version = "1.48.0", features = \["full"\] }
```
也可以在命令行中执行：
```bash
cargo add tokio --features full
```
**许多第三方库都会提供feature标志，允许开发者只启用自己需要的模块，从而减少编译时间，并缩小最终可执行文件体积** 。

tokio也不例外，但从入门学习的角度，通常建议直接开启 `full` ，这样可以一次性获得tokio的大部分常用能力，避免在学习过程中频繁补 feature。
# 二、创建异步运行时

## 1、创建Runtime

使用Tokio前，首先需要有一个Tokio提供的 **异步运行时环境** （runtime），然后在该runtime中执行异步任务。

可以通过 `tokio::runtime::Runtime::new()` 创建一个默认运行时：

```rust
fn main() {

let rt = tokio::runtime::Runtime::new().unwrap();

}
```
这里的 `Runtime::new()` 默认创建的是 **多线程运行时** 。在开启合适 feature 的前提下，它通常等价于一个启用了 I/O 和时间驱动的多线程 runtime。

除了直接使用 `Runtime::new()` 外，还可以使用 `tokio::runtime::Builder` 来显式配置运行时。

`Builder` 提供了两种常见的运行时构造方式，分别对应两种调度模型：

`new_current_thread()` ：当前线程运行时，也成current-thread runtime

`new_multi_thread()` ：多线程运行时，也称multi-thread runtime。

示例1：创建当前线程Runtime
```rust
let rt = tokio::runtime::Builder::new\_current\_thread()

.enable\_all()

.build()

.unwrap();
```
示例2：创建多线程Runtime
```rust
let rt = tokio::runtime::Builder::new\_multi\_thread()

.work\_threads(8) // 指定 8 个工作线程

.enable\_io() // 启用异步 I/O 驱动

.enable\_time() // 启用时间驱动

.build()

.unwarp();
```
注意事项：

`new_current_thread()` 的含义并不是额外创建一个工作线程，而是运行时就在当前所在线程上执行任务。也就是说，如果在主线程中创建 `current-thread runtime` ，那么异步任务就是在主线程上被驱动的，它不会额外再创建一个worker线程池。

`Runtime::new()` 或 `Builder::new_multi_thread()` 创建的是多线程runtime，这里runtime会创建一个worker线程池，用来并发调度异步任务。默认worker线程数一般与CPU可用并行度（CPU核心数）有关，也可以手动指定 `worker_threads(...)` 。

Tokio内部除了worker线程外，还可能使用其他线程资源，例如用于 `spawn_blocking` 的阻塞线程池。

`enable_io()` 和 `enable_time()` 开启I/O驱动和时间启动功能，如果两个都开，使用 `enable_all()` 。

示例：
```rust
use std::{thread::sleep, time::Duration};

use tokio::runtime::Runtime;

fn main() {

let \_rt = Runtime::new().unwrap();

sleep(Duration::from\_secs(120)); // 休眠 120 秒便于观察

}
```
如果在一台 14 核Mac机器上是实验，使用 **ps -M** 选项可以查看进程所包含的所有线程：

![[Image 101.png]]

可以看到，一共有15个线程（14个工作线程 + 1个主线程）。

然而，如果是通过 `Builder::new_current_thread()` 配置得到的当前线程运行时，线程的格式就是1个。
## 2、async main

对于 `main` 函数，除了手动创建 `Runtime` ，Tokio还提供了语法糖 `#[tokio::main]` 。

示例：

```rust
#\[tokio::main\]

async fn main() {

//...

}
```
这个宏会自动帮哦我们创建runtime，并在其中执行 `async fn main()` 的内容。

默认情况下， `#[tokio::main]` 创建的是多线程runtime。从概念上可以把它大致理解为：
```rust
fn main() {

let rt = tokio::runtime::Builder::new\_multi\_thread()

.enable\_all()

.build()

.unwrap();

rt.block\_on(async {

// 原来的 async main 内容

});

}
```
使用 `#[tokio::main]` 时，也可以通过参数配置 runtime：
```rust
#\[tokio::main(flavor = "multi\_thread")\]

async fn main() {}

#\[tokio::main(flavor = "multi\_thread", worker\_threads = 14)\]

async fn main() {}

#\[tokio::main(worker\_threads = 14)\]

async fn main() {}
```
上面的三种写法都表示创建一个拥有 14 个 worker 线程的多线程 runtime（假设默认CPU核心数就是14）。

如果希望使用当前线程 runtime，则可以写成：
```rust
#\[tokio::main(flavor = "current\_thread")\]

async fn main() {}
```
这里需要再次注意：  
`current_thread` 表示“在当前线程上驱动所有异步任务”，并不是“创建一个单独的工作线程”。
## 3、创建多个Runtime

一个程序理论上可以创建多个 `Runtime` 。例如，可以手动创建多个OS线程，并在不同线程中分别创建彼此独立的runtime。

示例：

```rust
fn main() {

let t1 = std::thread::spawn(|| {

let \_rt = tokio::runtime::Runtime::new().unwrap();

std::thread::sleep(std::time::Duration::from\_secs(60));

});

let t2 = std::thread::spawn(|| {

let \_rt = tokio::runtime::Runtime::new().unwrap();

std::thread::sleep(std::time::Duration::from\_secs(60));

});

t1.join().unwrap();

t2.join().unwrap();

}
```
实际在Mac 14核实验预期会有3 + 14 \* 2 = 31个线程。

上面这段代码中，两个新建的线程各自持有一个 **独立** 的 Tokio runtime，它们之间互不共享 **调度器和任务队列** 。

不过在实际工程中， **通常并不推荐随意创建多个 runtime** 。因为每个 runtime 都会维护自己的一套调度和驱动资源，多个 runtime 往往会增加复杂度和资源开销。 **大多数应用中，使用一个统一的 runtime 就足够了** 。
# 三、使用 Runtime 执行任务

## 1、std::thread::sleep和tokio::time::sleep

创建好 runtime 之后，就可以在其中执行异步任务了。很多异步任务涉及网络I/O，但为了先理解运行时如何调度任务，这里先使用Tokio的异步定时器 `tokio::time::sleep()` 来演示。

在开始之前，必须先区分两个概念：

`std::thread::sleep()` ：阻塞整个 OS 线程

`tokio::time::sleep()` ： **不会阻塞线程** ，而是让当前异步任务挂起，等到时间到了再被 runtime 唤醒继续执行

也就是说：

`std::thread::sleep()` 会让该线程在这段时间里什么都做不了

`tokio::time::sleep().await` 会让 **当前任务** 暂停，但线程可以去执行别的异步任务

这正是异步运行时高并发的基础之一。

## 2、block\_on()方法

`Runtime` 提供了 `block_on()` 方法。它接收一个 `Future` 作为参数，并在当前线程上阻塞，直到该 `Future` 执行完成后才返回。

示例：

```rust
use tokio::runtime::Runtime;

use chrono;

fn main() {

let rt = Runtime::new().unwrap();

rt.block\_on(

async {

println!("Before sleep: {}", chrono::Local::now().format("%F %T.%.3f"));

tokio::time::sleep(std::time::Duration::from\_secs(5)).await;

println!("After sleep: {}", chrono::Local::now().format("%F %T.%.3f"))

}

);

}
```
结果：

![[Image 102.png]]

`block_on()` **具有返回值，它的返回值就是被它驱动的那个** `Future` **的输出值** 。

示例：
```rust
use tokio::runtime::Runtime;

use chrono;

fn main() {

let rt = Runtime::new().unwrap();

let val = rt.block\_on(

async {

println!("Before sleep: {}", chrono::Local::now().format("%F %T.%.3f"));

tokio::time::sleep(std::time::Duration::from\_secs(5)).await;

println!("After sleep: {}", chrono::Local::now().format("%F %T.%.3f"));

10

}

);

println!("{}", val);

}
```
## 3、向Runtime中增加异步任务

前面的例子里，是直接把 `async {...}` 作为 `block_on` 的参数。而这个 `async {...}` 本质就是一个 `Future` 。在这个异步任务内部，还可以继续使用 `tokio::spawn()` 创建新的异步任务。

示例：

```rust
use tokio::runtime::Runtime;

use chrono;

fn now() -> String {

chrono::Local::now().format("%F %T.%.3f").to\_string()

}

fn main() {

let rt = Runtime::new().unwrap();

rt.block\_on(

async {

println!("create new async task: {}", now());

tokio::spawn(async {

tokio::time::sleep(std::time::Duration::from\_secs(3)).await;

println!("async task over: {}", now())

});

}

);

}
```
结果：

![[Image 103.png]]

上述的代码有问题，并没有看到后面的 `"async task over: xxx"` 打印。这是因为：

`tokio::spawn()` 只是把新任务交给runtime调度，并立即返回，因此 `block_on` 驱动的外层 `Future` 随之结束， `main` 结束，runtime离开作用域被销毁，同时整个进程结束，尚未执行完的新任务也就没有机会继续推进了。

事实上， `tokio::spawn()` 会返回一个任务句柄，即 `tokio::task::JoinHandle<T>` 。对该句柄`.await` ，就可以等待任务完成。

修改后的代码：
```rust
use tokio::runtime::Runtime;

use chrono;

fn now() -> String {

chrono::Local::now().format("%F %T.%.3f").to\_string()

}

fn main() {

let rt = Runtime::new().unwrap();

rt.block\_on(

async {

println!("create new async task: {}", now());

let t = tokio::spawn(async {

tokio::time::sleep(std::time::Duration::from\_secs(3)).await;

println!("async task over: {}", now())

});

t.await.unwrap();

}

);

}
```
结果：

![[Image 104.png]]

需要注意， `JoinHandle.await` 等待的是任务结果，并不会阻塞这个OS线程，它只是让当前异步任务等待该任务完成，runtime仍然可以继续调度其他任务。

除了 `tokio::spawn()` 外， `Runtime` 本身也提供了 `spawn()` 方法，因此也可以显式通过 `runtime` 来生成任务。

示例：
```rust
use tokio::runtime::Runtime;

use tokio::task::JoinHandle;

use chrono;

fn now() -> String {

chrono::Local::now().format("%F %T.%.3f").to\_string()

}

fn async\_task(rt: &Runtime) -> JoinHandle<()> {

println!("create new async task: {}", now());

rt.spawn(async {

tokio::time::sleep(std::time::Duration::from\_secs(3)).await;

println!("async task over: {}", now())

})

}

fn main() {

let rt = Runtime::new().unwrap();

rt.block\_on(

async {

let t = async\_task(&rt);

t.await.unwrap();

}

);

}
```
注意这里的 `async_task()` 传入的是 `Runtime` 的引用，这是必要的，因为如果按值传入，那么 `Runtime` 按值移动进函数内，函数调用结束后值被销毁，此时当前上下文的运行时就无法工作了。不过更常见的做法是让代码运行在 Tokio 上下文中，然后直接使用 `tokio::spawn()` 。
## 4、enter()方法

除了 `block_on()` 方法外， `Runtime` 还提供了 `enter()` 方法。 `enter()` **的作用不是执行任务，而是把当前线程临时标记为处于某个Tokio runtime的上下文中** 。这样，在这个作用域中， **一些依赖当前runtime上下文的API就可以正常工作** ，例如： `tokio::spawn(...)` 等。

示例：

```rust
use tokio::runtime::Runtime;

use chrono;

fn now() -> String {

chrono::Local::now().format("%F %T.%.3f").to\_string()

}

fn main() {

let rt = Runtime::new().unwrap();

let \_guard = rt.enter(); // 临时标记往下部分位于Tokio runtime上下文

let t1 = tokio::spawn(async {

println!("task1 start... {}", now());

tokio::time::sleep(tokio::time::Duration::from\_secs(1)).await;

println!("task1 done... {}", now());

});

let t2 = tokio::spawn(async {

println!("task2 start... {}", now());

tokio::time::sleep(tokio::time::Duration::from\_secs(2)).await;

println!("task2 done... {}", now());

});

rt.block\_on(async move {

t1.await.unwrap();

t2.await.unwrap();

});

}
```
结果：

![[Image 105.png]]

注意，上述例子用于教学演示，展示 `enter()` 可以标记Runtime上下文，这样就可以调用 `tokio::spawn(...)` 。但最后还是得靠 `block_on()` 。

`enter()` 不会主动驱动 `Future` ，它只是进入runtime上下文，并不意味着任务就开始自动被当前线程持续执行。
## 5、理解Runtime和异步调度

从整体上看，一个Tokio runtime大概包含以下几类核心功能：

任务调度器（scheduler）

I/O驱动器（通常基于操作系统事件机制）

时间驱动器（timer）

任务队列和唤醒机制

当一个异步任务准备好执行时，它会进入可调度状态，然后等待被调度器 `poll` 。如果某个任务在执行过程中遇到暂时无法完成的操作，例如：

等待socket可读/可写

等待定时器到期

等待某个异步资源准备好

那么它不会继续占用线程，而是返回 `Pending` ，并注册一个唤醒器（ `Waker` ）。等到对应事件发生后，runtime再把它重新放回可调度状态，等待后续继续 `poll` 。

# 四、取消异步任务

通过 `tokio::spawn()` 或 `rt.spawn()` 创建任务后，可以对返回的 `tokio::task::JoinHandle` 调用 `abort()` 来取消任务。注意，如果此时异步任务正在执行， `abort()` 通常不会把当前这一次执行硬生生掐断；而是等它运行到把执行权交还给 `Runtime` 的地方，之后 `Runtime` 就不会再继续推荐这个任务了。

示例：

```rust
use tokio::runtime::Runtime;

use chrono;

fn now() -> String {

chrono::Local::now().format("%F %T.%.3f").to\_string()

}

fn main() {

let rt = Runtime::new().unwrap();

rt.block\_on(async {

let t = tokio::spawn(async {

let mut i = 0u32;

loop {

i += 1;

println!("tick: {}", i);

tokio::time::sleep(std::time::Duration::from\_millis(200)).await;

}

});

// 先让异步任务充分运行下

tokio::time::sleep(std::time::Duration::from\_secs(1)).await;

println!("abort now");

// 取消异步任务

t.abort();

// 等待join结果，观察会返回JoinError（表示被取消）

match t.await {

Ok(\_) => println!("task finished normally"),

Err(e) => println!("task canceled: {e}"),

}
```
结果：

![[Image 106.png]]
# 五、Tokio的两种线程

## 1、工作线程和阻塞线程

Tokio中常见的线程资源可以分为两类：

用于执行异步任务的工作线程（worker thread）

用于执行阻塞代码的阻塞线程（blocking thread）

前面提到的 `new_multi_thread()` 创建的那些线程，指的主要是worker线程。它们负责执行异步任务，也负责配合runtime进行future的poll、任务切换以及部分驱动工作。

**这些worker线程适合执行的，是那类不会长时间卡住线程的任务，也就是典型的异步I/O型任务** 。

但是在实际编程中，也会遇到另一类任务：

**同步库调用**

**长时间CPU计算**

**会阻塞线程的系统系统**

**不能改写成async的旧代码**

如果把这类代码直接放进异步任务里执行，就会发生问题。最典型的例如：

```rust
fn main() {

let rt = tokio::runtime::Runtime::new().unwrap();

rt.block\_on(async {

std::thread::sleep(std::time::Duration::from\_secs(10));

});

}
```
这里使用的是 `std::thread::sleep()` ，它会直接阻塞当前 worker 线程。在阻塞期间，Tokio 无法在这个线程上继续调度其他异步任务。因此，这类阻塞操作会破坏异步调度的优势。

所以 Tokio 才区分出两种线程使用场景：

worker thread：用于执行异步任务，不适合长期阻塞

blocking thread：用于执行可能阻塞线程的同步代码，避免把 worker 线程卡住
## 2、spawn\_blocking()

在Tokio中，可以使用 `tokio::task::spawn_blocking()` 把同步阻塞代码放到专门的阻塞线程池中执行。

示例形式如下：

```rust
let v = tokio::task::spawn\_blocking(|| {

heavy\_compute()

}).await?;

`spawn_blocking()` 并不是“每调用一次就永久创建一个新线程”那么简单，更准确地说， **它会把任务提交到Tokio专门管理的阻塞线程池中执行。这个线程池可能按需创建线程，也会进行复用，并受运行时配置控制** 。
```
它和 `std::thread::spawn()` 的区别主要在于：

它属于Tokio的统一调度体系之外，但仍然Tokio统一管理：阻塞任务不是异步任务，不会在worker线程上以future的形式被poll，但它仍然由Tokio runtime负责管理其生命周期和线程池资源。

它返回的是Tokio的 `JoinHandle` ：因此可以直接在async代码块中`.await` 。
```rust
let res = tokio::task::spawn\_blocking(|| {

1 + 2

}).await.unwrap();
```
而 `std::thread::spawn()` 返回的是标准库线程句柄，只能 `join()` ，不能直接 `.await` 。

它适合桥接同步世界和 async 世界：当你必须调用某些同步阻塞代码时， `spawn_blocking()` 往往是更自然的过渡方式。
## 3、blocking thread的取消

**通过** `spawn_blocking()` **创建的任务，一旦开始在阻塞线程中执行，就不能像异步任务那样被可靠取消** 。如果对该任务的句柄调用 `abort()` ：

若任务还没真正开始执行，可能有机会阻止它启动

若任务已经开始执行， `abort()` 通常不会强行把它停下来

示例：

```rust
use tokio;

fn main() {

let rt = tokio::runtime::Runtime::new().unwrap();

rt.block\_on(async {

let h = tokio::task::spawn\_blocking(|| {

let mut i = 0u32;

loop {

i += 1;

println!("tick: {}", i);

std::thread::sleep(std::time::Duration::from\_millis(200));

}

});

tokio::time::sleep(tokio::time::Duration::from\_secs(1)).await;

println!("abort now");

h.abort();

match h.await {

Ok(\_) => println!("blocking task finished normally"),

Err(e) => println!("blocking task was cancelled: {}", e),

}

tokio::time::sleep(tokio::time::Duration::from\_secs(1)).await;

println!("main over");

});

}
```
结果：

![[Image 107.png]]

`abort()` 并不能像取消普通异步任务那样，把一个已经开始运行的 blocking 任务立刻停掉。可以看到，阻塞任务会一直运行。

因此要注意， `spawn_blocking()` 更适合执行：可控时长的阻塞逻辑、不会无限死循环的同步代码。 **如果把不可结束的死循环放进去，就可能给runtime关闭带来麻烦** ，后面会讨论。
## 4、spawn\_blocking()中的同步代码与async世界交换数据

为了让 `spawn_blocking()` 中的同步代码与async世界交互，常见有两种方式：简单返回值和流式通信。

### （1）简单返回值

当同步函数执行完之后只需要返回一个结果。不需要中途与async代码交互，那么直接返回值即可。

示例：

```rust
#\[tokio::main\]

async fn main() {

let t = tokio::task::spawn\_blocking(|| {

let mut sum = 0;

for i in 0..1\_000 {

sum += i;

}

sum

});

let res = t.await.unwrap();

println!("res={}", res);

}
```
### （2）边计算边向async代码发送数据

如果需要一边执行同步逻辑，一边把中间结果不断传给async世界，那么可以使用通道，例如 `tokio::sync::mpsc` 。

在同步代码中，可以使用：

`blocking_send()`

`blocking_recv()`

这类专门为阻塞上下文准备的方法。

示例：

```rust
use tokio::sync::mpsc;

#\[tokio::main\]

async fn main() {

let (tx, mut rx) = mpsc::channel::<String>(10);

let t = tokio::task::spawn\_blocking(move || {

for i in 0..5 {

tx.blocking\_send(format!("line: {}", i)).unwrap();

}

// tx drop时，rx可以感知到流结束

});

while let Some(msg) = rx.recv().await {

println!("recv: {}", msg);

}

let \_ = t.await;

}
```
关于tokio的通道，后续会专门介绍。
# 六、关闭Runtime

## 1、drop

Tokio的异步执行依赖runtime提供的调度器、I/O驱动、时间驱动、worker线程池、blocking线程池等资源。

而 `Runtime` 本身只是程序中的一个Rust普通值，因此当它离开作用域时，也会像普通值一样被 `drop` 。

当 `Runtime` 被 `drop` 时，会触发运行时关闭。

示例：

```rust
let rt = tokio::runtime::Runtime::new().unwrap();

//...

drop(rt);
```
这里的 `rt` 持有并管理整个运行时相关资源。当 `drop(rt)` 时，可以从整体上理解Tokio的关闭语义：

**停止接收新的工作**

Runtime进入关闭流程后，将不再继续接受新的任务注入，也不会再正常推进新的运行时活动。

**未完成的异步任务会被终止推进**

对于普通异步任务来说，runtime关闭后，它们不再被继续poll。从效果上看，这些未完成任务会被取消。

**I/O与时间驱动被关闭**

底层I/O驱动、定时器驱动等运行时基础设施会在关闭过程中被释放。

**worker线程会退出调度循环**

Tokio不会强杀worker线程，而是让它们在关闭流程中结束调度并退出。

**已开始执行的blocking任务可能导致关闭等待很久**

这是最需要注意的一点。对于spawn\_blocking()提交的任务，如果它们已经执行，那么Tokio无法强行终止它们，因此在默认drop runtime的过程中，Tokio会等待这些blocking任务的结束。

如果某个blocking任务是死循环，或者长期卡住不返回，那么runtime的关闭过程就可能被拖得很久，甚至看起来像“卡死”。
## 2、shutdown\_background

`Runtime` 提供了 `shutdown_background()` 方法，用来在后台发起关闭，而不是像普通drop那样等待所有相关工作等彻底结束。

它的典型用途是：

当前上下文不适合长时间等待runtime关闭

明确知道存在可能拖延关闭的blocking任务

希望runtime尽快从当前作用域中释放出来

需要注意， `shutdown_background()` 的含义并不是“立刻杀死所有任务和线程”，而是不再像普通drop那样在当前线程中等待完整关闭流程。

示例：

```rust
fn main() {

let rt = tokio::runtime::Runtime::new().unwrap();

rt.block\_on(async {

tokio::task::spawn\_blocking(move || {

loop {

println!("hello");

std::thread::sleep(std::time::Duration::from\_secs(1));

}

});

});

rt.shutdown\_background();

}
```
这里的blocking thread是一个死循环，如果最后没有使用 `rt.shutdown_background()` 而是普通 `drop` ，那么 `drop` 的过程中就会一直等待blocking thread结束，从而导致进程无法退出。而 `rt.shutdown_background()` 会立即返回，不再让当前线程等 `drop` 结束，最后主线程结束，进程结束。
