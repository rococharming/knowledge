# 一、Package与Crate

## 1、Package的基本概念

在 Rust 中，`package`是`Cargo`管理项目的基本单位。

一个`package`对应一个项目目录，并且项目根部有一个`Cargo.toml`文件。`Cargo.toml`是项目的配置文件，用来描述这个包的基本信息、依赖和构建配置等。

例如：

```text
hello_cargo/
├── Cargo.toml
└── src/
    └── main.rs
```

其中，`hello_cargo` 这个项目整体就是一个 `package`。

`Cargo.toml` 示例：

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
rand = "0.8.0"
```

这里的 `[package]` 描述当前包本身的信息，`[dependencies]` 描述当前包依赖哪些外部 `crate`。

日常说“创建一个 Rust 项目”，多数时候就是创建一个 Cargo package。

```shell
cargo new hello_cargo
```

这条命令会创建一个名为 `hello_cargo` 的 package。

## 2、crate的基本概念

`crate`是 Rust 编译和发布的基本单元。一个`crate`可以被编译成两类产物：

- 库`crate`：编译成库，供其他代码调用
- 二进制`crate`：编译成可执行程序

`package`和`crate`的关系是：

> 一个`package`可以包含一个或多个`crate`

不过 Cargo 对一个`package`中的`crate`有一些基本规则：

- 一个`package`最多只能有一个库`crate`
- 一个`package`可以有多个二进制`crate`
- 一个`package`至少要有一个`crate`

最常见的情况是：一个`package` 只有一个二进制 crate。

例如：

```text
hello_cargo/
├── Cargo.toml
└── src/
    └── main.rs
```

这里：

- `hello_cargo` 是 package。
- `src/main.rs` 对应一个二进制 crate。
- 编译后会生成一个可执行程序

如果是库项目：

```text
my_lib/
├── Cargo.toml
└── src/
    └── lib.rs
```

这里：

- `my_lib` 是 package。
- `src/lib.rs` 对应一个库 crate。
- 编译产物是供其他代码使用的库。

一个`crate`中，源码通常放在`src/`目录下。除外之外，`crate`中还会带上`test/`（测试）、`examples/`（示例）、`benches`（基准测试）、构建脚本和配置文件等内容。

很多复杂程序不会从零开始实现所有功能，而是使用社区维护的第三方库。这些第三方库以`crate`的形式发布，最常见的来源就是[crates.io](https://crates.io/)。

在 Cargo 项目中，只需要在`Cargo.toml`的`[dependencies]`添加第三方库即可使用：

```toml
[dependencies]
rand = "0.8.0"
```

这里的 `rand = "0.8.0"` 表示当前项目依赖 `rand` 这个第三方 `crate`。

## 3、库crate和二进制crate

库`crate`的入口通常是`src/lib.rs`。

```rust
pub fn add(left: i32, right: i32) -> i32 {
    left + right
}
```

这个 `crate` 不会直接运行，而是提供函数、类型、模块等接口，供其他代码使用。

二进制`crate`的入口通常是`src/main.rs`。

```rust
fn main() {
    println!("hello");
}
```

这个 `crate` 包含`main`函数，会被编译成可执行文件。

一个`package`也可以同时包含库`crate`和二进制`crate`：

```text
my_app/
├── Cargo.toml
└── src/
    ├── lib.rs
    └── main.rs
```

这种结构中：

- `src/lib.rs` 是库crate。
- `src/main.rs` 是二进制crate。
- `main.rs` 可以调用当前package中库crate暴露的代码。

## 4、多个二进制crate

一个`package`可以包含多个二进制`crate`。

除了`src/main.rs`外，还可以在`src/bin`下放多个入口文件：

```text
my_tools/
├── Cargo.toml
└── src/
    ├── main.rs
    └── bin/
        ├── server.rs
        └── client.rs
