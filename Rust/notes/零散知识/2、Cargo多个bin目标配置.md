---
title: Cargo多个bin目标配置
date: 2026-06-26
tags: [Rust, 零散知识, Cargo]
aliases:
  - Cargo多个bin目标配置
---

# 一、概述

通常一个 Cargo 二进制项目默认入口是 `src/main.rs`，Cargo 会自动生成一个与 package 同名的 bin target，无需额外声明。

但当一个项目需要针对不同平台（Linux / macOS / Windows）提供不同入口时，可以**故意不放 `src/main.rs`**，转而在 `Cargo.toml` 中用多个 `[[bin]]` 段显式指定各自的入口文件。

核心结论：

- 没有 `src/main.rs` 时，Cargo 不会自动生成默认 bin target；
- 每个 `[[bin]]` 段通过 `name` 和 `path` 声明一个独立的 bin target；
- 因为存在多个 bin target，运行时必须用 `--bin <name>` 指定具体入口，否则 `cargo run` 会失败。

# 二、默认入口规则

Rust 默认入口规则：如果存在 `src/main.rs`，Cargo 会自动生成一个与 package 同名的 bin target，无需 `[[bin]]` 声明。

也就是说，正常情况下只要把入口写在 `src/main.rs`，`cargo run` 就能直接跑起来。

# 三、显式 \[\[bin\]\] 配置

当项目故意不放 `src/main.rs`，而是用多个 `[[bin]]` 段分别指向不同平台的入口文件时，每个 `path` 指向一个包含 `fn main` 的源文件。

示例配置（`Cargo.toml`）：

```toml
[[bin]]
name = "app-linux"
path = "src/main_linux.rs"

[[bin]]
name = "app-mac"
path = "src/main_mac.rs"

[[bin]]
name = "app-windows"
path = "src/main_windows.rs"
```

这样配置后，Cargo 会识别出三个独立的 bin target，分别对应三个平台入口。

# 四、运行方式

因为该 package 有多个 bin target，运行时必须用 `--bin <name>` 选定具体入口：

```sh
cargo run --bin app-windows
cargo run --bin app-mac
cargo run --bin app-linux
```

如果直接 `cargo run`（不带 `--bin`）会失败，因为这个 package 有多个 bin target，Cargo 不知道该跑哪一个。

# 五、注意事项

多个平台入口分别维护时需要注意：

- 每个入口文件都需要独立的 `fn main`，公共逻辑应抽到 `src/` 下的共享模块中复用，避免三份代码各自演化；
- 平台特定的依赖可用 `[target.'cfg(...)'.dependencies]` 按目标平台条件引入，而不是把所有平台依赖混在一起；
- 可以配合 `cfg` 属性在单一入口内做平台分支，但完全分离的入口文件更适合平台差异巨大的场景。
