---
title: Cargo 构建配置
date: 2026-05-20
tags: [rust, cargo, build, profile]
source_count: 1
---

# Cargo 构建配置

## Cargo 与 rustc 的关系

Cargo 是 Rust 的**项目管理工具**，负责项目结构、依赖解析、构建流程编排。真正执行编译的是 `rustc`。

`cargo build` 的构建流程：

1. 读取 `Cargo.toml`
2. 更新依赖索引
3. 解析依赖图
4. 下载缺失的依赖源码
5. 按依赖顺序编译各个 crate
6. 最后编译当前项目
7. 输出构建产物到 `target/`

查看详细构建过程：

```bash
cargo build --verbose
```

编译库 crate 时，`rustc` 生成 `.rlib` 文件，其中包含编译后的代码和类型检查、泛型实例化、Trait 检查所需的元数据。编译二进制 crate 时，生成最终可执行文件。

Cargo 通过 `--extern crate名=库产物路径` 参数将依赖信息传递给 `rustc`。

## dev 与 release 构建

| 特性 | `cargo build` (dev) | `cargo build --release` (release) |
|---|---|---|
| Profile | `[profile.dev]` | `[profile.release]` |
| 编译速度 | 快 | 慢 |
| 运行性能 | 一般 | 高（充分优化） |
| 调试信息 | 完整 | 较少 |
| `debug_assert!` | 生效 | 默认不生效 |
| 整型溢出 | 触发检查并 panic | 二进制补码回绕 |

## Profile 配置

`Cargo.toml` 中可配置不同构建模式的行为：

```toml
[profile.dev]

[profile.release]

[profile.test]
```

常用覆盖：在 release 构建中保留调试符号，用于性能剖析：

```toml
[profile.release]
debug = true
```

## Edition 迁移

升级 Edition 时，推荐先使用自动迁移工具：

```bash
cargo fix --edition
```

这条命令尝试把代码改成同时兼容当前 Edition 和下一个 Edition 的写法。完成后修改 `Cargo.toml` 中的 `edition` 字段，再运行：

```bash
cargo check
cargo test
```

> `cargo fix` 只处理编译器能明确判断的问题，业务逻辑和 API 变更仍需人工检查。

## 关联

- [[Cargo]] — Cargo 工具实体概览
- [[Edition]] — 语言规则版本与迁移
- [[Package与Crate]] — 编译单元与项目结构
- [[Cargo.toml 表语法]] — `[ ]` 表与 `[[ ]]` 数组表的区别
- [[rustc]] — Rust 编译器

## 来源

- [[crate与模块]]
