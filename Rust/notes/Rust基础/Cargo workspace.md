---
title: Cargo workspace
date: 2026-05-28
tags: [Rust, Rust基础, Cargo]
aliases:
  - Cargo workspace
  - Cargoworkspace
---

# 一、基本概念

Cargo workspace 用来管理多个相关的 Rust package。这些 package 处于同一个工作空间，可以共享`Cargo.lock`和同一个构建输出目录。默认输出目录是 workspace 根目录下的`target/`。

需要先区分几个概念：

| 概念                 | 含义                                  |
| ------------------ | ----------------------------------- |
| `package`          | 一个包含 `Cargo.toml` 的 Cargo 包         |
| `crate`            | Rust 的编译单元，可以是库 crate，也可以是二进制 crate |
| `workspace member` | 被纳入同一个 workspace 管理的 package        |
| `workspace root`   | 包含顶层 `[workspace]` 配置的目录            |

Cargo workspace管理的是package。

一个package可以包含一个库 crate，也可以包含一个或多个二进制 crate。


# 二、Workspace 基本结构

下面使用一个简单项目说明 workspace 的结构。

项目名为 add，里面包含：

- adder：二进制package，作为程序入口
- add-one：库package，提供add_one()函数
- add-two：库package，提供add_two()函数

目录结构可以设计成这样：

```shell
add/
├── Cargo.toml
├── Cargo.lock
├── target/
├── adder/
│   ├── Cargo.toml
│   └── src/
│       └── main.rs
├── add-one/
│   ├── Cargo.toml
│   └── src/
│       └── lib.rs
└── add-two/
    ├── Cargo.toml
    └── src/
        └── lib.rs
```

顶层 `Cargo.toml` 只负责声明`workspace`：

```toml
[workspace]
resolver = "3"
members = [
    "adder",
    "add-one",
    "add-two",
]
```

- `members`用来声明哪些package属于当前workspace。
- `resolver = "3"`用来指令依赖解析器版本。`Cargo.toml`会根据`[package]`中的`edition`推断默认依赖解析器版本，如果Workspace无`[package]`，则需要在`[workspace]`中显式指定。

# 三、Root Package 和 Virtual Manifest

Workspace根目录的`Cargo.toml`有两种常见形式：**Root Package**和**Virtual Manifest**。

## 1、Root Package

如果根`Cargo.toml`同时包含`[package]`和`[workspace]`，那么根目录本身也是一个`package`。

```toml
[package]
name = "my-app"
version = "0.1.0"
edition = "2024"

[workspace]
members = [
    "crates/core",
    "crates/utils",
]
```

**这种结构适合根目录本身就是主程序，同时还包含一些内部库的项目**。

## 2、Virtual Manifest

如果根 `Cargo.toml` 只有 `[workspace]`，没有 `[package]`，它就是一个虚拟清单。

```toml
[workspace]
resolver = "3"
members = [
    "adder",
    "add-one",
    "add-two",
]
```

这种结构适合根目录只负责组织多个成员 package，本身不参与编译。前面的 `add` 示例就属于这种形式。

虚拟 workspace 中，具体代码都放在成员目录里，根目录只保留 workspace 配置、`Cargo.lock` 和 `target/`。

# 四、创建Workspace

## 1、创建 workspace 根目录

先创建 workspace 根目录：

```shell
mkdir add
cd add
```

在 `add/` 目录下创建顶层 `Cargo.toml`：

```toml
[workspace]
resolver = "3"
```


## 2、创建二进制package

创建 workspace 的第一个成员：二进制 package：

```shell
cargo new adder
```

执行后，会在 workspace 的根目录的`Cargo.toml`自动增加成员：

```toml
[workspace]
resolver = "3"
members = ["adder"]
```

此时目录结构如下：

```shell
add/
├── Cargo.toml
└── adder/
    ├── Cargo.toml
    └── src/
        └── main.rs
```

在 workspace 根目录运行：

```shell
cargo build
```

构建后会生成：

```shell
add/
├── Cargo.lock
├── Cargo.toml
├── target/
└── adder/
    ├── Cargo.toml
    └── src/
        └── main.rs
```

可以看到，`Cargo.lock` 和 `target/` 都在 workspace 根目录，而不是在 `adder/` 目录中。

## 3、增加库package

继续在 workspace 中添加库 package：

```shell
cargo new add-one --lib
```

顶层 `Cargo.toml` 会被自动修改为：

```toml
[workspace]
resolver = "3"
members = [
    "adder",
    "add-one",
]
```

目录结构变为：

```shell
add/
├── Cargo.toml
├── Cargo.lock
├── target/
├── adder/
│   ├── Cargo.toml
│   └── src/
│       └── main.rs
└── add-one/
    ├── Cargo.toml
    └── src/
        └── lib.rs
```

