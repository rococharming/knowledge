---
title: rustdoc
date: 2026-05-21
tags: [rust, rustdoc, documentation, toolchain]
source_count: 2
---

# rustdoc

`rustdoc` 是 Rust 工具链中的文档生成工具，用于解析 Rust 文档注释并生成 HTML API 文档。安装 [[rustup]] 时通常会一并安装 `rustc`、Cargo、`rustdoc` 等核心工具。

## 与文档注释

Rust 的文档注释使用 Markdown 语法，由 `rustdoc` 解析：

- `///` 为紧随其后的 item 添加文档
- `//!` 为当前模块或 crate 添加文档
- 代码块可作为文档测试运行

执行 `cargo doc` 时，Cargo 底层调用 `rustdoc` 生成文档。生成的 HTML 位于 `target/doc/` 目录下。

## 文档测试

文档注释中的示例代码可以作为 doctest 运行。这样 API 文档不仅说明用法，也能在测试中验证示例仍然可用。

## 关联

- [[注释]] — 文档注释语法、惯例标题与 doctest
- [[Cargo]] — `cargo doc` 命令
- [[rustup]] — 安装和管理 Rust 工具链
- [[rustc]] — Rust 编译器

## 来源

- [[Rust基础语法]]
- [[Rust安装与开发环境配置]]
