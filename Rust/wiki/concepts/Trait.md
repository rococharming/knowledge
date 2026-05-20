---
title: Trait
date: 2026-05-21
tags: [rust, trait, type-system, generic]
source_count: 4
---

# Trait

Trait 是 Rust 类型系统中描述“某类类型具备什么能力”的机制。一个类型实现某个 trait 后，就可以在对应上下文中使用该能力。知识库中已经多次出现 trait：[[Copy]] 是标记 trait，数组打印依赖 `Debug`，普通显示格式依赖 `Display`，动态大小类型中也会出现 `dyn Trait`。

## 核心作用

- **约束能力**：泛型代码可要求类型实现特定 trait
- **表达行为**：为结构体、枚举等类型定义可复用接口
- **参与编译检查**：Cargo 构建库 crate 时，`rustc` 会保留类型检查、泛型实例化和 trait 检查所需的元数据

## 标记 Trait

`Copy` 是典型标记 trait。实现了 `Copy` 的类型在赋值或传参时按位复制，原变量仍然可用；未实现 `Copy` 的类型默认发生 [[移动]]。

结构体和枚举默认不是 `Copy`。如果所有字段或变体携带的数据都支持 `Copy`，可以通过派生让类型支持复制：

```rust
#[derive(Copy, Clone)]
struct Point {
    x: i32,
    y: i32,
}
```

## Trait 与格式化

Rust 的格式化宏会根据格式符要求不同 trait。例如数组未实现 `Display` 时不能用 `{}` 直接打印，通常使用 `Debug` 格式：

```rust
println!("{:?}", [1, 2, 3]);
```

## Trait 与 DST

`dyn Trait` 是动态大小类型（DST）的一类。`std::mem::size_of::<T>()` 要求 `T: Sized`，因此不能直接用于 `dyn Trait`；而 `size_of_val` 可以通过引用元数据处理 DST。

## 关联

- [[Copy]] — 标记 trait 与按位复制语义
- [[移动]] — 非 `Copy` 类型的默认所有权转移
- [[数据类型]] — `Display` 与 `Debug` 打印差异
- [[size_of 与 size_of_val]] — `dyn Trait` 与 DST
- [[Cargo构建配置]] — 构建过程中 trait 检查所需元数据

## 来源

- [[Rust 所有权]]
- [[Rust基础语法]]
- [[size_of和size_of_val]]
- [[crate与模块]]
