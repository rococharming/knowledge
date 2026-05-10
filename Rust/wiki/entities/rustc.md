---
title: "rustc"
date: 2026-05-10
source_count: 1
tags: [rust, compiler, entity]
---

# rustc

## 定义

rustc 是 Rust 官方提供的**编译器**，用于将 Rust 源程序（`.rs`）编译成目标文件、可执行文件或库。它是 Cargo 的底层编译工具，日常使用 Cargo 时通常不直接调用 rustc。

## 关键信息

### 基本用法

```bash
# 编译生成可执行文件（默认 main / main.exe）
rustc main.rs

# 指定输出文件名
rustc -o hello main.rs

# 指定 Edition
rustc main.rs --edition=2021
```

### 编译库

```bash
# 编译 rlib 库
rustc --crate-type=rlib --crate-name=greet lib.rs

# 链接库到可执行文件
rustc -L. --extern greet=libgreet.rlib main.rs
```

### 常用选项

| 选项 | 作用 |
|------|------|
| `-o <name>` | 指定输出文件名 |
| `--edition=<year>` | 指定 Rust Edition（2015/2018/2021/2024） |
| `--crate-type=<type>` | 指定 crate 类型（bin、lib、rlib 等） |
| `--crate-name=<name>` | 指定 crate 名称 |
| `-L <path>` | 添加库搜索路径 |
| `--extern <name>=<path>` | 链接外部库 |

### Edition 机制

Rust 通过 Edition 实现语言规则的版本化管理：
- 同一 rustc 同时兼容多个 Edition
- 旧项目按旧规则编译，新项目可选新规则
- 主要 Edition：2015、2018、2021、2024
- 在 `Cargo.toml` 中通过 `edition` 字段指定

## 相关素材

- [[Rust安装与开发环境配置摘要]]
