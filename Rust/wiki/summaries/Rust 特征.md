---
title: Rust 特征
date: 2026-05-26
tags: [rust, trait]
source_count: 1
---

# Rust 特征

本文是对 Rust trait 系统的系统梳理，涵盖 trait 的定义、实现、约束与高级用法。

## 核心内容

Trait 是 Rust 中描述"类型具备某种能力"的机制。一个类型实现某个 trait 后，就可以在对应上下文中使用该能力。

### 主要知识点

- **Trait 定义与实现** — 使用 `trait` 关键字定义能力接口，`impl Trait for Type` 为具体类型实现
- **默认方法** — trait 可提供默认实现，实现者可复用或重写；默认实现可调用同 trait 中的其他方法
- **孤儿规则** — 实现 `impl Trait for Type` 时，trait 或类型至少有一个定义在当前 crate 中
- **Trait 作用域** — 调用 trait 方法通常需要将 trait 引入作用域（预导入模块中的 trait 除外）
- **Trait Bound** — 约束泛型参数必须具备的能力，支持 `T: Display` 和 `where` 子句写法
- **多重 Trait Bound** — `T: Display + Debug` 要求同时实现多个 trait
- **impl Trait** — trait bound 的语法糖，可用于参数位置和返回位置，但返回位置要求单一具体类型

Trait 与[[泛型]]紧密配合：泛型让代码适用于多种类型，trait 约束这些类型必须具备哪些能力。

## 关联页面

- [[Trait]] — trait 系统核心概念详解
- [[泛型]] — 类型参数与泛型代码
- [[Option]] — 标准库泛型枚举
- [[Result]] — 标准库泛型枚举

## 来源

- [[特征]]
