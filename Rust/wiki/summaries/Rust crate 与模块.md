---
title: Rust crate 与模块
date: 2026-05-20
tags: [rust, cargo, crate, module]
source_count: 1
---

# Rust crate 与模块

本文是对 Rust 项目结构、编译单元与代码组织机制的系统梳理，涵盖 Package/Crate 概念、Cargo 构建配置、模块系统、分文件组织与路径导入五大主题。

## 核心内容概览

### Package 与 Crate

- **Package** 是 Cargo 管理项目的基本单位，对应一个含 `Cargo.toml` 的目录
- **Crate** 是 Rust 的基本编译单元，分为库 crate（`src/lib.rs`）和二进制 crate（`src/main.rs`）
- 一个 Package 最多包含一个库 crate，但可包含多个二进制 crate（`src/main.rs` + `src/bin/` 下各文件）
- 依赖分为直接依赖和传递依赖，共同构成项目的**依赖图**

详见 [[Package与Crate]]。

### Cargo 构建与配置

- Cargo 负责项目管理，底层调用 `rustc` 执行编译
- 构建流程：读取配置 → 解析依赖图 → 下载源码 → 按顺序编译 crate → 输出到 `target/`
- `cargo build` 使用 dev profile（编译快、保留调试信息），`cargo build --release` 使用 release profile（优化充分、运行快）
- 可通过 `[profile.dev]` / `[profile.release]` 自定义构建行为
- `cargo fix --edition` 可自动修复 Edition 迁移中的兼容性问题

详见 [[Cargo构建配置]]、[[Edition]]。

### 模块系统

- **模块（module）** 是 crate 内部组织代码的方式，承担**命名空间管理**和**可见性管理**两个核心作用
- 未标记 `pub` 的语法项默认私有，私有项可被定义模块及其子模块访问
- 可见性修饰符：`pub`（完全公开）、`pub(crate)`（crate 内可见）、`pub(super)`（父模块可见）、`pub(in path)`（指定路径可见）
- 嵌套模块可按领域划分代码层级

详见 [[模块系统]]。

### 模块文件组织

- `mod shop;` 声明让编译器从对应文件加载模块内容
- 单文件模块：`src/shop.rs`
- 目录模块：`src/shop/mod.rs` + 子模块文件
- 现代方式：`src/shop.rs` + `src/shop/` 目录共存

详见 [[模块文件组织]]。

### 路径与导入

- 路径使用 `::` 分隔，`self` 表示当前模块，`super` 表示父模块，`crate` 表示 crate 根
- `use` 将路径引入当前作用域，支持合并导入 `{A, B}`、`as` 重命名、通配导入 `*`
- `pub use` 实现**重导出**，将外部路径作为当前模块的公开项重新暴露
- 父模块的 `use` 不会自动继承到子模块
- 标准库 `std::prelude::v1::*` 自动导入到每个模块

详见 [[路径与导入]]。

## 关联页面

- [[Cargo]] — Cargo 工具实体概览
- [[rustup]] — 工具链管理器
- [[rustc]] — Rust 编译器
- [[Edition]] — 语言规则版本机制
- [[语义化版本]] — 依赖版本解析规则

## 来源

- [[crate与模块]]
