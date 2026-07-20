---
title: rustc
date: 2026-07-20
tags: [rust, compiler, toolchain]
source_count: 1
---

# rustc

`rustc` 是 Rust 官方编译器，用于把 `.rs` 源码编译为可执行文件、目标文件或库。它的命令行使用方式类似 `gcc`，但真实项目中通常由 [[Cargo]] 组织构建流程，并在底层调用 `rustc`。

## 基本编译

最小 Rust 程序通常写在 `main.rs`：

```rust
fn main() {
    println!("Hello, world!");
}
```

直接编译：

```shell
rustc main.rs
```

在 macOS 或 Linux 上，默认会生成名为 `main` 的可执行文件；在 Windows 上通常是 `main.exe`。

![[Image 6.png|400]]

指定输出文件名：

```shell
rustc -o hello main.rs
```

![[Image 7.png|400]]

## Edition 选项

`rustc` 可以通过 `--edition` 按指定 [[Rust Edition]] 解析和编译代码：

```shell
rustc main.rs --edition=2021
```

这使同一个编译器能够兼容多个语言规则集合。实际项目通常在 `Cargo.toml` 的 `edition` 字段中声明 Edition，而不是手动为每次 `rustc` 调用指定。

## 相关页面

- [[rustup]]
- [[Cargo]]
- [[Rust Edition]]

## 来源

- [[Rust安装与开发环境配置]]
