---
title: 测试 Seam
date: 2026-07-24
tags:
  - testing
  - test-seam
aliases:
  - Test Seam
  - 测试接缝
  - 可替换连接口
---

# 一、测试 Seam

测试 Seam 是业务逻辑和外部依赖之间的一个可替换连接口。它让测试可以不碰真实时间、真实网络、真实数据库或真实进程，而是换成自己能控制、能模拟、能检查的测试实现。

更直白地说：

> 正式运行时，这里接真实对象；测试运行时，这里能换成假的对象。这个能替换的连接处，就是 Seam。

不要把 Seam 理解成代码里的某一行固定位置。它更像一个插座：电器通过插座接入电源，所以可以接墙上电源，也可以接测试电源。程序通过参数、Trait、闭包或模块边界接入依赖，所以测试时可以换成 Fake、Stub、Mock 或 Spy。

# 二、问题来源

## 1、依赖被焊死

没有 Seam 的代码通常把“获取外部数据”和“业务判断”写在一起。

示例：

```rust
fn is_morning() -> bool {
    let hour = chrono::Local::now().hour();
    hour < 12
}
```

这段代码同时做了两件事：

- 读取电脑的真实当前时间。
- 判断这个时间是否小于 12 点。

测试时无法稳定指定“现在是上午 9 点”或“现在是下午 3 点”，因为函数一定会读取真实系统时间。上午跑和下午跑，结果可能不同。

## 2、逻辑被拆开

加入 Seam 的第一步通常是把外部依赖的结果传进来。

示例：

```rust
fn is_morning(hour: u32) -> bool {
    hour < 12
}
```

测试可以直接控制输入：

```rust
#[test]
fn detects_morning() {
    assert!(is_morning(9));
    assert!(!is_morning(15));
}
```

正式代码仍然可以读取真实时间：

```rust
fn current_is_morning() -> bool {
    use chrono::Timelike;

    let hour = chrono::Local::now().hour();
    is_morning(hour)
}
```

这里的 `hour` 参数就是 Seam。它把“读取真实时间”和“判断是否上午”分开了。

# 三、三种能力

## 1、替换

替换是指测试可以不使用真实依赖，而是接入测试替身。

网络请求是典型例子：

```text
正式运行：业务逻辑 -> 真实 HTTP 客户端 -> 真实服务器
测试运行：业务逻辑 -> 假 HTTP 客户端 -> 预设响应
```

中间允许 HTTP 客户端互换的连接口，就是 Seam。

## 2、控制

控制是指测试能决定依赖返回什么、什么时候失败、是否为空、是否超时。

例如读取配置文件时，不一定要让业务逻辑直接读真实文件：

```rust
fn parse_config(content: &str) -> bool {
    content.contains("enabled=true")
}
```

测试可以构造任意内容：

```rust
#[test]
fn parses_enabled_flag() {
    assert!(parse_config("enabled=true"));
    assert!(!parse_config("enabled=false"));
}
```

这里的 `content` 参数让测试控制了“文件读取结果”。

## 3、观察

观察是指测试能检查业务代码是否正确调用了某个外部动作。

例如发送通知时，测试可能关心：

- 是否调用了发送逻辑。
- 发送了几次。
- 发送给谁。
- 发送内容是什么。

可以把通知能力抽象成接口：

```rust
trait Notifier {
    fn send(&self, message: &str);
}

fn register_user(notifier: &impl Notifier, name: &str) {
    let message = format!("欢迎你，{name}");
    notifier.send(&message);
}
```

测试时传入一个会记录消息的实现：

```rust
use std::cell::RefCell;

struct RecordingNotifier {
    messages: RefCell<Vec<String>>,
}

impl Notifier for RecordingNotifier {
    fn send(&self, message: &str) {
        self.messages.borrow_mut().push(message.to_string());
    }
}
```

测试结束后检查记录：

```rust
#[test]
fn sends_welcome_message() {
    let notifier = RecordingNotifier {
        messages: RefCell::new(Vec::new()),
    };

    register_user(&notifier, "小明");

    assert_eq!(
        notifier.messages.borrow().as_slice(),
        ["欢迎你，小明"]
    );
}
```

这里的 `notifier` 参数是 Seam，`RecordingNotifier` 是通过这个 Seam 接入的测试实现。

# 四、常见形式

## 1、函数参数

函数参数是最轻量的 Seam，适合已经能提前算出来的数据。

```rust
fn is_expired(now: u64, expires_at: u64) -> bool {
    now >= expires_at
}
```

适合放在参数里的依赖包括时间、随机值、配置项、文件内容和命令行参数。

## 2、Trait 接口

Trait 适合抽象一组外部能力，例如数据库、网络、文件系统、消息服务、系统时间或外部进程。

```rust
trait UserApi {
    fn get_user_name(&self, id: u32) -> Result<String, String>;
}

fn welcome_user(api: &impl UserApi, id: u32) -> Result<String, String> {
    let name = api.get_user_name(id)?;
    Ok(format!("欢迎你，{name}"))
}
```

正式环境传真实 HTTP 实现，测试环境传固定返回值的实现。

## 3、闭包参数

闭包适合把一个小行为交给调用方，例如重试、过滤、回调或延迟执行。

```rust
fn retry<F>(mut operation: F) -> Result<(), String>
where
    F: FnMut() -> Result<(), String>,
{
    operation()
}
```

测试可以传入一个完全受控的闭包：

```rust
#[test]
fn executes_operation() {
    let result = retry(|| Ok(()));
    assert!(result.is_ok());
}
```

## 4、模块边界

模块边界适合把外部交互集中到适配层：

```text
业务逻辑模块
  -> 外部适配模块
  -> 数据库、网络、文件系统、进程
```

测试业务逻辑时，可以绕过真实适配层，只测试输入、输出和错误处理。

# 五、测试替身

Seam 不等于 Mock。

| 名称 | 含义 | 关注点 |
|---|---|---|
| Seam | 可以替换依赖的连接口 | 依赖从哪里接入 |
| Stub | 返回预设结果的测试实现 | 给业务代码固定输入 |
| Fake | 简化但能工作的测试实现 | 用轻量实现代替真实系统 |
| Mock | 验证某个调用是否发生 | 检查交互是否符合预期 |
| Spy | 记录调用信息，之后检查 | 观察调用次数和参数 |

例如 `fn welcome_user(api: &impl UserApi, id: u32)` 里的 `api` 参数是 Seam。测试里的 `FakeUserApi`、`StubUserApi` 或 `SpyUserApi` 是通过这个 Seam 接入的测试替身。

没有 Seam，测试替身通常就无处注入。


# 六、判断方法

判断一段代码是否需要 Seam，可以问三个问题：

- 测试时，我能不能控制这个依赖返回什么？
- 测试时，我能不能模拟它失败、超时、为空或异常退出？
- 测试时，我能不能观察业务代码是否正确调用了它？

如果答案经常是“不能”，这里通常缺少合适的 Seam。

但 Seam 不是越多越好。不要为了测试到处加 Trait。优先使用最简单的形式：

| 需求 | 优先选择 |
|---|---|
| 只是控制一个值 | 函数参数 |
| 只是传入一个小行为 | 闭包 |
| 需要替换一组外部能力 | Trait |
| 需要隔离系统交互 | 模块边界 |
| 需要验证完整真实流程 | 集成测试或端到端测试 |

