---
title: cargo test 参数与运行控制
date: 2026-06-01
tags: [rust, testing, cargo, recipe]
source_count: 1
---

# cargo test 参数与运行控制

## cargo test 基本作用

执行 `cargo test` 会先编译测试代码，生成**测试二进制文件**，然后运行测试二进制文件。

## 参数分类

```shell
cargo test [Cargo 参数] [测试名称过滤] -- [测试二进制参数]
```

| 位置 | 传给谁 | 示例 |
| --- | --- | --- |
| `--` 之前 | 传给 Cargo | `cargo test --no-run` |
| `--` 之后 | 传给测试二进制文件 | `cargo test -- --test-threads=1` |

查看 Cargo 的测试参数：

```shell
cargo test --help
```

查看测试二进制支持的参数：

```shell
cargo test -- --help
```

## 控制测试运行方式

### 并行与顺序执行

默认情况下，测试执行器会**并行**运行多个测试。测试之间不要依赖共享状态。

如果测试之间存在共享资源，可以使用 `--test-threads` 参数将测试线程数设置为 1：

```shell
cargo test -- --test-threads=1
```

实践中更推荐让每个测试使用**独立资源**，例如每个测试使用不同的临时目录或文件名，避免测试之间互相影响。

### 显示测试输出

默认情况下：

- 测试通过时，测试函数中的 `println!` 输出不会显示
- 测试失败时，相关输出通常会显示在失败详情中

显示所有测试的输出：

```shell
cargo test -- --show-output
```

调试时常用 `--nocapture`：

```shell
cargo test -- --nocapture
```

`--nocapture` 会禁用输出捕获，让测试中的输出直接打印出来。由于 Rust 测试默认并行执行，多个测试的输出可能交错出现。如果希望输出更清晰，可以加上单线程参数：

```shell
cargo test -- --nocapture --test-threads=1
```

### 按名称运行部分测试

- 只运行指定测试：

```shell
cargo test add_two_and_two
```

- 运行名称中包含 `add` 的测试：

```shell
cargo test add
```

- 运行某个模块下的测试：

```shell
cargo test tests::add
```

名称过滤不是只能匹配前缀，只要测试完整路径中包含指定字符串，就会匹配。

### 忽略部分测试

对于耗时较长、依赖外部服务或暂时不想默认运行的测试，使用 `#[ignore]`：

```rust
#[test]
#[ignore]
fn one_hundred() {
    let result = add_two(100);
    assert_eq!(result, 102);
}
```

运行全部测试（包括被忽略的）：

```shell
cargo test -- --include-ignored
```

只运行被 `#[ignore]` 标记的测试：

```shell
cargo test -- --ignored
```

> `--ignored` 表示只运行被 `#[ignore]` 标记的测试，`--include-ignored` 表示普通测试和被忽略的测试都运行。

### 只编译测试但不运行

有时只想确认测试能否编译，不想真正运行测试：

```shell
cargo test --no-run
```

该命令会编译测试目标，但不会执行测试。

## 开发依赖

有些依赖只在测试、示例或 benchmark 中使用，不应该进入正常依赖构建。此时可以放在 `Cargo.toml` 的 `[dev-dependencies]` 中。

示例：

```toml
[dev-dependencies]
pretty_assertions = "1"
```

`pretty_assertions` 可以提供更清晰的断言差异输出，常用于测试场景。它会覆盖标准库预导入的 `assert_eq!` 宏，使失败输出更适合阅读。

`[dev-dependencies]` 适合放置：

| 依赖类型 | 示例 |
| --- | --- |
| 测试辅助库 | `pretty_assertions` |
| 临时目录工具 | `tempfile` |
| 测试数据生成工具 | `fake`、`proptest` |
| HTTP mock 工具 | `wiremock` |
| 异步测试运行时 | `tokio` 的测试功能 |

## 测试二进制文件

执行 `cargo test` 时，`Cargo` 会以**测试模式**编译当前包以及测试代码，生成测试二进制文件，然后运行这个测试二进制文件。测试二进制文件会查找并执行被 `#[test]` 标记的测试函数。

测试执行器输出示例：

```text
test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

| 字段 | 含义 |
| --- | --- |
| `1 passed` | 通过了 1 个测试 |
| `0 failed` | 没有失败的测试 |
| `0 ignored` | 没有被 `#[ignore]` 跳过的测试 |
| `0 measured` | 没有 benchmark 相关测试 |
| `0 filtered out` | 没有因为名称过滤而被排除的测试 |

## 来源

- [[测试]]
