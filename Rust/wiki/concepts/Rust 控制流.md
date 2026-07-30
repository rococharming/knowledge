---
title: Rust 控制流
date: 2026-07-21
tags: [rust, basics, control-flow]
source_count: 2
---

# Rust 控制流

控制流决定程序语句的执行顺序。Rust 的基础控制流包括条件分支、循环、范围遍历、`break` / `continue`，以及用于嵌套循环的循环标签。更复杂的 `match` 通常和枚举、模式匹配一起学习。

## 条件分支

Rust 使用 `if` 做条件判断。条件表达式不需要外层小括号，但条件必须是 `bool` 类型：

```rust
let age: u8 = 10;

if age < 18 {
    println!("You are young!");
} else {
    println!("You are old!");
}
```

Rust 不会像 C 或 C++ 那样把整数、指针等隐式转换成布尔值。需要显式写出判断条件：

```rust
let x = 1;

if x != 0 {
    println!("true");
}
```

当条件较多时，可以使用 `else if` 链式分支：

```rust
let score: u32 = 70;

if score >= 90 {
    println!("Got A");
} else if score >= 80 {
    println!("Got B");
} else if score >= 70 {
    println!("Got C");
} else {
    println!("Got D");
}
```

`if` 条件必须是 `bool`，因此它和 [[Rust 基本数据类型]] 中的布尔类型直接相关。

`if` 也可以作为表达式使用，例如 `let res = if cond { a } else { b };`。这种写法要求所有分支返回同一种类型，详见 [[Rust 函数、语句与表达式基础]]。

## `loop`

`loop` 表示无限循环。循环体会持续执行，除非遇到 `break`、程序退出、线程结束或发生不可恢复的控制转移：

```rust
let a = 10;

loop {
    println!("{a}");
}
```

通常会在循环体内部用条件配合 `break` 退出：

```rust
let mut count = 0;

loop {
    count += 1;

    if count == 5 {
        break;
    }
}

println!("count = {count}");
```

`continue` 会跳过本次循环剩余部分，直接进入下一次循环。

`loop` 还可以作为表达式使用。`break` 后面可以跟一个表达式，作为整个 `loop` 的值：

```rust
let mut count = 0;

let result = loop {
    count += 1;

    if count == 5 {
        break count * 2;
    }
};
```

## `while`

`while` 是条件循环。条件为 `true` 时执行循环体，条件变为 `false` 后退出：

```rust
let mut n = 10;

while n > 0 {
    println!("{n}");
    n -= 1;
}
```

当循环次数或结束条件取决于运行时状态，并且不自然表现为“遍历某个集合”时，`while` 往往比 `for` 更直接。

## `for`

`for` 常用于遍历集合或范围。它通常比手动维护索引更符合 Rust 的表达习惯：

```rust
for i in 0..5 {
    println!("i = {i}");
}

let arr = [1, 2, 3, 4, 5];

for val in arr {
    println!("val = {val}");
}
```

范围表达式 `0..5` 表示从 `0` 到 `5` 之前，即 `0, 1, 2, 3, 4`。范围表达式 `0..=5` 表示包含右端点，即 `0, 1, 2, 3, 4, 5`。

## `break` 与 `continue`

`break` 用于退出当前循环；`continue` 用于跳过当前这一轮循环，进入下一轮。它们默认作用于最近的一层循环：

```rust
for i in 0..10 {
    if i == 3 {
        continue;
    }

    if i == 8 {
        break;
    }

    println!("{i}");
}
```

在嵌套循环里，如果没有循环标签，`break` 和 `continue` 只影响当前最近的一层循环。

## 循环标签

Rust 支持给循环添加标签，用于指定 `break` 或 `continue` 作用于哪一层循环。标签写作 `'label`：

```rust
'outer: for i in 0..3 {
    for j in 0..3 {
        if i == 1 && j == 1 {
            break 'outer;
        }

        println!("i = {i}, j = {j}");
    }
}
```

这里 `break 'outer;` 会直接跳出外层循环，而不是只跳出内层循环。循环标签适合少数确实需要从嵌套循环中提前离开的场景；如果逻辑变得很绕，通常也可以考虑抽取函数并用 `return` 表达提前结束。

## 与模式匹配的关系

`match` 也是 Rust 中非常重要的控制流结构，但它通常不只是一种分支语法，还和枚举、模式匹配、穷尽性检查绑定在一起。基础学习时，可以先把 `if` / `else`、`loop`、`while`、`for` 作为控制流入门，把 `match` 放到模式匹配主题中深入整理。

## 相关页面

- [[Rust 基本数据类型]]
- [[Rust 变量绑定与常量基础]]
- [[Rust 函数、语句与表达式基础]]
- [[Rust 所有权系统]]

## 来源

- [[控制流]]
- [[函数、语句与表达式]]
