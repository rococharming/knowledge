---
title: "Cargo"
date: 2026-05-10
source_count: 1
tags: [rust, cargo, build-tool, entity]
---

# Cargo

## 定义

Cargo 是 Rust 的**官方构建工具和包管理器**，负责项目创建、依赖管理、代码构建、测试运行和文档生成。它是 Rust 开发的核心工具，底层调用 rustc 完成实际编译。

## 关键信息

### 核心功能

- **项目创建**：`cargo new` 生成标准项目结构
- **依赖管理**：自动下载、编译和配置 crates.io 上的库
- **代码构建**：`cargo build` 调用 rustc 编译项目
- **测试运行**：`cargo test` 执行项目中的测试代码
- **文档生成**：`cargo doc` 生成项目文档

### 常用命令

| 命令 | 作用 |
|------|------|
| `cargo new <name>` | 创建二进制项目 |
| `cargo new --lib <name>` | 创建库项目 |
| `cargo build` | 调试构建（`target/debug/`） |
| `cargo build --release` | 发布构建（`target/release/`） |
| `cargo run` | 构建并运行 |
| `cargo run --release` | 发布构建并运行 |
| `cargo check` | 检查代码是否可编译（不生成二进制） |
| `cargo test` | 运行测试 |
| `cargo clean` | 清理 `target/` 目录 |
| `cargo doc` | 生成文档 |

### 项目结构

```
hello_cargo/
├── .git/          # Git 仓库（自动生成）
├── .gitignore     # Git 忽略文件
├── Cargo.toml     # 项目配置
└── src/
    └── main.rs    # 入口文件（二进制项目）
```

### Cargo.toml 核心字段

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

### 构建模式对比

| 特性 | Debug 构建 | Release 构建 |
|------|-----------|-------------|
| 优化级别 | `opt-level=0` | `opt-level=3` |
| 编译速度 | 快 | 慢 |
| 可执行文件体积 | 大 | 小 |
| 运行速度 | 慢 | 快 |
| 调试符号 | 完整 | 较少 |
| 触发条件 | `cargo build` | `cargo build --release` |

### 依赖管理

- **`cargo add <crate>`**：自动添加依赖到 `Cargo.toml` 并更新 `Cargo.lock`
- **`cargo add <crate>@<version>`**：指定版本，支持 `^` 和 `~` 语义化范围
- **`cargo add <crate> --features <f1>,<f2>`**：启用 feature
- **`cargo add <crate> --dev`**：添加开发依赖（`[dev-dependencies]`）
- **`cargo add <crate> --build`**：添加构建依赖（`[build-dependencies]`）
- **`cargo remove <crate>`**：移除依赖

### Cargo.lock

- 自动生成的依赖锁定文件
- 记录项目使用的所有 crate 及其精确版本
- 确保不同环境下依赖一致，多人协作时应提交到版本控制

## 相关素材

- [[Rust安装与开发环境配置摘要]]
