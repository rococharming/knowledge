---
title: rustc
date: 2026-05-10
tags: [rust, compiler, rustc]
source_count: 2
---

# rustc

## 概述

rustc 是 Rust 官方编译器，用于将 Rust 源程序（`.rs`）编译成目标文件、可执行文件或库。其使用风格类似于 `gcc`。项目开发中通常使用 [[Cargo]] 来构建，但 Cargo 底层实际调用 rustc 完成编译。

## 基本用法

### 编译可执行文件

```bash
rustc main.rs              # 默认生成 main（macOS/Linux）或 main.exe（Windows）
rustc -o hello main.rs     # 指定输出文件名
```

在 macOS / Linux 上默认生成无后缀的可执行文件 `main`，Windows 上生成 `main.exe`。

默认输出：

![[Image 6.png|400]]

指定输出文件名：

![[Image 7.png|400]]

### 指定 Edition

```bash
rustc main.rs --edition=2021
```

[[Edition]] 是 Rust 语言规则的可选版本包，同一 rustc 同时兼容多个 Edition。

## 编译库

rustc 编译库时默认产生 Rust 自用的 **rlib** 格式。

### 编译 rlib 库

创建库源码 `lib.rs`：

```rust
pub fn hello() {
    println!("Hello, world!");
}
```

编译命令：

```bash
rustc --crate-type=rlib --crate-name=greet lib.rs
```

- `--crate-type=rlib`：指定 crate 类型为 rlib
- `--crate-name=greet`：指定 crate 名称为 greet

生成 `libgreet.rlib` 文件：

![[Image 8.png|500]]

### 链接 rlib 到可执行文件

创建可执行文件源码 `main.rs`：

```rust
fn main() {
    greet::hello();
}
```

> `greet` 是 `--crate-name` 指定的 crate 名。

链接并编译：

```bash
rustc -L . --extern greet=libgreet.rlib main.rs
```

- `-L .`：将当前目录作为库路径搜索目录
- `--extern greet=libgreet.rlib`：以 greet 作为 crate 名注入库

执行完成后生成可执行文件：

![[Image 9.png|600]]

## 与 Cargo 的关系

日常开发中直接使用 Cargo：

```bash
cargo build
cargo run
```

Cargo 会自动处理 rustc 的调用参数、依赖链接和 Edition 指定。

## 关联

- [[rustup]] — 管理 rustc 版本的工具链管理器
- [[Cargo]] — 底层调用 rustc 的构建工具
- [[Edition]] — rustc 支持的多版本语言规则机制
