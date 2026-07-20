---
title: crate与模块
date: 2026-05-20
tags: [Rust, Rust基础, 模块]
aliases:
  - crate与模块
---

# 一、Rust 代码组织的三层模型

学习 Rust 模块系统之前，需要先分清三个层级：`package`、`crate` 和 `module`。它们分别回答不同问题：

- `package`：Cargo 管理哪个项目。
- `crate`：Rust 编译器一次编译哪个单元。
- `module`：一个 crate 内部如何组织代码、路径和可见性。

这三个概念很容易混在一起。简单来说，Cargo 面向 package 工作，`rustc` 面向 crate 编译，模块系统在 crate 内部管理代码结构。

## 1、package：Cargo 管理的项目单位

`package` 是 Cargo 管理项目的基本单位。一个 package 通常对应一个包含 `Cargo.toml` 的项目目录，`Cargo.toml` 用来描述项目名称、版本、Edition、依赖和构建配置等信息。

示例：

```text
hello_cargo/
├── Cargo.toml
└── src/
    └── main.rs
```

其中，`hello_cargo` 这个项目整体就是一个 package。

`Cargo.toml` 示例：

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
rand = "0.10.1"
```

这里的 `[package]` 描述当前 package 本身的信息，`[dependencies]` 描述当前 package 依赖哪些外部 crate。

日常说“创建一个 Rust 项目”，多数时候就是创建一个 Cargo package：

```shell
cargo new hello_cargo
```

## 2、crate：Rust 的编译单元

`crate` 是 Rust 的基本编译单元。`rustc` 每次编译的核心对象不是整个 package，而是某个具体的 crate。

一个 crate 可以被编译成两类常见产物：

- **库 crate**：编译成库，供其他 crate 调用。
- **二进制 crate**：编译成可执行程序。

package 和 crate 的关系是：

> 一个 package 可以包含一个或多个 crate。

Cargo 对一个 package 中的 crate 有一些基本约定：

- 一个 package 最多只能有一个库 crate。
- 一个 package 可以有多个二进制 crate。
- 一个可构建的 package 至少要有一个编译目标，也就是至少有一个 crate。


## 3、module：crate 内部的命名空间

`module` 是 crate 内部组织代码的方式。它主要负责两件事：

- **命名空间管理**：把相关函数、类型、常量、子模块放在一个路径下。
- **可见性管理**：控制哪些内容只在当前模块内部使用，哪些内容可以对外暴露。

例如：

```rust
mod shop {
    pub fn checkout() {
        println!("checkout");
    }

