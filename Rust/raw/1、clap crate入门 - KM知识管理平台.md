---
title: "1、clap crate入门 - KM知识管理平台"
source: "https://wiki.vivo.xyz/knowledge/22886/content/201892"
author:
published:
created: 2026-05-13
description:
tags:
  - "clippings"
---
# AI摘要

## 为什么值得读

本文是一份非常实用的 Rust `clap` 库入门教程。`clap` 是 Rust 生态中最主流的命令行参数解析库，如果你正在用 Rust 开发 CLI 工具，掌握它能让你**用极少的代码写出专业、易用的命令行程序**，避免手写繁琐的参数解析逻辑，还能自动生成帮助信息、支持子命令和参数校验，极大提升开发效率和程序质量。

## 如何阅读与使用

文章按“从零到一”的顺序组织：
- **安装**：通过 `cargo add clap --features derive` 一步到位。
- **核心用法**：通过 `#[derive(Parser)]`、`#[arg(...)]`、`#[command(...)]` 等派生宏快速定义参数、选项、标志、子命令。
- **参数类型**：覆盖位置参数、选项（-n/--name）、标志（--verbose）、可选参数（`Option<T>`）、默认值（`default_value_t`）、子命令（`#[derive(Subcommand)]`）。
- **进阶特性**：通过 `action = ArgAction::Count` 实现计数标志，通过 `#[derive(ValueEnum)]` 实现枚举值校验。

## 核心要点（What）

1. **Derive API** 是推荐方式：用 `#[derive(Parser)]` 在结构体上声明参数，clap 自动完成解析和帮助信息生成。
2. **参数声明**：
   - 无 `#[arg]` 的字段→位置参数；加 `#[arg(short, long)]`→选项。
   - `bool` 字段默认是开关（`SetTrue`），`Vec<T>` 支持多值。
   - 用 `Option<T>` 让参数可选，用 `default_value_t` 设默认值。
3. **子命令**：通过 `#[derive(Subcommand)]` 定义枚举，用 `#[command(subcommand)]` 挂接到主结构体。
4. **校验**：可通过 `#[derive(ValueEnum)]` 限制参数只能取指定枚举值。

**一句话总结**：如果你在 Rust 中写 CLI，`clap` 是你最不该错过的高效工具，本文就是带你快速上手的通关指南。

---

# 原始正文

## 一、clap概述

## 1、简介

clap（Command Line Argument Parser for Rust），是Rust生态中最常用的命令行参数解析库之一。其设计目标为：

开箱即用，为用户提供精致的CLI体验：包括常见的参数行为、帮助信息自动生成、为用户提供的建议修复、彩色输出、Shell自动补全等。

足够灵活，便于移植现有的CLI接口

合理的解析性能

## 2、安装

展开

自动换行

cargo add clap --features derive

启用derive特性标志，因为它允许clap使用Rust的派生宏#\[derive(Parser)\]等快速生成命令行解析代码。

## 3、简单示例

展开

自动换行

use clap::Parser;

/// Simple program to greet a persion

#\[derive(Parser, Debug)\]

#\[command(version, about, long\_about = None)\]

struct Args {

/// Name of the person to greet

#\[arg(short, long)\]

name: String,

/// Number of times to greet

#\[arg(short, long, default\_value\_t = 1)\]

count: u8

}

fn main() {

let args = Args::parse();

for \_ in 0..args.count {

println!("Hello {}!", args.name);

}

}

运行结果：

