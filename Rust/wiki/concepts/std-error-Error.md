---
title: std::error::Error
date: 2026-06-01
tags: [rust, error-handling, trait, error-chain]
source_count: 1
---

# std::error::Error

`std::error::Error` 是 Rust 标准库提供的**错误公共接口**，是错误处理体系的核心 trait。许多标准库错误类型都实现了这个 trait。

## 实现了 Error 的标准库类型

- `std::io::Error`
- `std::num::ParseIntError`
- `std::str::Utf8Error`
- `std::fmt::Error`

一个类型实现了 `std::error::Error`，表示它可以作为"错误类型"被统一处理。

## Error trait 的定义

简化定义：

```rust
pub trait Error: Debug + Display {
    fn source(&self) -> Option<&dyn Error> {
        None
    }
}
```

核心要求：

- **前置 trait**：实现 `Error` 的类型必须先实现 `Debug`（面向开发者调试）和 `Display`（面向用户显示）
- **错误链**：`source()` 方法返回当前错误背后的底层原因，支持错误链追溯

## Error 的两个核心作用

1. **统一接口**：让不同错误类型可以被统一对待（如 `Box<dyn Error>`）
2. **错误链**：通过 `source()` 表示当前错误背后的底层原因，支持逐层追溯

## 错误链的应用

```rust
use std::error::Error;

fn print_error(mut error: &dyn Error) {
    eprintln!("error: {error}");
    while let Some(source) = error.source() {
        eprintln!("caused by: {source}");
        error = source;
    }
}
```

通过循环调用 `source()`，可以从高层业务错误逐层追溯到最底层的 I/O 错误或解析错误。

## 与 Box<dyn Error> 的关系

`Box<dyn std::error::Error>` 是 [[Trait对象与动态分发|特征对象]] 的一种形式，表示"把某个实现了 `Error` 的具体错误类型放在堆上，通过 `dyn Error` 统一使用"。

标准库提供了类似这样的 blanket impl：

```rust
impl<E> From<E> for Box<dyn Error>
where
    E: Error,
{
    fn from(error: E) -> Self {
        Box::new(error)
    }
}
```

因此，只要具体错误类型实现了 `Error`，`?` 就可以自动将其装箱为 `Box<dyn Error>`。

## 自定义错误类型接入

自定义错误类型要实现 `Error`，通常需要依次实现：

1. `#[derive(Debug)]` — 调试输出
2. `impl Display for MyError` — 用户显示
3. `impl Error for MyError` — 接入标准体系（可选实现 `source()`）
4. `impl From<底层错误> for MyError` — 配合 `?` 自动转换

详见 [[自定义错误类型]]。

## 关联

- [[自定义错误类型]] — 完整的自定义错误实现流程
- [[Trait对象与动态分发]] — `Box<dyn Error>` 的胖指针与虚表机制
- [[错误传播]] — `?` 运算符与 From 转换
- [[Result处理]] — Result 的方法速查

## 来源

- [[错误处理]]
