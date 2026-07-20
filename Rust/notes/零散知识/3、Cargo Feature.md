---
title: Cargo Feature
date: 2026-07-20
tags: [Rust, Cargo, Feature]
aliases:
  - Cargo Feature
  - Rust Feature
  - Cargo features
---

# 一、Cargo Feature 的基本概念

Cargo feature 是 Cargo 提供的一套 **条件编译与可选依赖管理机制**。它允许一个 crate 暴露若干可启用的能力，让使用者按需选择是否编译相关代码和依赖。

常见用途包括：

- 为库提供可选能力，例如 `serde` 支持、不同图片格式支持、不同 TLS 后端支持。
- 控制可选依赖是否参与编译，减少不必要的依赖和编译成本。
- 用 `#[cfg(feature = "...")]` 对代码进行条件编译。
- 为常见组合提供一个统一开关，例如 `full`、`std`、`default`。

简单来说：

```text
feature = 一个有名字的编译开关
```

启用某个 feature 后，Cargo 会把对应的 `cfg` 信息传给 `rustc`，代码就可以通过 `#[cfg(feature = "...")]` 或 `cfg!(feature = "...")` 判断它是否启用。

# 二、在 `[features]` 中声明功能

## 1、最小 feature

功能特性定义在 `Cargo.toml` 的 `[features]` 表中。每个 feature 对应一个数组，数组中列出启用它时需要同时启用的其他 feature 或可选依赖。

示例：一个二维图像处理库可以选择性支持 WebP：

```toml
[features]
webp = []
```

这里的 `webp = []` 表示：

- 定义一个名为 `webp` 的 feature。
- 启用 `webp` 时，不会额外启用其他 feature 或依赖。

代码中可以这样做条件编译：

```rust
#[cfg(feature = "webp")]
pub mod webp;
```


## 2、feature 启用其他 feature

一个 feature 可以启用其他 feature，用来表达“组合能力”。

例如 ICO 图像中可能包含 BMP 和 PNG 图像，因此启用 ICO 支持时，应当同时启用 BMP 和 PNG 支持：

```toml
[features]
bmp = []
png = []
ico = ["bmp", "png"]
webp = []
```

这里：

```toml
ico = ["bmp", "png"]
```

表示启用 `ico` 时，Cargo 会同时启用 `bmp` 和 `png`。

这种关系适合表达依赖链：

```text
ico
├── bmp
└── png
```

# 三、默认功能特性

## 1、default

默认情况下，用户不显式启用的普通 feature 不会自动打开。但 Cargo 有一个特殊 feature：`default`。

如果在 `[features]` 中定义了 `default`，Cargo 默认构建这个 crate 时会启用它：

```toml
[features]
default = ["ico", "webp"]
bmp = []
png = []
ico = ["bmp", "png"]
webp = []
```

这个配置的启用链是：

```text
default
├── ico
│   ├── bmp
│   └── png
└── webp
```

因此默认构建时，最终会启用：

```text
ico、webp、bmp、png
```

## 2、禁用默认功能

命令行中可以使用：

```shell
cargo build --no-default-features
```

这会禁用当前所选包的默认 feature。

在依赖声明中，也可以禁用某个依赖的默认 feature：

```toml
[dependencies]
some-crate = { version = "1", default-features = false }
```

这表示：使用 `some-crate` 时，不启用它的 `default` feature。

## 3、默认 feature 的取舍

默认 feature 可以让用户开箱即用，不必手动列出常见能力。但它也会带来两个成本：

- 默认依赖更多，编译时间和二进制体积可能增加。
- 依赖图中只要有一个地方没有禁用默认 feature，这个依赖的默认 feature 就可能仍然被启用。

因此，库作者应谨慎决定哪些能力放进 `default`。如果一个能力依赖重、平台受限或容易改变行为，通常不适合默认启用。

# 四、可选依赖项

## 1、`optional = true`

依赖项被标记为 `optional`，表示它默认不会参与编译。

示例：为 GIF 图像支持添加可选依赖：

```toml
[dependencies]
gif = { version = "0.11.1", optional = true }
```

默认情况下，这个可选依赖会隐式创建一个同名 feature，效果近似于：

```toml
[features]
gif = ["dep:gif"]
```

也就是说，只有启用 `gif` feature 时，`gif` 依赖项才会被包含进来：

```shell
cargo build --features gif
```

代码中可以配合条件编译：

```rust
#[cfg(feature = "gif")]
pub mod gif_support;
```

## 2、使用 `dep:` 隐藏内部依赖

有时不希望对外暴露一个与可选依赖同名的 feature，例如：

- 该依赖只是内部实现细节。
- 一个用户可见 feature 需要同时启用多个内部依赖。
- 想为功能提供更语义化的名称。

只要在 `[features]` 表中使用 `dep:` 前缀引用某个可选依赖，Cargo 就不会再为这个依赖自动创建同名 feature。

例如，为 AVIF 图像格式支持启用两个内部依赖：

