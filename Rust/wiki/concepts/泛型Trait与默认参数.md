---
title: 泛型 Trait 与默认参数
date: 2026-05-29
tags: [rust, trait, generic, default-type-parameter, type-system]
source_count: 1
---

# 泛型 Trait 与默认参数

Trait 本身也可以带泛型参数。不同的类型参数可以理解为不同的 trait 实例。

## 泛型 Trait 的基本概念

```rust
trait Convert<T> {
    fn convert(&self) -> T;
}
```

这里的 `T` 是 trait 的泛型参数。`Convert<String>` 和 `Convert<i32>` 可以视为两个不同的 trait。

## 为同一类型实现不同 Trait 实例

一个类型可以针对不同类型参数实现同一个泛型 trait：

```rust
struct NumberText(String);

impl Convert<i32> for NumberText {
    fn convert(&self) -> i32 {
        self.0.parse().unwrap()
    }
}

impl Convert<String> for NumberText {
    fn convert(&self) -> String {
        self.0.clone()
    }
}
```

调用时，编译器根据上下文推断：

```rust
let nt = NumberText(String::from("12345"));
let number: i32 = nt.convert();
let text: String = nt.convert();
```

如果上下文不足以推断，需要使用[[完全限定方法调用]]：

```rust
let number = <NumberText as Convert<i32>>::convert(&nt);
let text = <NumberText as Convert<String>>::convert(&nt);
```

## 默认类型参数

泛型 trait 可以给类型参数设置默认值。

标准库中的 `std::ops::Add` 使用了这种设计：

```rust
trait Add<Rhs = Self> {
    type Output;

    fn add(self, rhs: Rhs) -> Self::Output;
}
```

| 项目 | 含义 |
|---|---|
| `Rhs` | 右操作数类型 |
| `Rhs = Self` | 默认右操作数和左操作数是同一类型 |
| `Output` | 加法结果类型，是关联类型 |

当代码中写 `a + b` 时，Rust 会根据类型调用对应的 `Add::add` 实现。

## 关联类型 vs 泛型参数

| 特性 | 关联类型 | 泛型参数 |
|---|---|---|
| 每个实现可指定的数量 | 1 个 | 多个 |
| 调用时是否需要标注 | 通常由实现固定 | 可能需显式指定 |
| 典型用途 | 输出类型、元素类型 | 输入类型转换、多态操作数 |

标准库中 `Iterator` 使用关联类型 `Item`（每个迭代器只产生一种元素），而 `Add` 使用泛型参数 `Rhs`（支持不同类型相加）。

## 关联

- [[Trait中的Self]] — `Self` 在泛型 trait 中的使用
- [[完全限定方法调用]] — 泛型 trait 实例的歧义消除
- [[泛型]] — 泛型函数与泛型 trait 的配合
- [[Trait关联项]] — 关联类型与泛型参数的选择策略
