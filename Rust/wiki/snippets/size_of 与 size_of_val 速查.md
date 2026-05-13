---
title: size_of 与 size_of_val 速查
date: 2026-05-12
tags: [rust, memory, std-mem, snippet]
source_count: 1
---

# size_of 与 size_of_val 速查

## 基础类型大小速查

```rust
use std::mem::size_of;

fn main() {
    println!("{}", size_of::<i8>());    // 1
    println!("{}", size_of::<i32>());   // 4
    println!("{}", size_of::<i64>());   // 8
    println!("{}", size_of::<f32>());   // 4
    println!("{}", size_of::<f64>());   // 8
    println!("{}", size_of::<bool>());  // 1
    println!("{}", size_of::<char>());  // 4
}
```

## 复合类型大小

```rust
use std::mem::size_of;

fn main() {
    println!("{}", size_of::<[i32; 4]>());     // 16
    println!("{}", size_of::<(i32, f64)>());   // 16（可能有对齐填充）
    println!("{}", size_of::<()>());           // 0
}
```

## size_of vs size_of_val

```rust
use std::mem::{size_of, size_of_val};

fn main() {
    let x: i32 = 42;
    assert_eq!(size_of::<i32>(), 4);
    assert_eq!(size_of_val(&x), 4);  // 结果相同
}
```

## DST 大小查询

```rust
use std::mem::size_of_val;

fn main() {
    let s: &str = "hello";
    println!("{}", size_of_val(s));   // 5  — 字符串内容
    println!("{}", size_of_val(&s));  // 16 — &str 胖指针（64 位）

    let arr: &[i32] = &[1, 2, 3];
    println!("{}", size_of_val(arr)); // 12 — 三个 i32
}
```

## 堆内存 vs 结构大小

```rust
use std::mem::size_of;

fn main() {
    // String 结构本身（指针 + 长度 + 容量）
    println!("{}", size_of::<String>()); // 24（64 位平台）

    // Vec 结构本身
    println!("{}", size_of::<Vec<i32>>()); // 24（64 位平台）

    // Box 指针
    println!("{}", size_of::<Box<i32>>());  // 8（64 位平台）
}
```

## 常量上下文使用

```rust
const INT_SIZE: usize = std::mem::size_of::<i32>();
const BUF: [u8; INT_SIZE] = [0; 4];

fn main() {
    println!("{:?}", BUF); // [0, 0, 0, 0]
}
```

## 相关页面

- [[size_of 与 size_of_val]] — 完整概念解释与原理说明

## 来源

- [[size_of和size_of_val]]
