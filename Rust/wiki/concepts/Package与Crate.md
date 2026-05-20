---
title: Package 与 Crate
date: 2026-05-20
tags: [rust, cargo, package, crate]
source_count: 1
---

# Package 与 Crate

## Package

**Package** 是 Cargo 管理项目的基本单位，对应一个包含 `Cargo.toml` 配置文件的目录。

```
hello_cargo/
├── Cargo.toml
└── src/
    └── main.rs
```

`Cargo.toml` 描述包信息、依赖和构建配置：

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
rand = "0.10.1"
```

创建命令：

```bash
cargo new hello_cargo      # 二进制项目
cargo new --lib my_lib     # 库项目
```

## Crate

**Crate** 是 Rust 的基本编译单元，编译产物分为两类：

| 类型 | 入口文件 | 产物 |
|---|---|---|
| 库 crate | `src/lib.rs` | 库文件（`.rlib` 等），供其他代码调用 |
| 二进制 crate | `src/main.rs` | 可执行文件 |

## Package 与 Crate 的关系

> 一个 Package 可以包含一个或多个 Crate。

Cargo 的限制规则：

- 一个 Package **最多只能有一个库 crate**
- 一个 Package **可以有多个二进制 crate**
- 一个 Package **至少有一个 crate**

### 同时包含库与二进制

```
my_app/
├── Cargo.toml
└── src/
    ├── lib.rs
    └── main.rs
```

`main.rs` 可调用当前 Package 中库 crate 暴露的代码。

### 多个二进制 crate

除 `src/main.rs` 外，可在 `src/bin/` 下放置多个入口文件：

```
my_tools/
├── Cargo.toml
└── src/
    ├── main.rs          # -> 二进制名：my_tools
    └── bin/
        ├── server.rs    # -> 二进制名：server
        └── client.rs    # -> 二进制名：client
```

运行指定二进制：

```bash
cargo run --bin server
cargo run --bin client
```

## 依赖图

项目依赖分为：

- **直接依赖**：`Cargo.toml` 中显式列出的依赖
- **传递依赖**：依赖的 crate 所依赖的其他 crate

所有依赖共同构成**依赖图**，Cargo 按依赖顺序编译（先编译被依赖的 crate，再编译依赖它们的 crate）。

```bash
cargo tree    # 查看依赖树
```

## 关联

- [[Cargo]] — 构建工具和包管理器
- [[Cargo构建配置]] — 构建流程与 profile 配置
- [[Edition]] — `Cargo.toml` 中的语言规则版本
- [[语义化版本]] — 依赖版本解析规则

## 来源

- [[crate与模块]]
