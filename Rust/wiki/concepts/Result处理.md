---
title: Result 处理
date: 2026-06-01
tags: [rust, result, error-handling, match, unwrap]
source_count: 1
---

# Result 处理

`Result<T, E>` 是 Rust 中表示可恢复错误的核心类型。除了基础的 [[模式匹配机制|模式匹配]] 外，标准库提供了丰富的方法来处理 `Result`，覆盖从严格分支到快捷操作的各种场景。

## match 完整处理

处理 `Result` 最完整的方式是 `match`：

```rust
use std::fs::File;

let file = match File::open("hello.txt") {
    Ok(file) => file,
    Err(error) => {
        panic!("打开文件失败：{error}");
    }
};
```

根据错误类型采取不同措施：

```rust
use std::fs::File;
use std::io::ErrorKind;

let file = match File::open("hello.txt") {
    Ok(file) => file,
    Err(error) => match error.kind() {
        ErrorKind::NotFound => match File::create("hello.txt") {
            Ok(f) => f,
            Err(e) => panic!("创建文件失败：{e}"),
        },
        other_error => panic!("打开文件失败：{other_error:?}"),
    },
};
```

**适合 match 的场景**：成功和失败都要明确处理、不同错误走不同逻辑、错误处理是当前函数的重要逻辑。

## unwrap 与 expect

### unwrap()

- `Ok(v)` → 返回 `v`
- `Err(e)` → 触发 panic

```rust
let file = File::open("hello.txt").unwrap();
```

适合示例代码、测试代码，或错误发生时直接终止确实合理的场景。**不应滥用**。

### expect()

与 `unwrap()` 类似，但可自定义 panic 信息：

```rust
let file = File::open("hello.txt").expect("无法打开 hello.txt");
```

`expect()` 更适合表达"这里为什么可以假设成功"：

```rust
let home: IpAddr = "127.0.0.1"
    .parse()
    .expect("硬编码的 IP 地址应该是合法的");
```

![[Pasted image 20260526170746.png|600]]

## 提供默认值

### unwrap_or

失败时返回给定的默认值：

```rust
let result: Result<i32, &str> = Err("error");
let number = result.unwrap_or(0);  // 0
```

### unwrap_or_else

通过闭包延迟计算默认值，仅在 `Err` 时执行：

```rust
let number = result.unwrap_or_else(|error| {
    println!("error: {error}");
    0
});
```

## 布尔判断

仅判断成功或失败，不取出内部数据：

```rust
let result: Result<i32, &str> = Ok(10);
result.is_ok();   // true
result.is_err();  // false
```

## 转换为 Option

### ok()

`Result<T, E>` → `Option<T>`：

- `Ok(v)` → `Some(v)`
- `Err(e)` → `None`

```rust
let result: Result<i32, &str> = Ok(10);
let option = result.ok();  // Some(10)
```

### err()

`Result<T, E>` → `Option<E>`：

- `Ok(v)` → `None`
- `Err(e)` → `Some(e)`

```rust
let result: Result<i32, &str> = Err("error");
let option = result.err();  // Some("error")
```

> 这两个方法会丢弃另一侧的信息，只适合确实不关心其中一侧的场景。

## 不消耗 Result 的访问

### as_ref

`Result<T, E>` → `Result<&T, &E>`，避免按值消耗：

```rust
let result: Result<String, String> = Ok(String::from("hello"));
let option = result.as_ref().ok();  // Option<&String>
// result 仍可用
```

### as_mut

`Result<T, E>` → `Result<&mut T, &mut E>`，适合在不移动的前提下修改内部值：

```rust
let mut result: Result<i32, ()> = Ok(10);
if let Ok(v) = result.as_mut() {
    *v += 1;
}
```

## #[must_use]

`Result<T, E>` 带有 `#[must_use]` 属性，如果返回 `Result` 的表达式完全不处理，编译器会发出警告：

![[Pasted image 20260530211324.png|400]]

显式忽略时应写成：

```rust
let _ = some_function_returning_result();
```

`#[must_use]` 也可以标注在函数上：

```rust
#[must_use]
fn build_number() -> i32 { 100 }

build_number();  // 编译警告
```

![[Pasted image 20260530211637.png|400]]

## 方法速查

| 方法 | 成功时 | 失败时 | 消耗 Result |
|---|---|---|---|
| `match` | 按分支处理 | 按分支处理 | 是 |
| `unwrap()` | 返回值 | panic | 是 |
| `expect(msg)` | 返回值 | panic（带自定义信息） | 是 |
| `unwrap_or(d)` | 返回值 | 返回 `d` | 是 |
| `unwrap_or_else(f)` | 返回值 | 执行 `f` 返回 | 是 |
| `is_ok()` | `true` | `false` | 否 |
| `is_err()` | `false` | `true` | 否 |
| `ok()` | `Some(v)` | `None` | 是 |
| `err()` | `None` | `Some(e)` | 是 |
| `as_ref()` | `Ok(&v)` | `Err(&e)` | 否 |
| `as_mut()` | `Ok(&mut v)` | `Err(&mut e)` | 否 |

## 关联

- [[Result]] — Result 枚举的定义与基础概念
- [[模式匹配机制]] — match 的完整语法
- [[简洁控制流]] — `if let`、`let else` 简化 Result 处理
- [[panic机制]] — unwrap/expect 触发 panic 的行为
- [[错误传播]] — `?` 运算符与错误传播

## 来源

- [[错误处理]]
