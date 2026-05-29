---
title: 子 Trait 与超 Trait
date: 2026-05-29
tags: [rust, trait, supertrait, subtrait, trait-bound]
source_count: 1
---

# 子 Trait 与超 Trait

Rust 中可以声明一个 trait 依赖另一个 trait。被依赖的 trait 称为**超 trait**（supertrait），依赖其他 trait 的 trait 称为**子 trait**（subtrait）。

## 基本语法

```rust
trait SubTrait: SuperTrait {
    // ...
}
```

这表示：实现 `SubTrait` 的类型，必须也实现 `SuperTrait`。

```rust
trait Render {
    fn render(&self);
}

trait Movable: Render {
    fn position(&self) -> (i32, i32);
}
```

`Movable: Render` 表示实现 `Movable` 的类型必须也实现 `Render`。

## 子 Trait 中使用超 Trait 方法

因为所有实现 `Movable` 的类型都必须实现 `Render`，所以 `Movable` 的默认方法中可以直接调用 `Render` 提供的方法：

```rust
trait Movable: Render {
    fn position(&self) -> (i32, i32);

    fn report(&self) {
        let (x, y) = self.position();
        println!("position = ({x}, {y})");
        self.render();
    }
}
```

`report()` 中调用 `self.render()` 是合法的，因为 `Movable: Render` 已经保证了实现者一定具备 `render()` 方法。

## 实现子 Trait 的要求

让 `Player` 实现 `Movable`，就必须同时实现 `Render`：

```rust
struct Player {
    x: i32,
    y: i32,
}

impl Render for Player {
    fn render(&self) {
        println!("draw player");
    }
}

impl Movable for Player {
    fn position(&self) -> (i32, i32) {
        (self.x, self.y)
    }
}
```

两个 `impl` 的顺序不重要，但最终 `Player` 必须同时满足两个实现。

## 不是类继承

子 trait **不是**面向对象语言中的类继承。它不会继承字段，也不会自动继承具体实现。它表达的是一种**能力约束**：

> 如果一个类型具备 `Movable` 能力，那么它必须也具备 `Render` 能力。

## 多个超 Trait

一个子 trait 也可以依赖多个超 trait：

```rust
trait Printable: std::fmt::Display + std::fmt::Debug {
    fn print_all(&self) {
        println!("{}", self);
        println!("{:?}", self);
    }
}
```

实现 `Printable` 的类型，必须同时实现 `Display` 和 `Debug`。

## 关联

- [[Trait]] — trait 的定义与实现基础
- [[Trait Bound]] — 超 trait 本质上是一种 trait bound 约束
- [[泛型]] — 泛型代码中对 trait 能力的约束
