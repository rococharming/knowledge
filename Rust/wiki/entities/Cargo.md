---
title: Cargo
date: 2026-07-21
tags: [rust, cargo, toolchain]
source_count: 2
---

# Cargo

`cargo` 是 Rust 的构建工具和包管理工具。它负责创建项目、读取 `Cargo.toml`、下载和编译依赖、组织构建流程、运行测试、生成文档，并在底层调用 [[rustc]] 完成编译。

## 项目创建

创建二进制可执行项目：

```shell
cargo new hello_cargo
```

典型目录结构：

```text
hello_cargo/
├── .git/
├── .gitignore
├── Cargo.toml
└── src/
    └── main.rs
```

![[Image 10.png|800]]

如果不希望自动初始化 Git，可以使用：

```shell
cargo new hello_cargo --vcs=none
```

创建库项目：

```shell
cargo new --lib my_library
```

库项目默认生成 `src/lib.rs`，没有 `main` 函数，主要用于被其他代码调用。

## Cargo.toml

`Cargo.toml` 是 Cargo 项目的核心配置文件。新建项目后通常包含：

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

`[package]` 描述包名、版本、Edition 等元信息；`[dependencies]` 声明第三方 crate 依赖。依赖管理的展开内容适合后续单独编译为 wiki 页面。

> [!note]
> 默认生成的 Edition 取决于本机 Rust/Cargo 版本；较旧环境可能仍生成 `2021`。

## 常用开发命令

```shell
cargo build
cargo build --release
cargo run
cargo run --release
cargo check
cargo test
cargo doc
cargo clean
```

`cargo build` 默认使用调试构建，产物位于 `target/debug`；`cargo build --release` 使用发布构建，产物位于 `target/release`。调试构建编译更快、保留更多调试信息；发布构建优化更强，更适合发布或性能测试。

`cargo run` 会完成“构建 + 运行”；`cargo check` 做类型检查和借用检查但不生成最终可执行文件，因此常用于开发过程中快速发现编译错误。

`cargo doc` 会生成项目 API 文档，底层调用 `rustdoc` 解析 [[Rust 注释与 rustdoc 文档]] 中的文档注释。常用 `cargo doc --open` 在生成后直接打开浏览器查看。

## 相关页面

- [[rustup]]
- [[rustc]]
- [[Rust IDE 环境配置]]
- [[Rust 注释与 rustdoc 文档]]

## 来源

- [[Rust安装与开发环境配置]]
- [[注释与rustdoc]]
