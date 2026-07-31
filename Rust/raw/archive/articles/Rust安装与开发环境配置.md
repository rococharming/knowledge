---
title: Rust安装与开发环境配置
date: 2026-05-09
tags: [Rust, Rust基础]
aliases:
  - Rust安装与开发环境配置
---

# 一、Rust简介

Rust 语言在 2006 年作为 Mozilla 员工 `Graydon Hoare`（格雷登·霍尔）的私人项目出现，Mozilla 于2009年开始赞助该项目。第一个有版本的 Rust 编译器于2012年1月发布。 **Rust 1.0 作为第一个稳定版本于 2015年5月15日 发布** 。

相比于 C/C++ 语言，Rust 具有如下优点：

**内存安全：** Safe Rust 在编译期防止悬垂引用、空引用解引用和数据竞争等常见内存安全问题；但 `unsafe`、FFI 或逻辑错误仍需要开发者谨慎处理。

**性能高效：** Rust 具有与 C/C++ 相当的性能

**并发安全：** 所有权系统和借用规则使得Rust非常适合编写线程安全的代码

**社区支持：** Rust拥有活跃的社区，在 [https://crates.io/](https://crates.io/) 上提供了很多开源库、工具和框架，可以大幅提升开发效率

**统一包管理**：C/C++最令人诟病的就是包管理，如果想要使用一个库，需要自己下载、安装和配置。Rust提供了统一的包管理程序`cargo`，只需在`Cargo.toml`中增加一行代码，即可自动下载、安装和配置包，还提供对应的文档，便于开发者理解。

# 二、安装Rust

## 1、安装rustup

与C/C++一样，Rust也是**编译型语言**，因此Rust源代码（`.rs`）需要编译成二进制可执行程序才能运行。

进入Rust官网 [https://rust-lang.org/](https://rust-lang.org/) ，点击上方的install，如下图所示：

![[assets/Image.png|600]]

Rust官网比较智能，可以自动识别当前主机的操作系统，从而给出不同的安装方案。

>注意：由于国内安装Rust以及拉取crates.io的包可能存在流量出境不稳定问题，因此可使用国内镜像代理加快下载速度。如果想使用代理，直接跳过本小节，移步[[#^setting-proxy|设置国内镜像源]]。

`rustup` 是 Rust 官方推荐的 **Rust 工具链管理器**，主要用于安装、更新和切换不同版本的 Rust 编译器及相关工具链。

通过 `rustup` 安装的工具链通常包含 `rustc`、`cargo`、`rustdoc`、标准库以及相关组件。其中，`rustc` 是 Rust 编译器，`cargo` 是 Rust 构建系统和包管理工具。

### （1）macOS / Linux

在 macOS 或 Linux 上，通常直接在终端执行：

```shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

这条命令会先下载 `rustup-init.sh`，再由它下载并安装当前平台对应的 `rustup` 和默认 Rust 工具链。默认情况下，安装的是 `stable` 工具链。

### （2）Windows

在 Windows 上，通常进入 Rust 官网安装页面，下载并运行 `rustup-init.exe`。

Windows 上的安装过程需要分成两件事理解：

- **Rust 工具链**：由 `rustup-init.exe` 下载和安装，包含 `rustc`、`cargo`、`rustdoc`、标准库等。
- **MSVC 构建环境**：由 Visual Studio 或 Visual Studio Build Tools 提供，包含链接器、Windows SDK 和 Windows API 库。

Rust 本身不是 C++，但 Rust 在 Windows 上默认使用 MSVC 工具链，例如：

```text
x86_64-pc-windows-msvc
```

这里的 `msvc` 表示它使用微软 Visual C++ 生态的 ABI 和链接规则。Rust 源码经 `rustc` 编译后，还需要链接器把目标文件、Rust 标准库和 Windows 系统库链接成 `.exe` 文件。所以 Rust 需要借用 Windows 平台上的 MSVC 链接器和系统库。

启动 `rustup-init.exe`后，安装程序通常会给出三个选择：

```text
1) Quick install via the Visual Studio Community installer
2) Manually install the prerequisites
3) Don't install the prerequisites
```

三个选项的区别如下：

| 选项 | 含义 | 适合场景 |
|---|---|---|
| `1` | 让 `rustup-init.exe` 调用 Visual Studio Community 安装器，自动安装 Rust 所需的 MSVC 前置组件 | 个人学习、开源项目、希望省事 |
| `2` | 自己安装 Visual Studio 或 Visual Studio Build Tools，并手动选择需要的组件 | 企业环境、想控制安装内容、不想安装完整 IDE |
| `3` | 不安装 MSVC 前置组件 | 明确使用 GNU ABI / MinGW 工具链 |

如果需要走 GNU ABI / MinGW 工具链路线，详见 [[4、Windows切换Rust GNU工具链|Windows 切换 Rust GNU 工具链]]。

### （3）系统构建工具

Rust 工具链由 `rustup` 下载，但最终生成可执行文件时，还需要当前操作系统上的链接器和系统库。Windows 上这一步通常体现为 MSVC / Visual Studio Build Tools；macOS 和 Linux 也有类似需求，只是安装方式不同。

| 系统 | Rust 工具链 | 系统构建工具 |
|---|---|---|
| Windows | `rustup-init.exe` 下载 | Visual Studio Build Tools、MSVC、Windows SDK |
| macOS | `rustup-init.sh` 下载 | Xcode Command Line Tools，通常可用 `xcode-select --install` 安装 |
| Linux | `rustup-init.sh` 下载 | GCC / Clang、`make`、链接器和系统开发包 |

macOS 和 Linux 不一定默认自带完整构建工具。很多开发者机器上已经因为 Git、Homebrew、C/C++ 或其他开发环境装过，所以 Rust 安装时不一定明显提示；如果缺少这些工具，通常会在编译阶段报错，再按系统提示或发行版包管理器补装。

### （4）验证安装

安装完成后，用户可以在 Cargo 的 `bin` 目录下看到 `rustup`、`rustc`、`cargo` 等命令入口，如下图所示：

![[assets/Image 1.png]]

> 在 Windows 上，对应目录通常是 `%USERPROFILE%\.cargo\bin`；在 macOS 或 Linux 上，对应目录通常是 `~/.cargo/bin`。

需要注意的是，这些命令入口并不一定是真正的编译器或构建工具入口本体；在 `rustup` 管理的环境中，`cargo`、`rustc`、`rustdoc` 等通常是由 `rustup` 管理的代理入口。

例如，当在命令行中执行 `cargo build` 时，系统会先根据 `PATH` 找到 Cargo `bin` 目录中的 `cargo` 入口。这个入口会转交给 `rustup`，由 `rustup` 根据当前目录、环境变量或默认配置判断应该使用哪个 toolchain，然后再调用对应 toolchain 中真正的 `cargo` 二进制文件。

可以通过`rustup which cargo`来查找真实cargo二进制的位置：

```shell
rustup which cargo
```

结果：

![[assets/Image 2.png]]

上述细节了解即可。要执行这些程序，需要将 Cargo `bin` 目录加入到 `PATH` 环境变量。但一般安装过程中，`rustup` 会自动配置好。安装完成之后，重启终端即可。

执行如下命令验证是否安装配置成功：

```shell
rustup --version
rustc --version
cargo --version
rustup show
```

示例：

![[assets/Image 3.png]]

在 Windows 上，如果 `rustup show` 中看到类似下面的默认工具链，说明当前使用的是 MSVC 工具链：

```text
stable-x86_64-pc-windows-msvc
```

还可以创建一个最小项目验证完整编译流程：

```shell
cargo new hello-rust
cd hello-rust
cargo run
```

如果能够输出 `Hello, world!`，说明 Rust 工具链和系统链接环境都已经配置成功。如果出现 `link.exe not found` 之类的错误，通常说明 Visual Studio Build Tools、MSVC 组件或 Windows SDK 还没有安装完整。

## 2、设置国内镜像源 ^setting-proxy

这里推荐`RsProxy`代理，官网： [https://rsproxy.cn/](https://rsproxy.cn/) 。官网已经给出了Linux/macOS设置镜像源的方法，按照步骤操作即可。为了保证本教程的完整性，这里再赘述一遍：

1. 设置rustup镜像

需要设置两个环境变量，本机`macOS`上默认使用的是`zsh` shell，因此`~/.zshrc`中添加：

```shell
export RUSTUP_DIST_SERVER="https://rsproxy.cn"
export RUSTUP_UPDATE_ROOT="https://rsproxy.cn/rustup"
```

添加完成后，重启终端或者在当前终端执行`source ~/.zshrc`使其生效。

2. 安装Rust

执行：

```shell
curl --proto '=https' --tlsv1.2 -sSf https://rsproxy.cn/rustup-init.sh | sh
```

3. 设置crates.io镜像

修改配置文件`~/.cargo/config.toml`，以支持 git 协议和 sparse 协议，>=1.68 版本建议使用 sparse-index，速度更快。

增加如下内容：

```toml
[source.crates-io]
replace-with = 'rsproxy-sparse'
[source.rsproxy]
registry = "https://rsproxy.cn/crates.io-index"
[source.rsproxy-sparse]
registry = "sparse+https://rsproxy.cn/index/"
[registries.rsproxy]
index = "https://rsproxy.cn/crates.io-index"
[net]
git-fetch-with-cli = true
```

上述操作完成后，同样地执行如下命令验证：

```shell
rustup --version
rustc --version
```

# 三、rustup命令

## 1、查看版本

查看rustup的版本。

```shell
rustup --version
```
![[assets/Image 4.png]]

>注意：这里提示输出的是rustup的版本而非rustc版本，并且也给出了rustc的版本。

## 2、更新

更新分为**更新rustup自身**和**更新Rust工具链**。

### （1）更新rustup自身

```shell
rustup self update
```

### （2）更新Rust工具链

```shell
rustup update  # 更新已经安装的 toolchain
```

> 现在 `rustup update` 也会在更新 toolchain 时自动检查并更新 `rustup` 自身

## 3、安装Rust工具链

### （1）Rust工具链分类

Rust 的工具链主要有三种发布通道：

- **stable**：稳定版本，也是`rustup`默认安装和使用的版本。每6周发布一次，经过相对充分的测试，适合日常开发和生产项目使用。
- **beta**：测试版本，也就是下一个 `stable` 版本的候选版本。`beta` 通常用于提前测试即将进入稳定版的功能和变更。它比 `stable` 更新，但比 `nightly` 更稳定。
- **nightly**：每夜版，每天构建一次，包含最新的 Rust 开发成果，但可能不稳定。

### （2）查看工具链状态

```shell
rustup show
```

该命令可以查看当前 Rust 安装状态，包括：
- 当前平台
- 已安装的工具链（`installed toolchains`）
- 当前正在使用的工具链（`active toolchain`）

![[assets/Image 5.png|400]]

### （3）安装工具链

- 安装每夜版

```shell
rustup install nightly
```

- 安装测试版

```shell
rustup install beta
```

- 安装稳定版

```shell
rustup install stable
```

### （4）切换工具链

```shell
rustup default stable
rustup default beta
rustup default nightly
```

## 4、卸载

```shell
rustup self uninstall
```

这条命令会卸载`rustup`自身，并移除`rustup`管理的Rust工具链、组件和相关工具。


# 四、rustc编译器

`rustc`是 Rust 官方提供的编译器，用于将Rust源程序，也就是`.rs`文件，编译成目标文件、可执行文件或库。它在使用风格上类似于`gcc`命令。

在实际项目开发中，我们通常使用更强大的`cargo`命令来构建Rust项目。`cargo`负责读取`Cargo.toml`文件、管理依赖、组织构建流程等。`cargo`在构建项目时，底层实际调用`rustc`完成实际编译。因此，虽然日常开发中不一定直接使用`rustc`，但了解它的基本用法仍然很有必要。

## 1、查看版本

查看`rustc`的版本。

```shell
rustc --version
```

## 2、最基本用法：生成可执行文件

下面是一个最简单的 Rust 程序，用于打印 `Hello, world!`。

main.rs

```rust
fn main() {
	println!("Hello, world!");
}
```

### （1）默认输出

执行：

```shell
rustc main.rs
```

执行上述命令后，默认会生成一个可执行文件。在 macOS 或 Linux 上，默认生成名为 `main` 的文件；在 Windows 上，通常生成 `main.exe`。

结果：

![[assets/Image 6.png|400]]

### （2）指定输出文件名

可以使用 `-o` 选项指定输出的可执行文件名：

```shell
rustc -o hello main.rs
```

![[assets/Image 7.png|400]]

### （3）指定Edition

`Edition`是**Rust语言规则的一组版本集合**。

Rust需要同时满足**稳定性和进化性**：

- 稳定性：旧项目多年之后仍应能被新编译器编译运行
- 进化性：语言本身需要继续改进，例如引入新语法、新关键字、新的宏规则、新的预导入内容。

如果只有一套语言规则，那么语言规则一旦变化，就可能导致旧项目在新编译器上无法编译。

因此，就有了`Edition`。Rust 目前支持 2015、2018、2021、2024  Edition。每个项目可以选择一个 Edition，编译器会按照对应 Edition 的规则解析和编译代码。

同一个 `rustc` 可以兼容多个 Edition。要让代码按照指定的 Edition 编译，可以使用 `--edition` 选项：

```shell
rustc main.rs --edition=2021
```

`rustc` 也可以直接编译库产物，例如 `rlib`。不过实际项目通常交给 Cargo 管理构建、依赖和链接。相关内容放在 [[13、crate与模块|crate 与模块]] 中单独说明。

# 五、Cargo

## 1、Cargo概述

直接使用 `rustc` 编译一个个 Rust 源码文件比较费时费力。在实际项目开发中，更常用的是 `cargo`。

`cargo` 是 Rust 的**构建工具和包管理工具**。通过 `rustup` 安装 Rust 时，通常会安装默认的 `stable` 工具链，而 `cargo` 是该工具链中的组件之一。

使用`cargo`可以完成项目创建、代码构建、依赖下载与编译、测试和文档生成等工作。在构建代码时，`cargo` 底层会调用 `rustc` 完成实际编译。

通过 `cargo`，可以做如下事情：

- `cargo new` 新建项目
- `cargo build`构建项目
- `cargo run`构建并运行项目
- `cargo check`检查项目是否可以通过编译，但不生成最终可执行文件
- `cargo test`测试项目
- `cargo doc`构建项目文档
- `cargo clean`清理构建产物

## 2、创建Cargo项目

### （1）创建二进制可执行项目

命令：

```shell
cargo new <project_name>
```

例如，创建 `hello_cargo` 项目：

```shell
cargo new hello_cargo
```

执行后，会在当前目录生成一个 `hello_cargo` 项目文件夹。

![[assets/Image 10.png|800]]

进入该文件夹后，可以看到类似下面的目录结构：

```text
hello_cargo/
├── .git/        # Git 仓库目录，默认自动生成
├── .gitignore   # Git 忽略文件
├── Cargo.toml   # Cargo 项目配置文件
└── src/
    └── main.rs  # Rust 主程序源文件
```

默认情况下，如果当前目录不在已有版本控制仓库中，`cargo new` 会为新项目初始化 Git 仓库。如果不想使用 Git 版本控制，可以在执行 `cargo new` 时加上 `--vcs=none` 选项：

```shell
cargo new hello_cargo --vcs=none
```

打开`Cargo.toml`文件，内容类似如下：

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

其中：
- `[package]`是该包的基本信息，包括名字、版本、Edition等。除了默认生成的字段外，还可增加`description`、`license`、`authors`等其他信息。
- `[dependencies]`：用于声明项目依赖的第三方 crate，这是Cargo进行包管理的核心机制。详见[[Cargo 依赖管理]]。

> 需要注意的是，如果你使用的是较旧版本的 Rust，默认生成的 Edition 可能是 `2021`；较新的 Rust 版本默认生成的通常是 `2024`。

进入 `src` 目录，可以看到自动生成的 `main.rs` 文件，内容如下：

```rust
fn main() {
    println!("Hello, world!");
}
```

`main.rs` 是二进制可执行项目的入口文件。

说明：

- `fn` 是 Rust 的关键字，用于定义函数。
- `main` 是函数名称。对于二进制可执行程序来说，`main` 是程序入口函数，通常不能随意改成其他名字。
- `println!` 是 Rust 的一个宏，用于向控制台输出内容。

### （2）创建库项目

除了可以创建二进制可执行项目，还可以创建库项目。库项目与二进制项目的主要区别是：库项目默认没有 `main` 函数，因此不能直接作为程序运行，而是用于被其他代码调用。

使用 `--lib` 选项可以创建库项目：

```shell
cargo new --lib <project_name>
```

库项目的目录结构与二进制项目类似，区别是 `src` 目录下自动生成的是 `lib.rs` 文件，而不是 `main.rs` 文件。

`src/lib.rs` 内容默认如下：

```rust
pub fn add(left: u64, right: u64) -> u64 {
    left + right
}

#[cfg(test)]
mod tests {
	use super::*;
	
	#[test]
	fn it_works() {
		let result = add(2, 2);
		assert_eq!(result, 4);
	}
}
```

其中，`#[cfg(test)]` 和 `#[test]` 是与测试相关的内容，详见[[Rust/notes/Rust基础/20、测试|测试]]。

## 3、构建Cargo项目

在创建好的 Cargo 项目目录中执行：

```shell
cargo build
```

即可构建（编译）项目。

对于二进制项目，执行 `cargo build` 后会生成可执行文件，默认位于项目顶层目录的 `target/debug` 目录下。因为 `cargo build` 默认使用**调试构建**，也就是`dev profile`，所以生成结果位于 `debug` 目录中。

当项目准备发布时，可以执行：

```shell
cargo build --release
```

这是**发布构建**（`release profile`）。构建产物位于项目顶层目录的`target/release`目录下。

> 调试构建与发布构建
> 
> 调试构建：也就是默认的`cargo build`，使用`dev profile`。它通常优化较少，编译速度快，并保留更多的调试信息。
> 
> 发布构建：也就是 `cargo build --release`，使用`release profile`。它会启用更高级别的优化，通常编译速度较慢，但生成的程序运行速度更快，更适合发布或性能测试场景。

构建完成后，就可以运行生成的可执行文件了。以调试构建为例，运行如下：

![[assets/Image 11.png]]

## 4、构建并运行Cargo项目

执行`cargo build`只会构建项目，如果要运行程序，还需要手动执行生成的可执行文件。

Cargo 提供了 `cargo run`，可以一次完成“构建 + 运行”两个步骤：

```shell
cargo run
```

结果：

![[assets/Image 12.png]]

`cargo run`默认也是调试构建。如果希望以发布模式构建并运行，可以使用：

```shell
cargo run --release
```

## 5、检查代码确保其可编译

Cargo 还提供了 `cargo check` 命令，用于快速检查代码是否可以通过编译：

```shell
cargo check
```

`cargo check`会执行类型检查、借用检查等编译检查工作，但不会生成最终的可执行文件，因此通常比`cargo build`更快。开发过程中，可以经常使用`cargo check`快速发现编译错误。

## 6、清理项目

`cargo clean` 用于删除 Cargo 生成的构建产物。通常来说，它会删除项目中的 `target` 目录。

命令如下：

```shell
cargo clean
```

## 7、测试

Cargo 还提供了 `cargo test` 用于运行测试。关于测试的内容较多，参考[[Rust/notes/Rust基础/20、测试|测试]]。

命令如下：

```shell
cargo test
```

# 六、IDE环境

使用IDE或带插件的编辑器开发Rust项目会更加高效。这里推荐两种常见选择：`VS Code`和`RustRover`。

## 1、VS Code

`VS Code`是目前非常受欢迎的代码编辑器，可以用于开发多种语言的项目。通过安装 `Rust` 相关插件，`VS Code`也可以获得接近`IDE`的`Rust`开发体验。

在使用 `cargo new` 创建一个新项目并进入项目文件夹后，可以执行下面的命令用 VS Code 打开当前项目：

```shell
code .
```

如果终端提示 `code: command not found`，说明还没有把 VS Code 的 `code` 命令安装到 `PATH` 中。

在 VS Code 中打开命令面板（<kbd>Command</kbd> + <kbd>P</kbd>），搜索`> Shell Command`并选择`Shell Command: Install 'code' command in PATH`：

![[assets/Pasted image 20260511163624.png|600]]

打开项目后，还需要安装Rust相关插件。点击 VS Code 左侧栏的 Extensions，然后搜索并安装以下插件。

![[assets/Image 13.png|600]]

- `rust-analyzer`：Rust 官方推荐的语言服务器插件，也是`VS Code`开发 Rust 的最核心插件。它可以提供代码补全、类型提示、错误诊断、跳转定义、查找引用、代码重构等。
- `Error Lens`：可以在错误、警告、提示信息直接显示在代码行旁边，让诊断信息更加醒目。它不是Rust专用插件。也不是必须插件，但对新手比较友好，可以直观地看到错误信息。

安装这些插件后，VS Code 就可以作为 Rust 开发环境使用。当输入代码的前几个字符时，VS Code 会自动弹出代码提示。出现提示后，可以按 <kbd>Tab</kbd> 或<kbd>Enter</kbd>接受补全。

![[assets/Image 14.png|600]]

对于`Cargo`项目，`rust-analyzer`通常会在`main`函数、测试函数等位置上方显示`Run`和`Debug`按钮。

点击`Run`可以直接运行当前程序：

![[assets/Image 15.png|600]]

点击`Debug`进入调试状态，如下图所示：

![[assets/Image 16.png|600]]

关于调试相关概念，参考：[[Rust/notes/其他/1、调试|调试]]。

## 2、RustRover

`RustRover`是`JetBrains`推出的Rust专用IDE。相比`VS Code`，`RustRover`更接近“开箱即用”的完整IDE。安装后就内置了Rust项目开发的很多功能，例如代码补全、错误提示、Cargo集成、运行、测试、Git集成等。

如果已经使用`cargo new`创建了一个Rust项目，可以直接用`RustRover`打开项目目录。

![[assets/Pasted image 20260511224024.png|600]]

打开项目后，`RustRover`会识别项目中的`Cargo.toml`文件，并将该目录作为一个`Cargo`项目加载。前面已经说过，`Cargo.toml`是`Cargo`项目的核心配置文件，因此`RustRover`通常以它为入口识别项目结构。

当然，也可以新建项目：

![[assets/Pasted image 20260511224649.png|600]]

![[assets/Pasted image 20260511224814.png|600]]

![[assets/Pasted image 20260511224856.png|600]]

下面简单介绍几个功能：

1. 代码补全与错误提示

`RustRover`内置 Rust 代码分析能力，可以提供常见IDE功能，如代码补全、类型提示、错误提示、跳转定义、查找引用、快速修复等。

例如，在编辑 `main.rs` 时，输入代码的前几个字符，RustRover 会自动弹出补全提示。选择候选项后，可以按 <kbd>Enter</kbd> 或 <kbd>Tab</kbd> 接受补全。

如果代码中存在语法错误、类型错误或借用检查相关问题，RustRover 会在编辑器中直接标记出来，并在部分场景下提供 quick fix，也就是快速修复建议。

2. Cargo工具窗口

`RustRover`对`Cargo`有内置支持。打开 Cargo 项目后，可以在 IDE 侧边栏看到 Cargo 工具窗口。如果没有，需要从菜单中通过`View → Tool Windows → Cargo` 打开。

![[assets/Pasted image 20260511225507.png]]

Cargo 工具窗口中通常可以看到项目中的：

- bin target  
- lib target  
- test target  
- example target  
- benchmark target

你可以在终端执行`cargo`命令运行对应目标，也可以在`Cargo`工具窗口中运行目标。

3. 运行代码

在`RustRover`中运行Rust程序很方便。打开 `src/main.rs` 后，通常可以在 `main` 函数左侧看到绿色运行按钮。点击该按钮，可以选择运行当前程序。也可以使用顶部工具栏的运行按钮，或者使用快捷键运行。

![[assets/Pasted image 20260511230042.png]]

4. 调试代码

`RustRover` 内置调试功能。`RustRover`提供完整调试器，支持断点、变量查看、单步执行、内存视图和反汇编视图等功能。

使用方式如下：

1. 在代码行号左侧点击，设置断点；
2. 点击 `main` 函数左侧的运行图标；
3. 选择 `Debug`；
4. 程序运行到断点处会暂停；
5. 可以在 Debug 窗口中查看变量、调用栈，并进行单步执行。

![[assets/Pasted image 20260511231034.png|600]]
