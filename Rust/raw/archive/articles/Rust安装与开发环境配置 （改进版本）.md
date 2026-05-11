# 一、Rust简介

Rust 语言在 2006 年作为 Mozilla 员工 `Graydon Hoare`（格雷登·霍尔）的私人项目出现，Mozilla 于2009年开始赞助该项目。第一个有版本的 Rust 编译器于2012年1月发布。 **Rust 1.0 作为第一个稳定版本于 2015年5月15日 发布** 。

相比于 C/C++ 语言，Rust 具有如下优点：

**内存安全：** Rust的所有内存访问都经过了编译器的严格检查，因此运行时不会出现空指针访问、数据竞争等问题。

**性能高效：** Rust 具有与 C/C++ 相当的性能

**并发安全：** 所有权系统和借用规则使得Rust非常适合编写线程安全的代码

**社区支持：** Rust拥有活跃的社区，在 [https://crates.io/](https://crates.io/) 上提供了很多开源库、工具和框架，可以大幅提升开发效率

**统一包管理**：C/C++最令人诟病的就是包管理，如果想要使用一个库，需要自己下载、安装和配置。Rust提供了统一的包管理程序`cargo`，只需在`Cargo.toml`中增加一行代码，即可自动下载、安装和配置包，还提供对应的文档，便于开发者理解。

# 二、安装Rust

## 1、安装rustup

与C/C++一样，Rust也是**编译型语言**，因此Rust源代码（`.rs`）需要编译成二进制可执行程序才能运行。

进入Rust官网 [https://rust-lang.org/](https://rust-lang.org/) ，点击上方的install，如下图所示：

![[Image.png|600]]

Rust官网比较智能，可以自动识别当前主机的操作系统，从而给出不同的安装方案。

>注意：由于国内安装Rust以及拉取crates.io的包可能存在流量出境不稳定问题，因此可使用国内镜像代理加快下载速度。如果想使用代理，直接跳过本小节，移步[[#^setting-proxy|设置国内镜像源]]。

以`macOS`为例，在终端命令行执行如下命令：

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

该命令就是安装`rustup`以及Rust的stable工具链（默认）。

`rustup`是Rust官方推荐的**Rust工具链管理器**，
主要用于安装、更新和切换不同版本的Rust编译器及相关工具链。

通过`rustup`安装的工具链通常包含`rustc`、`cargo`、`rustdoc`、标准库以及相关组件。其中，`rustc`是Rust编译器，`cargo`是Rust构建系统和包管理工具，`rustdoc`用来生成文档。

安装完成后，用户可以在`~/.cargo/bin`目录下看到`rustup`、`rustc`、`cargo`等命令入口，如下图所示：

![[Image 1.png]]

需要注意的是，这些命令入口并不一定是真正的编译器或构建工具入口本体；在 `rustup` 管理的环境中，`cargo`、`rustc`、`rustdoc` 等通常是由 `rustup` 管理的代理入口，因此这里的大部分命令都是软链接。

例如，当在命令行中执行 `cargo build` 时，系统会先根据 `PATH` 找到 `~/.cargo/bin/cargo`。这个入口会转交给 `rustup`，由 `rustup` 根据当前目录、环境变量或默认配置判断应该使用哪个 toolchain，然后再调用对应 toolchain 中真正的 `cargo` 二进制文件。

可以通过`rustup which cargo`来查找真实cargo二进制的位置：

```bash
rustup which cargo
```

结果：

![[Image 2.png]]

上述细节了解即可。要执行这些程序，需要将`~/.cargo/bin`目录加入到`PATH`环境变量。但一般安装过程中，`rustup`会自动配置好。安装完成之后，重启终端即可。

执行如下命令验证是否安装配置成功：

```bash
rustup --version
```

示例：

![[Image 3.png]]

## 2、设置国内镜像源 ^setting-proxy

这里推荐`RsProxy`代理，官网： [https://rsproxy.cn/](https://rsproxy.cn/) 。官网已经给出了Linux/macOS设置镜像源的方法，按照步骤操作即可。为了保证本教程的完整性，这里再赘述一遍：

1. 设置rustup镜像

需要设置两个环境变量，本机`macOS`上默认使用的是`zsh` shell，因此`~/.zshrc`中添加：

```bash
export RUSTUP_DIST_SERVER="https://rsproxy.cn"
export RUSTUP_UPDATE_ROOT="https://rsproxy.cn/rustup"
```

添加完成后，重启终端或者在当前终端执行`source ~/.zshrc`使其生效。

2. 安装Rust

执行：

```bash
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

```bash
rustup --version
```
![[Image 4.png]]

>注意：这里提示输出的是rustup的版本而非rustc版本，并且也给出了rustc的版本。

## 2、更新

更新分为**更新rustup自身**和**更新Rust工具链**。

### （1）更新rustup自身

```bash
rustup self update
```
### （2）更新Rust工具链

```bash
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
- 当前目标平台
- 已安装的工具链（`installed toolchains`）
- 当前正在使用的工具链（`active toolchain`）

![[Image 5.png|400]]

### （3）安装工具链

- 安装每夜版

```bash
rustup install nightly
```

- 安装测试版

```bash
rustup install beta
```

- 安装稳定版

```bash
rustup install stable
```

### （4）切换工具链

```bash
rustup default stable
rustup default beta
rustup default nightly
```

## 4、卸载

```bash
rustup self uninstall
```

这条命令会卸载`rustup`自身，并移除`rustup`管理的Rust工具链、组件和相关工具。


# 四、rustc编译器

`rustc`是 Rust 官方提供的编译器，用于将Rust源程序，也就是`.rs`文件，编译成目标文件、可执行文件或库。它在使用风格上类似于`gcc`命令。

在实际项目开发中，我们通常使用更强大的`cargo`命令来构建Rust项目。`cargo`负责读取`Cargo.toml`文件、管理依赖、组织构建流程等。`cargo`底层实际调用`rustc`完成实际编译。因此，虽然日常开发中不一定直接使用`rustc`，但了解它的基本用法仍然很有必要。

## 1、查看版本

查看`rustc`的版本。

```bash
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

执行上述命令后，默认会生成一个可执行文件。在 macOS / Linux 上，默认生成名为 `main` 的文件；在 Windows 上，通常生成 `main.exe`。

结果：

![[Image 6.png|400]]

### （2）指定输出文件名

可以使用 `-o` 选项指定输出的可执行文件名：

```bash
rustc -o hello main.rs
```

![[Image 7.png|400]]

### （3）指定Edition

`Edition`是**Rust语言规则的一组版本集合**。Rust 目前支持 2015、2018、2021、2024 等 Edition。每个项目可以选择一个 Edition，编译器会按照对应 Edition 的规则解析和编译代码。

Rust需要同时满足**稳定性和进化性**。稳定性是指旧项目多年之后仍应能被新编译器编译运行；进化性是指语言本身需要继续改进，例如引入新语法、新关键字、新的宏规则、新的预导入内容。

如果只有一套语言规则，那么语言规则一旦变化，就可能导致旧项目在新编译器上无法编译。同一个 `rustc` 可以兼容多个 Edition。要让代码按照指定的 Edition 编译，可以使用 `--edition` 选项：

```bash
rustc main.rs --edition=2021
```

## 3、编译库

Rust 的编译产物不只有可执行文件，也可以是各种类型的库。

使用`rustc`编译库时，常见的一种输出格式是`rlib`。`rlib`是Rust使用的静态库格式，主要用于 Rust crate 之间的链接。这里简单介绍如何使用`rustc`编译并链接一个`rlib`库。

先编写两个源文件：`lib.rs` 和 `main.rs`。其中 `lib.rs` 是库源码，`main.rs` 是可执行文件源码，它会调用库中的函数。

lib.rs

```rust
pub fn hello() {
	println!("Hello, world!");
}
```

> 这里的`pub`关键字用于让 hello 函数对外可见。

main.rs

```rust
fn main() {
	greet::hello();
}
```

> 这里的 `greet`是 crate 名，也就是后面编译库时通过 `--crate-name` 指定的名称。 

### （1）编译 rlib 库

```bash
rustc --crate-type=rlib --crate-name=greet lib.rs
```

说明：

- `--crate-type`用于指定crate的类型，这里显式指定`rlib`

- `--crate-name`用于指定crate的名字，这里为`greet`。

编译完成后，当前目录会生成`libgreet.rlib`文件：

![[Image 8.png|500]]

### （2）链接rlib生成可执行文件

```bash
rustc -L . --extern greet=libgreet.rlib main.rs
```

说明：

- `-L .`表示将当前目录加入库搜索路径

- `--extern greet=libgreet.rlib`表示把`libgreet.rlib`作为名为`greet`的外部`crate`提供给当前编译单元。

执行完成后，会生成可执行文件。

![[Image 9.png|600]]

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

```bash
cargo new <project_name>
```

例如，创建 `hello_cargo` 项目：

```shell
cargo new hello_cargo
```

执行后，会在当前目录生成一个 `hello_cargo` 项目文件夹。

![[Image 10.png]]

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

打开Cargo.toml文件，内容类似如下：

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

其中：
- `[package]`是该包的基本信息，包括名字、版本、Edition等。除了默认生成的字段外，还可增加`description`、`license`、`authors`等其他信息。
- `[dependencies]`：用于声明项目依赖的第三方 crate，这是Cargo进行包管理的核心机制。详见[[#^package-manager|包管理]]。

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

```bash
cargo new --lib <project_name>
```

库项目的目录结构与二进制项目类似，区别是 `src` 目录下自动生成的是 `lib.rs` 文件，而不是 `main.rs` 文件。

`src/lib.rs` 内容类似如下：

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

其中，`#[cfg(test)]` 和 `#[test]` 是与测试相关的内容，后续可以再详细介绍。 ^d6141b

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

![[Image 11.png]]

## 4、构建并运行Cargo项目

执行`cargo build`只会构建项目，如果要运行程序，还需要手动执行生成的可执行文件。

Cargo 提供了 `cargo run`，可以一次完成“构建 + 运行”两个步骤：

```bash
cargo run
```

结果：

![[Image 12.png]]

`cargo run`默认也是调试构建。如果希望以发布模式构建并运行，可以使用：

```bash
cargo run --release
```

## 5、检查代码确保其可编译

Cargo 还提供了 `cargo check` 命令，用于快速检查代码是否可以通过编译：

```bash
cargo check
```

`cargo check`会执行类型检查、借用检查等编译检查工作，但不会生成最终的可执行文件，因此通常比`cargo build`更快。开发过程中，可以经常使用`cargo check`快速发现编译错误。

## 6、清理项目

`cargo clean` 用于删除 Cargo 生成的构建产物。通常来说，它会删除项目中的 `target` 目录。

命令如下：

```bash
cargo clean
```

## 7、测试

Cargo 还提供了 `cargo test` 用于运行测试。关于测试的内容较多，后续可以再具体介绍。^4420bb

命令如下：

```bash
cargo test
```

# 六、IDE环境

使用IDE或带插件的编辑器开发Rust项目会更加高效。这里推荐两种常见选择：`VS Code`和`RustRover`。

## 1、VS Code

`VS Code`是目前非常受欢迎的代码编辑器，可以用于开发多种语言的项目。通过安装 `Rust` 相关插件，`VS Code`也可以获得接近`IDE`的`Rust`开发体验。

在使用 `cargo new` 创建一个新项目并进入项目文件夹后，可以执行下面的命令用 VS Code 打开当前项目：

```bash
code .
```

如果终端提示 `code: command not found`，说明还没有把 VS Code 的 `code` 命令安装到 `PATH` 中。可以在 VS Code 中打开命令面板（`Command + P`），搜索`> Shell Command`并选择`Shell Command: Install 'code' command in PATH`：

![[Pasted image 20260511163624.png]]

打开项目后，还需要安装Rust相关插件。点击 VS Code 左侧栏的 Extensions，然后搜索并安装以下插件。

![[Image 13.png]]

- `rust-analyzer`：Rust 官方推荐的语言服务器插件，也是`VS Code`开发 Rust 的最核心插件。它可以提供代码补全、类型提示、错误诊断、跳转定义、查找引用、代码重构等。
- `Error Lens`：可以在错误、警告、提示信息直接显示在代码行旁边，让诊断信息更加醒目。它不是Rust专用插件。也不是必须插件，但对新手比较友好，可以直观地看到错误信息。

安装这些插件后，VS Code 就可以作为 Rust 开发环境使用。当输入代码的前几个字符时，VS Code 会自动弹出代码提示。出现提示后，可以按  `Tab` 或`Enter`接受补全。

![[Image 14.png]]

对于`Cargo`项目，`rust-analyzer`通常会在`main`函数、测试函数等位置上方显示`Run`和`Debug`按钮。

点击`Run`可以直接运行当前程序：

![[Image 15.png]]

点击`Debug`进入调试状态，如下图所示：

![[Image 16.png]]

关于调试相关概念，参考：[[1、调试|调试]]。

## 2、RustRover

`RustRover`是`JetBrains`推出的Rust专用IDE。相比`VS Code`，`RustRover`更接近“开箱即用”的完整IDE。安装后就内置了Rust项目开发的很多功能，例如代码补全、错误提示、Cargo集成、运行、测试、Git集成等。

如果已经使用`cargo new`创建了一个Rust项目，可以直接用`RustRover`打开项目目录。

![[Pasted image 20260511224024.png]]

打开项目后，`RustRover`会识别项目中的`Cargo.toml`文件，并将该目录作为一个`Cargo`项目加载。前面已经说过，`Cargo.toml`是`Cargo`项目的核心配置文件，因此`RustRover`通常以它为入口识别项目结构。

当然，也可以新建项目：

![[Pasted image 20260511224649.png]]

![[Pasted image 20260511224814.png]]

![[Pasted image 20260511224856.png]]

下面简单介绍几个功能：

1. 代码补全与错误提示

`RustRover`内置Rust代码分析能力，可以提供常见IDE功能，如代码补全、类型提示、错误提示、跳转定义、查找引用、快速修复等。

例如，在编辑 `main.rs` 时，输入代码的前几个字符，RustRover 会自动弹出补全提示。选择候选项后，可以按 `Enter` 或 `Tab` 接受补全。

如果代码中存在语法错误、类型错误或借用检查相关问题，RustRover 会在编辑器中直接标记出来，并在部分场景下提供 quick fix，也就是快速修复建议。

2. Cargo工具窗口

`RustRover`对`Cargo`有内置支持。打开 Cargo 项目后，可以在 IDE 侧边栏看到 Cargo 工具窗口。如果没有，需要从菜单中通过`View → Tool Windows → Cargo` 打开。

![[Pasted image 20260511225507.png]]

Cargo 工具窗口中通常可以看到项目中的：

- bin target  
- lib target  
- test target  
- example target  
- benchmark target

你可以在终端执行`cargo`命令运行对应目标，也可以在`Cargo`工具窗口中运行目标。

3. 运行代码

在`RustRover`中运行Rust程序很方便。打开 `src/main.rs` 后，通常可以在 `main` 函数左侧看到绿色运行按钮。点击该按钮，可以选择运行当前程序。也可以使用顶部工具栏的运行按钮，或者使用快捷键运行。

![[Pasted image 20260511230042.png]]

4. 调试代码

`RustRover` 内置调试功能。`RustRover`提供完整调试器，支持断点、变量查看、单步执行、内存视图和反汇编视图等功能。

使用方式如下：

1. 在代码行号左侧点击，设置断点；
2. 点击 `main` 函数左侧的运行图标；
3. 选择 `Debug`；
4. 程序运行到断点处会暂停；
5. 可以在 Debug 窗口中查看变量、调用栈，并进行单步执行。

![[Pasted image 20260511231034.png]]



# 七、包管理 ^package-manager

`Cargo`不只是Rust的构建工具，也是Rust的包管理工具。

在Rust中，一个可复用的代码包通常称为`crate`。开发者可以把自己的 `crate` 发布到 [crates.io](https://crates.io/)，其他项目则可以通过 `cargo` 引入并使用这些 `crate`。

`Cargo`的包管理主要围绕两个文件展开：

- `Cargo.toml`：项目配置文件，用于声明项目的基本信息和依赖关系。例如项目名称、版本、Edition，以及需要使用哪些第三方 crate。
- `Cargo.lock`：`Cargo`自动生成的依赖锁定文件，用于记录当前项目实际解析出来的精确依赖版本。它可以保证项目在不同机器上构建时尽量使用相同的依赖版本，从而提高构建结果的一致性。

通常来说，开发者主要手动编辑的是 `Cargo.toml`，而 `Cargo.lock` 由 Cargo 自动生成和维护，一般不需要手动修改。

## 1、增加依赖

假如现在想在项目中使用随机数，可以添加`rand`crate。在 [crates.io](https://crates.io/) 中搜索 `rand`，如下：

![[Pasted image 20260511232736.png]]

![[Pasted image 20260511232803.png]]

`rand` 主页右侧给出了安装该`crate`的方式，一个是使用`cargo add`命令增加（马上介绍），一个就是在`Cargo.toml`的`[dependencies]`下添加`rand = "0.10.1"`（`"0.10.1"`是版本）。

打开项目根目录下的`Cargo.toml`，添加如下：

```toml
[package]  
name = "hello_cargo"  
version = "0.1.0"  
edition = "2024"  
  
[dependencies]  
rand = "0.10.1"
```
![[Image 17.png.png]]

保存 `Cargo.toml` 后，Cargo 会在后续执行构建命令时自动解析并下载依赖，例如执行：

```shell
cargo build
```

> 依赖下载后，相关 crate 的源码默认会缓存到用户家目录下的 `.cargo` 目录中，例如`~/.cargo/registry/src/`。如果配置了镜像源，例如 rsproxy，那么上层目录名可能会显示为对应镜像源或索引地址相关的名称。这是 Cargo 的正常缓存机制，如`~/.cargo/registry/src/rsproxy.cn-e3de039b2554c837`。

添加依赖后，可以在代码中使用 `rand`：

```Rust
use rand::RngExt;  
  
fn main() {  
      
    // 创建一个 1~10 之内的随机数  
    let number = rand::rng().random_range(1..=10);  
    println!("随机数是： {}", number);  
}
```

结果：

![[Pasted image 20260511233913.png]]

此时还可以发现，项目目录下通常会多出一个 `Cargo.lock` 文件。该文件用于**记录当前项目实际使用到的所有 crate 版本及其依赖版本**，由 Cargo 自动生成和管理，一般不需要手动修改。

`Cargo.toml`记录的是“你希望使用什么依赖”，而`Cargo.lock`记录的是“Cargo实际解析出了哪些精确版本“。

例如，项目依赖A、B两个库，而A和B又都依赖C。Cargo 会根据版本规则选择一个合适的 C 版本，并把最终解析结果写入 `Cargo.lock`。

这样做的好处是：只要提交了 `Cargo.lock`，别人再次构建项目时，就会尽量使用同一组依赖版本，从而提高构建结果的一致性和可复现性。

对于二进制应用项目，建议提交 `Cargo.lock`。

对于库项目，是否提交 `Cargo.lock` 要看项目习惯和使用场景；如果是发布到 crates.io 的库，最终使用者主要根据 `Cargo.toml` 重新解析依赖。

## 2、cargo add

除了手动修改 `Cargo.toml` 添加依赖外，也可以在命令行中使用 `cargo add` 命令添加依赖。

`cargo add` 是 Cargo 的依赖管理命令之一，用于将依赖添加到 `Cargo.toml` 的 `[dependencies]`、`[dev-dependencies]` 或 `[build-dependencies]` 等依赖区域中，并更新 `Cargo.lock` 文件。
### （1）基本使用

例如添加 `rand`：

```bash
cargo add rand
```

执行后，Cargo 会自动在 `Cargo.toml` 的 `[dependencies]` 中添加类似内容：

```toml
[dependencies]  
rand = "0.10.1"
```

具体版本号会根据当前 crates.io 上的最新版本而变化。同时，Cargo 也会更新 `Cargo.lock`，记录实际解析出来的依赖版本。

### （2）指定版本

可以使用 `crate@version` 的形式指定版本要求。`cargo add` 支持使用 `crate@version` 从 registry 添加指定版本约束的依赖。

```bash
cargo add rand@0.10.1
```

这会在 `Cargo.toml` 中添加类似内容：

```
[dependencies]rand = "0.10.1"
```

需要注意，这里的 `"0.10.1"` 在 Cargo 中默认是 **caret requirement**（^），也就是兼容版本要求，不是绝对固定到 `0.10.1`。

如果想写成精确的版本，可以使用：

```shell
cargo add rand@=0.10.1
```

对应 `Cargo.toml` 类似：

```
[dependencies]rand = "=0.10.1"
```

### （3）语义化版本范围

`Cargo`支持多种版本要求写法，最常见的是 `caret requirement` 和 `tilde requirement`。

- `caret requirement`

示例：

```shell
cargo add serde@^1.0
```

一般来说，`^1.2.3`表示`>=1.2.3, <2.0.0`。

对于`0.x`版本，规则更保守：

- `^0.3.5` 表示 `>=0.3.5, <0.4.0`
- `^0.0.5` 表示 `>=0.0.5, <0.0.6`

大多数情况下使用`caret requirements`，例如 `"1.2.3"` 这种默认就是`^1.2.3`，因为这样既保持兼容性，又给依赖解析器保留足够灵活性。

- `tilde requirement`

示例：

```shell
cargo add serde@~1.0
```

`~`表示允许较小范围内的版本更新。`~1.2.3`表示`>=1.2.3, <1.3.0`，`~1.2`表示`>=1.2.0, <1.3.0`，`~1`表示`>=1.0.0, <2.0.0`。

### （4）启用feature

Rust 库普遍追求**最小默认依赖**、**较快编译速度**和**较小体积**。因此，很多库作者会把不是所有用户都需要的功能放到`feature`中。

在代码层面，`feature`常见写法如下：

```Rust
#[cfg(feature = "foo")]
pub fn foo() {
	// ...
}
```

如果没有启用`foo` feature，那么这段代码不会被编译，对调用方来说就像不存在一样。

以`serde`为例，如果想启用它的 `derive` feature，可以执行：

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

```
[dependencies]tokio = { version = "1", features = ["rt-multi-thread", "macros"] }
```

### （5）增加不同依赖

- **普通依赖**：增加到`[dependencies]`

默认情况下，`cargo add`会把依赖添加到`[dependencies]`：

```bash
cargo add anyhow
```

普通依赖会参与项目的正常构建，是库或二进制程序运行时通常需要的依赖。

- **开发依赖**：添加到`dev-dependencies`

开发依赖主要用于测试、基准测试、示例等开发阶段场景：

```bash
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

- **构建依赖**：添加到`[build-dependencies]`

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

- 编译C/C++代码并链接进Rust
- 自动生成Rust代码，例如从 proto / IDL / 模板生成
- 检测系统库是否存在
- 读取环境变量
- 决定链接参数

## 3、cargo remove

使用 `cargo remove` 可以从 `Cargo.toml` 中移除依赖。Cargo 官方文档说明，`cargo remove` 用于从 `Cargo.toml` manifest 中移除一个或多个依赖，并支持 `--dev`、`--build` 等选项。

- 移除普通依赖

	```shell
	cargo remove serde 
	```

- 移除开发依赖

```shell
cargo remove --dev pretty_assertions 
```

- 移除构建依赖

```shell
cargo remove --build cc 
```
