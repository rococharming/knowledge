---
title: size_of 与 size_of_val
date: 2026-05-12
tags: [rust, memory, std-mem, dst]
source_count: 1
---

# size_of 与 size_of_val

Rust 标准库 `std::mem` 提供两个用于查询内存占用的核心函数：`size_of` 面向类型，`size_of_val` 面向具体值。两者都是 `const fn`，可在常量上下文中使用。

## 核心区别

| 函数 | 签名 | 面向对象 | 关键约束 |
|---|---|---|---|
| `size_of` | `size_of::<T>() -> usize` | 类型 `T` | `T: Sized` |
| `size_of_val` | `size_of_val::<T: ?Sized>(val: &T) -> usize` | 具体值 `*val` | 接受 DST |

**关键差异**：`size_of_val` 计算的是 `*val`（引用指向的值）的大小，而非引用 `&T` 本身的大小。

## size_of

`size_of::<T>()` 返回类型 `T` 在内存中的字节数，要求 `T` 在编译期有确定大小（`T: Sized`）。

```rust
use std::mem::size_of;

fn main() {
    println!("{}", size_of::<i32>());      // 4
    println!("{}", size_of::<char>());     // 4
    println!("{}", size_of::<bool>());     // 1
    println!("{}", size_of::<[i32; 3]>()); // 12
}
```

**DST 限制**：动态大小类型（如 `str`、`[T]`、`dyn Trait`）没有编译期确定大小，不能直接作为 `size_of` 的类型参数：

```rust
// size_of::<str>();  // 错误：str 是 DST
```

## size_of_val

`size_of_val` 接受一个引用，返回被引用值的大小。由于签名使用 `?Sized`，它可以处理 DST。

### Sized 类型

对于普通固定大小类型，结果与 `size_of::<T>()` 一致：

```rust
use std::mem::size_of_val;

fn main() {
    let x: i32 = 5;
    println!("{}", size_of_val(&x)); // 4
}
```

### DST 类型

`size_of_val` 的真正价值体现在 DST 上。它利用胖指针携带的元数据（如长度信息）计算实际大小：

```rust
fn main() {
    let s: &str = "hello";

    println!("{}", size_of_val(s));   // 5  — str 内容本身的字节数
    println!("{}", size_of_val(&s));  // 16 — &str 胖指针的大小（64 位平台）
}
```

注意区分：
- `size_of_val(s)` → `s` 是 `&str`，`*s` 是 `str`，计算字符串内容大小
- `size_of_val(&s)` → `&s` 是 `&&str`，`*&s` 是 `&str`，计算胖指针本身大小

### 胖指针结构

`&str` 等 DST 引用是**胖指针**，包含两部分：
- 数据指针（8 字节，64 位平台）
- 长度信息（8 字节，64 位平台）

因此 `&str` 本身占 16 字节，但其指向的字符串内容可能只有几个字节。

## 重要注意事项

### 不递归统计堆内存

两个函数计算的是**值本身在栈或结构体内的直接大小**，不递归统计内部指针指向的堆内存。

```rust
use std::mem::size_of;

fn main() {
    // String 结构本身只含指针、长度、容量
    println!("{}", size_of::<String>()); // 24（64 位平台）
    // 不包含字符串在堆上的实际内容
}
```

### const fn 特性

两者都是 `const fn`，可在编译期常量上下文中使用：

```rust
const ARRAY_SIZE: usize = std::mem::size_of::<i64>();
```

## 相关页面

- [[size_of 与 size_of_val 速查]] — 速查代码示例
- [[数据类型]] — 标量类型与复合类型的内存布局
- [[所有权]] — Rust 内存管理模型与值语义
