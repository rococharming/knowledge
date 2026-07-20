---
title: Rust 安装与镜像源配置
date: 2026-07-20
tags: [rust, toolchain, setup]
source_count: 1
---

# Rust 安装与镜像源配置

Rust 官方推荐使用 [[rustup]] 安装和管理工具链。安装完成后，常用开发入口包括 [[rustc]]、[[Cargo]] 和 `rustdoc`。

## 官方安装路径

进入 Rust 官网安装页面，网站会根据操作系统给出对应安装方案。

![[Image.png|600]]

macOS 或 Linux 常用安装命令：

```shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

安装完成后，重启终端或确认 `~/.cargo/bin` 已加入 `PATH`。验证命令：

```shell
rustup --version
rustc --version
cargo --version
```

![[Image 3.png]]

## 使用 RsProxy 镜像

在网络访问 crates.io 或 Rust 官方分发源不稳定时，可以使用 RsProxy 镜像。素材给出的 macOS/zsh 配置方式是在 `~/.zshrc` 中加入：

```shell
export RUSTUP_DIST_SERVER="https://rsproxy.cn"
export RUSTUP_UPDATE_ROOT="https://rsproxy.cn/rustup"
```

然后重启终端，或执行：

```shell
source ~/.zshrc
```

通过 RsProxy 安装 Rust：

```shell
curl --proto '=https' --tlsv1.2 -sSf https://rsproxy.cn/rustup-init.sh | sh
```

## 配置 crates.io 镜像

编辑 `~/.cargo/config.toml`：

```toml
[source.crates-io]
replace-with = 'rsproxy-sparse'

[source.rsproxy]
registry = "https://rsproxy.cn/crates.io-index"

[source.rsproxy-sparse]
registry = "sparse+https://rsproxy.cn/index/"

[registries.rsproxy]
index = "https://rsproxy.cn/crates.io-index"

[net]
git-fetch-with-cli = true
```

素材建议 Rust `>=1.68` 时优先使用 sparse-index，因为 sparse 协议通常速度更快。

## 验证清单

- `rustup --version` 能显示 rustup 版本。
- `rustc --version` 能显示编译器版本。
- `cargo --version` 能显示 Cargo 版本。
- `rustup show` 能显示当前平台、已安装工具链和当前激活工具链。

## 相关页面

- [[rustup]]
- [[rustc]]
- [[Cargo]]

## 来源

- [[Rust安装与开发环境配置]]
