# 一、简介

`clap`是 Rust 常用的命令行参数解析 crate，用于把终端输入的参数解析成 Rust 中的结构体、枚举和字段值。它支持位置参数、选项参数、布尔标志、默认值、子命令、自动帮助信息和参数校验。

`clap` 同时提供 `derive` API 和 `builder` API，快速入门阶段优先使用 `derive` API，即通过派生宏自动实现相关 Trait 。

例如命令行输入：

```shell
myapp input.txt --output result.txt --verbose
```

可以解析成类似这样的 Rust 数据：

```rust
Cli {
    input: "input.txt",
    output: Some("result.txt"),
    verbose: true,
}
```

常见能力：

| 能力   | 示例                     |
| ---- | ---------------------- |
| 位置参数 | `myapp input.txt`      |
| 长选项  | `--output result.txt`  |
| 短选项  | `-o result.txt`        |
| 布尔标志 | `--verbose`            |
| 默认值  | 不传参数时使用默认配置            |
| 子命令  | `git add`、`git commit` |
| 枚举参数 | `--format json`        |
| 自动帮助 | `--help`、`--version`   |


# 二、安装依赖

新建项目：

```shell
cargo new clap-demo
cd clap-demo
```

添加依赖：

```shell
cargo add clap --features derive
```

`derive` 功能用于启用 `#[derive(Parser)]`、`#[derive(Subcommand)]`、`#[derive(Args)]`、`#[derive(ValueEnum)]` 这类宏。

`Cargo.toml`中大致是：

```toml
[dependencies]  
clap = { version = "4.6.1", features = ["derive"] }
```


# 三、最小示例

先写一个只接收文件名的CLI：

```rust
use clap::Parser;  
  
#[derive(Parser, Debug)]  
struct Cli {  
    /// 要处理的文件路径  
    file: String  
}  
  
  
fn main() {  
    let cli = Cli::parse();  
  
    println!("file: {}", cli.file)  
}
```

运行：

```shell
cargo run -- hello.txt
```

输出：

```text
file: hello.txt
```

这里的核心关系是：

| 写法                  | 作用                |
| ------------------- | ----------------- |
| `use clap::Parser;` | 引入 `Parser` trait |
| `#[derive(Parser)]` | 让结构体具备命令行解析能力     |
| `Cli::parse()`      | 从当前进程参数中解析出 `Cli` |
| `file: String`      | 一个必填位置参数          |

`Parser::parse()`会从当前进程的命令行参数中解析数据；解析失败时会打印错误并退出程序。

查看帮助信息：

```shell
cargo run -- --help
```

输出：

![[assets/Pasted image 20260604181114.png|200]]

**字段上的文档注释会进入帮助信息**，所以 `/// 要处理的文件路径` 会显示在 `<FILE>` 后面。


# 四、命令基本信息

可以通过`#[command(...)]`配置命令名称、版本和说明。

```rust
use clap::Parser;

#[derive(Parser, Debug)]
#[command(name = "rgrep")]
#[command(version = "0.1.0")]
#[command(about = "A tiny grep-like command line tool")]
struct Cli {
    /// Pattern to search
    pattern: String,

    /// File to read
    file: String,
}

fn main() {
    let cli = Cli::parse();

    println!("pattern = {}", cli.pattern);
    println!("file = {}", cli.file);
}
```

查看版本：

```shell
cargo run -- --version
```

输出：

```text
rgrep 0.1.0
```

查看帮助：

```shell
cargo run -- --help
```

输出：

![[assets/Pasted image 20260604181907.png|200]]


# 五、位置参数、选项和标志

## 1、位置参数

位置参数不带`--`或`-`，依靠出现顺序解析。

```rust
use clap::Parser;  
  
#[derive(Parser, Debug)]  
struct Cli {  
    /// Search pattern  
    pattern: String,  
  
    /// Input file  
    file: String  
}  
  
  
fn main() {  
    let cli = Cli::parse();  
  
    println!("{:?}", cli);  
}
```

运行：

```shell
cargo run -- hello input.txt
```

输出：

```text
Cli { pattern: "hello", file: "input.txt" }
```

`hello` 绑定到 `pattern`，`input.txt` 绑定到 `file`。

## 2、选项参数

选项参数通常写成`--name value`或`-n value`。

```rust
use std::path::PathBuf;  
use clap::Parser;  
  
#[derive(Parser, Debug)]  
struct Cli {  
  
    file: PathBuf,  
  
    #[arg(short, long)]  
    output: Option<PathBuf>,  
}  
  
  
fn main() {  
    let cli = Cli::parse();  
  
    println!("{:?}", cli);  
}
```

运行：

```shell
cargo run -- input.txt --output result.txt
```

也可以写成：

```shell
cargo run -- input.txt -o result.txt
```

输出类似：

```text
Cli { file: "input.txt", output: Some("result.txt") }
```

`#[arg(short, long)]` 会同时生成短选项和长选项：

```shell
-o result.txt
--output result.txt
```

`Option<PathBuf>` 表示这个选项可以不传。


## 3、布尔标志

布尔标志表示开关，不需要额外传值。

