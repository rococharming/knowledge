---
title: Cargo.toml 表语法
date: 2026-06-26
tags: [rust, cargo, toml]
source_count: 0
---

# Cargo.toml 表语法

## 核心结论

`[ ]` 和 `[[ ]]` 是 **TOML 规范本身的两种表语法**，并非 Cargo 特有：

- `[name]` 定义一个**表（table）**，同名只能出现一次；
- `[[name]]` 定义一个**表数组（array of tables）**，同名可重复出现，每出现一次向数组追加一个表元素。

之所以 `[[bin]]` 用双括号，正是因为一个 Package 可以有多个二进制 crate（见 [[Package与Crate]]），需要数组来容纳。

## [name] —— 表

含义：定义一个名为 `name` 的表，包含一组键值对。**同名表只能出现一次**，重复写会报错。用于描述"唯一"的配置块。

`Cargo.toml` 中的典型用例（见 [[Package与Crate]]、[[Cargo构建配置]]）：

```toml
[package]          # 整个包的信息，只有一份
name = "hello_cargo"
version = "0.1.0"

[dependencies]     # 依赖列表，只有一份
rand = "0.10.1"

[profile.release]  # release 构建配置，只有一份
debug = true
```

## [[name]] —— 数组表

含义：定义一个名为 `name` 的**数组**，数组每个元素是一个表。**同名 `[[name]]` 可重复出现**，每次追加一个表元素。用于描述"多个同类条目"。

`Cargo.toml` 中的典型用例是 `[[bin]]`：

```toml
[[bin]]
name = "app-linux"
path = "src/main_linux.rs"

[[bin]]
name = "app-mac"
path = "src/main_mac.rs"
```

等价于 TOML 层面的数组：

```toml
bin = [
  { name = "app-linux", path = "src/main_linux.rs" },
  { name = "app-mac",   path = "src/main_mac.rs" },
]
```

## 对照表

| 语法 | TOML 类型 | 可否重复 | Cargo 用途 |
|---|---|---|---|
| `[name]` | 单个表 | 否（同名只能一次） | 唯一配置块：`[package]`、`[dependencies]`、`[profile.*]`、`[features]` |
| `[[name]]` | 表数组 | 是（每次追加一个元素） | 多条目配置：`[[bin]]`、`[[bench]]`、`[[example]]`、`[[test]]` |

## 关键要点

- `[ ]` = 表，`[[ ]]` = 表数组，是 TOML 语法，不是 Cargo 发明的。
- 能写多次的用 `[[ ]]`（如 `[[bin]]`）；只写一次的用 `[ ]`（如 `[package]`）。
- Cargo 中 `[[bin]]`/`[[bench]]`/`[[example]]`/`[[test]]` 用双括号，因为它们各自允许"多个同类目标"。
- 默认入口规则：有 `src/main.rs` 时 Cargo 自动生成一个同名 bin target，无需 `[[bin]]`（见 [[Package与Crate]]）。

## 关联

- [[Cargo构建配置]] — `[profile.*]`、`[package]` 等表的实际用法与构建流程
- [[Package与Crate]] — 多二进制 crate 组织、`src/bin/` 约定与 `cargo run --bin`
- [[Cargo]] — 构建工具与包管理器实体

## 来源

Query 综合归档（2026-06-26），基于 [[Cargo构建配置]]、[[Package与Crate]] 及 TOML 通用规范。
