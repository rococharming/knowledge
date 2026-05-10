---
title: Cargo
date: 2026-05-10
tags: [rust, cargo, package-management]
source_count: 1
---

# Cargo

## 概述

Cargo 是 Rust 的**构建工具和包管理工具**。安装 [[rustup]] 时会一并安装 Cargo 的最新 stable 版本。通过 Cargo 可以新建项目、构建代码、下载编译依赖库、运行测试和生成文档。构建时底层隐式调用 [[rustc]] 进行编译。

## 创建项目

### 二进制可执行项目

```bash
cargo new hello_cargo
```

自动生成目录结构：

```
hello_cargo/
├── .git/
├── .gitignore
├── Cargo.toml
└── src/
    └── main.rs
```

- `Cargo.toml`：项目配置文件，包含包信息和依赖
- `src/main.rs`：程序入口文件

不使用 Git 版本控制时，加 `--vcs=none` 选项。

### 库项目

```bash
cargo new --lib my_lib
```

生成 `src/lib.rs` 而非 `main.rs`。

## 常用命令

| 命令 | 作用 |
|---|---|
| `cargo build` | 调试构建，输出到 `target/debug/` |
| `cargo build --release` | 发布构建，输出到 `target/release/` |
| `cargo run` | 构建并运行 |
| `cargo run --release` | 发布构建并运行 |
| `cargo check` | 检查代码是否可编译（不生成产物，速度快） |
| `cargo test` | 运行测试 |
| `cargo doc` | 构建项目文档 |
| `cargo clean` | 清理构建产物（删除 `target/`） |

## 构建模式

| 模式 | 优化级别 | 编译速度 | 文件大小 | 运行速度 | 调试符号 |
|---|---|---|---|---|---|
| Debug（默认） | `opt-level=0` | 快 | 大 | 慢 | 完整 |
| Release | `opt-level=3` | 慢 | 小 | 快 | 较少 |

## 包管理

### 添加依赖

```bash
cargo add ferris-says              # 添加最新版本
cargo add ferris-says@0.3.2        # 指定精确版本
cargo add serde@^1.0               # 语义化版本范围
```

版本规则遵循 [[语义化版本]]。

### 启用 Features

Rust 库追求最小默认依赖，非核心功能放入 feature 中按需启用：

```bash
cargo add serde --features derive
cargo add tokio --features rt-multi-thread,macros
```

在代码中通过 `#[cfg(feature = "foo")]` 控制条件编译。

### 依赖类型

| 类型 | 命令 | 用途 |
|---|---|---|
| 普通依赖 | `cargo add crate` | 加到 `[dependencies]`，项目运行必需 |
| 开发依赖 | `cargo add crate --dev` | 加到 `[dev-dependencies]`，仅测试/基准时使用 |
| 构建依赖 | `cargo add crate --build` | 加到 `[build-dependencies]`，供 `build.rs` 构建脚本使用 |

### 移除依赖

```bash
cargo remove serde
cargo remove pretty_assertions --dev
cargo remove cc --build
```

### Cargo.lock

由 Cargo 自动生成，锁定项目所有依赖的确切版本。多人协作时应提交到版本控制，确保所有环境依赖一致。

## Cargo.toml 示例

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
ferris-says = "0.3.2"
serde = { version = "1", features = ["derive"] }

[dev-dependencies]
pretty_assertions = "1.4"
```

## 关联

- [[rustup]] — 管理 Cargo 版本的工具链管理器
- [[rustc]] — Cargo 底层调用的编译器
- [[语义化版本]] — Cargo 依赖版本解析规则
- [[Edition]] — Cargo.toml 中指定的语言规则版本
