---
title: "Rust安装与开发环境配置摘要"
date: 2026-05-10
source_count: 1
tags: [rust, setup, toolchain, cargo]
---

# Rust安装与开发环境配置摘要

来源：[[Rust安装与开发环境配置]]

## 核心观点

本文是一篇面向初学者的 Rust 开发环境搭建指南，系统介绍了从安装到第一个项目运行的完整流程，包括 rustup 工具链管理、rustc 基础编译、Cargo 项目构建，以及 VS Code IDE 配置。

## 关键要点

### 1. Rust 简介

- Rust 由 Graydon Hoare 于 2006 年发起，Mozilla 于 2009 年赞助，**1.0 稳定版于 2015 年 5 月 15 日发布**
- 核心优势：内存安全、性能高效（与 C/C++ 相当）、并发安全、统一包管理（Cargo）

### 2. 安装 Rust

- 通过 [[rustup]] 安装：`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
- 国内用户使用 [rsproxy.cn](https://rsproxy.cn/) 镜像加速，需配置环境变量和 `~/.cargo/config.toml`
- 安装后工具存放在 `~/.cargo/bin`，包含 cargo、rustc、rustdoc 等（均为 rustup 的软链接）

### 3. rustup 工具链管理

- `rustup update`：更新工具链
- `rustup self update`：更新 rustup 自身
- `rustup install stable/beta/nightly`：安装指定版本
- `rustup default stable/beta/nightly`：切换默认工具链

### 4. rustc 编译器

- 最基本用法：`rustc main.rs`，生成可执行文件
- `-o` 指定输出文件名，`--edition=2021` 指定 Edition
- 编译库：`--crate-type=rlib --crate-name=xxx`，链接时用 `-L. --extern`

### 5. Cargo 项目构建

- `cargo new <project>`：创建二进制项目（默认），`--lib` 创建库项目
- `cargo build`：调试构建（`target/debug`），`--release` 发布构建（`target/release`）
- `cargo run`：构建并运行，`cargo check`：快速检查编译可行性
- `cargo test`：运行测试，`cargo clean`：清理构建产物

### 6. IDE 环境

- **VS Code**：安装 rust-analyzer（代码补全、类型推导、错误提示）和 Error Lens
- **RustRover**：JetBrains 出品的专用 IDE（文中待补充）

### 7. 包管理

- 手动：在 `Cargo.toml` 的 `[dependencies]` 中添加 crate 和版本
- `cargo add <crate>`：自动添加并更新 `Cargo.lock`
- 语义化版本：`^X.Y.Z`（兼容大版本）、`~X.Y.Z`（兼容小版本）
- 依赖类型：普通依赖（默认）、开发依赖（`--dev`）、构建依赖（`--build`）
- `cargo remove <crate>`：移除依赖

## 相关页面

- [[rustup]]
- [[Cargo]]
- [[rustc]]
- [[Rust工具链]]
- [[Rust开发环境配置]]