```

这里会产生多个二进制`crate`：

- `src/main.rs`
- `src/bin/server.rs`
- `src/bin/client.rs`

每个文件都需要有自己的`main`函数。

运行指定二进制：

```shell
cargo run --bin hello-cargo
cargo run --bin server
cargo run --bin client
```

初学阶段不需要频繁使用多个二进制`crate`，但要知道：一个 package 不一定只对应一个可执行程序。

## 5、依赖图

编写一个库或可执行程序，顶层程序依赖一些`crate`（如图像处理、数值计算、并行库），而依赖的这些`crate`又依赖更底层的`crate`（比如解码库、压缩库等），最底层往往还依赖系统相关的库（例如libc）以及Rust标准库std。

因此，可以将依赖分为**直接依赖**和**传递依赖**：

- 直接依赖：自己项目的`Cargo.toml`中列出的依赖
- 传递依赖：自己项目依赖的`crate`依赖的一些`crate`

所有这些依赖加起来构成了项目的**依赖图**：它告诉`Cargo`需要构建哪些依赖，以及应该按什么顺序构建（必须先把依赖编译出来，才能构建依赖它们的crate）。

示例：

编写一个掷骰子小程序，其依赖于`rand` crate。

Cargo.toml

```toml
[package]  
name = "hello_cargo"  
version = "0.1.0"  
edition = "2024"  
  
[dependencies]  
rand = "0.10.1"
```

src/main.rs

```rust
use rand::RngExt;  
  
fn main() {  
    let mut rng = rand::rng();  
  
    println!("dice: {}", rng.random_range(1..7));  
}
```

`[dependencies]`虽然只写了`rand`一个依赖，但`rand`又依赖一些底层crate，这些依赖构成了依赖图，Cargo会解析依赖图并自动处理。

可以执行`cargo tree`查看依赖图：

```shell
cargo tree
```

结果：
![[Pasted image 20260520011515.png|500]]

依赖图能帮助理解：项目最终不是只编译自己的代码，而是要把所有相关依赖都构建出来。


## 6、Cargo与rustc的关系

`Cargo`是Rust的项目管理工具，负责项目结构、依赖解析、构建流程和调用编译器。

真正执行编译工作的工具是`rustc`。

执行：

```shell
cargo build
```

大致会经历这些步骤：

1. 读取`Cargo.toml`
2. 更新依赖索引
3. 解析依赖图
4. 下载缺失的依赖源码
5. 按依赖顺序编译各个`crate`
6. 最后编译当前项目
7. 将构建产物放到 `target/` 目录下。

如果想看到更详细的构建过程，可以使用：

```shell
cargo build --verbose
```

在执行前，如果在IDE（如RustRover）中给`Cargo.toml`增加依赖后，IDE会自动更新`crates.io`索引、下载依赖源码。因此，为了观察，可以先删掉`~/.cargo/registry`目录：

```shell
rm -rf ~/.cargo/registry
```

同时，为了确保target/目录干净，先执行一次`cargo clean`：

```shell
cargo clean
```

最终`cargo build --verbose`结果如下：

![[Pasted image 20260520010913.png]]

![[Pasted image 20260520011146.png]]

> 注意：由于配置了镜像源，因此更新依赖索引没有直接使用官方`crates.io`索引，而是使用了`rsproxy`镜像源。

Cargo 在编译依赖时，会为依赖图中的多个 `crate` 分别调用 `rustc`。

编译库 `crate` 时，`rustc` 会生成供其他 `crate` 使用的库产物，例如 `.rlib` 文件。`.rlib` 中不仅包含已经编译出的内容，也包含编译器后续做类型检查、泛型实例化、Trait 检查等所需的元数据。

编译二进制 `crate` 时，`rustc` 会生成最终的可执行文件。

当代码中写了：

```rust
use rand::RngExt;
```

`rustc`需要知道`rand`这个外部`crate`的编译产物在哪里。Cargo 在调用 `rustc` 编译当前项目时，会通过参数把依赖 `crate` 的名字和对应产物路径告诉 `rustc`。