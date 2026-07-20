---
title: anyhow
date: 2026-06-08
tags: [Rust, RustCrate, anyhow]
aliases:
  - anyhow
---

# 一、简介

`anyhow`是 Rust 生态中最常用的应用层错误处理 crate 之一。它建立在 `Result`、`?` 和错误传播这些基础概念之上，相关内容见 [[Rust/notes/Rust基础/19、错误处理|错误处理]]。

它提供了统一的`anyhow::Error`类型，可以将不同来源的错误统一封装，从而简化错误传播和错误处理代码。

在实际开发中，一个函数可能同时产生：

- `std::io::Error`
- `std::num::ParseIntError`
- `serde_json::Error`
- ...

如果严格为所有错误定义统一枚举，代码会比较繁琐。

`anyhow`的思路是：

> 应用层统一返回`anyhow::Error`，底层错误通过`?`自动转换并向上传播。

适用场景：

|场景|是否推荐|
|---|---|
|CLI 工具|推荐|
|应用程序|推荐|
|Web 服务|推荐|
|原型项目|推荐|
|库 crate 对外 API|通常不推荐|
如果正在编写公共库，通常应该定义明确的错误类型，而不是直接暴露 `anyhow::Error`。

# 二、安装依赖

在 `Cargo.toml` 中添加：

```toml
[dependencies]
anyhow = "1"
```

或者：

```bash
cargo add anyhow
```

# 三、Result别名类型

## 1、anyhow::Result

`anyhow`提供了一个非常常用的类型别名：

```rust
pub type Result<T> = std::result::Result<T, anyhow::Error>;
```

因此，导入`use anyhow::Result;`后，就可以写：

```rust
fn read_config() -> Result<String> {
	// ...
}
```

等价于：

```rust
fn read_config() -> std::result::Result<String, anyhow::Error> {
	// ...
}
```

## 2、错误自动转换

示例：

```rust
use anyhow::Result;  
use std::fs;  
  
fn get_cargo_toml() -> Result<String> {  
    let content = fs::read_to_string("Cargo.toml")?;  
    Ok(content)  
}  
  
  
fn main() -> Result<()> {  
  
    let content = get_cargo_toml()?;  
    println!("{content}");  
    Ok(())  
}
```

这里`read_to_string("Cargo.toml")`返回`std::io::Result<String>`，但函数返回`anyhow::Result<String>`。

由于`std::io::Error`实现了`std::error::Error`，因此`?`可以自动将其转换为`anyhow::Error`。

# 四、错误上下文

很多时候底层错误信息并不能帮助快速定位问题。

例如：

```text
No such file or directory (os error 2)
```

看到这个错误，你并不知道：

- 读取的是哪个文件
- 正在执行哪个步骤
- 哪个配置项出了问题

因此`anyhow`提供了`Context` Trait。

## 1、引入Context

```rust
use anyhow::Context;
```

如果没有引入这个 Trait：

```rust
.context(...)
.with_context(...)
```

将无法调用，这是因为这两个方法来自`Context` Trait。

## 2、context

示例：

```rust
use anyhow::{Context, Result};  
use std::fs;  
  
fn get_file(path: &str) -> Result<String> {  
  
    let content = fs::read_to_string(path)  
        .context("failed to read file")?;  
  
    Ok(content)  
}  
  
  
fn main() -> Result<()> {  
  
    let content = get_file("hello.txt")?;  
    println!("{content}");  
    Ok(())  
}
```

报错时：

```text
Error: failed to read file

Caused by:
    No such file or directory (os error 2)
```

`failed to read file`会被追加到错误链中。

## 3、with_context

```rust
use anyhow::{Context, Result};  
use std::fs;  
  
fn get_file(path: &str) -> Result<String> {  
  
    let content = fs::read_to_string(path)  
        .with_context(|| format!("failed to read file: {path}"))?;  
  
    Ok(content)  
}  
  
  
fn main() -> Result<()> {  
  
    let content = get_file("hello.txt")?;  
    println!("{content}");  
    Ok(())  
}
```

报错时输出：

```text
Error: failed to read file: hello.txt

Caused by:
    No such file or directory (os error 2)
```


## 4、context和with_context的区别

| 方法               | 参数   | 是否惰性计算 |
| ---------------- | ---- | ------ |
| `context()`      | 直接传值 | 否      |
| `with_context()` | 闭包   | 是      |

例如：

```rust
.context("failed")
```

无论是否出错，字符串都会构造。

而：

```rust
.with_context(|| format!("failed: {path}"))
```

只有真正发生错误时才执行闭包。

因此涉及`format!`、路径拼接、复杂计算时，优先选择`with_context()`。

# 五、常用宏

## 1、anyhow!

`anyhow!`用于构造一个`anyhow::Error`。

```rust
use anyhow::{anyhow, Result};  
  
fn must_be_positive(x: i32) -> Result<i32> {  
    if x <= 0 {  
       return Err(anyhow!("x must be positive, got {x}"));  
    }  
  
    Ok(x)  
}  
  
  
fn main() -> Result<()> {  
  
    let n = must_be_positive(-1)?;  
    println!("{n}");  
    Ok(())  
}
```

等价于：

```rust
let err = anyhow::Error::msg(...);
```

但更常用、更灵活。

## 2、bail!

`bail!`用于主动创建错误并返回。

示例：

```rust
use anyhow::{bail, Result};  
  
fn must_be_positive(x: i32) -> Result<i32> {  
    if x <= 0 {  
       bail!("x must be positive, got {}", x);  
    }  
  
    Ok(x)  
}
```

本质上：

```rust
bail!("xxx");
```

等价于：

```rust
return Err(anyhow!("xxx"));
```

## 3、ensure!

很多时候只是想校验条件：

```rust
if x <= 0 {
    bail!("x must be positive");
}
```

此时可以写成：

```rust
use anyhow::{Result, ensure};

fn must_be_positive(x: i32) -> Result<i32> {
    ensure!(x > 0, "x must be positive, got {x}");

    Ok(x)
}
```

本质上：

```rust
ensure!(cond, ...)
```

等价于：

```rust
if !cond {  
	bail!(...);  
}
```

但语义更加清晰。


# 六、错误链

假设代码：

```rust
use anyhow::{Context, Result};

fn read_file(path: &str) -> Result<String> {
    std::fs::read_to_string(path)
        .with_context(|| format!("failed to read file: {path}"))
}
```

最终错误链可能是：

```
failed to read file: config.toml

Caused by:
    No such file or directory (os error 2)
```

错误上下文会一层层包裹底层错误。

```text
业务上下文
    ↓
文件读取错误
    ↓
OS错误
```

这是 `anyhow` 最有价值的能力之一。
