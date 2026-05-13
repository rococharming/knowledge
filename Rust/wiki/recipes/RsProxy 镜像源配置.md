---
title: RsProxy 镜像源配置
date: 2026-05-10
tags: [rust, mirror, setup, china]
source_count: 1
---

# RsProxy 镜像源配置

## 问题

国内访问 Rust 官方源和 crates.io 可能存在网络不稳定问题，导致 rustup 安装失败或 cargo 依赖下载缓慢。

## 方案

使用 [RsProxy](https://rsproxy.cn/) 国内镜像代理加速 Rust 工具链安装和 crates 下载。

## 前置条件

- 已安装 curl
- 有写入 `~/.bashrc` 或 `~/.zshrc` 的权限

## 步骤

### 步骤 1：设置 rustup 镜像环境变量

编辑 shell 配置文件：

**bash：**
```bash
echo 'export RUSTUP_DIST_SERVER="https://rsproxy.cn"' >> ~/.bashrc
echo 'export RUSTUP_UPDATE_ROOT="https://rsproxy.cn/rustup"' >> ~/.bashrc
source ~/.bashrc
```

**zsh：**
```bash
echo 'export RUSTUP_DIST_SERVER="https://rsproxy.cn"' >> ~/.zshrc
echo 'export RUSTUP_UPDATE_ROOT="https://rsproxy.cn/rustup"' >> ~/.zshrc
source ~/.zshrc
```

### 步骤 2：通过 RsProxy 安装 Rust

```bash
curl --proto '=https' --tlsv1.2 -sSf https://rsproxy.cn/rustup-init.sh | sh
```

### 步骤 3：配置 crates.io 镜像

创建或编辑 `~/.cargo/config.toml`：

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

> Rust >= 1.68 版本建议使用 `sparse-index` 协议，速度更快。

## 验证

```bash
rustup --version
cargo new test_project && cd test_project && cargo build
```

如果 cargo build 能正常下载依赖并编译，说明镜像配置成功。

## 关联

- [[rustup]] — 通过 RsProxy 加速安装的 Rust 工具链管理器
- [[Cargo]] — 通过镜像加速依赖下载的包管理工具

## 来源

- [[Rust安装与开发环境配置]]