```rust
use clap::Parser;  
  
#[derive(Parser, Debug)]  
struct Cli {  
    /// Enable verbose output  
    #[arg(short, long)]  
    verbose: bool,  
}  
  
  
fn main() {  
    let cli = Cli::parse();  
  
    println!("{:?}", cli);  
}
```

运行：

```shell
cargo run -- --verbose
```

或：

```shell
cargo run -- -v
```

输出：

```text
Cli { verbose: true }
```

不传时：

```shell
cargo run --
```

输出：

```text
Cli { verbose: false }
```


# 六、默认值和可选参数

## 1、默认值

字符串默认值可以使用`default_value`。

```rust
  
use clap::Parser;  
  
#[derive(Parser, Debug)]  
struct Cli {  
	/// Server host
    #[arg(long, default_value = "127.0.0.1")]  
    host: String,
    
}  
  
  
fn main() {  
    let cli = Cli::parse();  
  
    println!("{:?}", cli);  
}
```

运行：

```shell
cargo run --
```

输出：

```
Cli { host: "127.0.0.1" }
```

数字、布尔值、枚举等类型更适合使用 `default_value_t`：

```rust
use clap::Parser;  
  
#[derive(Parser, Debug)]  
struct Cli {  
    /// Server host  
    #[arg(long, default_value = "127.0.0.1")]  
    host: String,  
  
    /// Server port  
    #[arg(long, default_value_t = 8000)]  
    port: u16  
}  
  
  
fn main() {  
    let cli = Cli::parse();  
  
    println!("{:?}", cli);  
}
```

运行：

```shell
cargo run --
```

输出：

```text
Cli { host: "127.0.0.1", port: 8000 }
```


## 2、Option\<T>和默认值的区别

| 写法                                      | 含义       | 适合场景        |
| --------------------------------------- | -------- | ----------- |
| `name: T`                               | 必须传      | 程序运行必须依赖该参数 |
| `name: Option<T>`                       | 可传可不传    | 参数本身是可选信息   |
| `#[arg(default_value_t = ...)] name: T` | 不传时使用默认值 | 参数有合理默认配置   |
例如：

```rust
#[arg(long)]
output: Option<PathBuf>
```

表示用户不一定要指定输出文件。

```rust
#[arg(long, default_value_t = 8080)]
port: u16
```

表示用户不传端口时使用 `8080`。


# 七、多值参数和计数标志

## 1、多次出现的参数

如果同一个参数可以出现多次，可以使用`Vec<T>`。

```rust
use clap::Parser;  
  
#[derive(Parser, Debug)]  
struct Cli {  
    /// Include paths  
    #[arg(short = 'I', long)]  
    include: Vec<String>  
}  
  
  
fn main() {  
    let cli = Cli::parse();  
  
    println!("{:?}", cli);  
}
```

运行：

```shell
cargo run -- -I src -I tests --include examples
```

输出：

```
Cli { include: ["src", "tests", "examples"] }
```

## 2、统计标志出现的次数

`-v`、`-vv`、`-vvv`这类写法可以用`ArgAction::Count`统计。

```rust
  
use clap::Parser;  
use clap::ArgAction;  
  
#[derive(Parser, Debug)]  
struct Cli {  
    /// Increase log verbosity  
    #[arg(short, long, action = ArgAction::Count)]  
    verbose: u8,  
}  
  
  
fn main() {  
    let cli = Cli::parse();  
  
    println!("{:?}", cli);  
}
```

运行：

```shell
cargo run -- -vvv
```

输出：

```
Cli { verbose: 3 }
```


# 八、枚举参数

如果参数只能从固定值中选择，可以使用`ValueEnum`。

```rust
use clap::{Parser, ValueEnum};  
  
#[derive(Parser, Debug)]  
struct Cli {  
      
    /// Output format  
    #[arg(long, value_enum, default_value_t = Format::Text)]  
    format: Format,  
}  
  
  
#[derive(Debug, Clone, ValueEnum)]  
enum Format {  
    Text,  
    Json,  
    Markdown  
}  
  
  
  
fn main() {  
    let cli = Cli::parse();  
  
    println!("{:?}", cli);  
}
```

运行：

```shell
cargo run -- --format json
```

输出：

```text
Cli { format: Json }
```

查看帮助：

```shell
cargo run -- --help
```

可以看到可选值：

![[assets/Pasted image 20260604214530.png|500]]

`ValueEnum`用于把命令行参数解析为枚举值；字段配合`#[arg(value_enum)]`后，输入值会被限制在枚举可选项内。

默认情况下，枚举变体会转换成命令行常见的 kebab-case：

```rust
enum OutputFormat {
    PlainText,
    PrettyJson,
}
```

命令行中对应：

```
plain-text
pretty-json
```

> kebab-case 表示所有单词小写，单词之间用连字符隔开。


# 九、子命令

子命令适合表达类似`git add`、`git commit`、`cargo build`这样的命令结构。

