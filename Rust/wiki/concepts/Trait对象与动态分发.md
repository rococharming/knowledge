---
title: Trait 对象与动态分发
date: 2026-05-29
tags: [rust, trait-object, dynamic-dispatch, static-dispatch, vtable, dst]
source_count: 1
---

# Trait 对象与动态分发

## Trait Object 基本概念

**Trait Object** 是 Rust 中实现**运行时多态**的一种方式。它允许代码在不知道具体类型的情况下，通过某个 trait 提供的接口操作值。

```rust
trait Animal {
    fn speak(&self);
}

struct Dog;
struct Cat;

impl Animal for Dog {
    fn speak(&self) { println!("woof"); }
}

impl Animal for Cat {
    fn speak(&self) { println!("meow"); }
}

fn make_sound(animal: &dyn Animal) {
    animal.speak();
}

fn main() {
    let dog = Dog;
    let cat = Cat;
    make_sound(&dog);
    make_sound(&cat);
}
```

`&dyn Animal` 表示：引用一个实现了 `Animal` 的值，但具体类型在函数签名中被隐藏了，运行时才知道。

## 常见形式

| 写法 | 含义 |
|---|---|
| `&dyn Trait` | 共享借用一个实现了 trait 的值 |
| `&mut dyn Trait` | 可变借用一个实现了 trait 的值 |
| `Box<dyn Trait>` | 拥有一个实现了 trait 的值，具体值通常放在堆上 |

`&dyn Trait` 和 `&mut dyn Trait` 只是借用；`Box<dyn Trait>` 拥有具体值，适合需要把不同类型放进同一个容器的场景。

## 必须放在指针后面

不能直接写 `let animal: dyn Animal;`，因为 `dyn Animal` 是**动态大小类型**（DST）。编译器在编译期不知道它背后具体是哪种类型，因此也不知道它的大小。

正确写法是放在指针后面：

```rust
let animal: &dyn Animal;
let animal: &mut dyn Animal;
let animal: Box<dyn Animal>;
```

指针本身的大小是已知的，即使指向的具体值大小未知，也可以通过指针间接访问。

## 胖指针本质

`&dyn Animal` 是**胖指针**，包含两个指针：

```text
   &dyn Animal
┌──────────────────────┐
│ data_ptr             │  指向具体值
│ vtable_ptr           │  指向该具体类型对应的虚表
└──────────────────────┘
```

- `data_ptr` 指向真实数据
- `vtable_ptr` 指向虚表，保存了该具体类型对这个 trait 的方法实现入口，以及析构、大小、对齐信息

调用 `animal.speak()` 时，运行时通过虚表找到对应方法，而不是编译期直接确定。

## 异构集合

Trait object 的典型用途是**异构集合**：

```rust
let animals: Vec<Box<dyn Animal>> = vec![
    Box::new(Dog),
    Box::new(Cat),
];

for animal in animals {
    animal.speak();
}
```

`Vec<T>` 要求所有元素是同一种类型。`Box<dyn Animal>` 是同一种类型，因此可以把 `Dog` 和 `Cat` 放进同一个 `Vec`。

## 关联类型在 Trait Object 中

如果带有关联类型的 trait 被用作 trait object，必须明确写出关联类型：

```rust
fn dump(iter: &mut dyn Iterator<Item = String>) {
    for value in iter {
        println!("{value}");
    }
}
```

不能只写 `dyn Iterator`，因为如果不指定 `Item`，编译器不知道 `next()` 返回什么类型。

---

## 静态分发与动态分发

| 写法 | 分发方式 | 调用目标 |
|---|---|---|
| `T: Trait` / `impl Trait` | 静态分发 | 编译期确定 |
| `dyn Trait` | 动态分发 | 运行时通过虚表确定 |

### 静态分发

编译器在编译期就知道最终调用哪个具体类型的方法。泛型函数会在编译期根据实际使用的具体类型生成专门版本（**单态化**）。

**特点**：
- 调用目标编译期确定
- 通常没有额外间接调用开销
- 编译器更容易内联和优化
- 不同具体类型可能生成多份代码，增加编译时间和二进制体积

### 动态分发

编译器在编译期只知道值实现了某个 trait，不知道背后的具体类型。真正调用哪个方法，需要在运行时通过虚表确定。

**特点**：
- 调用目标运行时通过虚表确定
- 有一次间接调用开销
- 可以统一处理不同具体类型
- 通常不如静态分发容易内联

### 选择原则

- 编译期能确定具体类型，不需要把不同类型统一放在一起 → 优先使用静态分发
- 需要运行时统一处理不同具体类型 → 使用动态分发
- 需要拥有不同具体类型并放进同一个容器 → 使用 `Vec<Box<dyn Trait>>`

---

## dyn 兼容（对象安全）

不是所有的 trait 都能写成 `dyn Trait`。如果一个 trait 可以作为 trait object 使用，就说它满足 **dyn 兼容**，也叫**对象安全**。

dyn 兼容的核心前提是：**方法调用在具体类型擦除后仍然可行**。

### 常见不兼容情况

| 情况 | 原因 |
|---|---|
| 方法返回 `Self` | 擦除后不知道返回值的具体大小 |
| 方法参数中使用 `Self` | 无法保证两个 `dyn Trait` 背后是同一种类型 |
| 方法带泛型参数 | 虚表需要固定方法入口，无法为任意 `T` 生成新版本 |
| 关联函数（无 `self`） | 没有接收者，无法通过虚表调用 |
| 关联常量 | 需要依赖具体实现类型 |

### 使用 `where Self: Sized` 排除方法

有些 trait 里既有适合动态分发的方法，也有不适合的方法：

```rust
trait StringSet {
    fn new() -> Self
    where
        Self: Sized;

    fn contains(&self, value: &str) -> bool;
    fn add(&mut self, value: &str);
}
```

`where Self: Sized` 表示 `new` 只适用于已知大小的具体类型，不属于 trait object 可调用的接口。这样就可以把 `StringSet` 用作 `dyn StringSet`，同时保留 `new()` 给具体类型使用。

## 关联

- [[Trait]] — trait 的定义与实现基础
- [[Trait中的Self]] — `Self` 对 dyn 兼容的影响
- [[泛型]] — 静态分发的单态化机制
- [[size_of 与 size_of_val]] — DST 与 `dyn Trait` 的大小问题
