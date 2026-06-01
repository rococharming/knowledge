---
title: main 函数错误处理
date: 2026-06-01
tags: [rust, error-handling, recipe, main, cli]
source_count: 1
---

# main 函数错误处理

Rust 的 `main` 函数是程序入口，它有几种常见的错误处理方式，适用于不同复杂度的程序。

## 方式一：expect（简单场景）

小程序或示例代码中，可以直接使用 `expect()`：

```rust
use std::fs;

fn main() {
    let content = fs::read_to_string("hello.txt").expect("读取 hello.txt 失败");
    println!("{content}");
}
```

特点：
- 写法简单
- 错误发生时直接 panic
- 适合示例、测试、临时脚本
- 不适合需要精细错误处理的程序

## 方式二：main 返回 Result

更常见的方式是让 `main` 返回 `Result`，这样就可以在 `main` 中使用 `?`：

```rust
use std::error::Error;
use std::fs;

fn main() -> Result<(), Box<dyn Error>> {
    let content = fs::read_to_string("hello.txt")?;
    println!("{content}");
    Ok(())
}
```

特点：
- 比到处写 `expect()` 更整洁
- 如果 `main` 返回 `Err`，Rust 会打印错误并以失败状态退出
- `Box<dyn Error>` 表示可以返回多种实现了 `Error` 的错误类型
- 适合稍复杂的程序

## 方式三：run() 分离模式

命令行程序中常见结构：真正逻辑写在 `run()` 中，`main()` 只负责统一处理错误和退出码。

### 单一错误类型场景

```rust
use std::io;
use std::fs;
use std::process;

fn main() {
    if let Err(error) = run() {
        eprintln!("{}", error);
        process::exit(1);
    }
}

fn run() -> io::Result<()> {
    let content = fs::read_to_string("hello.txt")?;
    println!("{content}");
    Ok(())
}
```

### 多种错误类型场景

```rust
fn run() -> Result<(), Box<dyn std::error::Error>> {
    // ...
    Ok(())
}
```

### 自定义错误类型场景

```rust
fn run() -> Result<(), AppError> {
    // ...
    Ok(())
}
```

### run() 分离的好处

- **核心逻辑可以使用 `?`**：避免在 main 中写大量错误处理代码
- **main 统一打印错误**：错误输出风格一致
- **明确控制退出码**：通过 `process::exit(1)` 返回非零状态
- **程序结构更清楚**：逻辑与入口职责分离

## 选择指南

| 场景 | 推荐方式 |
|---|---|
| 示例/临时脚本 | `expect()` |
| 单一错误类型的 CLI 工具 | `main() -> io::Result<()>` |
| 涉及多种错误的程序 | `main() -> Result<(), Box<dyn Error>>` |
| 需要精确错误控制的库/应用 | `run() -> Result<(), CustomError>` |

## 关联

- [[Result处理]] — Result 的方法速查
- [[自定义错误类型]] — 自定义错误枚举的实现
- [[错误处理策略]] — 错误处理方式的整体决策指南
- [[Cargo 命令速查]] — CLI 工具开发相关

## 来源

- [[错误处理]]
