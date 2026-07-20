---
title: Cargo Feature
date: 2026-07-20
tags: [Rust, 零散知识, Cargo, Feature]
aliases:
  - Cargo Feature
  - Rust Feature
  - features
---

# 一、Feature 的基本概念

Cargo Feature 是 Cargo 提供的 **可选功能开关** 。它允许一个 crate 把部分能力做成可选择启用的模块，而不是默认把所有代码、依赖和编译成本都带进来。

简单来说，Feature 解决的是这个问题：同一个 crate 面向不同使用者时，可能不需要总是启用全部能力。例如 `serde` 只有在启用 `derive` feature 后，才提供常用的 `#[derive(Serialize, Deserialize)]` 派生能力，相关用法见 [[Rust/notes/常用crate/1、serde和serde_json|serde 和 serde_json]]。

# 二、Feature 写在哪里

## 1、依赖方启用 Feature

使用别人 crate 时，通常在 `Cargo.toml` 的依赖配置里启用 feature：

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
tokio = { version = "1", features = ["rt", "macros"] }
```

这里表示：

- `serde` 这个依赖除了默认能力外，还启用 `derive`；
- `tokio` 这个依赖启用 `rt` 和 `macros` 两个可选能力。

也可以用命令添加：

```sh
cargo add serde --features derive
```

## 2、crate 作者声明 Feature

如果自己写库，也可以在当前 crate 的 `Cargo.toml` 中声明 feature：

```toml
[features]
default = ["std"]
std = []
json = ["dep:serde_json"]

[dependencies]
serde_json = { version = "1", optional = true }
```

这里的含义是：

- `default` 表示默认启用哪些 feature；
- `std = []` 表示声明一个叫 `std` 的 feature，但它本身不额外启用其他 feature 或依赖；
- `json = ["dep:serde_json"]` 表示启用 `json` 时，同时启用可选依赖 `serde_json`；
- `optional = true` 表示这个依赖不是默认必需的。

这里的 `std` 只是一个约定俗成的 feature 名。它真正的作用通常体现在代码里的条件编译，例如 `#[cfg(feature = "std")]` 或 `#![cfg_attr(not(feature = "std"), no_std)]`。也就是说，`std = []` 本身只是一个开关名；代码是否根据这个开关启用标准库能力，要看 crate 作者怎么写。

# 三、Feature 如何影响代码

## 1、用 cfg 条件编译

Feature 本质上会转成编译期配置，代码里可以用 `#[cfg(feature = "...")]` 判断某个 feature 是否启用：

```rust
#[cfg(feature = "json")]
pub fn parse_json(input: &str) -> serde_json::Value {
    serde_json::from_str(input).unwrap()
}
```

当 `json` feature 没有启用时，这个函数不会参与编译，因此也不能被调用。

如果需要为同一个 API 提供不同实现，可以配合 `cfg_attr`、`cfg` 模块或多个函数实现。但普通学习和小项目里，先用最直接的 `#[cfg(feature = "...")]` 就够了。

## 2、Feature 是加法开关

Cargo 的 feature 是 **加法模型** ：依赖图里只要有一个地方启用了某个 feature，最终构建这个 crate 时就会启用它。

例如：

```text
app
├── a 依赖 foo，并启用 feature x
└── b 依赖 foo，不启用 feature x
```

最终 `foo` 会带着 `x` 一起编译。Cargo 不会为 `a` 和 `b` 分别编译两个不同 feature 组合的 `foo`。

> 注意：Feature 适合表达“增加能力”，不适合表达互斥选择。不要设计成 `mysql` 和 `postgres` 只能二选一却互相冲突的 feature；如果必须互斥，应在代码里明确给出编译错误或重新设计配置方式。

# 四、default-features

## 1、默认 Feature

很多 crate 会把常用能力放进默认 feature。普通写法会自动启用默认 feature：

```toml
some_crate = "1"
```

这大致等价于：

```toml
some_crate = { version = "1", default-features = true }
```

## 2、关闭默认 Feature

如果只想要最小能力集，可以关闭默认 feature：

```toml
some_crate = { version = "1", default-features = false, features = ["small"] }
```

这在几类场景中常见：

- 做嵌入式或 `no_std` 项目，不想引入标准库相关能力；
- 想减少编译时间和依赖体积；
- 只需要某个 crate 的核心类型或 trait，不需要完整功能。

关闭默认 feature 前要确认文档，因为很多常用 API 可能就定义在默认 feature 里。比如学习 [[Rust/notes/Rust进阶/异步编程/2、Tokio Runtime|Tokio Runtime]] 时，直接启用 `full` 省心；正式项目再按需缩小 feature。

# 五、常见使用场景

| 场景 | Feature 的作用 | 示例 |
|---|---|---|
| 派生宏 | 只在需要宏时启用 | `serde/derive` |
| 运行时能力 | 按模块启用异步、网络、时间等能力 | `tokio/rt`、`tokio/time` |
| 格式支持 | 按需启用 JSON、YAML、TOML 等格式 | `json`、`yaml` |
| 平台能力 | 为不同平台启用不同后端 | `x11`、`wayland` |
| `no_std` | 默认不依赖标准库，需要时再启用 `std` | `std` |

# 六、容易踩的坑

## 1、以为 Feature 只影响当前依赖声明

Feature 会在依赖图中合并，所以它不是“当前这一行依赖独享”的局部开关。理解依赖图可以回到 [[Rust/notes/Rust基础/9、crate与模块|crate 与模块]] 中的 package、crate 和依赖关系。

## 2、乱开 full

`full` feature 通常方便学习或快速验证，但会带来更多依赖和编译成本。应用程序可以为了省事启用 `full`，库 crate 则应该谨慎，因为库的 feature 会传递影响下游使用者。

## 3、把 Feature 当运行时开关

Feature 是编译期选择，不是运行时配置。程序编译完成后，不能通过命令行参数或配置文件临时打开一个未编译进去的 feature。

# 七、小结

Cargo Feature 可以理解为 crate 的“按需装配”机制：

- 使用依赖时，用 `features = [...]` 启用别人提供的能力；
- 写库时，用 `[features]` 和 `optional = true` 把可选能力暴露给使用者；
- 代码中用 `#[cfg(feature = "...")]` 控制条件编译；
- Feature 是加法合并模型，适合增加能力，不适合做互斥配置；
- 默认 feature 可以关闭，但要确认是否会影响常用 API。

日常学习 Rust 时，先记住一句话就够了：**Feature 决定一个 crate 在编译时带上哪些可选能力。**
