---
title: Rust 错误处理
date: 2026-06-01
tags: [rust, error-handling, panic, result]
source_count: 1
---

# Rust 错误处理

Rust 没有传统异常机制，而是通过类型系统将错误显式分为**可恢复错误**和**不可恢复错误**，分别由 `Result<T, E>` 和 `panic!` 处理。错误处理是 Rust 类型安全的核心组成部分之一。

## 核心内容总览

### 错误分类

| 错误类型 | 推荐方式 | 典型场景 |
|---|---|---|
| 可预期、可处理的错误 | `Result<T, E>` | 文件不存在、解析失败、网络失败 |
| 程序逻辑错误 | `panic!` | 越界访问、断言失败、不可能分支 |
| 临时示例或测试 | `unwrap()` / `expect()` | 示例程序、单元测试、快速验证 |
| 复杂应用程序错误 | 自定义错误类型 | 命令行工具、库、业务程序 |

判断原则：调用者有机会处理 → 返回 `Result`；程序无法合理继续 → `panic!`。

### 素材涵盖的主要知识点

- **panic 机制**：主动触发、被动触发、栈展开 vs abort、backtrace 调用栈分析、双重 panic、线程级 panic
- **Result 处理**：`match` 分支处理、`unwrap`/`expect`、`unwrap_or`/`unwrap_or_else`、`is_ok`/`is_err`、`ok`/`err` 转换、`as_ref`/`as_mut`、#[must_use]
- **错误传播**：手动传播、`?` 运算符、`?` 的链式写法与错误类型自动转换、`?` 用于 Option
- **统一错误类型**：`Box<dyn Error>` 的应用场景与 `From` 转换机制
- **自定义错误类型**：枚举定义、实现 `Debug` + `Display` + `std::error::Error` + `From`、保留底层错误链
- **Result 类型别名**：`std::io::Result<T>` 等标准库别名与项目自定义别名
- **main 函数中的错误处理**：`expect()`、`main` 返回 `Result`、`run()` 分离模式

## 关联页面

- [[panic机制]] — panic! 的触发方式、栈展开/abort、backtrace 与线程行为
- [[Result处理]] — Result 的多种处理方法与实用方法速查
- [[自定义错误类型]] — 自定义错误枚举与标准错误体系接入
- [[std-error-Error]] — std::error::Error trait 与错误链机制
- [[错误处理策略]] — 错误分类、处理策略对比与最佳实践
- [[main函数错误处理]] — main 函数中常见的错误处理模式
- [[Result]] — Result 枚举的定义与模式匹配基础
- [[Option]] — Option 枚举与 `?` 运算符在 Option 上的应用
- [[Trait对象与动态分发]] — `Box<dyn Error>` 的特征对象本质

## 来源

- [[错误处理]]
