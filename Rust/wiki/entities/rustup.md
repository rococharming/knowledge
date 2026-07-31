---
title: rustup
date: 2026-07-31
tags: [rust, toolchain]
source_count: 1
---

# rustup

`rustup` 是 Rust 官方推荐的工具链管理器，用于安装、更新、切换和卸载 Rust 编译器、标准库及相关组件。通过 `rustup` 安装 Rust 时，通常会安装默认的 `stable` 工具链，并在本机提供 `rustc`、`cargo`、`rustdoc` 等入口。

## 工具链代理入口

安装完成后，`~/.cargo/bin` 下会出现 `rustup`、`rustc`、`cargo` 等命令入口。它们在 `rustup` 管理的环境中通常是代理入口：当执行 `cargo build` 或 `rustc --version` 时，系统先通过 `PATH` 找到这些入口，再由 `rustup` 根据当前目录、环境变量或默认配置选择实际 toolchain。

可以用下面命令查看真实 `cargo` 二进制位置：

```shell
rustup which cargo
```

![[Image 2.png]]

## 发布通道

Rust 工具链主要有三类发布通道：

- `stable`：稳定版本，适合日常开发和生产项目。
- `beta`：下一个稳定版本的候选通道，用于提前测试即将稳定的功能和变更。
- `nightly`：每日构建版本，包含最新语言和编译器成果，但稳定性风险更高。

`rustup show` 可以查看当前平台、已安装工具链和当前激活工具链。

![[Image 5.png|400]]

## 常用命令

```shell
rustup --version
rustup show
rustup update
rustup self update
rustup install stable
rustup install beta
rustup install nightly
rustup default stable
rustup self uninstall
```

`rustup update` 用于更新已安装的 Rust toolchain；在较新的 rustup 行为中，它也会在更新 toolchain 时检查并更新 rustup 自身。

## Windows 工具链选择

Windows 上的 [[rustup]] 默认通常安装 MSVC 工具链，例如 `stable-x86_64-pc-windows-msvc`。MSVC 路线需要 Visual Studio 或 Visual Studio Build Tools 提供链接器和 Windows SDK。

如果项目明确要求 GNU ABI / MinGW 生态，可以安装 GNU 工具链：

```shell
rustup toolchain install stable-gnu
```

临时使用 GNU 工具链时，可以在 Cargo 命令前加工具链前缀：

```shell
cargo +stable-gnu run
```

更完整的 Windows MSVC/GNU 选择与 MinGW-w64 构建工具配置见 [[Windows Rust 工具链选择]]。

## 相关页面

- [[Rust 安装与镜像源配置]]
- [[Windows Rust 工具链选择]]
- [[rustc]]
- [[Cargo]]

## 来源

- [[Rust安装与开发环境配置]]
