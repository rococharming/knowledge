---
title: size_of 与 size_of_val
date: 2026-05-13
tags: [rust, memory-safety]
source_count: 1
---

本文是 Rust `std::mem::size_of` 与 `std::mem::size_of_val` 学习笔记的整体摘要，涵盖两个函数的核心区别、使用场景以及与动态大小类型（DST）的关系。

## 核心内容概览

### 函数区别

| 函数 | 签名 | 作用 |
|---|---|---|
| `size_of::<T>()` | `fn size_of<T>() -> usize` | 查看类型 `T` 占用的字节数 |
| `size_of_val(&value)` | `fn size_of_val<T: ?Sized>(val: &T) -> usize` | 查看具体值占用的字节数 |

- `size_of` 面向**类型**，`size_of_val` 面向**具体值**
- 对于普通 `Sized` 类型，两者结果通常相同
- 对于 DST（`str`、`[T]`、`dyn Trait`），`size_of_val` 更有意义，可利用引用元数据计算实际大小

### 关键特性

- 两个函数都是 `const fn`，可在常量上下文中使用
- `size_of::<T>()` 要求 `T: Sized`，不能直接用于 DST
- 计算的是**值本身的大小**，不递归统计内部指向的堆内存（如 `String` 只统计 `ptr`/`len`/`cap` 结构，不包括堆上字符串内容）

### 使用示例

```rust
size_of::<i32>();       // 4
size_of::<[i32; 3]>();  // 12
size_of::<str>();       // 错误，DST 无法确定大小

let s: &str = "hello";
size_of_val(s);         // 5，字符串内容字节数
size_of_val(&s);        // 16，&str 胖指针大小（64位平台）
```

## 衍生 wiki 页面

- [[size_of 与 size_of_val]] — 两个函数的详细说明与对比
- [[size_of 与 size_of_val 速查]] — 常用代码片段速查

## 来源

- [[size_of和size_of_val]]
