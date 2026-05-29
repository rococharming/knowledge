---
title: Rust 特征对象
date: 2026-05-29
tags: [rust, trait, trait-object, dynamic-dispatch, static-dispatch, vtable, dyn-compatibility]
source_count: 1
---

# Rust 特征对象

本文是对 Rust trait object 与分发机制的系统梳理，涵盖 trait object 用法、静态/动态分发与 dyn 兼容。

## 核心内容

### Trait Object 基本概念

Trait Object 是 Rust 中实现运行时多态的方式。`&dyn Trait` 表示引用一个实现了某个 trait 的值，但具体类型在函数签名中被隐藏，运行时才知道。

常见形式：
- `&dyn Trait` — 共享借用
- `&mut dyn Trait` — 可变借用
- `Box<dyn Trait>` — 拥有值

`dyn Trait` 是动态大小类型（DST），不能直接作为变量类型，必须放在指针后面。

### 胖指针与虚表

`&dyn Trait` 是胖指针，包含 `data_ptr`（指向具体值）和 `vtable_ptr`（指向虚表）。调用方法时，运行时通过虚表找到对应实现。

### 静态分发与动态分发

| 方式 | 写法 | 特点 |
|---|---|---|
| 静态分发 | `T: Trait` / `impl Trait` | 编译期确定，单态化，无间接调用开销 |
| 动态分发 | `dyn Trait` | 运行时通过虚表确定，支持异构集合 |

编译期能确定具体类型时优先静态分发；需要运行时统一处理不同类型时用动态分发。

### dyn 兼容（对象安全）

不是所有 trait 都能写成 `dyn Trait`。常见不兼容情况：
- 方法返回 `Self`
- 方法参数中使用 `Self`
- 方法带泛型参数
- 关联函数（无 `self`）

可用 `where Self: Sized` 排除不适合动态分发的方法，让 trait 其余部分保持 dyn 兼容。

## 关联页面

- [[Trait对象与动态分发]] — trait object、胖指针与分发机制详解
- [[Trait中的Self]] — `Self` 对 dyn 兼容的影响
- [[Trait]] — trait 的定义与实现基础
- [[泛型]] — 静态分发的单态化机制
- [[size_of 与 size_of_val]] — DST 与 `dyn Trait` 的大小问题

## 来源

- [[特征对象]]
