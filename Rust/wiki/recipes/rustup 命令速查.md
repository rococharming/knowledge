---
title: rustup 命令速查
date: 2026-05-11
tags: [rust, rustup, toolchain, recipe]
source_count: 3
---

# rustup 命令速查

## 安装与卸载

| 命令 | 作用 |
|---|---|
| `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \| sh` | 官方安装脚本 |
| `rustup self update` | 更新 rustup 自身 |
| `rustup self uninstall` | 完全卸载 rustup 及管理的所有工具链 |

安装后工具存放在 `~/.cargo/bin`，rustup 自动配置 `PATH`。

## 工具链管理

| 命令 | 作用 |
|---|---|
| `rustup install stable` | 安装稳定版工具链 |
| `rustup install beta` | 安装测试版工具链 |
| `rustup install nightly` | 安装每夜版工具链 |
| `rustup update` | 更新所有已安装的工具链，同时自动检查并更新 rustup 自身 |
| `rustup default stable` | 切换默认工具链为 stable |
| `rustup default nightly` | 切换默认工具链为 nightly |
| `rustup show` | 显示已安装工具链和当前活跃工具链 |
| `rustup which cargo` | 查找真实 cargo 二进制的位置 |
| `rustup --version` | 查看 rustup 和 rustc 版本 |

`rustup --version` 输出示例（同时显示 rustc 版本）：

![[Image 4.png]]

`rustup show` 输出示例（当前目标平台、已安装的工具链、当前活跃工具链）：

![[Image 5.png|400]]

## 工具链版本说明

- **stable**：稳定版，每 6 周发布，默认安装，最可靠
- **beta**：测试版，即将成为下一个 stable 的候选版本，每天更新
- **nightly**：每夜版，每天构建，包含最新实验性特性，可能不稳定

## 国内加速

国内网络环境下，推荐配置 RsProxy 镜像源加速安装和依赖下载，详见 [[RsProxy 镜像源配置]]。

## 工作原理

`~/.cargo/bin/cargo` 等命令实际都是指向 `~/.cargo/bin/rustup` 的软链接。执行命令时 rustup 读取当前环境配置，决定调用哪个工具链中的真实二进制。

## 相关页面

- [[rustup]] — 工具链管理器完整说明
- [[Rust 安装与开发环境配置]] — 开发环境搭建指南
- [[RsProxy 镜像源配置]] — 国内镜像加速配置
