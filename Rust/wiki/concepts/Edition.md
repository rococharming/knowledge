---
title: Edition
date: 2026-05-10
tags: [rust, edition, compiler]
source_count: 2
---

# Edition

## 定义

Edition（版本纪元）是 Rust 语言规则的一组**可选版本包**。同一门 Rust 语言下，编译器支持多套规则，每个项目选择一个 Edition，编译器按该规则解析与编译代码。

## 目的

Rust 需要同时满足两个看似矛盾的目标：

- **稳定性**：旧项目在多年之后仍应能编译运行
- **进化性**：语言需要持续改进（语法糖、关键字、宏、预导入等）

如果只有一套规则，改进规则就会导致旧项目在新编译器上不可用。Edition 的作用就是让**新规则可选**，旧项目仍然按照旧规则编译。

## 现有版本

同一 rustc 同时兼容多个 Edition：

- **2015**：Rust 1.0 的初始规则
- **2018**：引入 async/await 关键字、模块系统改进等
- **2021**：持续改进
- **2024**：最新版本

## 使用方法

在 `Cargo.toml` 中指定：

```toml
[package]
edition = "2024"
```

> 较新版本的 Rust 默认生成 `edition = "2024"`，较旧版本可能默认生成 `2021`。

或通过 rustc 命令行指定：

```bash
rustc main.rs --edition=2021
```

## 特性

- 不同 Edition 的代码可以互相调用（库和可执行文件可以使用不同 Edition）
- Edition 的切换通常只需要修改 `Cargo.toml` 中的一行配置
- Edition 不是版本号，同一 rustc 编译器同时支持所有 Edition

## Edition 迁移

升级 Edition 时，推荐先使用自动迁移工具而非直接手动修改 `Cargo.toml`：

```bash
cargo fix --edition
```

这条命令根据编译器的可自动修复建议直接修改源码，尝试把代码改成同时兼容当前 Edition 和下一个 Edition 的写法。

迁移流程：

1. 运行 `cargo fix --edition`
2. 修改 `Cargo.toml` 中的 `edition` 字段为目标版本
3. 运行 `cargo check` 检查
4. 运行 `cargo test` 验证

示例：Rust 2018 引入 `async`/`await` 关键字后，旧代码中名为 `async` 的标识符可能被自动改为原始标识符写法：

```rust
let r#async = 1;  // r#前缀表示将关键字当作普通标识符使用
```

> `cargo fix --edition` 不是万能工具，只能处理编译器能明确判断的问题。涉及业务逻辑、API 设计、依赖版本升级的部分仍需人工检查。

## 关联

- [[rustc]] — 支持多 Edition 的编译器
- [[Cargo]] — 在 `Cargo.toml` 中指定项目 Edition

## 来源

- [[Rust安装与开发环境配置]]
- [[crate与模块]]
