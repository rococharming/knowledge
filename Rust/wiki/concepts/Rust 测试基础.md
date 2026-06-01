---
title: Rust 测试基础
date: 2026-06-01
tags: [rust, testing, assert, should_panic]
source_count: 1
---

# Rust 测试基础

Rust 内置了测试支持，通过 `cargo test` 编译并运行项目中的测试代码。测试函数围绕**设置数据 → 运行代码 → 断言结果**三个步骤展开。

## 测试函数基本结构

使用 `cargo new adder --lib` 创建库项目时，`src/lib.rs` 会生成测试模板：

```rust
pub fn add(left: u64, right: u64) -> u64 {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
```

| 代码 | 作用 |
| --- | --- |
| `#[cfg(test)]` | 只在测试构建时编译该模块 |
| `mod tests` | 约定俗成的测试模块名 |
| `use super::*;` | 将父模块中的内容引入当前测试模块 |
| `#[test]` | 标记测试函数，使测试执行器可以发现并运行它 |
| `assert_eq!` | 断言左右两边的值相等 |

测试模块中**也可以定义普通辅助函数**，不会被当作测试运行。

执行 `cargo test` 时，Cargo 会以**测试模式**编译当前包及测试代码，生成测试二进制文件并运行。测试执行器发现被 `#[test]` 标记的函数并执行。

## 常用断言宏

| 宏 | 作用 |
| --- | --- |
| `assert!(expr)` | 断言表达式为 `true` |
| `assert_eq!(left, right)` | 断言两个值相等 |
| `assert_ne!(left, right)` | 断言两个值不相等 |
| `panic!` | 主动触发 panic，使测试失败 |

测试是否通过取决于函数是否正常执行结束。只要发生 panic，测试就会失败。上述断言宏在失败时都会触发 panic。

可以指定运行某个测试：

```shell
cargo test add_two_and_two
```

## 自定义失败信息

`assert!` 和 `assert_eq!` 宏支持自定义失败信息，格式类似 `format!`：

```rust
assert!(
    result.contains(target),
    "greeting should contain name: {}, actual greeting: {}",
    target, result
);
```

复杂测试中建议写清楚失败原因，尤其是测试数据较多、断言条件较复杂时。

## should_panic

### 测试是否发生 panic

有些函数的预期行为就是在非法输入时 panic，使用 `#[should_panic]` 标记：

```rust
#[should_panic]
#[test]
fn greater_than_hundred() {
    Number::new(101);
}
```

该测试只有在 `Number::new(101)` 发生 panic 时才会通过。

### 指定期望的 panic 信息

通过 `expected` 精确匹配 panic 信息片段：

```rust
#[should_panic(expected = "less than or equal to 100")]
#[test]
fn greater_than_hundred() {
    Number::new(200);
}
```

`expected` 判断的是实际 panic 信息中是否**包含**指定字符串，不要求完全相等。

## 返回 Result<T, E> 的测试函数

测试函数可以返回 `Result<T, E>`，适合测试中使用 `?` 运算符的场景：

```rust
#[test]
fn it_works() -> Result<(), String> {
    let result = add_two(2);
    if result == 4 {
        Ok(())
    } else {
        Err(String::from("two plus two does not equal four"))
    }
}
```

| 返回值 | 测试结果 |
| --- | --- |
| `Ok(())` | 测试通过 |
| `Err(e)` | 测试失败，并输出错误信息 |

返回 `Result` 的测试函数**不适合**再使用 `#[should_panic]`。如需测试错误返回，直接断言 `Result` 状态：

```rust
assert!(result.is_err());
```

或使用 `match` 进一步检查错误内容：

```rust
match result {
    Ok(value) => panic!("expected error, got {}", value),
    Err(e) => {
        assert_eq!(e.kind(), &std::num::IntErrorKind::InvalidDigit)
    }
}
```

## 来源

- [[测试]]
