# 一、简介

`clap`是 Rust 常用的命令行参数解析 crate，用于把终端输入的参数解析成Rust 中的结构体、枚举和字段值。它支持位置参数、选项参数、布尔标志、默认值、子命令、自动帮助信息和参数校验。

`clap`同时提供`derive`API和`builder`API，快速入门阶段优先使用`derive`API，即通过派生宏自动实现相关 Trait 。

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
file = hello.txt
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

![[Pasted image 20260604181114.png|200]]

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

![[Pasted image 20260604181907.png|200]]


# 五、位置参数、选项和标志

## 1、位置参数

位置参数不带`--`或`-`，依靠出现顺序解析。

```rust

```