---
title: Edition
date: 2026-05-10
tags: [rust, edition, compiler]
source_count: 1
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
edition = "2021"
```

或通过 rustc 命令行指定：

```bash
rustc main.rs --edition=2021
```

## 特性

- 不同 Edition 的代码可以互相调用（库和可执行文件可以使用不同 Edition）
- Edition 的切换通常只需要修改 `Cargo.toml` 中的一行配置
- Edition 不是版本号，同一 rustc 编译器同时支持所有 Edition

## 关联

- [[rustc]] — 支持多 Edition 的编译器
- [[Cargo]] — 在 `Cargo.toml` 中指定项目 Edition
