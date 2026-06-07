---
title: Rust 运算符重载
date: 2026-06-07
tags: [rust, trait, operator-overloading]
source_count: 1
---

# Rust 运算符重载

Rust 中大多数运算符并非独立语法，而是建立在标准库 `std::ops` 和 `std::cmp` 中的 trait 之上的统一接口。为自定义类型实现对应 trait，即可让这些类型支持自然运算符语法。

## 核心思想

- 运算符 = trait 方法调用的语法糖：`x + y` 等价于 `x.add(y)`
- 行为受类型系统约束：参数类型、返回类型由 trait 定义决定
- 与所有权系统一致：部分 trait 按值接收（`self`），部分按引用接收（`&self`）
- **不能自定义新运算符**，只能重载 Rust 已支持的运算符
- **不可重载**：借用（`&`）、赋值（`=`）、短路逻辑（`&&`/`||`）、错误传播（`?`）、范围（`..`/`..=`）、函数调用

## 内容概览

| 主题 | 对应 trait | 关键要点 |
|------|-----------|---------|
| [[运算符重载\|一元与二元运算符]] | `Neg`、`Not`、`Add`、`Mul` 等 | `Output` 关联类型、`Rhs` 泛型参数、按值/按引用接收 |
| [[相等性比较\|相等性比较]] | `PartialEq`、`Eq` | 部分相等 vs 完全相等、浮点 `NaN` 不满足自反性、可派生 |
| [[有序性比较\|有序性比较]] | `PartialOrd`、`Ord` | `Option<Ordering>` 返回值、`sort` 依赖 `Ord`、`Reverse` 反转顺序 |
| [[索引运算符\|索引运算符]] | `Index`、`IndexMut` | `Output` 关联类型、必须返回已有元素的引用、`HashMap` 不支持 `IndexMut` |

## 按运算符类别划分

### 一元运算符

- `std::ops::Neg` — `-x`，一元负号
- `std::ops::Not` — `!x`，逻辑取反或按位取反（Rust 不区分 `!` 和 `~`）

### 二元算术运算符

- `std::ops::Add`、`Sub`、`Mul`、`Div`、`Rem`
- `Add<Rhs = Self>` 右操作数默认同类型，也可自定义跨类型相加

### 按位运算符

- `std::ops::BitAnd`、`BitOr`、`BitXor`、`Shl`、`Shr`

### 复合赋值运算符

- `std::ops::AddAssign`、`SubAssign`、`MulAssign`、`DivAssign`、`RemAssign`
- 以及对应的按位复合赋值：`BitAndAssign`、`BitOrAssign`、`BitXorAssign`、`ShlAssign`、`ShrAssign`
- 无 `Output` 关联类型，直接修改左操作数（`&mut self`），表达式结果类型为 `()`

### 相等性比较

- `std::cmp::PartialEq` — `==`、`!=`，部分相等（不要求自反性）
- `std::cmp::Eq` — `PartialEq` 的语义增强，承诺完全满足数学相等关系
- `f32`/`f64` 只有 `PartialEq`，没有 `Eq`（`NaN != NaN`）

### 有序性比较

- `std::cmp::PartialOrd` — `<`、`>`、`<=`、`>=`，返回 `Option<Ordering>`
- `std::cmp::Ord` — 全序关系，`cmp` 返回 `Ordering`（非 `Option`），是 `sort` 等方法的前提
- `std::cmp::Reverse<T>` — 包装类型，反转比较方向

### 索引运算符

- `std::ops::Index` — 只读索引 `a[i]`，返回 `&Self::Output`
- `std::ops::IndexMut` — 可变索引 `a[i] = v`，继承自 `Index`
- 索引参数不限于 `usize`，也可以是范围或自定义类型
- `HashMap` 支持 `Index` 但不支持 `IndexMut`（因为 `index_mut` 必须返回已有元素的引用）

## 重要设计约束

1. **不能自定义新运算符**，只能实现 Rust 已支持的运算符 trait
2. **参数与返回类型受 trait 约束**：如 `Add` 的 `Rhs` 和 `Output` 关联类型
3. **所有权一致性**：`Add` 按值接收可能消耗原值，`PartialEq` 按引用接收以保留所有权
4. **复合赋值结果类型为 `()`**：`x += y` 不等价于 `x = x + y` 的返回值
5. **并非所有运算符都能重载**：赋值、借用、短路逻辑、错误传播、范围运算符属于语言核心语义

## 来源

- [[运算符重载]]
