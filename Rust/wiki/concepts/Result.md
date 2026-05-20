---
title: Result
date: 2026-05-21
tags: [rust, enum, result, error-handling]
source_count: 2
---

# Result

`Result<T, E>` 是 Rust 标准库中表示“操作可能成功，也可能失败”的泛型枚举。它常作为函数返回类型，用于把错误作为类型系统的一部分显式表达。

## 定义形态

`Result<T, E>` 可理解为：

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

- `Ok(T)` 表示操作成功，并携带成功值
- `Err(E)` 表示操作失败，并携带错误信息

示例：

```rust
fn divide(n: i32, m: i32) -> Result<i32, String> {
    if m == 0 {
        Err(String::from("cannot divide by zero"))
    } else {
        Ok(n / m)
    }
}
```

## 与模式匹配

`Result<T, E>` 常通过 [[模式匹配机制]] 拆解：

```rust
match text.parse::<i32>() {
    Ok(n) => println!("{}", n),
    Err(e) => println!("parse failed: {}", e),
}
```

如果主流程只关心成功值，可使用 [[简洁控制流]] 中的 `let else`：

```rust
let Ok(n) = text.parse::<i32>() else {
    return;
};
```

## 常见场景

- 输入解析、文件读取、网络请求等可能失败的操作
- 函数需要向调用者报告错误原因
- 文档注释中 `# Errors` 标题通常说明函数返回 `Result` 时的失败条件

## 关联

- [[枚举类型]] — `Result<T, E>` 的枚举本质
- [[模式匹配机制]] — 处理 `Ok` 与 `Err`
- [[简洁控制流]] — 使用 `let else` 简化错误提前返回
- [[注释]] — 文档惯例中的 `# Errors`

## 来源

- [[枚举]]
- [[模式匹配机制]]
