---
title: Trait 中的 Self
date: 2026-05-29
tags: [rust, trait, self, type-system]
source_count: 1
---

# Trait 中的 Self

`Self`（大写）在 trait 中表示**当前实现该 trait 的具体类型**。它是类型层面的名称，与方法参数中的 `self`（小写，表示实例接收者）完全不同。

## 返回当前实现类型

`Self` 常用于表示方法返回当前实现类型：

```rust
trait CloneLike {
    fn clone_like(&self) -> Self;
}

struct Dog;

impl CloneLike for Dog {
    fn clone_like(&self) -> Self {
        Dog
    }
}
```

在 `impl CloneLike for Dog` 中，`Self` 就是 `Dog`。这种写法适合构造、重置、转换后仍然返回同类型的场景。

## 要求参数是同一种类型

`Self` 可以表达"参数必须和当前实现类型相同"：

```rust
trait Merge {
    fn merge(&self, other: &Self) -> Self;
}

impl Merge for String {
    fn merge(&self, other: &Self) -> Self {
        format!("{self}{other}")
    }
}
```

`other: &Self` 等价于 `other: &String`。这种写法明确表达"只能和同类型的另一个值交互"。

**注意**：这种写法会影响 `dyn Trait` 的使用，因为 `dyn Trait` 擦除了具体类型，无法保证两个 trait object 背后是同一种具体类型。

## 访问当前实现类型的关联项

`Self` 也用于访问当前实现类型的关联项：

```rust
trait Parser {
    type Output;

    fn parse(&self) -> Self::Output;
}

struct NumberParser;

impl Parser for NumberParser {
    type Output = i32;

    fn parse(&self) -> Self::Output {
        42
    }
}
```

`Self::Output` 表示当前实现类型指定的关联类型。在 `impl Parser for NumberParser` 中，`Self::Output` 就是 `i32`。

`Self::关联项` 这种写法在关联类型、关联常量和关联函数中都很常见。

## 与 impl 块中 Self 的区别

在结构体的 `impl` 块中，`Self` 也是当前类型的别名：

```rust
impl Counter {
    fn reset(self) -> Self {
        Self { value: 0 }
    }
}
```

这与 trait 中的 `Self` 语义一致，都表示"当前正在实现的类型"。

## 关联

- [[Trait关联项]] — 关联类型、关联函数、关联常量详解
- [[Trait对象与动态分发]] — `Self` 对 `dyn Trait` 兼容性的影响
- [[完全限定方法调用]] — 使用 `<Type as Trait>::method` 消除歧义
- [[泛型Trait与默认参数]] — 泛型 trait 中 `Self` 与类型参数的关系