在 `add-one/src/lib.rs` 中写一个简单函数：

```rust
pub fn add_one(x: i32) -> i32 {  
	x + 1  
}
```

此时，`add-one` 只是 workspace 中的一个成员。它不会自动被 `adder` 使用。

按照同样的方式添加第二个库`package`：`add-two`。

## 4、成员之间的依赖关系

**Workspace 只表示这些 package 被统一管理，不代表它们之间自动相互依赖**。

如果`adder`要使用`add-one`和`add-two`，必须在`adder/Cargo.toml`中显式声明路径依赖：

```toml
[dependencies]
add-one = { path = "../add-one" }
add-two = { path = "../add-two" }
```

这里有个命名细节：package名可以是add-one，Rust代码中引用crate时使用`add_one`。

> crate 名在代码中会把连字符 `-` 转成下划线 `_`。

在 `adder/src/main.rs` 中调用：

```rust
fn main() {
    let num = 10;

    println!(
        "Hello, world! {num} plus one is {}!",
        add_one::add_one(num)
    );
    
     println!(
        "Hello, world! {num} plus two is {}!",
        add_two::add_two(num)
    );
}
```

在 workspace 根目录构建：

```shell
cargo build
```

Cargo 会先编译 `add-one`和`add-two`，再编译依赖它的 `adder`。

如果要从 workspace 根目录运行 `adder`：

```shell
cargo run -p adder
```

`-p` 是 `--package` 的简写，用来指定要操作 workspace 中的哪个 package。



# 五、共享 Cargo.lock 和 target 目录

Workspace 成员共享根目录下的`Cargo.lock`和`/target/`。

## 1、共享 Cargo.lock

`Cargo.lock`记录依赖解析结果。一个`workspace`只有一个根`Cargo.lock`，这可以让所有成员在同一套依赖解析结果下构建。

例如，假设 adder 和 add_one 都依赖 `rand`，只要版本要求兼容，`Cargo`会尽量解析到同一个版本，并记录在根目录的`Cargo.lock`中。

但要注意：**共享`Cargo.lock`不代表共享依赖作用域**。

如果 `add-one` 依赖了 `rand`，`adder` 并不会自动获得 `rand`。`adder` 如果也要使用 `rand`，仍然必须在自己的 `Cargo.toml` 中声明依赖。

## 2、共享 target 目录

Workspace 的构建产物默认放在根目录的 `target/` 中。

即使进入成员目录运行：

```shell
cd adder
cargo build
```

构建结果仍然会放到：

```shell
add/target/
```

共享 `target/` 的好处是减少重复构建。Workspace 中的成员经常相互依赖，如果每个成员都有自己的 `target/`，就可能重复编译相同依赖或相同内部 crate。



# 六、workspace.dependencies

每个 workspace member 都有自己的 `[dependencies]`。如果某个成员在自己的`Cargo.toml`增加了外部依赖，该成员本身可以使用该依赖，但其他成员并不自动也可以使用该依赖，每个成员仍然要声明自己直接使用的依赖。

不过，如果每个成员都需要使用同一个依赖，可以在根`Cargo.toml`中使用`[workspace.dependencies]`统一声明依赖版本，然后由成员显式继承。

根目录 `Cargo.toml`：

```rust
[workspace]
resolver = "3"
members = [
    "adder",
    "add-one",
    "add-two",
]

[workspace.dependencies]
rand = "0.10.1"
```

成员 `add-one/Cargo.toml`：

```toml
[dependencies]  
rand.workspace = true
```

也可以写成：

```toml
[dependencies]  
rand = { workspace = true }
```

注意事项：

- `[workspace.dependencies]` 不会自动把依赖添加给所有成员，成员必须显式写 `workspace = true`
- 成员可以在继承时额外添加 features
- workspace dependency 的 features 会和成员侧启用的 features 合并

# 七、workspace.package

除了依赖版本，也可以在根目录统一声明部分 package 元信息。成员再通过 `.workspace = true` 继承。

根目录`Cargo.toml`：

```toml
[workspace]
resolver = "3"
members = [
    "adder",
    "add-one",
    "add-two",
]

[workspace.package]
edition = "2024"
version = "0.1.0"
license = "MIT"
authors = ["Your Name <you@example.com>"]
```

成员 `add-one/Cargo.toml`：

```toml
[package]
name = "add-one"
edition.workspace = true
version.workspace = true
license.workspace = true
authors.workspace = true
```

这种写法适合在一个仓库中维护多个内部 crate 时，统一 `edition`、`version`、`license`、`authors` 等信息。
