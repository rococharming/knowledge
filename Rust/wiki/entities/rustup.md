---
title: "rustup"
date: 2026-05-10
source_count: 1
tags: [rust, toolchain, entity]
---

# rustup

## 定义

rustup 是 Rust 官方提供的**工具链管理器**，用于安装、更新和切换不同的 Rust 编译器及相关工具。

## 关键信息

### 功能

- 安装 Rust 工具链（stable、beta、nightly）
- 管理多个工具链版本并存
- 更新工具链和自身
- 提供 rustc、cargo、rustdoc 等工具的入口（通过软链接机制）

### 安装

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

国内镜像安装：
```bash
curl --proto '=https' --tlsv1.2 -sSf https://rsproxy.cn/rustup-init.sh | sh
```

### 常用命令

| 命令 | 作用 |
|------|------|
| `rustup --version` | 查看 rustup 版本 |
| `rustup self update` | 更新 rustup 自身 |
| `rustup update` | 更新所有工具链 |
| `rustup show` | 显示已安装和当前使用的工具链 |
| `rustup install <toolchain>` | 安装指定工具链 |
| `rustup default <toolchain>` | 切换默认工具链 |
| `rustup which cargo` | 查找真实 cargo 二进制位置 |
| `rustup self uninstall` | 完全卸载 rustup 及所有工具链 |

### 工具链类型

- **stable**：稳定版，每 6 周发布，默认安装
- **beta**：测试版，下一个 stable 的候选，每天更新
- **nightly**：每夜版，包含最新实验特性，可能不稳定

### 工作机制

rustup 通过软链接管理工具调用：
- `~/.cargo/bin/cargo`、`rustc` 等均为指向 `rustup` 的软链接
- 当执行 `cargo build` 时，rustup 读取当前配置，决定使用哪个 toolchian，再调用真实的二进制

## 相关素材

- [[Rust安装与开发环境配置摘要]]
