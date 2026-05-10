# 一、Rust简介

Rust 语言在 2006 年作为 Mozilla员工 `Graydon Hoare`（格雷登·霍尔）的私人项目出现，Mozilla 于2009年开始赞助该项目。第一个有版本的 Rust 编译器于2012年1月发布。 **Rust 1.0 作为第一个稳定版本于 2015年5月15日 发布** 。

相比于 C/C++ 语言，Rust 具有如下优点：

**内存安全：** Rust的所有内存访问都经过了编译器的严格检查，因此运行时不会出现空指针访问、数据竞争等问题。

**性能高效：** Rust具有与C/C++相当的性能

**并发安全：** 所有权系统和借用规则使得Rust非常适合编写线程安全的代码

**社区支持：** Rust拥有活跃的社区，在 [https://crates.io/](https://crates.io/) 上提供了很多开源库、工具和框架，可以大幅提升开发效率

**统一包管理**：C/C++最令人诟病的就是包管理，如果想要使用一个库，需要自己下载、安装和配置。Rust提供了统一的包管理程序`cargo`，只需在`Cargo.toml`中增加一行代码，即可自动下载、安装和配置包，还提供对应的文档，便于开发者理解。

# 二、安装Rust

## 1、安装rustup

与C/C++一样，Rust也是**编译型语言**，因此Rust源代码（`.rs`）需要编译成二进制可执行程序才能运行。

进入Rust官网 [https://rust-lang.org/](https://rust-lang.org/) ，点击上方的install，如下图所示：

![[Image.png]]

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

需要设置两个环境变量，本机`macOS`上默认使用的是`zsh`shell，因此`~/.zshrc`中添加：

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

修改配置文件`~/.cargo/config.toml`，已支持git协议和sparse协议，>=1.68 版本建议使用 sparse-index，速度更快。

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

> 现在 `rustup update`也会在更新toolchain的自动检查并更新`rustup`自身

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

该命令可以查看当前 Rust 安装状，包括：
- 当前目标平台
- 已安装的工具链（`installed toolchains`）
- 当前正在使用的工具链（`active toolchain`）

![[Image 5.png]]

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

这条命令会卸载`rustup`自身、并移除`rustup`管理的Rust工具链、组件和相关工具。

# 四、rustc编译器

rustc是Rust官方提供的编译器，用于将Rust源程序（.rs）编译成目标文件、可执行文件或库。其在使用风格上类似于gcc命令。尽管项目开发中通常使用强大的cargo命令来构建Rust项目，但cargo底层实际上调用的就是rustc命令来构建代码的，因此，有必要对rustc有一定的了解。

## 1、查看版本

查看rustc的版本。

```bash
rustc --version
```
## 2、最基本用法（生成可执行文件）

下面给出最简单的Rust程序，用于打印Hello, world!。

```rust
fn main() {

println!("Hello, world!");

}

（1）默认输出
```
```bash
rustc main.rs
```
执行上述命令后，默认生成名为main（MacOS或Linux）或main.exe（Windows）的可执行文件。

结果：

![[Image 6.png]]

（2）指定输出文件名

使用-o选项指定输出的可执行文件名。
```bash
rustc -o hello main.rs
```
![[Image 7.png]]

（3）指定edition

Edition（版本纪元）是Rust语言规则的一组“可选版本包”。同一门Rust语言下，编译器支持多套规则：2015 / 2018 / 2021 / 2024...，每个项目需要选择一个Edition，编译器按该规则解析与编译代码。

Rust需要同时满足稳定性和进化性，稳定性是指旧项目在多年之后仍应能编译运行，进化性要求语言要改进（语法糖、关键字、宏、预导入等）。如果只有一套规则，改规则就导致旧项目在新编译器上不可用。为此，Edition的作用就是让新规则可选，旧项目仍然按照旧规则编译。

同一个rustc同时兼容多个Edition，要让代码按照指定的Edition规则编译，通过–edition选项来指定。

示例：
```bash
rustc main.rs --edition=2021
```
## 3、编译库

Rust编译产物不止可执行文件，还可以是各种库类型。

rustc编译库时默认产生的是Rust自用的rlib格式库，因此这里也只简单介绍rlib库的编译。

先编写两个源文件：main.rs和lib.rs。其中lib.rs为库文件源码，main.rs是可执行文件源码，它将调用库中的函数。

lib.rs

```rust
pub fn hello() {

println!("Hello, world!");

}
```
注：pub关键字用于让hello函数对外可见。

main.rs
```rust
fn main() {

greet::hello();

}
```
注：greet是crate名，是后面即将编译的库名。

编译过程：

（1）编译rlib库
```bash
rustc --crate-type=rlib --crate-name=greet lib.rs
```
说明：

--crate-type用于指定crate的类型，这里显式指定rlib

--crate-name用于指定crate的名字，这里为greet。

编译完成后，当前目录会生成libgreet.rlib文件，如下所示：

![[Image 8.png]]

（2）链接rlib进二进制可执行文件
```bash
rustc -L. --extern greet=libgreet.rlib main.rs
```
说明：

-L. 表示将当前目录作为库路径的搜索目录

--extern greet=libgreet.rlib表示以greet作为crate名将libgreet.rlib注入当前编译单元。

结果：

![[Image 9.png]]
# 五、Cargo

## 1、Cargo概述

直接使用rustc编译一个个Rust源码文件费时费力，项目开发中常使用cargo，它是Rust的构建工具和包管理工具。在安装rustup之后，会一并安装cargo的最新stable版本。使用cargo，可以构建代码，下载，编译依赖库等。在构建代码时，cargo底层隐式调用了rustc进行编译。

通过cargo，可以做如下事情：

cargo new新建项目

cargo build构建项目

cargo run构建并运行项目

cargo check检查项目是否可编译但不构建

cargo test进行测试

cargo doc构建项目文档

cargo clean清理项目

...

## 2、创建Cargo项目

### （1）创建二进制可执行项目

命令：

```bash
cargo new <project_name>
```
例如，创建hello_cargo项目，执行cargo new hello_cargo后，会在当前目录生成一个hello_cargo项目文件夹，进入项目文件夹里，看到：

![[Image 10.png]]

在hello_cargo目录下，自动生成了一个.git目录、.gitignore文件、Cargo.toml文件以及src目录，在src目录下包含一个main.rs源文件，目录结构如下：
```text
hello_cargo/

├──.git/ # Git仓库目录（自动生成）

├──.gitignore # Git忽略文件

├── Cargo.toml # Cargo 项目配置文件

└── src/

└── main.rs # Rust 主程序源文件

cargo默认会将生成的项目纳入Git版本控制，如果不想使用Git版本控制系统（vcs），在执行cargo new时可以加上--vcs=none选项。
```
打开Cargo.toml文件，内容如下：
```toml
[package]

name = "hello_cargo"

version = "0.1.0"

edition = "2024"

[dependencies]

[package]是该包的基本信息，包括名字（name）、版本（version）、版本纪元（edition）等。除了上述默认生成的，还有其他信息，例如描述（description）等。

[dependencies]是项目依赖的第三方库（crate），这是Cargo进行包管理的核心机制，后续会详细介绍。
```
进入src目录，里面有一个自动生成的main.rs文件，内容如下：
```rust
fn main() {

println!("Hello, world!");

}

main.rs是整个项目的入口文件。
```
说明：

fn是Rust的关键字，用于定义函数，后面紧跟函数名

main是函数名称（这里不可更改，因为是整个程序的入口函数）

println!是Rust的一个宏，用于简化输出一个字符串到控制台的步骤
### （2）创建库项目

除了可以创建二进制可执行项目，还可以创建库项目。库项目与二进制项目的最大区别就是库项目没有main函数，因此无法执行。cargo new通过--lib选项指定生成库项目，命令如下：

```bash
cargo new --lib project_name
```
库项目的目录结构与二进制项目类似，区别是src目录下自动生成的是lib.rs文件，内容如下：
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
其中相关的#[cfg(test)]和#[test]是和测试相关的内容，后续介绍。
## 3、构建Cargo项目

在创建好的Cargo项目的任意目录执行cargo build以构建项目：

```bash
cargo build
```
对于二进制项目，执行cargo build会生成可执行文件，默认位于项目顶层目录的target/debug目录。由于cargo build默认是调试构建（debug build），因此可执行文件位于debug目录。

项目最终准备发布时，执行cargo build加上--release选项则进行发布构建（release build）：
```bash
cargo build --release
```
发布构建生成的可执行文件位于项目顶层目录的target/release目录。

调试构建和发布构建：

调试构建：构建时几乎不做任何优化（opt-level=0），编译速度快，可执行文件体积大，运行速度慢。调试构建包含完整的调试符号，更容易触发边界检查，panic信息更完整。

发布构建：构建时进行高级别优化（opt-level=3），编译速度慢，可执行文件体积小，运行速度快。调试符号较少，不适合调试，优化 panic 处理等性能相关设置。

构建完成后，就可以运行生成的可执行文件了。依然使用之前的hello_cargo项目，以调试构建为例，运行如下：

![[Image 11.png]]
## 4、构建并运行Cargo项目

执行cargo build仅仅是构建项目，需要手动运行可执行文件。因此Cargo提供了cargo run来实现上述两步操作：

```bash
cargo run
```
结果：

![[Image 12.png]]

同样地，cargo run默认也是调试构建，使用--release选项则进行发布构建：
```bash
cargo run --release
```
## 5、检查代码确保其可编译

Cargo还提供了cargo check命令用于检查代码是否可编译，它不会进行实际编译构建。实际编译往往耗时较长，通过cargo check可以快速检查代码正确与否，提高开发效率。

命令如下：

```bash
cargo check
```
## 6、清理项目

cargo clean用于删除cargo生成的所有构建产物，让项目回到只剩源码的初始状态。具体来说就是删除target目录。

命令如下：

```bash
cargo clean
```
## 7、测试

Cargo还提供了cargo test用于代码测试，关于测试的内容较多，后续再具体介绍。

命令如下：

```bash
cargo test
```
# 六、IDE环境

使用IDE开发Rust项目会非常高效，推荐两款IDE软件：VS Code和RustRover。

## 1、VS Code

VS Code是目前非常受欢迎的一个编辑器，它可以用来开发各种语言的项目。

在cargo new一个新项目并进入项目文件夹，执行code .命令可以用VS Code打开该项目：

```bash
code .
```
不过，VS Code只是一个编辑器，要开发Rust项目，还需要安装Rust插件，来打造该编辑器成为一个IDE。方法很简单，只需要在VS Code左侧栏点击插件选项，搜索安装如下插件即可：

![[Image 13.png]]

rust-analyzer：提供很多增强Rust编程体验的功能，如代码补全、类型推导、错误提示等功能。

Error Lens：将错误警告内嵌显示在代码里，

至此，就完成了VS Code Rust开发环境的配置。现在，输出前几个字符时，就会自动弹出代码提示：

![[Image 14.png]]

这时，只需按 `Enter` 键就可以自动填充代码。

运行代码的方式也变得很简单，只需要点击main函数上面的Run按钮，就可以直接运行：

![[Image 15.png]]

也可以直接点击Debug进入调试状态：

![[Image 16.png]]
## 2、RustRover（待补充）

# 七、包管理

## 1、增加依赖

例如想使用ferris-says crate，在Cargo.toml文件的[dependencies]项添加一下这个库：

![[Image 17.png]]

后面这个数字是库的版本号，这个版本号可以去 [https://crates.io/](https://crates.io/) 网站上搜索库获取，如下所示：

![[Image 18.png]]

Ctrl+S保存后，VS Code就会自动拉取这个包到本地。实际上，ferris_says这个库的安装位置默认在家目录的.cargo目录下。

![[Image 19.png]]

至于库代码的上层目录，则是仓库名，因为这里换了镜像源rsproxy，原本可能是github之类的。

此时还可以发现，在项目目录下多了一个Cargo.lock文件，该文件用于记录当前项目用到的所有crate及其依赖，由Cargo自动管理，一般无需关心。

Cargo.lock文件主要用于锁定某个库版本。例如，项目依赖A、B两个库，而A和B两个库又都依赖C这个库，此时由Cargo.lock选择C库的版本。Rust编译器会根据规则指定此时C库的版本，并将其写入Cargo.lock文件中。这样做的好处是只要程序在本地可以编译成功，将这个Cargo.lock文件发给别人，别人也一定能编译成功，因为此时依赖包是完全一样的。相反，如果不发Cargo.lock文件，只发源码和项目配置文件，实际别人编译的程序和当前本地编译的程序所依赖的包版本不一定相同，这在需要多人合作开发的大型项目中需要额外注意。

## 2、cargo add

除了在Cargo.toml中手动增加依赖的库以外，还可以在命令行执行cargo add命令。

cargo add是Cargo的依赖管理命令之一，用于将依赖增加到Cargo.toml 的[`dependencies]（` 或其它依赖区）中，并自动更新Cargo.lock文件。

### （1）基本使用

```bash
cargo add ferris-says
```
效果等价于在 `Cargo.toml` 中加：
```text
[dependencies]

ferris-says = "0.3.2"
```
并更新 `Cargo.lock` 。
### （2）指定版本

指定精确版本

```bash
cargo add ferris-says@0.3.2
```
指定语义化范围版本

示例1：
```bash
cargo add serde@^1.0

^X.Y.Z表示>=X.Y.Z, <(X+1).0.0
```
注意0.x版本是例外：
```text
^0.3.5 ⇒ >=0.3.5, <0.4.0

^0.0.5 ⇒ >=0.0.5, <0.0.6
```
示例2：
```bash
cargo add serde@~1.0

~X.Y.Z表示>=X.Y.Z, < X.(Y+1).Z
```
### （3）启用features

Rust库普遍追求最小默认依赖、最快编译和最小体积。因此很多库作者会把不是所有人都会用到的功能放进feature里。在代码层面设置如下：

```rust
#[cfg(feature = "foo")]

pub fn foo() {

//...

}
```
如果没有启用foo feature，那么上述代码不会被编译且不能调用，编译器当作不存在。

以serde库为例，想要启用其derive feature，执行：
```bash
cargo add serde --features derive
```
在Cargo.toml，对应如下：
```toml
serde = { version = "1", features = ["derive"] }
```
如果要指定多个feature，通过逗号隔开多个feature，示例如下：
```bash
cargo add tokio --features rt-multi-thread,macros
```
### （4）增加不同依赖

**1） 增加普通依赖：默认情况下加到[dependencies]**

示例：

```bash
cargo add anyhow
```
**2）增加开发依赖：测试/基准用，增加到[dev-dependencies]**
```bash
cargo add pretty_assertions --dev
```
**3）增加构建依赖（build.rs），增加到[build-dependencies]**
```bash
cargo add cc --build
```
**开发依赖（dev-dependencies）:**

只在开发阶段需要，典型场景是：

跑测试：cargo test

跑基准：cargo bench

...

其特点是不会在库/二进制的正常构建与运行带上，即cargo build / cargo run一般不需要这些依赖。

**构建依赖（build-dependencies）:**

只在构建阶段需要，而且通常是给 **build.rs** 用的。

Cargo支持在编译crate之前先运行一个构建脚本，如build.rs，用来做编译前准备工作，常见用途：

编译C/C++代码并链接进Rust

自动生成 Rust 代码（从 proto/idl/模板生成）

检测系统库是否存在、读取环境变量、决定链接参数

...
## 3、cargo remove

使用 **cargo remove** 移除依赖。

示例：

```bash
cargo remove serde // 移除普通依赖

cargo remove pretty_assertions --dev // 移除开发依赖

cargo remove cc --build // 移除构建依赖
```
