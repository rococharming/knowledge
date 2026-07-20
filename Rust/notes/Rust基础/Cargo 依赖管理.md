---
title: Cargo 依赖管理
date: 2026-07-20
tags: [Rust, Rust基础, Cargo]
aliases:
  - Cargo依赖管理
  - Cargo 包管理
---

# 一、Cargo 依赖管理概述

`Cargo` 不只是 Rust 的构建工具，也是 Rust 的包管理工具。

在 Rust 中，一个可复用的代码包通常称为 `crate`。开发者可以把自己的 crate 发布到 [crates.io](https://crates.io/)，其他项目则可以通过 Cargo 引入并使用这些 crate。

Cargo 的依赖管理主要围绕两个文件展开：

- `Cargo.toml`：项目配置文件，用于声明项目的基本信息和依赖关系。例如项目名称、版本、Edition，以及需要使用哪些第三方 crate。
- `Cargo.lock`：Cargo 自动生成的依赖锁定文件，用于记录当前项目实际解析出来的精确依赖版本。它可以保证项目在不同机器上构建时尽量使用同一组依赖版本。

通常来说，开发者主要手动编辑的是 `Cargo.toml`，而 `Cargo.lock` 由 Cargo 自动生成和维护，一般不需要手动修改。

# 二、增加依赖

假如现在想在项目中使用随机数，可以添加 `rand` crate。在 [crates.io](https://crates.io/) 中搜索 `rand` 后，可以把依赖写入 `Cargo.toml`：

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
rand = "0.10.1"
```

保存 `Cargo.toml` 后，Cargo 会在后续执行构建命令时自动解析并下载依赖，例如执行：

```shell
cargo build
```

依赖下载后，相关 crate 的源码默认会缓存到用户家目录下的 `.cargo` 目录中，例如 `~/.cargo/registry/src/`。如果配置了镜像源，例如 rsproxy，那么上层目录名可能会显示为对应镜像源或索引地址相关的名称。这是 Cargo 的正常缓存机制。

添加依赖后，可以在代码中使用 `rand`：

```rust
use rand::RngExt;

fn main() {
    let number = rand::rng().random_range(1..=10);
    println!("随机数是： {}", number);
}
```

# 三、Cargo.lock

添加依赖并构建后，项目目录下通常会多出一个 `Cargo.lock` 文件。该文件用于记录当前项目实际使用到的所有 crate 版本及其依赖版本，由 Cargo 自动生成和管理。

`Cargo.toml` 记录的是“你希望使用什么依赖”，而 `Cargo.lock` 记录的是“Cargo 实际解析出了哪些精确版本”。

例如，项目依赖 A、B 两个库，而 A 和 B 又都依赖 C。Cargo 会根据版本规则选择一个合适的 C 版本，并把最终解析结果写入 `Cargo.lock`。

这样做的好处是：只要提交了 `Cargo.lock`，别人再次构建项目时，就会尽量使用同一组依赖版本，从而提高构建结果的一致性和可复现性。

对于二进制应用项目，建议提交 `Cargo.lock`。

对于库项目，是否提交 `Cargo.lock` 要看项目习惯和使用场景；如果是发布到 crates.io 的库，最终使用者主要根据 `Cargo.toml` 重新解析依赖。

# 四、cargo add

除了手动修改 `Cargo.toml` 添加依赖外，也可以在命令行中使用 `cargo add` 命令添加依赖。

`cargo add` 是 Cargo 的依赖管理命令之一，用于将依赖添加到 `Cargo.toml` 的 `[dependencies]`、`[dev-dependencies]` 或 `[build-dependencies]` 等依赖区域中，并更新 `Cargo.lock` 文件。

## 1、基本使用

例如添加 `rand`：

```shell
cargo add rand
```

执行后，Cargo 会自动在 `Cargo.toml` 的 `[dependencies]` 中添加类似内容：

```toml
[dependencies]
rand = "0.10.1"
```

具体版本号会根据当前 crates.io 上的最新版本而变化。同时，Cargo 也会更新 `Cargo.lock`，记录实际解析出来的依赖版本。

## 2、指定版本

可以使用 `crate@version` 的形式指定版本要求。`cargo add` 支持使用 `crate@version` 从 registry 添加指定版本约束的依赖。

```shell
cargo add rand@0.10.1
```

这会在 `Cargo.toml` 中添加类似内容：

```toml
[dependencies]
rand = "0.10.1"
```

需要注意，这里的 `"0.10.1"` 在 Cargo 中默认是 caret requirement，也就是兼容版本要求，不是绝对固定到 `0.10.1`。

如果想写成精确的版本，可以使用：

```shell
cargo add rand@=0.10.1
```

对应 `Cargo.toml` 类似：

```toml
[dependencies]
rand = "=0.10.1"
```

## 3、语义化版本范围

Cargo 支持多种版本要求写法，最常见的是 caret requirement 和 tilde requirement。

caret requirement 示例：

```shell
cargo add serde@^1.0
```

一般来说，`^1.2.3` 表示 `>=1.2.3, <2.0.0`。

对于 `0.x` 版本，规则更保守：

- `^0.3.5` 表示 `>=0.3.5, <0.4.0`
- `^0.0.5` 表示 `>=0.0.5, <0.0.6`

大多数情况下使用 caret requirement，例如 `"1.2.3"` 这种默认就是 `^1.2.3`，因为这样既保持兼容性，又给依赖解析器保留足够灵活性。

tilde requirement 示例：

```shell
cargo add serde@~1.0
```

`~` 表示允许较小范围内的版本更新。`~1.2.3` 表示 `>=1.2.3, <1.3.0`，`~1.2` 表示 `>=1.2.0, <1.3.0`，`~1` 表示 `>=1.0.0, <2.0.0`。

# 五、依赖类型

## 1、普通依赖

默认情况下，`cargo add` 会把依赖添加到 `[dependencies]`：

```shell
cargo add anyhow
```

普通依赖会参与项目的正常构建，是库或二进制程序运行时通常需要的依赖。

## 2、开发依赖

开发依赖主要用于测试、基准测试、示例等开发阶段场景：

```shell
cargo add pretty_assertions --dev
```

它会添加到：

```toml
[dev-dependencies]
pretty_assertions = "..."
```

开发依赖的典型使用场景包括：

- `cargo test`
- `cargo bench`

正常的 `cargo build` / `cargo run` 不会把这些依赖作为普通运行依赖带上。

## 3、构建依赖

构建依赖通常供 `build.rs` 构建脚本使用：

```shell
cargo add cc --build
```

它会添加到：

```toml
[build-dependencies]
cc = "..."
```

Cargo 支持在编译 crate 之前先运行构建脚本 `build.rs`，用于做一些编译前准备工作，例如：

- 编译 C/C++ 代码并链接进 Rust。
- 自动生成 Rust 代码，例如从 proto / IDL / 模板生成。
- 检测系统库是否存在。
- 读取环境变量。
- 决定链接参数。

构建脚本属于偏工程化的内容，入门阶段了解它和 `[build-dependencies]` 的关系即可。

# 六、启用依赖 feature

很多 crate 会通过 feature 提供可选能力。使用 `cargo add` 增加依赖时，也可以顺手启用 feature：

```shell
cargo add serde --features derive
```

对应的 `Cargo.toml` 通常类似：

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
```

如果要同时启用多个 feature，可以用逗号分隔：

```shell
cargo add tokio --features rt-multi-thread,macros
```

对应的 `Cargo.toml` 类似：

```toml
[dependencies]
tokio = { version = "1", features = ["rt-multi-thread", "macros"] }
```

feature 的设计和合并规则见 [[Cargo Feature]]。

# 七、cargo remove

使用 `cargo remove` 可以从 `Cargo.toml` 中移除依赖，并支持 `--dev`、`--build` 等选项。

移除普通依赖：

```shell
cargo remove serde
```

移除开发依赖：

```shell
cargo remove --dev pretty_assertions
```

移除构建依赖：

```shell
cargo remove --build cc
```
