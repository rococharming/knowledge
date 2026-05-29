---
title: Rust 特征基础
date: 2026-05-29
tags: [rust, trait, trait-bound, impl-trait, orphan-rule]
source_count: 1
---

# Rust 特征基础

本文是对 Rust trait 系统基础部分的系统梳理，涵盖 trait 定义实现、默认方法、孤儿规则、trait bound 与 `impl Trait`。

## 核心内容

### Trait 定义与实现

Trait 使用 `trait` 关键字定义，描述类型具备的能力。使用 `impl Trait for Type` 为具体类型实现。

```rust
trait Animal {
    fn eat(&self);
}

impl Animal for Dog {
    fn eat(&self) {
        println!("eating");
    }
}
```

### 默认方法

Trait 可提供默认实现，实现者可复用或重写。默认方法可调用同 trait 中的其他方法。标准库 `Iterator` 大量使用此模式。

### 孤儿规则

实现 `impl Trait for Type` 时，trait 或类型至少有一个定义在当前 crate 中。避免不同 crate 为同一组外部 trait + 外部类型提供冲突实现。

### Trait 作用域

调用 trait 方法通常需要将 trait 引入作用域（预导入模块中的 trait 除外）。

### Trait Bound

约束泛型参数必须具备的能力：
- `T: Display` — 基本写法
- `where T: Display` — 复杂约束更清晰
- `T: Display + Debug` — 多重 bound

### impl Trait

- 参数位置：`fn show(value: impl Display)`，是显式泛型的语法糖
- 返回位置：`fn create() -> impl Animal`，调用方不知道具体类型
- 返回位置要求单一具体类型，不能根据条件返回不同类型

## 关联页面

- [[Trait]] — trait 系统核心概念详解
- [[泛型]] — 类型参数与泛型代码
- [[Trait中的Self]] — `Self` 在 trait 中的类型级语义
- [[Trait关联项]] — 关联函数、关联类型与关联常量
- [[Trait对象与动态分发]] — `dyn Trait` 与运行时多态

## 来源

- [[特征基础]]
