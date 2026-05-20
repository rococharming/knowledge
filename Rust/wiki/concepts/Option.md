---
title: Option
date: 2026-05-21
tags: [rust, enum, option, error-handling]
source_count: 2
---

# Option

`Option<T>` 是 Rust 标准库中表示“可能有值，也可能无值”的泛型枚举。Rust 没有 `null`，因此当一个值可能不存在时，应使用 `Option<T>` 显式建模。它是 [[枚举类型]] 的典型应用。

## 定义形态

`Option<T>` 可理解为：

```rust
enum Option<T> {
    Some(T),
    None,
}
```

- `Some(T)` 表示存在一个类型为 `T` 的值
- `None` 表示没有值

直接写 `None` 时，编译器通常无法推断 `T`，需要显式标注类型：

```rust
let x = Some(1);
let y: Option<i32> = None;
```

## 与模式匹配

`Option<T>` 常通过 [[模式匹配机制]] 拆开：

```rust
fn print_value(value: Option<i32>) {
    match value {
        Some(n) => println!("{}", n),
        None => println!("no value"),
    }
}
```

只关心有值的情况时，可以使用 [[简洁控制流]]：

```rust
if let Some(n) = value {
    println!("{}", n);
}
```

`let else` 适合“没有值就提前退出”的流程，`while let` 适合持续取值直到 `None`。

## 常见场景

- 可选配置、可选输入、查找结果
- 容器弹出元素，如 `Vec::pop()` 返回 `Option<T>`
- 整型检查运算，如 `checked_add` 溢出时返回 `None`
- 引用可能存在也可能不存在，如 `Option<&T>`

## 内存优化

Rust 会对某些 `Option` 做空值优化。典型例子是 `Option<&T>`：引用本身不能是空指针，因此编译器可用空指针表示 `None`，非空指针表示 `Some(...)`，使 `Option<&T>` 通常与 `&T` 大小相同。

## 关联

- [[枚举类型]] — `Option<T>` 的枚举本质
- [[模式匹配机制]] — 处理 `Some` 和 `None` 的完整形式
- [[简洁控制流]] — `if let`、`let else`、`while let`
- [[数据类型]] — `checked_add` 等返回 `Option<T>` 的数值操作

## 来源

- [[枚举]]
- [[模式匹配机制]]
