---
title: Trait
date: 2026-05-29
tags: [rust, trait, type-system, generic, trait-bound]
source_count: 6
---

# Trait

Trait 是 Rust 类型系统中描述"类型具备某种能力"的机制。一个类型实现某个 trait 后，就可以在对应上下文中使用该能力。Trait 负责声明能力，具体类型负责实现能力。

## 核心作用

- **约束能力**：泛型代码可要求类型实现特定 trait
- **表达行为**：为结构体、枚举等类型定义可复用接口
- **参与编译检查**：构建库 crate 时保留类型检查、泛型实例化和 trait 检查所需元数据

## Trait 定义

使用 `trait` 关键字定义：

```rust
trait Animal {
    fn eat(&self);
}
```

Trait 中可以包含：
- 只有签名的方法
- 带默认实现的方法
- 关联函数
- 关联类型
- 关联常量

## 为类型实现 Trait

使用 `impl Trait for Type`：

```rust
struct Dog {
    name: String,
}

impl Animal for Dog {
    fn eat(&self) {
        println!("{} is eating", self.name);
    }
}
```

Trait 方法的接收者形式与结构体方法相同：
- `&self` — 共享借用
- `&mut self` — 可变借用
- `self` — 取得所有权

## 默认方法

Trait 可以为方法提供默认实现：

```rust
trait Animal {
    fn name(&self) -> &str;

    fn sound(&self) {
        println!("{} makes sound", self.name());
    }
}
```

实现该 trait 的类型只要提供 `name`，即可复用 `sound` 的默认实现。默认方法也可以被具体类型重写。

默认实现可以调用同一个 trait 中的其他方法，即使被调用的方法没有默认实现：

```rust
trait Animal {
    fn name(&self) -> String;
    fn sound(&self) {
        println!("{} makes sound", self.name());
    }
}
```

标准库中的 `Iterator` 就大量使用这种模式：实现者只需提供核心的 `next` 方法，其余方法都有默认实现。

## 孤儿规则

实现 `impl Trait for Type` 时，**Trait 或 Type 至少有一个必须定义在当前 crate 中**。例如，不能在自己的 crate 中为 `String` 实现标准库的 `Display`。

该规则避免不同 crate 为同一组"外部 Trait + 外部类型"提供冲突实现。

## Trait 作用域

调用 trait 方法时，对应的 trait 名称通常必须在作用域内：

```rust
use std::io::Write;

let mut file = File::create("hello.txt").unwrap();
file.write_all(b"hello world\n").unwrap();
```

若不引入 `Write`，即使 `File` 实现了该 trait，也无法调用 `write_all`。

标准库预导入模块中的 trait（如 `Clone`、`Iterator`、`ToString`）无需手动导入即可使用。

## Trait Bound

### 基本写法

泛型参数本身没有任何已知能力，需要 trait bound 约束：

```rust
use std::fmt::Display;

fn show<T: Display>(value: T) {
    println!("{}", value);
}
```

也可以写在 `where` 子句中：

```rust
fn show<T>(value: T)
where
    T: Display,
{
    println!("{}", value);
}
```

约束简单时直接写在泛型参数后；约束复杂时 `where` 子句更清晰。

### 多重 Trait Bound

一个类型参数可同时要求实现多个 trait：

```rust
fn show<T: Display + Debug>(value: T) {
    println!("{}", value);
    println!("{:?}", value);
}
```

### 对关联类型增加约束

不只是类型参数本身，其关联类型也可约束：

```rust
use std::fmt::Debug;

fn dump<I>(iter: I)
where
    I: Iterator,
    I::Item: Debug,
{
    for (index, value) in iter.enumerate() {
        println!("{index}: {value:?}");
    }
}
```

`I::Item: Debug` 表示迭代器产生的元素类型必须实现 `Debug`。

## impl Trait

`impl Trait` 是 trait bound 的语法糖。

### 参数位置

```rust
fn show(value: impl Display) {
    println!("{}", value);
}
```

参数位置的 `impl Trait` 比显式泛型参数表达能力弱：以下写法中 `a` 和 `b` 可以是不同类型：

```rust
fn show_pair(a: impl Display, b: impl Display) {
    println!("{a}, {b}");
}
```

若要求两个参数是同一种具体类型，需使用显式泛型参数：

```rust
fn show_pair<T: Display>(a: T, b: T) {
    println!("{a}, {b}");
}
```

### 返回位置

```rust
fn create_animal() -> impl Animal {
    Dog
}
```

返回某个实现了 `Animal` 的具体类型，但调用方不知道具体类型。调用方只能按照 `Animal` 暴露的能力使用返回值。

返回位置的 `impl Trait` 在一个函数中必须对应**单一具体类型**。即使 `Dog` 和 `Cat` 都实现了 `Animal`，也不能在同一函数中根据条件返回不同类型：

```rust
// 错误：不能返回不同具体类型
fn create_animal(flag: bool) -> impl Animal {
    if flag { Dog } else { Cat }
}
```

若需在运行时返回不同具体类型，通常使用 trait object。

## 标记 Trait

`Copy` 是典型标记 trait。实现了 `Copy` 的类型在赋值或传参时按位复制，原变量仍然可用；未实现 `Copy` 的类型默认发生[[移动]]。

结构体和枚举默认不是 `Copy`。如果所有字段或变体携带的数据都支持 `Copy`，可以通过派生让类型支持复制：

```rust
#[derive(Copy, Clone)]
struct Point {
    x: i32,
    y: i32,
}
```

## Trait 与格式化

Rust 的格式化宏会根据格式符要求不同 trait。例如数组未实现 `Display` 时不能用 `{}` 直接打印，通常使用 `Debug` 格式：

```rust
println!("{:?}", [1, 2, 3]);
```

## Trait 与 DST

`dyn Trait` 是动态大小类型（DST）的一类。`std::mem::size_of::<T>()` 要求 `T: Sized`，因此不能直接用于 `dyn Trait`；而 `size_of_val` 可以通过引用元数据处理 DST。

## 关联

- [[泛型]] — trait bound 与 impl trait 是对泛型参数的约束机制
- [[Copy]] — 标记 trait 与按位复制语义
- [[移动]] — 非 `Copy` 类型的默认所有权转移
- [[数据类型]] — `Display` 与 `Debug` 打印差异
- [[size_of 与 size_of_val]] — `dyn Trait` 与 DST
- [[Option]] — `Option<T>` 中的 `T` 可被 trait bound 约束
- [[Result]] — `Result<T, E>` 中的类型参数约束
- [[Cargo构建配置]] — 构建过程中 trait 检查所需元数据
- [[Trait中的Self]] — `Self` 在 trait 中的类型级语义
- [[Trait关联项]] — 关联函数、关联类型与关联常量
- [[泛型Trait与默认参数]] — 泛型 trait 与默认类型参数
- [[完全限定方法调用]] — UFCS 消除方法调用歧义
- [[子Trait与超Trait]] — trait 之间的能力依赖关系
- [[Trait对象与动态分发]] — `dyn Trait` 与运行时多态

## 来源

- [[Rust 所有权]]
- [[Rust基础语法]]
- [[size_of和size_of_val]]
- [[crate与模块]]
- [[特征]]
- [[特征基础]]
- [[特征进阶]]
- [[特征对象]]
