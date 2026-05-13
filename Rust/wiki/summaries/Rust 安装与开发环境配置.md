---
title: Rust 安装与开发环境配置
date: 2026-05-10
tags: [rust, setup, toolchain]
source_count: 1
---

# Rust 安装与开发环境配置

## 概述

Rust 是 Mozilla 于 2006 年发起的系统级编程语言，2015 年发布 1.0 稳定版。相比 C/C++，Rust 的核心优势在于编译期保障的内存安全、与 C/C++ 相当的性能、基于所有权系统的并发安全，以及统一的包管理工具链。

本文涵盖 Rust 工具链的安装配置、核心组件使用及开发环境搭建。

进入 Rust 官网 [https://rust-lang.org/](https://rust-lang.org/)，点击 Install，官网会根据当前操作系统给出对应的安装方案：

![[Image.png|600]]

## 核心组件

Rust 开发环境由以下核心组件构成：

- [[rustup]] — Rust 工具链管理器，负责安装、更新和切换不同版本的 Rust 编译器
- [[rustc]] — Rust 官方编译器，将 `.rs` 源文件编译为可执行文件或库
- [[Cargo]] — Rust 的构建工具和包管理工具，是项目开发的核心工具

## 安装方式

### 官方安装

通过 rustup 官方安装脚本：

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

安装后工具存放在 `~/.cargo/bin`，rustup 会自动配置 `PATH`。

### 国内镜像安装

国内网络环境下，推荐通过 [[RsProxy 镜像源配置]] 加速安装和依赖拉取。

## 开发环境

### IDE 配置

推荐使用 [[VS Code Rust 开发环境配置]] 搭建 IDE 开发环境，或使用 [[RustRover 开发环境配置]]（JetBrains 出品的专用 Rust IDE，开箱即用，内置 Cargo 集成和调试器）。

## 包管理

Cargo 提供声明式依赖管理。在 `Cargo.toml` 中添加依赖后自动下载安装：

```toml
[dependencies]
ferris-says = "0.3.2"
```

或使用命令行：

```bash
cargo add ferris-says
```

依赖版本遵循 [[语义化版本]] 规则。Rust 库普遍通过 [[Edition]] 机制管理语言版本兼容性。

## 参考

- [Rust 官网](https://rust-lang.org/)
- [crates.io](https://crates.io/)

## 来源

- [[Rust安装与开发环境配置]]
