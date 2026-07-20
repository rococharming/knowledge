---
title: Rust 变量绑定与常量基础
date: 2026-07-21
tags: [rust, basics]
source_count: 1
---

# Rust 变量绑定与常量基础

Rust 使用 `let` 创建变量绑定。默认情况下，绑定是不可变的；需要重新赋值时必须显式写出 `mut`。这使变量的可变性成为代码审查时可见的设计选择，也是 Rust 倾向于减少意外状态变化的一部分。

## 变量绑定

最基本的变量定义使用 `let`：

```rust
let a = 10;
```

Rust 会根据上下文推断类型；没有额外约束时，整数字面量通常推断为 `i32`。需要明确类型时，可以使用类型注解：

```rust
let a: u32 = 10;
```

如果变量被定义但没有使用，编译器会给出未使用变量警告。变量名前加 `_` 可以表达“这是有意不用”的意图：

```rust
let _a: u32 = 10;
```

显式类型转换使用 `as`。例如 `3.14 as i32` 会把浮点数转换成整数，结果保留整数部分并丢弃小数部分：

```rust
let a = 3.14 as i32;
```

Rust 的变量名和函数名通常使用 snake_case；结构体、枚举、trait 等类型名通常使用 PascalCase。

## 不可变性与 `mut`

`let` 绑定默认不可变：

```rust
let a = 10;
a = 20; // 编译错误
```

如果一个值确实需要在同一绑定上变化，应使用 `mut`：

```rust
let mut a = 10;
a = 20;
```

`mut` 只表示该绑定允许重新赋值或以可变方式借用，并不意味着值本身脱离了 Rust 的借用检查规则。是否能同时存在其他引用，仍由所有权和借用规则决定。

## 变量遮蔽

变量遮蔽是指用新的 `let` 声明创建一个同名的新绑定，让后续代码中的名字指向新绑定：

```rust
let x = 5;
let x = x + 1;

{
    let x = x * 2;
    println!("{x}");
}

println!("{x}");
```

遮蔽不是修改旧变量，而是创建新变量。它常用于在同一语义位置复用名字，同时改变值、类型或可变性：

```rust
let spaces = "   ";
let spaces = spaces.len();

let a = 1;
let mut a = a;
a = 2;
```

和 `mut` 相比，遮蔽更适合表达“经过一次转换后得到新的概念状态”；`mut` 更适合表达“同一个绑定在流程中会被反复更新”。

## `const` 常量

`const` 定义编译期常量：

```rust
const SECONDS_IN_HOUR: usize = 3_600;
const SECONDS_IN_DAY: usize = 24 * SECONDS_IN_HOUR;
```

`const` 的特点是：

- 必须显式指定类型。
- 值必须是编译期可计算的常量表达式。
- 名称通常使用全大写 snake case。
- 可以定义在模块级、函数内或更内层的块中。
- 同一作用域内不能重复定义同名 `const`。

`const` 更像编译期符号，编译器通常会把值内联到使用处，因此它不保证运行时存在一个固定内存地址。

## `static` 变量

`static` 定义具有静态存储期的变量：

```rust
static NUM: i32 = 100;
```

`static` 必须显式指定类型，在程序整个运行期间存在，并且代表一个固定的静态存储位置。与 `const` 不同，它通常不是简单内联值；对同一个 `static` 的引用会指向同一个存储位置。

`static` 默认不可变。可变静态变量需要写成 `static mut`，但它代表全局可变状态，可能引入数据竞争，因此读写都必须放进 `unsafe` 块：

```rust
static mut NUM: i32 = 100;

fn main() {
    unsafe {
        NUM += 1;
        let value = NUM;
        println!("NUM: {value}");
    }
}
```

`unsafe` 不是让代码变安全，而是把相关安全责任交给程序员。对全局整数计数器，通常应优先考虑原子类型；对更复杂的全局状态，通常应考虑 `Mutex`、`RwLock`、`OnceLock` 或 `LazyLock`。

在 [[Rust Edition]] 2024 中，`static_mut_refs` lint 默认是 `deny`。直接把 `static mut` 传给 `println!` 这类格式化宏时，格式化过程可能创建对它的共享引用，因此会被拒绝。先把值复制到局部变量再打印，是避免创建 `static mut` 引用的一种写法。

## 相关页面

- [[Rust Edition]]
- [[Rust 基本数据类型]]
- [[Rust 函数、语句与表达式基础]]

## 来源

- [[变量绑定与常量]]
