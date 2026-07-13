---
title: panic 机制
date: 2026-06-01
tags: [rust, panic, error-handling, unwind, backtrace]
source_count: 1
---

# panic 机制

在 Rust 中，`panic` 是程序遇到**不可恢复错误**时进入的异常终止流程。`panic!` 是一个宏，用于主动触发 panic。panic 是线程级别的受控终止机制，而非未定义行为。

## 主动触发 panic

使用 `panic!` 宏主动进入不可恢复状态：

```rust
fn main() {
    panic!("crash and burn");
}
```

`panic!` 支持格式化参数，与 `println!` 语法一致：

```rust
fn check_age(age: i32) {
    if age < 0 {
        panic!("age cannot be negative: {age}");
    }
}
```

`panic!` 适合表达"程序已进入不应该继续执行的状态"。普通业务错误、用户输入错误等可预期问题，通常应使用 [[Result]] 而非 `panic!`。

## 被动触发 panic

某些 panic 由 Rust 或标准库在运行时自动触发，通常说明程序逻辑存在问题：

| 场景 | 触发方式 |
|---|---|
| 数组、切片、`Vec<T>` 越界访问 | `v[99]` 等索引操作 |
| 整数除以零 | 算术运算 |
| `assert!`、`assert_eq!` 断言失败 | 条件不满足 |
| 在 `Err` 上调用 `unwrap()` 或 `expect()` | 显式解包失败 |
| 在 `None` 上调用 `unwrap()` 或 `expect()` | 显式解包失败 |

被动触发的 panic 往往意味着代码逻辑有缺陷。Rust 选择在运行时立即暴露错误，而不是让程序继续在错误状态下运行。

## 默认行为：栈展开（unwind）

panic 发生时，Rust 默认执行**栈展开**：

1. 输出错误信息，说明 panic 的位置和原因
2. 如果设置了 `RUST_BACKTRACE=1`，输出调用栈
3. 从当前函数开始，沿调用栈逐层退出
4. 退出过程中清理局部变量，调用它们的 `drop` 方法
5. 当前线程结束；如果是主线程 panic，整个进程结束

示例：panic 时 `drop` 仍会被调用

```rust
struct Guard;

impl Drop for Guard {
    fn drop(&mut self) {
        println!("Guard dropped");
    }
}

fn main() {
    let _guard = Guard;
    panic!("something went wrong");  // 仍会打印 "Guard dropped"
}
```

![[assets/Pasted image 20260526161155.png|500]]

这说明在安全 Rust 中，panic 不会破坏内存安全。

## backtrace 调用栈信息

设置环境变量 `RUST_BACKTRACE=1` 可查看完整调用栈：

```bash
RUST_BACKTRACE=1 cargo run
```

![[assets/Pasted image 20260526162447.png|800]]

调用栈解读要点：

- **越靠上越接近错误发生位置，越靠下越接近程序入口**
- `hello_cargo::main at ./src/main.rs:5:6` — 用户代码层，排查时最该关注
- `<alloc::vec::Vec<T> as core::ops::index::Index<I>>::index` — 说明对 Vec 执行了索引操作
- `core::panicking::panic_bounds_check` — 边界检查失败，触发 panic 的决定点
- `__rustc::rust_begin_unwind` — 进入 unwind 阶段的底层入口

> 调用栈信息受操作系统、Rust 版本、构建模式、优化等级影响，不同环境下输出可能不同。

## abort：直接终止

除默认栈展开外，Rust 支持 `abort` 模式。在 `Cargo.toml` 中配置：

```toml
[profile.release]
panic = 'abort'
```

`abort` 模式下，panic 发生时程序直接终止，不进行栈展开，也不调用 `drop`。

| 特性 | unwind | abort |
|---|---|---|
| 清理局部变量 | 是 | 否 |
| 可执行文件大小 | 较大 | 较小 |
| 捕获 panic | 可能（通过 `catch_unwind`） | 不可 |
| 适用场景 | 需要清理资源、库代码 | 嵌入式、追求最小体积 |

## 双重 panic

如果程序正在处理第一次 panic，栈展开过程中又发生第二次 panic，Rust 通常会直接终止进程。这种情况称为**双重 panic**。

典型场景：在类型的 `drop` 方法中再次触发 panic。

```rust
struct BadDrop;

impl Drop for BadDrop {
    fn drop(&mut self) {
        panic!("panic in drop");  // 危险！
    }
}

fn main() {
    let _x = BadDrop;
    panic!("first panic");  // 展开时 drop 再次 panic → 双重 panic → 进程终止
}
```

实际开发中应避免在 `drop` 中触发 panic。

## 线程中的 panic

panic 是**线程级别**的：

- 子线程 panic → 默认只终止该子线程，其他线程继续运行
- 主线程 panic → 整个进程通常退出

线程 panic 的详细内容可参见多线程相关笔记。

## 关联

- [[Result]] — 可恢复错误的标准处理方式
- [[错误处理策略]] — 何时使用 panic，何时使用 Result
- [[所有权系统]] — 栈展开时 drop 与 RAII 的关系

## 来源

- [[错误处理]]
