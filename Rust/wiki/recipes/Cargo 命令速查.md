---
title: Cargo 命令速查
date: 2026-05-10
tags: [rust, cargo, cheatsheet]
source_count: 1
---

# Cargo 命令速查

## 项目创建

| 命令 | 作用 |
|---|---|
| `cargo new <name>` | 创建二进制可执行项目 |
| `cargo new --lib <name>` | 创建库项目 |
| `cargo new --vcs=none <name>` | 创建项目但不初始化 Git |

## 构建与运行

| 命令 | 作用 |
|---|---|
| `cargo build` | 调试构建，输出到 `target/debug/` |
| `cargo build --release` | 发布构建，输出到 `target/release/` |
| `cargo run` | 构建并运行 |
| `cargo run --release` | 发布构建并运行 |
| `cargo check` | 检查代码是否可编译（类型检查、借用检查，不生成产物，速度最快） |
| `cargo clean` | 清理构建产物（删除 `target/`） |

## 测试与文档

| 命令 | 作用 |
|---|---|
| `cargo test` | 运行测试 |
| `cargo doc` | 构建项目文档（含 `rustdoc`） |

## 依赖管理

| 命令 | 作用 |
|---|---|
| `cargo add <crate>` | 添加最新版本依赖 |
| `cargo add <crate>@<version>` | 添加指定版本 |
| `cargo add <crate>@^<major>` | 按语义化版本范围添加 |
| `cargo add <crate> --features <f1>,<f2>` | 添加依赖并启用 features |
| `cargo add <crate> --dev` | 添加开发依赖（`[dev-dependencies]`） |
| `cargo add <crate> --build` | 添加构建依赖（`[build-dependencies]`） |
| `cargo remove <crate>` | 移除依赖 |
| `cargo remove <crate> --dev` | 移除开发依赖 |
| `cargo remove <crate> --build` | 移除构建依赖 |

## 构建模式对比

| 模式 | 优化级别 | 编译速度 | 文件大小 | 运行速度 | 调试符号 |
|---|---|---|---|---|---|
| Debug（默认） | `opt-level=0` | 快 | 大 | 慢 | 完整 |
| Release | `opt-level=3` | 慢 | 小 | 快 | 较少 |

## 关键提示

- **`cargo check`** 是开发中最常用的命令，执行类型检查、借用检查等编译检查工作，但不生成最终可执行文件，速度远快于 `cargo build`。开发过程中可频繁使用以快速发现编译错误。
- **Release 模式**适合生产部署，但编译时间长，日常开发用 Debug 模式即可。
- **`cargo add/remove`** 会自动修改 `Cargo.toml`，无需手动编辑。
- **`Cargo.lock`** 锁定依赖精确版本，多人协作时应提交到版本控制。

## 关联页面

- [[Cargo]] — Cargo 完整功能介绍
- [[语义化版本]] — 版本号解析规则
- [[RsProxy 镜像源配置]] — 国内环境加速配置

## 来源

- [[Rust安装与开发环境配置]]