```rust
use clap::{Parser, Subcommand};

#[derive(Parser, Debug)]
#[command(name = "todo")]
#[command(version, about = "A tiny todo CLI")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Add a new todo item
    Add {
        /// Todo text
        text: String,
    },

    /// List todo items
    List,

    /// Remove a todo item
    Remove {
        /// Todo id
        id: u32,
    },
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::Add { text } => {
            println!("add todo: {text}");
        }
        Commands::List => {
            println!("list todos");
        }
        Commands::Remove { id } => {
            println!("remove todo: {id}");
        }
    }
}
```

运行：

```shell
cargo run -- add "learn clap"
```

输出：

```text
add todo: learn clap
```

运行：

```shell
cargo run -- remove 1
```

输出：

```text
remove todo: 1
```

`Subcommand` 用来把子命令解析到枚举中；父级结构体通过 `#[command(subcommand)]` 接收子命令。

如果子命令不是必填，可以写成：

```rust
#[command(subcommand)]  
command: Option<Commands>,
```

这样用户不传子命令时，程序可以自己处理默认逻辑：

```rust
use clap::{Parser, Subcommand};  
  
  
const ABOUT: &str = "a tiny todo CLI";  
  
  
#[derive(Parser, Debug)]  
#[command(name = "todo")]  
#[command(version, about = ABOUT)]  
struct Cli {  
    #[command(subcommand)]  
    command: Option<Commands>  
}  
  
  
#[derive(Debug, Subcommand)]  
enum Commands {  
    /// Add a new todo item  
    Add {  
        /// Todo text  
        text: String,  
    },  
  
    /// List todo items  
    List,  
  
    /// Remove a todo item  
    Remove {  
        /// Todo id  
        id: u32  
    }  
  
  
}  
  
  
  
fn main() {  
    let cli = Cli::parse();  
  
    match cli.command {  
        Some(Commands::Add { text }) => {  
            println!("add todo: {text}");  
        }  
        Some(Commands::List) => {  
            println!("list todos");  
        }  
        Some(Commands::Remove { id }) => {  
            println!("remove todo: {id}")  
        }  
        None => {  
            println!("{ABOUT}");  
        }  
    }  
  
}
```

结果：

```text
a tiny todo CLI
```

# 十、复用参数组

多个子命令共享同一组参数时，可以使用`Args`抽取公共参数，再通过`flatten`合并进去。

```rust
use clap::{Args, Parser, Subcommand};  
  
  
#[derive(Parser, Debug)]  
struct Cli {  
  
    #[command(subcommand)]  
    command: Command,  
}  
  
  
#[derive(Subcommand, Debug)]  
enum Command {  
    Serve(ServeArgs),  
    Test(TestArgs),  
}  
  
  
// 可复用参数  
#[derive(Args, Debug)]  
struct CommonArgs {  
    /// Enable verbose output  
    #[arg(short, long)]  
    verbose: bool  
}  
  
  
#[derive(Args, Debug)]  
struct ServeArgs {  
  
    #[command(flatten)]  
    common: CommonArgs,  
  
    /// Server port  
    #[arg(long, default_value_t = 8088)]  
    port: u16,  
}  
  
  
#[derive(Args, Debug)]  
struct TestArgs {  
  
    #[command(flatten)]  
    common: CommonArgs,  
  
    /// Run ignored tests  
    #[arg(long)]  
    ignore: bool,  
  
}  
  
  
  
fn main() {  
    let cli = Cli::parse();  
    println!("{:?}", cli);  
}
```

运行：

```shell
cargo run -- serve --verbose --port 3000
```

输出类似：

```text
Cli { command: Serve(ServeArgs { common: CommonArgs { verbose: true }, port: 3000 }) }
```

`Args` 用来定义一组可复用参数，`flatten` 用来把这组参数展开到父级命令或子命令中。


# 十一、参数校验

## 1、类型解析校验

字段类型本身可以完成基础校验。

```rust
use clap::Parser;  
  
#[derive(Debug, Parser)]  
struct Cli {  
  
    /// Server port  
    #[arg(long)]  
    port: u16  
}  
  
  
fn main() {  
  
    let cli = Cli::parse();  
  
    println!("{:?}", cli);  
}
```

执行：

```shell
cargo run -- --port abc
```

结果：

```text
error: invalid value 'abc' for '**--port <PORT>**': invalid digit found in string
```

因为 `port` 是 `u16`，所以非数字字符串无法解析。


## 2、自定义解析函数

复杂规则可以通过`value_parser`指定解析函数。

```rust
use clap::Parser;

#[derive(Parser, Debug)]
struct Cli {
    /// Number between 1 and 10
    #[arg(long, value_parser = parse_range)]
    count: u8,
}

fn parse_range(value: &str) -> Result<u8, String> {
    let number: u8 = value
        .parse()
        .map_err(|_| "must be a number".to_string())?;

    if (1..=10).contains(&number) {
        Ok(number)
    } else {
        Err("must be between 1 and 10".to_string())
    }
}

fn main() {
    let cli = Cli::parse();

    println!("{cli:?}");
}
```

运行：

```shell
cargo run -- --count 5
```

输出：

```text
Cli { count: 5 }
```

运行：

```shell
cargo run -- --count 20
```

会得到错误：

```
error: invalid value '20' for '--count <COUNT>': must be between 1 and 10
```