```toml
[dependencies]
ravif = { version = "0.6.3", optional = true }
rgb = { version = "0.8.25", optional = true }

[features]
avif = ["dep:ravif", "dep:rgb"]
```

这里启用 `avif` 时，会同时启用 `ravif` 和 `rgb`：

```shell
cargo build --features avif
```

但用户不能再单独通过 feature 名称启用 `ravif` 或 `rgb`。对外暴露的是语义清晰的 `avif`，而不是内部依赖名。

# 五、启用依赖项的 feature

Cargo feature 不只用于当前 crate，也可以在依赖声明中启用依赖 crate 提供的 feature。

例如启用 `serde` 的 `derive` feature：

```toml
[dependencies]
serde = { version = "1.0", features = ["derive"] }
```

这里的 `derive` 不是当前包定义的 feature，而是 `serde` crate 提供的 feature。

如果还想禁用依赖的默认 feature，可以同时写：

```toml
[dependencies]
flate2 = { version = "1.0.3", default-features = false, features = ["zlib-rs"] }
```

这表示：

- 不启用 `flate2` 的 `default` feature。
- 额外启用 `flate2` 的 `zlib-rs` feature。

需要注意的是，`default-features = false` 只影响当前这条依赖声明。如果依赖图中的另一个 crate 也依赖 `flate2`，并且没有禁用默认 feature，那么 `flate2` 的默认 feature 仍然可能被启用。

## 1、使用 cargo add 启用依赖 feature

使用 `cargo add` 增加依赖时，也可以直接启用依赖 crate 提供的 feature。

例如启用 `serde` 的 `derive` feature：

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

# 六、Feature 的合并规则

Cargo feature 的一个重要规则是：

> feature 是加法式的。只要依赖图中任何地方启用了某个 feature，它最终就会被启用。

例如：

```toml
[dependencies]
foo = { version = "1", features = ["a"] }
bar = { version = "1" }
```

如果 `bar` 的依赖链中也使用了 `foo`，并启用了 `foo` 的 `b` feature，那么最终编译 `foo` 时可能同时启用：

```text
a + b
```

这意味着 feature 设计时应尽量遵守加法原则：

- 启用 feature 应该增加能力，而不是关闭能力。
- 不要设计互斥 feature，例如 `backend-a` 和 `backend-b` 同时启用就报错的模式。
- 如果必须表达互斥选择，通常应考虑用不同 crate、运行时配置或清晰的编译错误提示。

`default-features = false` 也要放在这个规则下理解：它只能阻止当前依赖声明启用默认 feature，不能阻止依赖图中其他路径重新启用默认 feature。

# 七、命令行常用写法

常见命令如下：

```shell
# 启用单个 feature
cargo build --features webp

# 启用多个 feature
cargo build --features "ico webp"

# 禁用默认 feature
cargo build --no-default-features

# 禁用默认 feature，并启用指定 feature
cargo build --no-default-features --features webp
```

在 workspace 中，如果要为指定包启用 feature，通常需要同时指定包：

```shell
cargo build -p image-lib --features webp
```

如果当前目录只包含单个包，则可以省略 `-p`。

# 八、实践建议

## 1、命名要表达能力，而不是依赖名

如果 feature 是对外 API，优先使用能力名称：

```toml
[features]
json = ["dep:serde", "dep:serde_json"]
```

这比直接暴露 `serde_json` 更稳定，因为以后内部实现可以替换，但对外的 `json` 能力不必改变。

## 2、默认 feature 保持克制

适合放进 `default` 的通常是：

- 大多数用户都会用到的能力。
- 依赖成本低、平台兼容性好的能力。
- 不会显著改变行为的能力。

不适合默认启用的通常是：

- 重依赖或编译很慢的能力。
- 只适用于特定平台的能力。
- 会改变运行时行为或引入额外系统依赖的能力。

## 3、让 feature 保持加法式

一个好的 feature 应该像“打开更多能力”，而不是“关掉另一种能力”。这样依赖图中多个 crate 同时使用你时，feature 合并才不容易出问题。

# 九、小结

Cargo feature 可以从三个层次理解：

| 层次 | 作用 | 示例 |
|---|---|---|
| 当前 crate 的 feature | 控制当前 crate 的条件编译 | `#[cfg(feature = "webp")]` |
| 可选依赖 | 控制依赖是否参与编译 | `gif = { optional = true }` |
| 依赖 crate 的 feature | 启用依赖提供的能力 | `serde = { features = ["derive"] }` |

核心规则如下：

- feature 写在 `Cargo.toml` 的 `[features]` 表中。
- `default` 是特殊 feature，会被默认启用。
- `optional = true` 会让依赖默认不参与编译。
- `dep:` 可以把可选依赖隐藏为内部实现细节。
- 依赖声明中的 `features = [...]` 启用的是依赖 crate 的 feature。
- feature 是加法式合并的，设计时应避免互斥开关。
