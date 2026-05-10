---
title: "Rust开发环境配置"
date: 2026-05-10
source_count: 1
tags: [rust, setup, recipe, ide]
---

# Rust开发环境配置

## 前置条件

- macOS / Linux / Windows 系统
- 网络连接（或使用国内镜像）
- 终端（Shell）访问权限

## 步骤

### 1. 安装 rustup 和 Rust 工具链

**标准安装（国际网络）：**

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

**国内镜像安装（推荐）：**

配置环境变量（bash 修改 `~/.bashrc`，zsh 修改 `~/.zshrc`）：

```bash
export RUSTUP_DIST_SERVER="https://rsproxy.cn"
export RUSTUP_UPDATE_ROOT="https://rsproxy.cn/rustup"
```

执行安装：

```bash
curl --proto '=https' --tlsv1.2 -sSf https://rsproxy.cn/rustup-init.sh | sh
```

### 2. 配置 crates.io 镜像

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

> 注：`sparse+` 协议需要 Rust >= 1.68，速度更快。

### 3. 验证安装

```bash
rustup --version
rustc --version
cargo --version
```

### 4. 配置 VS Code 开发环境

1. 在 Cargo 项目目录执行 `code .` 打开项目
2. 安装插件：
   - **rust-analyzer**：代码补全、类型推导、错误提示
   - **Error Lens**：将错误和警告内嵌显示在代码中
3. 编写代码时自动获得代码提示
4. 点击 main 函数上方的 **Run** 按钮直接运行
5. 点击 **Debug** 进入调试模式

### 5. 创建第一个项目

```bash
# 创建二进制项目
cargo new hello_rust
cd hello_rust

# 构建并运行
cargo run
```

## 相关素材

- [[Rust安装与开发环境配置摘要]]
- [[rustup]]
- [[Cargo]]