    fn check_stock() {
        println!("check stock");
    }
}
```

这里的 `shop` 是一个模块，`shop::checkout` 是公开函数，`shop::check_stock` 默认私有。

模块不是 Cargo 管理单位，也不是 `rustc` 的独立编译单位。模块只是 crate 内部的代码组织结构。

## 4、三者关系总览表

| 概念 | 所属层级 | 主要作用 | 常见位置 |
|---|---|---|---|
| `package` | Cargo 项目层 | 管理项目元信息、依赖和构建配置 | `Cargo.toml` 所在目录 |
| `crate` | 编译单元层 | 作为 `rustc` 的编译单位，生成库或可执行文件 | `src/lib.rs`、`src/main.rs`、`src/bin/*.rs` |
| `module` | 代码组织层 | 管理 crate 内部的命名空间和可见性 | `mod` 声明、模块文件 |

三者可以这样理解：

```text
package
└── crate
    └── module
        └── 函数、结构体、枚举、Trait 等语法项
```

在更复杂的项目中，一个 package 也可能包含多个 crate；多个 package 又可以放进同一个 [[Cargo workspace|workspace]] 中统一管理。

# 二、crate 的入口与类型

crate 的入口文件称为 crate root。编译器会从 crate root 开始解析模块树，并沿着 `mod` 声明加载更多模块。

## 1、什么是 crate root

crate root 是一个 crate 的根模块文件。它有两个作用：

- 作为编译器开始解析当前 crate 的入口。
- 作为当前 crate 模块树的根，也就是路径 `crate::` 指向的位置。

在 Cargo 的默认约定中：

| crate 类型 | 默认 crate root | 说明 |
|---|---|---|
| 库 crate | `src/lib.rs` | 定义当前库对外暴露的模块、函数、类型等 |
| 默认二进制 crate | `src/main.rs` | 定义可执行程序入口，必须有 `main` 函数 |
| 额外二进制 crate | `src/bin/name.rs` | 每个文件都是一个独立二进制 crate 的 crate root |

需要注意：每个 crate 都有自己的 crate root。即使它们位于同一个 package 中，`src/lib.rs` 和 `src/main.rs` 也是两个不同 crate 的入口。

因此，在 `src/lib.rs` 中，`crate::` 表示当前库 crate 的根；在 `src/main.rs` 中，`crate::` 表示当前二进制 crate 的根。

## 2、二进制 crate：`src/main.rs`

二进制 crate 用来生成可执行程序，入口通常是 `src/main.rs`，并且需要包含 `main` 函数。

示例：

```text
hello_cargo/
├── Cargo.toml
└── src/
    └── main.rs
```

`src/main.rs`：

```rust
fn main() {
    println!("hello");
}
```

这里，`src/main.rs` 是一个二进制 crate 的 crate root。执行 `cargo run` 时，Cargo 会构建这个二进制 crate 并运行生成的可执行文件。

## 3、库 crate：`src/lib.rs`

库 crate 用来提供函数、类型、模块等接口，供其他 crate 调用。它的入口通常是 `src/lib.rs`。

示例：

```text
my_lib/
├── Cargo.toml
└── src/
    └── lib.rs
```

`src/lib.rs`：

```rust
pub fn add(left: i32, right: i32) -> i32 {
    left + right
}
```

这个 crate 不会直接运行，而是作为库被其他 crate 使用。

## 4、一个 package 中可以有哪些 crate

一个 package 可以只包含一个二进制 crate，也可以只包含一个库 crate，还可以同时包含一个库 crate 和一个或多个二进制 crate。

示例：

```text
my_app/
├── Cargo.toml
└── src/
    ├── lib.rs
    └── main.rs
```

这里：

- `src/lib.rs` 是库 crate 的 crate root。
- `src/main.rs` 是二进制 crate 的 crate root。
- 这意味着同一个 package 中同时存在两个 crate：一个库 crate，一个二进制 crate。
- 二进制 crate 如何调用库 crate，涉及路径与导入规则，后文会在“路径与导入”中展开。

## 5、多个二进制 crate：`src/bin/*.rs`

一个 package 可以包含多个二进制 crate。除了 `src/main.rs` 外，还可以在 `src/bin/` 下放多个入口文件。

示例：

```text
my_tools/
├── Cargo.toml
└── src/
    ├── main.rs
    └── bin/
        ├── server.rs
        └── client.rs
```

这里会产生多个二进制 crate：

- `src/main.rs`：二进制名默认为 package 名，例如 `my_tools`。
- `src/bin/server.rs`：二进制名为 `server`。
- `src/bin/client.rs`：二进制名为 `client`。

每个二进制 crate 都需要有自己的 `main` 函数。

运行默认二进制：

```shell
cargo run
```

运行指定二进制：

```shell
cargo run --bin server
cargo run --bin client
```

如果一个 package 中存在多个二进制目标，而 Cargo 无法从上下文推断要运行哪一个，就需要使用 `--bin` 显式指定。

# 三、依赖 crate 如何进入当前项目

Rust 项目不会把所有功能都从零实现。很多功能来自外部 crate，例如随机数、序列化、日志、命令行解析等。Cargo 负责解析这些依赖，并把它们作为外部 crate 提供给当前 crate 使用。

更完整的依赖规则可以参考 [[Cargo 依赖管理]]。本节只关注依赖 crate 如何进入当前项目。

## 1、Cargo.toml 中的 dependencies

在 Cargo 项目中，可以通过 `Cargo.toml` 的 `[dependencies]` 添加第三方 crate：

```toml
[dependencies]
rand = "0.10.1"
```

这里的 `rand = "0.10.1"` 表示当前 package 依赖 `rand` 这个外部 crate。构建时，Cargo 会解析版本要求、下载缺失的源码，并参与后续编译。

代码中可以使用这个外部 crate：

```rust
use rand::RngExt;

fn main() {
    let mut rng = rand::rng();
    println!("dice: {}", rng.random_range(1..7));
}
```

`Cargo.toml` 负责声明依赖，Rust 代码中的 `use rand::RngExt` 负责把依赖 crate 中的路径引入当前作用域。

## 2、直接依赖与传递依赖

依赖可以分为直接依赖和传递依赖：

- **直接依赖**：当前项目的 `Cargo.toml` 中明确列出的依赖。
- **传递依赖**：直接依赖自身依赖的其他 crate。

例如，项目只在 `[dependencies]` 中写了 `rand`，但 `rand` 自己还会依赖一些底层 crate。这些 crate 不需要手动逐个写入当前项目的 `Cargo.toml`，Cargo 会根据依赖图自动解析和构建。

可以执行 `cargo tree` 查看依赖图：

```shell
cargo tree
```

结果：

![[assets/Pasted image 20260520011515.png|500]]

依赖图能帮助理解：项目最终不是只编译自己的代码，而是要把所有相关依赖都构建出来。

## 3、crate 名与代码中的路径

`Cargo.toml` 中声明的是 package 依赖，但代码中使用的是 crate 名。大多数情况下，package 名和 crate 名相同，因此不会感觉到区别。

例如：

```toml
[dependencies]
rand = "0.10.1"
```

代码中可以写：

```rust
use rand::RngExt;
```

但也有一些情况需要注意：

- 如果 package 名包含连字符，默认 crate 名通常使用下划线，例如 package 名 `my-lib` 对应 crate 名 `my_lib`。
- 如果依赖通过 `package = "..."` 重命名，`Cargo.toml` 左侧的名字会成为当前项目中使用的 crate 名。

示例：

```toml
[dependencies]
rng = { package = "rand", version = "0.10.1" }
```

此时当前代码中使用的外部 crate 名是 `rng`：

```rust
use rng::RngExt;
```

## 4、Cargo 如何把外部 crate 传给 rustc

真正执行编译的是 `rustc`，但实际项目通常不会手动调用它。Cargo 会先根据依赖图编译依赖 crate，再在编译当前 crate 时，把外部 crate 的名字和编译产物路径传给 `rustc`。

这个过程大致对应 `rustc` 的 `--extern` 参数：

```shell
rustc --extern rand=path/to/librand.rlib src/main.rs
```

这只是帮助理解的简化写法。真实的 Cargo 构建命令还会包含 Edition、目标目录、元数据、依赖搜索路径、编译配置等大量参数。

如果想观察 Cargo 实际如何调用 `rustc`，可以使用：

```shell
cargo build --verbose
```

补充理解：库 crate 常见的 Rust 编译产物之一是 `.rlib`。`.rlib` 不只是普通目标代码，还包含供编译器后续做类型检查、泛型实例化、Trait 检查等使用的 Rust 元数据。实际项目中通常由 Cargo 管理这些产物，不需要手动编译和链接 `.rlib`。

# 四、Cargo 构建流程概览

Cargo 是 Rust 的项目管理工具，负责项目结构、依赖解析、构建流程和调用编译器。`rustc` 则是真正执行编译工作的编译器。

## 1、cargo build 做了什么

执行：

```shell
cargo build
```

大致可能经历这些步骤：

1. 读取 `Cargo.toml` 和必要的 Cargo 配置。
2. 检查依赖索引和本地缓存，必要时更新索引或下载缺失依赖。
3. 解析依赖图，确定需要构建哪些 crate。
4. 按依赖顺序编译各个 crate。
5. 最后编译当前 package 中的目标 crate。
6. 将构建产物放到 `target/` 目录下。

> 所谓依赖索引，它记录 crates.io 上有哪些 crates、每个 crate 有哪些版本、每个版本依赖什么。

需要注意的是，并不是每次 `cargo build` 都会更新依赖索引或重新下载依赖。依赖已经解析并缓存后，Cargo 会尽量复用已有结果。

如果希望清理当前项目的构建产物，可以使用：

```shell
cargo clean
```

如果希望观察更详细的构建过程，可以使用：

```shell
cargo build --verbose
```

> 注意：如果配置了镜像源，Cargo 更新依赖索引时可能不会直接使用官方 `crates.io` 索引，而是使用镜像源。详见 [[Rust/notes/Rust基础/1、Rust安装与开发环境配置#^setting-proxy|设置国内镜像源]]。

## 2、dev 与 release profile

`cargo build` 默认使用开发配置，也就是 dev profile。

开发构建的特点是：

- 编译速度较快。
- 运行性能不是最高。
- 通常保留更多调试信息，更适合开发与调试。
- `debug_assert!` 会生效。
- 整型溢出会触发检查并 `panic`。

`cargo build --release` 使用发布配置，也就是 release profile。

发布构建的特点是：

- 编译速度较慢。
- 运行性能更高。
- 优化更充分。
- `debug_assert!` 默认不生效。
- 整型溢出默认按二进制补码回绕。

`Cargo.toml` 也可以配置不同构建模式下的编译行为。常见 profile 包括：

```toml
[profile.dev]

[profile.release]

[profile.test]
```

- `cargo build` 使用 `[profile.dev]`。
- `cargo build --release` 使用 `[profile.release]`。
- `cargo test` 使用 `[profile.test]`。

有时希望在 release 构建中也保留调试信息，例如用于性能剖析或更可读的崩溃回溯，可以这样配置：

```toml
[profile.release]
debug = true
```

这样得到的仍然是经过优化的发布构建，但会包含调试符号。

## 3、Edition 与 crate 解析规则

Rust 重视向后兼容，目标是让旧代码尽量能在新的 Rust 编译器上继续编译。但语言本身仍然需要演进，有些新特性可能会影响旧代码的解析方式，例如新增关键字、调整路径规则等。为了解决语言演进与兼容性之间的问题，Rust 引入了 Edition。

`Edition` 不是 Rust 编译器版本号，而是一组语言规则。每个 crate 可以在自己的 `Cargo.toml` 中指定自己使用的 Edition：

```toml
[package]
edition = "2024"
```

不同 Edition 的 crate 可以在同一个项目中相互依赖。Edition 主要影响当前 crate 内部代码的语法和解析规则，不影响正常的依赖使用。

Rust 的 Edition 不是每年发布，而是在需要承载一批语言规则变化时才发布。常见 Edition 包括：

- Rust 2015
- Rust 2018
- Rust 2021
- Rust 2024

## 4、cargo fix --edition 的迁移用途

如果维护旧项目，升级 Edition 时通常不建议只手动修改 `Cargo.toml` 中的 `edition` 字段，更推荐先使用 `cargo fix --edition` 让 Cargo 帮助做自动迁移。

`cargo fix` 的作用是：

> 根据编译器给出的可自动修复建议，直接修改源码。

它本质不是格式化工具，而是利用 `rustc` 的诊断信息，对一些确定可改的代码做机械化修复。

Edition 迁移时，常用流程是：

```shell
cargo fix --edition
```

这条命令会检查当前项目，并尝试把代码改成同时兼容当前 Edition 和下一个 Edition 的写法。

例如，某些旧代码可能使用了后来变成关键字的变量名。Rust 2018 引入 `async` / `await` 后，如果旧代码中有名为 `async` 的标识符，迁移工具可能会把它改成原始标识符写法：

```rust
let r#async = 1;
```

这里的 `r#async` 表示：虽然 `async` 是关键字，但这里仍然把它当作普通标识符使用。

完成自动修复后，再修改 `Cargo.toml` 中的 Edition 版本，然后重新检查项目：

```shell
cargo check
```

如果项目有测试，也应该继续运行：

```shell
cargo test
```

需要注意，`cargo fix --edition` 不是万能迁移工具。它只能修复编译器能够明确判断、并且能安全给出修改建议的问题。涉及业务逻辑、API 设计、依赖版本升级、行为差异确认的部分，仍然需要人工检查。


# 五、模块系统基础

模块（module）是 crate 内部组织代码的方式。它不决定 Cargo 如何构建项目，也不是单独的编译单元；它主要负责把代码组织成路径，并控制哪些名字可以被哪些地方访问。

可以把模块理解成：

> 给一组相关代码取一个名字，并用这个名字管理命名空间与可见性。

模块中可以放很多语法项：

- 函数
- 结构体
- 枚举
- Trait
- 常量
- 静态变量
- 类型别名
- 子模块
- `use` 声明

## 1、模块的两个核心作用

模块最核心的作用有两个：**命名空间管理**和**可见性管理**。

命名空间管理指的是：不同模块中可以存在同名函数或类型，调用时通过路径区分。

示例：

```rust
mod shop {
    pub fn create() {
        println!("create shop item");
    }
}

mod user {
    pub fn create() {
        println!("create user");
    }
}

fn main() {
    shop::create();
    user::create();
}
```

这里 `shop::create` 和 `user::create` 是两个不同函数，因为它们处在不同模块路径下。

可见性管理指的是：模块可以控制哪些内容允许外部访问，哪些内容只作为内部实现细节。

```rust
mod shop {
    pub fn checkout() {
        println!("checkout");
    }

    fn check_stock() {
        println!("check stock");
    }
}

fn main() {
    shop::checkout();

    // shop::check_stock(); // 错误：check_stock 是私有函数
}
```

Rust 的默认规则是：

> 未标记 `pub` 的语法项默认私有。

## 2、默认私有与父子模块

Rust 中，未标记 `pub` 的语法项默认是私有的。私有项可以在定义它的模块内部使用，也可以被它的子模块访问。

示例：

```rust
mod shop {
    fn check_stock() {
        println!("check stock");
    }

    pub mod admin {
        pub fn run() {
            super::check_stock();
        }
    }
}

fn main() {
    shop::admin::run();
}
```

这里的 `super::check_stock()` 表示访问父模块 `shop` 中的 `check_stock` 函数。`admin` 是 `shop` 的子模块，所以可以访问父模块中的私有项。

不过，模块外部不能直接访问 `shop::check_stock()`。

> 注意：`shop` 本身没有声明为 `pub`，但 `main` 可以访问 `shop::admin::run()`，是因为 `main` 和 `shop` 都位于同一个父模块中，也就是当前 crate 的根模块。私有性限制的是“从模块外部跨边界访问”，不是禁止同一模块中的兄弟项互相看见。

## 3、pub 与整条路径可见

`pub` 表示某个语法项可以被外部访问，但它能不能真正被访问，还取决于整条路径是否可见。

示例：

```rust
mod outer {
    pub mod inner {
        pub fn hello() {
            println!("hello");
        }
    }
}

fn main() {
    outer::inner::hello();
}
```

这里 `inner` 是 `pub mod`，`hello` 是 `pub fn`，所以 `main` 可以通过 `outer::inner::hello()` 访问。

如果中间路径是私有的，就算最终函数是 `pub`，外部也访问不到：

```rust
mod outer {
    mod inner {
        pub fn hello() {
            println!("hello");
        }
    }
}

fn main() {
    // outer::inner::hello(); // 错误：inner 是私有模块
}
```

这里 `hello` 虽然是 `pub fn`，但 `inner` 模块本身没有公开，所以 `outer` 外部无法经过 `inner` 这段路径访问它。

## 4、结构体字段也有独立可见性

结构体本身的可见性和字段的可见性是两层规则。一个结构体可以是公开的，但它的字段仍然默认私有。

示例：

```rust
mod shop {
    pub struct Product {
        pub name: String,
        price: u32,
    }

    pub fn create_product(name: &str, price: u32) -> Product {
        Product {
            name: name.to_string(),
            price,
        }
    }
}

fn main() {
    let product = shop::create_product("milk", 100);

    println!("{}", product.name);
    // println!("{}", product.price); // 错误：price 字段私有
}
```

这里 `Product` 是公开结构体，`name` 是公开字段，`price` 是私有字段。因此模块外部可以拿到 `Product` 值，也可以读 `name`，但不能直接读 `price`。

## 5、受限制的公开可见性

除了普通的 `pub`，Rust 还支持更细粒度的可见性控制，用来表达“不是完全公开接口，但也不是当前模块私有实现”的中间状态。

| 写法 | 含义 | 常见用途 |
|---|---|---|
| `pub` | 沿着可见路径对外公开 | 库的公共 API |
| `pub(crate)` | 只在当前 crate 内可见 | crate 内部共享工具 |
| `pub(super)` | 只对父模块可见 | 子模块给父模块使用的内部接口 |
| `pub(in path)` | 只在指定模块路径内可见 | 大型模块中的精确边界控制 |

### （1）pub(crate)

`pub(crate)` 表示只在当前 crate 内可见。

```rust
mod pricing {
    pub(crate) fn calc_member_price(price: u32) -> u32 {
        price * 80 / 100
    }
}

fn main() {
    let price = pricing::calc_member_price(100);
    println!("{price}");
}
```

`calc_member_price` 可以在当前 crate 内使用。但如果这个项目作为库被其他项目依赖，外部项目不能调用它。

### （2）pub(super)

`pub(super)` 表示只对父模块可见。

```rust
mod shop {
    pub mod order {
        pub(super) fn normalize_order_id(id: &str) -> String {
            id.trim().to_uppercase()
        }
    }

    pub fn test() {
        let id = order::normalize_order_id(" ab-123 ");
        println!("{id}");
    }
}

fn main() {
    shop::test();

    // shop::order::normalize_order_id(" ab-123 "); // 错误
}
```

这里 `normalize_order_id` 对父模块 `shop` 可见，但对 `shop` 外部不可见。它适合表达：这个函数是给父模块协调内部逻辑用的，不是对外接口。

### （3）pub(in path)

`pub(in path)` 可以把可见性限制在指定模块路径内。

```rust
mod shop {
    pub mod order {
        pub mod internal {
            pub(in crate::shop::order) struct OrderId(String);

            pub(in crate::shop::order) fn create_order_id(raw: &str) -> OrderId {
                OrderId(raw.trim().to_uppercase())
            }
        }

        pub fn demo() {
            let _id = internal::create_order_id(" x001 ");
            println!("order id created");
        }
    }

    pub fn test() {
        // order::internal::create_order_id(" x001 "); // 错误
    }
}
```

这里 `OrderId` 和 `create_order_id` 只在 `crate::shop::order` 这个模块范围内可见。`shop` 模块本身无法直接访问它们。

## 6、嵌套模块

模块可以嵌套，也就是在模块中继续定义子模块。

```rust
mod shop {
    pub mod product {
        pub fn list() {
            println!("product list");
        }
    }

    pub mod order {
        pub fn create() {
            println!("create order");
        }
    }

    pub mod user {
        pub fn login() {
            println!("user login");
        }
    }
}

fn main() {
    shop::product::list();
    shop::order::create();
    shop::user::login();
}
```

这种结构适合按领域划分代码，例如 `shop::product`、`shop::order`、`shop::user`。嵌套模块让代码层级更清楚，也让命名空间更明确。


# 六、模块的分文件编写

前面的模块示例都把模块内容直接写在同一个文件中。真实项目中，模块通常会拆到多个文件里。

分文件时要抓住一个关键点：

> `mod name;` 是模块声明，它告诉编译器“这里有一个叫 name 的模块，请去约定位置加载它的内容”。

`mod` 不是 `use`。`mod` 负责把模块纳入当前 crate 的模块树；`use` 只是把已有路径引入当前作用域。

## 1、从内联模块到独立文件

内联模块写法：

```rust
mod shop {
    pub fn run() {
        println!("shop is running");
    }
}

fn main() {
    shop::run();
}
```

拆成文件后：

```text
src/
├── main.rs
└── shop.rs
```

`src/main.rs`：

```rust
mod shop;

fn main() {
    shop::run();
}
```

src/shop.rs

```rust
pub fn run() {
    println!("shop is running");
}
```

注意，`shop.rs` 里面不需要再写 `mod shop { ... }`。因为 `mod shop;` 已经声明了模块名，`shop.rs` 文件本身就是 `shop` 模块的内容。

## 2、子模块放在哪里

如果 `shop` 模块下面还有 `product`、`order` 等子模块，推荐使用现代文件组织方式：

```text
src/
├── main.rs
├── shop.rs
└── shop/
    ├── product.rs
    └── order.rs
```

src/main.rs

```rust
mod shop;

fn main() {
    shop::start();
}
```

src/shop.rs

```rust
pub mod product;
pub mod order;

pub fn start() {
    println!("shop start");
    product::list_products();
    order::create_order();
}
```

src/shop/product.rs

```rust
pub struct Product {
    pub name: String,
    price: u32,
}

pub fn list_products() {
    println!("product list: milk, chocolate, strawberry");
}

pub(crate) fn default_price() -> u32 {
    100
}
```

src/shop/order.rs：

```rust
pub fn create_order() {
    println!("create order");

    let price = super::product::default_price();
    println!("default price: {}", price);
}
```

这里：

- `shop.rs` 是 `shop` 模块的入口文件。
- `shop/product.rs` 是 `shop::product` 子模块。
- `shop/order.rs` 是 `shop::order` 子模块。
- `super::product::default_price()` 表示从 `order` 的父模块 `shop` 访问兄弟模块 `product`。

## 3、mod 声明写在父模块中

子模块要在哪里声明，取决于它是谁的子模块。

例如：

```text
src/
├── main.rs
├── shop.rs
└── shop/
    └── product.rs
```

`product` 是 `shop` 的子模块，所以 `pub mod product;` 应该写在 `shop.rs` 中，而不是写在 `main.rs` 中。

```rust
// src/shop.rs
pub mod product;
```

这样得到的路径是：

```rust
crate::shop::product
```

如果把模块声明放错位置，模块路径也会跟着变，甚至找不到对应文件。模块的层级关系由 `mod` 声明的位置决定，而不是只由文件夹长相决定。

## 4、mod.rs 旧式组织

Rust 也支持 `mod.rs` 风格的目录模块：

```text
src/
├── main.rs
└── shop/
    ├── mod.rs
    ├── product.rs
    ├── order.rs
    └── user.rs
```

src/main.rs

```rust
mod shop;

fn main() {
    shop::product::list();
    shop::order::create();
    shop::user::login();
}
```

src/shop/mod.rs

```rust
pub mod product;
pub mod order;
pub mod user;
```

src/shop/product.rs

```rust
pub fn list() {
    println!("product list");
}
```

`mod.rs` 方式在旧项目中很常见，现代项目更常见的是 `shop.rs` 加 `shop/` 子目录。两种方式表达的模块路径可以相同，但同一个模块不要同时使用 `shop.rs` 和 `shop/mod.rs` 两个入口文件，否则会造成歧义。

## 5、文件拆分不改变可见性规则

把模块拆到多个文件以后，可见性规则没有变化。文件只是模块内容的存放位置，真正决定访问权限的仍然是模块路径和 `pub`。

例如 `shop/order.rs` 中可以通过 `super::product::default_price()` 访问父模块 `shop` 下的兄弟模块：

```rust
pub fn create_order() {
    let price = super::product::default_price();
    println!("default price: {}", price);
}
```

这里能访问成功，不是因为两个文件都在 `shop/` 文件夹下，而是因为它们在模块树中都是 `shop` 的子模块，并且 `default_price` 是 `pub(crate)`。

# 七、路径与导入

Rust 使用路径定位某个语法项的位置。模块可以嵌套，不同模块中也可能有同名项，所以 Rust 需要通过路径明确指定要访问的是哪个函数、类型或模块。

路径使用 `::` 分隔：

```rust
std::mem::swap
```

它表示：`std` 模块中的 `mem` 子模块中的 `swap` 函数。

## 1、绝对路径与相对路径

Rust 路径可以分为绝对路径和相对路径。

绝对路径从某个根开始：

- `crate::...`：从当前 crate 根模块开始。
- `std::...`：从外部 crate `std` 开始。
- `::image::...`：从外部 crate 根开始，常用于和本地模块重名时消歧。

相对路径从当前位置开始：

- `self::...`：从当前模块开始。
- `super::...`：从父模块开始。
- 普通名字：从当前作用域中查找。

项目变复杂后，`crate::...` 的写法通常更稳定，因为它不依赖当前代码所在模块的位置。

## 2、crate、self 和 super

`crate` 表示当前 crate 的根模块。

```text
src/
├── main.rs
└── account.rs
```

src/main.rs

```rust
mod account;

use crate::account::User;

fn main() {
    let user = User {
        name: String::from("Tom"),
    };

    println!("{}", user.name);
}
```

`src/account.rs`：

```rust
pub struct User {
    pub name: String,
}
```

`crate::account::User` 表示从当前 crate 根部开始，进入 `account` 模块，再找到 `User`。

`self` 表示当前模块：

```rust
mod account {
    pub enum Role {
        Admin,
        User,
        Guest,
    }

    pub fn print_role(role: self::Role) {
        match role {
            self::Role::Admin => println!("Admin"),
            self::Role::User => println!("User"),
            self::Role::Guest => println!("Guest"),
        }
    }
}
```

很多时候可以直接写 `Role`，但 `self::Role` 会更明确地表达：这个名字来自当前模块。

`super` 表示父模块：

```rust
mod account {
    pub struct User {
        pub name: String,
    }

    pub mod auth {
        use super::User;

        pub fn login(user: &User) {
            println!("login: {}", user.name);
        }
    }
}
```

这里 `auth` 是 `account` 的子模块，`super::User` 表示到父模块 `account` 中查找 `User`。`super` 常用于子模块访问父模块中的类型、函数或兄弟模块。

## 3、use 导入名字

`use` 可以把某个路径引入当前作用域，让后续代码使用更短的名字。

示例：

```rust
use std::mem;

fn main() {
    let mut a = 1;
    let mut b = 2;

    mem::swap(&mut a, &mut b);

    println!("a = {}, b = {}", a, b);
}
```

这里的 `use std::mem;` 表示把 `std::mem` 这个模块名引入当前作用域。之后就可以写 `mem::swap`，而不必每次都写 `std::mem::swap`。

`use` 不会复制代码，也不会把定义搬到当前文件。它只是让当前作用域多了一个可用名字。

也可以直接导入具体函数：

```rust
use std::mem::swap;

fn main() {
    let mut a = 1;
    let mut b = 2;

    swap(&mut a, &mut b);

    println!("a = {}, b = {}", a, b);
}
```

一般来说，Rust 代码常见风格是：

- 类型、Trait、模块通常导入到当前作用域。
- 函数可以保留模块前缀，让来源更清楚。

例如 `HashMap` 常直接导入：

```rust
use std::collections::HashMap;

fn main() {
    let mut scores = HashMap::new();
    scores.insert("Tom", 90);
    scores.insert("Alice", 85);
}
```

而 `std::mem::swap` 这类函数，有时保留 `mem::swap` 会更清晰。

## 4、use 的作用范围

`use` 可以放在模块级别，也可以放在代码块级别。

放在模块级别时，当前模块后续代码都可以使用：

```rust
use std::collections::HashMap;

fn main() {
    let mut scores = HashMap::new();
    scores.insert("Tom", 90);
}
```

放在代码块内部时，只在当前代码块内有效：

```rust
fn sort_pair(mut a: i32, mut b: i32) -> (i32, i32) {
    use std::mem;

    if a > b {
        mem::swap(&mut a, &mut b);
    }

    (a, b)
}
```

小范围 `use` 适合临时使用某个名字，避免扩大当前模块的名字集合。

## 5、合并导入、重命名与通配导入

Rust 支持把同一路径下的多个名字一起导入：

```rust
use std::collections::{HashMap, HashSet};
```

也可以同时导入模块本身和模块中的某个成员：

```rust
use std::fs::{self, File};
```

这里的 `self` 表示 `std::fs` 模块本身，等价于：

```rust
use std::fs;
use std::fs::File;
```

如果导入的名字太长，或者两个名字冲突，可以使用 `as` 重命名：

```rust
use std::fmt::Result as FmtResult;
use std::io::Result as IoResult;
```

通配导入 `*` 可以导入某个模块公开的所有名字：

```rust
use std::io::prelude::*;
```

通配导入可以减少重复书写，但也容易让名字来源不清楚，甚至造成命名冲突。建议只在常见 prelude 场景或小范围代码中使用。

## 6、use 不会被子模块继承

每个模块都有自己的名字作用域。父模块中的 `use` 不会自动继承到子模块中。

错误示例：

```rust
mod parent {
    pub struct User {
        pub name: String,
    }

    use std::mem;

    pub mod child {
        pub fn func(a: &mut i32, b: &mut i32) {
            let user = User {
                name: String::from("Tom"),
            };

            mem::swap(a, b);
        }
    }
}
```

在 `child` 模块中，`User` 和 `mem` 都找不到。因为它们只在 `parent` 模块的作用域中可见，不会自动进入 `child` 模块。

可以这样修正：

```rust
mod parent {
    pub struct User {
        pub name: String,
    }

    pub mod child {
        use std::mem;

        pub fn func(a: &mut i32, b: &mut i32) {
            let user = super::User {
                name: String::from("Tom"),
            };

            mem::swap(a, b);

            println!("{}", user.name);
        }
    }
}
```

这里：

- `super::User` 表示从父模块 `parent` 中访问 `User`。
- `use std::mem;` 写在 `child` 模块内部，所以 `child` 可以使用 `mem::swap`。

这条规则很重要：模块之间不是共享一个大作用域，每个模块都有自己的名字空间。

## 7、标准库预导入

每个模块都有自己的名字作用域，不过这个作用域并不是完全空白的。Rust 会自动做两件事。

第一，标准库 `std` 默认链接到项目中，因此可以直接写完整路径：

```rust
fn main() {
    let mut a = 1;
    let mut b = 2;

    std::mem::swap(&mut a, &mut b);
}
```

第二，Rust 会自动导入标准库预导入模块中的常见名字。可以近似理解为，每个模块开头都默认带有这一句：

```rust
use std::prelude::v1::*;
```

所以很多常用类型和 Trait 不需要手动导入：

```rust
let numbers: Vec<i32> = Vec::new();
let option: Option<i32> = Some(2);
let result: Result<i32, String> = Ok(1);
```

这里的 `Vec`、`Option`、`Some`、`Result` 以及 `Ok` 等名字可以直接使用，就是因为它们来自标准库预导入。

需要注意，`prelude` 只是一个约定名称。标准库中的 `std::prelude::v1` 会被 Rust 自动导入，但其他库即使提供了名为 `prelude` 的模块，也不会自动导入。

例如，某些库可能提供：

```rust
use some_crate::prelude::*;
```

这种写法表示把该库认为最常用的一组名字一次性导入当前作用域。它需要用户手动写出，Rust 不会自动帮你导入。

## 8、外部 crate 与本地模块重名

如果外部 crate 与本地模块重名，需要明确区分路径来源。

假设项目依赖了外部 `image` crate，同时自己也定义了本地 `image` 模块：

```rust
mod image {
    pub struct Sampler;
}
```

使用当前 crate 内的模块，可以写：

```rust
use crate::image::Sampler;
```

也可以在合适位置写：

```rust
use self::image::Sampler;
```

如果要使用外部 `image` crate 中的 `Sampler`，可以使用以 `::` 开头的路径：

```rust
use ::image::Sampler;
```

`::image` 表示从外部 crate 根开始查找，而不是当前模块中的 `image`。

这种情况不算特别常见，但当本地模块名和依赖名相同时，需要知道如何消除歧义。

## 9、pub use 重导出

`use` 可以把某个路径引入当前作用域，让当前模块内部可以用更短的名字访问它。

如果 `use` 前面加上 `pub`，就变成了 `pub use`。它不仅把名字引入当前作用域，还会把这个名字作为当前模块的公开项重新导出。这称为重导出。

例如，项目结构如下：

```text
src/
├── lib.rs
└── plant_structures/
    ├── mod.rs
    ├── leaves.rs
    └── roots.rs
```

`plant_structures/leaves.rs`：

```rust
pub struct Leaf;
```

`plant_structures/roots.rs`：

```rust
pub struct Root;
```

`plant_structures/mod.rs`：

```rust
pub mod leaves;
pub mod roots;

pub use self::leaves::Leaf;
pub use self::roots::Root;
```

这里的：

```rust
pub use self::leaves::Leaf;
pub use self::roots::Root;
```

表示把 `plant_structures::leaves::Leaf` 和 `plant_structures::roots::Root` 重新导出到 `plant_structures` 模块下。

因此，外部既可以使用原始路径：

```rust
plant_structures::leaves::Leaf
plant_structures::roots::Root
```

也可以使用更短的重导出路径：

```rust
plant_structures::Leaf
plant_structures::Root
```

`pub use` 不会复制类型，也不会创建新的类型。`plant_structures::Leaf` 只是 `plant_structures::leaves::Leaf` 的公开别名。

重导出常用于整理库的公共 API。库内部可以按文件和模块拆得很细，但对外暴露时，可以提供更简洁、更稳定的访问路径。

## 10、同 package 中二进制 crate 调用库 crate

最后看一个综合例子：如果同一个 package 的 `src/` 里同时有 `lib.rs` 和 `main.rs`，它们是两个不同 crate。

- `src/lib.rs`：库 crate 的 crate root。
- `src/main.rs`：二进制 crate 的 crate root。

二进制 crate 要使用库 crate 暴露的内容时，应该通过库 crate 名访问，而不是把 `lib.rs` 当成本地模块引入。

示例：

```text
my_app/
├── Cargo.toml
└── src/
    ├── lib.rs
    └── main.rs
```

`Cargo.toml`：

```toml
[package]
name = "my-app"
version = "0.1.0"
edition = "2024"
```

`src/lib.rs`：

```rust
pub fn add(left: i32, right: i32) -> i32 {
    left + right
}

pub mod greeting {
    pub fn hello(name: &str) {
        println!("hello, {name}");
    }
}
```

`src/main.rs`：

```rust
use my_app::add;

fn main() {
    let result = add(1, 2);
    println!("{result}");

    my_app::greeting::hello("Tom");
}
```

这里的 `my_app` 是库 crate 名。因为 `Cargo.toml` 中的 package 名是 `my-app`，所以代码中默认使用下划线形式 `my_app`。

> 注意：`main.rs` 不需要写 `mod lib;`。`lib.rs` 不是二进制 crate 的子模块，而是同一个 package 中的另一个库 crate。

如果在 `main.rs` 中写：

```rust
use crate::add;
```

通常是不对的。因为在 `main.rs` 这个二进制 crate 中，`crate::` 指向的是二进制 crate 自己的根，也就是 `main.rs`，不是 `lib.rs`。
