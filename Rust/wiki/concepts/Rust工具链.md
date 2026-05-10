---
title: "Rust工具链"
date: 2026-05-10
source_count: 1
tags: [rust, toolchain, concept]
---

# Rust工具链

## 定义

Rust 工具链是由 [[rustup]] 管理的一组相关工具的集合，包括 [[rustc]] 编译器、[[Cargo]] 构建工具、rustdoc 文档工具等。不同版本的工具链可以并存，通过 rustup 灵活切换。

## 关键信息

### 工具链组成

一个完整的 Rust 工具链包含：
- **rustc**：Rust 编译器
- **cargo**：构建和包管理工具
- **rustdoc**：文档生成工具
- **其他组件**：clippy（静态分析）、rustfmt（格式化）等

### 工具链类型

| 类型 | 更新频率 | 稳定性 | 适用场景 |
|------|---------|--------|---------|
| **stable** | 每 6 周 | 最高 | 生产环境、日常开发 |
| **beta** | 每天 | 较高 | 提前适配即将发布的新特性 |
| **nightly** | 每天 | 实验性 | 尝试最新不稳定特性 |

### 工具链管理

```bash
# 查看当前工具链
rustup show

# 安装其他版本
rustup install nightly
rustup install beta

# 切换默认工具链
rustup default nightly

# 更新所有工具链
rustup update
```

### 安装路径

工具链安装在 `~/.rustup/toolchains/` 下，每个版本一个目录。rustup 通过 `~/.cargo/bin` 中的软链接将用户调用路由到当前默认工具链的实际二进制。

## 相关素材

- [[Rust安装与开发环境配置摘要]]
