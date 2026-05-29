---
title: Rust 特征进阶
date: 2026-05-29
tags: [rust, trait, self, associated-type, associated-constant, generic, ufcs, supertrait]
source_count: 1
---

# Rust 特征进阶

本文是对 Rust trait 高级特性的系统梳理，涵盖 `Self` 语义、关联项、泛型 trait、UFCS 与超 trait。

## 核心内容

### Self 在 Trait 中的含义

`Self`（大写）在 trait 中表示**当前实现该 trait 的具体类型**，与方法参数中的 `self`（小写）完全不同。常见用法包括：
- 返回当前实现类型：`fn clone_like(&self) -> Self`
- 要求参数是同一种类型：`fn merge(&self, other: &Self) -> Self`
- 访问关联项：`Self::Output`、`Self::Item`

`Self` 会影响 `dyn Trait` 的兼容性。

### 关联项

Trait 可定义三类关联项：
- **关联函数** — 无 `self` 参数的函数，如构造实例 `T::new()`
- **关联类型** — 类型占位符，如 `Iterator::Item`
- **关联常量** — 类型相关常量，如默认容量、名称

标准库 `Iterator` 和 `Add` 都大量使用了关联项设计。

### 泛型 Trait 与默认参数

Trait 本身可带泛型参数。`Convert<String>` 和 `Convert<i32>` 可视为两个不同的 trait，同一类型可针对不同类型参数分别实现。

默认类型参数用于设置常用默认值：`trait Add<Rhs = Self>`。

### 完全限定方法调用（UFCS）

当多个 trait 存在同名方法，或固有方法与 trait 方法同名时，使用 `<Type as Trait>::method` 明确指定方法来源。关联函数歧义时也必须使用完全限定语法。

### 子 Trait 与超 Trait

`trait Movable: Render` 表示实现 `Movable` 必须先实现 `Render`。这不是类继承，而是一种能力约束。

## 关联页面

- [[Trait中的Self]] — `Self` 的详细语义与使用场景
- [[Trait关联项]] — 关联函数、关联类型与关联常量详解
- [[泛型Trait与默认参数]] — 泛型 trait 与默认类型参数
- [[完全限定方法调用]] — UFCS 语法与歧义消除
- [[子Trait与超Trait]] — 超 trait 与子 trait 的能力依赖关系
- [[Trait]] — trait 系统核心概念
- [[Trait对象与动态分发]] — `Self` 对 dyn 兼容的影响

## 来源

- [[特征进阶]]
