---
title: rustup
date: 2026-05-10
tags: [rust, toolchain, rustup]
source_count: 2
---

# rustup

## 概述

rustup 是 Rust 官方提供的**工具链管理器**，用于安装、更新和切换不同的 Rust 编译器及相关工具。安装 rustup 时会一并安装 rustc、cargo、rustdoc 等核心工具。

## 安装

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

安装完成后，工具存放在 `~/.cargo/bin` 目录下。rustup 会自动将该目录加入 `PATH`。

## 核心命令

| 命令 | 作用 |
|---|---|
| `rustup --version` | 查看 rustup 版本（同时显示 rustc 版本） |
| `rustup self update` | 更新 rustup 自身 |
| `rustup update` | 更新所有已安装的 Rust 工具链，同时自动检查并更新 rustup 自身 |
| `rustup self uninstall` | 完全卸载 rustup 及管理的所有工具链 |
| `rustup show` | 显示已安装工具链和当前活跃工具链 |
| `rustup install stable/beta/nightly` | 安装指定版本工具链 |
| `rustup default stable/beta/nightly` | 切换默认工具链 |
| `rustup which cargo` | 查找真实 cargo 二进制的位置 |

## 工具链版本

rustup 管理三种工具链版本：

- **stable**：稳定版，每 6 周发布一次，默认安装，最稳定可靠
- **beta**：测试版，即将成为下一个 stable 的候选版本，每天更新
- **nightly**：每夜版，每天构建，包含最新实验性特性，可能不稳定

## 工作原理

rustup 通过软链接机制管理工具调用：`~/.cargo/bin/cargo` 等命令实际都是指向 `~/.cargo/bin/rustup` 的软链接。当执行 `cargo build` 时，rustup 读取当前环境配置，决定使用哪个 toolchains，再调用其中的真实二进制。

## 关联

- [[rustc]] — rustup 管理的 Rust 编译器
- [[Cargo]] — rustup 管理的构建和包管理工具
- [[RsProxy 镜像源配置]] — 国内环境下的 rustup 加速配置