![](https://veditor.vivo.xyz/api/v1/attachment/file/H29xWCOmpz-z3HC9eTLxR13B8MjVNUKRnoLfcNGm42whwUuMrX_ytHPhBesbED3n)

说明：

#\[derive(Parser)\]会自动为当前定义的Args结构体实现Parser Trait，为其实现参数解析逻辑方法parser

#\[command(...)\]用于定义整个CLI程序的元信息，例如名称、版本、描述等。

name：CLI程序名称，默认使用Cargo.toml的项目名

version：CLI版本， **只有定义了version字段，才会为CLI程序自动生成--version选项** ，默认输出Cargo.toml的项目名以及版本名

about：项目简单描述

#\[arg(...)\]定义单个参数短选项名、长选项名等

short：参数短选项名，未指定则默认使用下方字段的首字母，使用name的n

long：参数长选项名，未指定默认使用下方字段整个单词，如name

default\_value\_t：指定选项的默认选项值

从--help的结果来看，可以看到///这些文档注释信息会显示出来，例如选项的含义，以及项目的描述（因为这里的about没指定，就使用结构体上方的///注释内容作为描述）

## 二、clap Derive API入门

本节介绍如何使用Rust的clap库的 **Derive API（派生方式）** 来构建命令行程序。

## 1、Quick Start

要使用Derive API，需要在Cargo.toml中启用derive特性。

展开

自动换行

cargo add clap --features derive

示例：

展开

自动换行

use std::path::PathBuf;

use clap::{Parser, Subcommand};

#\[derive(Parser)\]

#\[command(version, about = "A simple to use, efficient, and full-featured Command Line Argument Parser", long\_about = None)\]

struct Cli {

/// 可选的名字

name: Option<String>,

/// 自定义配置文件

#\[arg(short, long, value\_name = "FILE")\]

config: Option<PathBuf>,

/// 调试等级

#\[arg(short, long, action = clap::ArgAction::Count)\]

debug: u8,

#\[command(subcommand)\]

command: Option<Commands>

}

#\[derive(Subcommand)\]

enum Commands {

/// 执行测试

Test {

/// 是否列出测试值

#\[arg(short, long)\]

list: bool

}

}

结果：

![](https://veditor.vivo.xyz/api/v1/attachment/file/JVen4GxN4bmd7EoU3dN0kyNB7PY_gpI93dE1KFgc0iHgZR7qk2tO1F3ZllyoYaD1)

说明：

#\[derive(Subcommand)\]用于将enum Commands的各个变体作为CLI的子命令。在结构体Cli中，通过#\[command(subcommand)\]将某个字段标注为子命令

name: Option<String>没有#\[args()\]标注，那么name不是选项，而是位置参数（即不能用选项+选项值）

#\[arg(short, long, action = clap::ArgAction::Count)\]表示把当前参数视为可重复出现的开关，出现一次+1，一次不出现默认为0。

对于子命令test，仅仅执行test，list默认为false，需要加上test --list或者test -l，list才为true。

## 2、配置解析器

通过派生（derive）Parser Trait来构建一个解析器。

示例：

展开

自动换行

use clap::{Parser};

#\[derive(Parser)\]

#\[command(name = "MyApp")\]

#\[command(version = "1.0")\]

#\[command(about = "Does awesome things", long\_about = None)\]

struct Cli {

#\[arg(long)\]

two: String,

#\[arg(long)\]

one: String

}

fn main() {

let cli = Cli::parse();

println!("two: {:?}", cli.two);

println!("one: {:?}", cli.two);

}

结果：

![](https://veditor.vivo.xyz/api/v1/attachment/file/JM1ZQ2S3a6912lwx0zsaRPhbAC-gPsIrczJ5WTxfPwSBKSVooSrqHvsX0MuVfgn8)

可以在结构体上使用#\[command(version, about)\]的默认行为，这会从Cargo.toml中自动填充这些字段。注意about对应Cargo.toml中的\[package\] description。

可以在结构体上使用#\[command\]属性，来修改clap在应用层级（整体程序层面）的行为。任何Command构建器里的函数，都可以作为属性来使用，例如Command::next\_line\_help。

示例：

展开

自动换行

use clap::{Parser};

#\[derive(Parser)\]

#\[command(version, about, long\_about = None)\]

#\[command(next\_line\_help = true)\]

struct Cli {

#\[arg(long)\]

two: String,

#\[arg(long)\]

one: String

}

fn main() {

let cli = Cli::parse();

println!("two: {:?}", cli.two);

println!("one: {:?}", cli.two);

}

结果：

![](https://veditor.vivo.xyz/api/v1/attachment/file/R1o-xi6HJXdfCXCXr8wwGIJx8mX2ihE_YASpKq94DDC1-NmZ0WjoZ7Xe5a5ODpXD)

## 三、添加参数

参数（Arguments）是根据结构体中的字段自动推断出来的。

## 1、位置参数（Positionals）

默认情况下，结构体中的字段会被定义为位置参数（Positionals）。

示例：

展开

自动换行

use clap::{Parser};

#\[derive(Parser)\]

#\[command(version, about, long\_about = None)\]

struct Cli {

name: String

}

fn main() {

let cli = Cli::parse();

println!("name: {}", cli.name);

}

结果：

![](https://veditor.vivo.xyz/api/v1/attachment/file/UPs1wckXZe7cGUHurXo_R4uyOanTCPCeKAuxaScy8gk8BmcXfzIsJJdavUo1YP1C)

注意：默认的 **ArgAction** 是Set，即这个参数只保存一个值。如果希望接收多个参数，用Vec把action改为Append。

示例：

展开

自动换行

use clap::{Parser};

#\[derive(Parser)\]

#\[command(version, about, long\_about = None)\]

struct Cli {

name: Vec<String>

}

fn main() {

let cli = Cli::parse();

println!("name: {:?}", cli.name);

}

结果：

![](https://veditor.vivo.xyz/api/v1/attachment/file/WR_AvKhrXBpaERlWDXD-CSuXuTXoo-1OGm5t7QUOrUEeL_vslhLdeME454VV21GI)

## 2、选项（Options）

可以通过flag来给参数命令：

参数的含义更清晰

参数的顺序不再重要

**要为一个参数指定flag，在字段上使用#\[arg(short = 'n')\]或#\[arg(long = "name")\]这样的属性。当没有显式给出值时（例如#\[arg(short)\]，标志名会根据字段名自动推断出来** 。

示例：

展开

自动换行

use clap::Parser;

#\[derive(Parser)\]

#\[command(version, about, long\_about = None)\]

struct Cli {

#\[arg(short, long)\]

name: String,

}

fn main() {

let cli = Cli::parse();

println!("name: {:?}", cli.name);

}

结果：

![](https://veditor.vivo.xyz/api/v1/attachment/file/c046wtmC0NBqh4JJcZ1bJzhx0nQr3JAejW1xJk_NBJlGg6L2nuc2FXo6C5YQoM2v)

**注意默认的ArgAction是Set，为了接收更多的参数，通过Vec将action重写为Append** 。

示例：

展开

自动换行

use clap::{Parser};

#\[derive(Parser)\]

#\[command(version, about, long\_about = None)\]

struct Cli {

#\[arg(short, long)\]

name: Vec<String>

}

fn main() {

let cli = Cli::parse();

println!("name: {:?}", cli.name);

}

结果：

![](https://veditor.vivo.xyz/api/v1/attachment/file/NEZ1dJU26MyqV733IgNcnjFwiv2_zWN8YVPaeM54u-fDJbjwCyn2hgm7kPmywcmn)

## 3、标志（Flags）

标志（Flags）也可以作为开关使用，用来表示“开启/关闭”状态。

示例：

展开

自动换行

use clap::{Parser};

#\[derive(Parser)\]

#\[command(version, about, long\_about = None)\]

struct Cli {

#\[arg(short, long)\]

verbose: bool

}

fn main() {

let cli = Cli::parse();

println!("verbose: {:?}", cli.verbose);

}

结果：

![](https://veditor.vivo.xyz/api/v1/attachment/file/ja_q4ajnhyh62VaaVNyIibieT1nunWPqemE0fMNQNKnF6fnhEiWH8cHYDM8amXah)

不加--verbose或者-v，则verbose字段默认为false，加了则变为true。

**当字段类型为bool时，clap默认把它当作“开关”，并且默认ArgAction是SetTrue** 。如果想让同一个开关重复出现并统计次数，可以将action设置Count。

示例：

展开

自动换行

use clap::Parser;

#\[derive(Parser)\]

#\[command(version, about, long\_about = None)\]

struct Cli {

#\[arg(short, long, action = clap::ArgAction::Count)\]

verbose: u8,

}

fn main() {

let cli = Cli::parse();

println!("verbose: {:?}", cli.verbose);

}

结果：

![](https://veditor.vivo.xyz/api/v1/attachment/file/d5MFEUQ62-JaUFb0s-yyVtxCGzP8TGGPDe9punLpX99oN3H7CWU-L7r2zwxxVbAm)

## 4、可选（Optional）

默认情况下，参数会被认为是必填（required）的， **要让一个参数变为可选（Optional），可以把字段类型用Option包起来** 。

示例：

展开

自动换行

use clap::{Parser};

#\[derive(Parser)\]

#\[command(version, about, long\_about = None)\]

struct Cli {

name: Option<String>

}

fn main() {

let cli = Cli::parse();

println!("name: {:?}", cli.name);

}

结果：

![](https://veditor.vivo.xyz/api/v1/attachment/file/vrNOYc9v4AP2p7vLg3jbG6P1Tkf3olmvlfQ01ywmQOFAre_P2ADIh2mxC_IVJVTg)

## 5、默认值（Defaults）

参数可以是必填或可选的。当参数需要可选时，使用Option，并且可以用unwrap\_or来提供一个默认值。 **另外，也可以通过设置#\[arg(default\_value\_t)\]来直接指定默认值** 。

示例：

展开

自动换行

use clap::{Parser};

#\[derive(Parser)\]

#\[command(version, about, long\_about = None)\]

struct Cli {

#\[arg(default\_value\_t = 8888)\]

port: u16

}

fn main() {

let cli = Cli::parse();

println!("port: {:?}", cli.port);

}

结果：

![](https://veditor.vivo.xyz/api/v1/attachment/file/g2mAO_F0rP3rr7n9kefy9NklsrUmqoEKgKpDTHQHT2552hjXUsRdVqbo9sdtlHIQ)

## 6、子命令（Subcommands）

子命令（Subcommands）可以通过 **#\[derive(Subcommand)\]** 派生生成，并且在使用该类型的字段上加上 **#\[command(subcommand)\]属性** ，把它加入到主命令中。

每一个子命令实例都拥有自己的版本号、作者信息、参数（Args），设置还可以有它自己的子命令。

展开

自动换行

use clap::{ Parser, Subcommand };

#\[derive(Parser)\]

#\[command(version, about, long\_about = None)\]

#\[command(propagate\_version = true)\]

struct Cli {

#\[command(subcommand)\]

command: Commands,

}

#\[derive(Subcommand)\]

enum Commands {

/// Add files to MyApp

Add {

name: Option<String>,

}

}

fn main() {

let cli = Cli::parse();

match &cli.command {

Commands::Add { name} => {

println!("'myapp add' was used, name is: {name:?}");

}

}

}

这里使用了结构体变体来定义add子命令，另外，也可以使用一个单独的结构体（该结构体需要使用#\[derive(Args)】派生宏）定义该子命令的参数。

示例：

展开

自动换行

use clap::{ Parser, Subcommand, Args };

#\[derive(Parser)\]

#\[command(version, about, long\_about = None)\]

#\[command(propagate\_version = true)\]

struct Cli {

#\[command(subcommand)\]

command: Commands,

}

#\[derive(Subcommand)\]

enum Commands {

/// Add files to MyApp

Add(AddArgs)

}

#\[derive(Args)\]

struct AddArgs {

name: Option<String>,

}

fn main() {

let cli = Cli::parse();

match &cli.command {

Commands::Add(name) => {

println!("'myapp add' was used, name is: {:?}", name.name);

}

}

}

当使用command: Commands来指定子命令时，这个子命令就是必填的。 **默认情况下，如果缺少子命令，程序会显示帮助信息，而不是报错。**

结果：

![](https://veditor.vivo.xyz/api/v1/attachment/file/nwb8RKDjKCMAnfGpjfIaUmJZQSp-8_dS6BEuoqd6WeXPk5ZJvgCZXIe6hQmY30DJ)

要让一个子命令变成可选，可以用Options包起来（例如：command: Option<Commands>）

示例：

展开

自动换行

use clap::{ Parser, Subcommand, Args };

#\[derive(Parser)\]

#\[command(version, about, long\_about = None)\]

#\[command(propagate\_version = true)\]

struct Cli {

#\[command(subcommand)\]

command: Option<Commands>,

}

#\[derive(Subcommand)\]

enum Commands {

/// Add files to MyApp

Add {

name: Option<String>,

}

}

fn main() {

let cli = Cli::parse();

match &cli.command {

Some(Commands::Add { name }) => {

println!("'myapp add' was used, name is: {:?}", name);

}

None => {

eprintln!("No subcommand was provided. Use --help to see available subcommands.");

}

}

}

因为我们指定了 `#[command(propagate_version = true)]` ，所以 `--version` 这个标志在所有子命令中都可以使用：

![](https://veditor.vivo.xyz/api/v1/attachment/file/s9YJKDbQ4BSvnAwqYSI9YkVQYQuZnYZGI1kbJrVmcbKt4Z6y0ElX0MNl-Mpl9A2t)

## 四、校验（Validation）

## 1、枚举值（Enumerated values）

如果你有一个参数，它只能取你想检查的某些特定值，你可以为它派生ValueEnum