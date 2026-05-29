---
title: Trait 关联项
date: 2026-05-29
tags: [rust, trait, associated-type, associated-function, associated-constant]
source_count: 1
---

# Trait 关联项

Trait 中不仅可以定义方法，还可以定义**关联项**。关联项是和某个类型关联在一起的项目，常见形式包括关联函数、关联类型和关联常量。

## 关联函数

Trait 中可以定义没有 `self` 参数的函数，这些函数叫**关联函数**：

```rust
trait Factory {
    fn create() -> Self;
}

struct User {
    name: String,
}

impl Factory for User {
    fn create() -> Self {
        Self {
            name: String::from("anonymous"),
        }
    }
}
```

调用使用 `类型名::函数名`：

```rust
let user = User::create();
```

### 在泛型代码中调用

关联函数可以在泛型代码中通过类型参数调用：

```rust
fn make<T: Factory>() -> T {
    T::create()
}
```

因为 `T: Factory`，编译器知道 `T` 一定提供 `create()`。

## 关联类型

关联类型是在 trait 中定义的**类型占位符**。它表示：实现该 trait 的具体类型，需要指定某个和类型相关的类型。

最典型的例子是 `Iterator`：

```rust
trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;
}
```

`type Item` 是关联类型，表示迭代器每次产生的元素类型。不同迭代器可以有不同的 `Item`。

```rust
impl Iterator for std::env::Args {
    type Item = String;

    fn next(&mut self) -> Option<Self::Item> {
        // ...
    }
}
```

### 在泛型代码中使用关联类型

可以在泛型代码中使用 `I::Item` 引用关联类型：

```rust
fn collect_into_vec<I>(iter: I) -> Vec<I::Item>
where
    I: Iterator,
{
    let mut values = Vec::new();
    for item in iter {
        values.push(item);
    }
    values
}
```

也可以对关联类型增加约束：

```rust
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

或直接指定关联类型：

```rust
fn dump_string<I>(iter: I)
where
    I: Iterator<Item = String>,
{
    for value in iter {
        println!("{value}");
    }
}
```

## 关联常量

Trait 中也可以定义关联常量。实现该 trait 的类型需要提供某个和类型相关的常量值：

```rust
trait HasDefaultCapacity {
    const DEFAULT_CAPACITY: usize;
}

struct SmallBuffer;
struct LargeBuffer;

impl HasDefaultCapacity for SmallBuffer {
    const DEFAULT_CAPACITY: usize = 8;
}

impl HasDefaultCapacity for LargeBuffer {
    const DEFAULT_CAPACITY: usize = 1024;
}
```

### 在泛型代码中使用

```rust
fn create_buffer<T: HasDefaultCapacity>() -> Vec<u8> {
    Vec::with_capacity(T::DEFAULT_CAPACITY)
}
```

### 带默认值的关联常量

```rust
trait HasName {
    const NAME: &'static str = "unknown";
}

struct User;

impl HasName for User {
    const NAME: &'static str = "User";
}

struct Product;

impl HasName for Product {}
```

实现者可以复用默认值，也可以重写。

## 关联项速览

| 关联项 | 作用 | 典型场景 |
|---|---|---|
| 关联函数 | 定义没有 `self` 参数的函数 | 构造实例 `T::new()` |
| 关联类型 | 由实现者指定某个相关类型 | 迭代器元素类型 `Iterator::Item` |
| 关联常量 | 由实现者提供某个类型相关常量 | 默认容量、名称、版本号 |

## 关联

- [[Trait中的Self]] — `Self::Output` 等关联项访问方式
- [[泛型Trait与默认参数]] — 泛型 trait 中关联类型与类型参数的区别
- [[Trait对象与动态分发]] — 关联类型在 `dyn Trait` 中的使用限制
- [[泛型]] — 泛型代码中对关联类型的约束
