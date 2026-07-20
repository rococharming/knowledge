---
title: GitHub CI
date: 2026-07-20
tags: [GitHub, CI, GitHub-Actions, Rust]
aliases:
  - GitHub Actions CI
  - GitHub 持续集成
---

# 一、CI 的基本概念

CI 是 Continuous Integration（持续集成）的缩写，指团队把代码频繁合并到主干，并在每次合并前后自动运行检查。它解决的是“代码能不能稳定合在一起”的问题。

没有 CI 时，格式问题、测试失败、依赖遗漏和构建错误往往要到人工合并后才暴露。CI 把这些检查前移到提交和 Pull Request 阶段，让问题尽早失败、尽早修。

GitHub CI 通常指用 GitHub Actions 实现的持续集成流程：在代码提交或 Pull Request 时自动运行格式检查、静态检查、测试和构建等。它的核心目的不是“帮你发布”，而是在代码合入前确认项目仍然处于可工作的状态。

GitHub Actions 的工作流文件一般放在仓库的 `.github/workflows/` 目录下，文件格式是 [[通用计算机知识/notes/数据格式/4、YAML|YAML]]。一个工作流由触发条件、权限、环境变量、Job 和 Step 组成。

```text
事件触发
  ↓
创建临时运行环境
  ↓
检出代码
  ↓
安装依赖或工具链
  ↓
运行检查、测试、构建
  ↓
返回成功或失败
```

> 简单来说，CI 是把“本地应该跑的检查”搬到统一、可复现的远端环境里，避免只在某个人机器上能通过。

# 二、工作流文件的核心结构

## 1、name：工作流名称

`name` 是工作流在 GitHub Actions 页面上显示的名字。

示例：

```yaml
name: Rust CI
```

这个名字只影响显示，不影响执行逻辑。

## 2、on：触发条件

`on` 定义什么时候运行工作流。最常见的是 `pull_request` 和 `push`。

示例：

```yaml
on:
  pull_request:
    branches:
      - main

  push:
    branches:
      - main
```

这里表示：

- **Pull Request 目标分支是 `main` 时运行**：用于检查准备合入 `main` 的代码。
- **有提交进入 `main` 时运行**：用于确认已经进入主分支的代码仍然可用。

需要注意的是，`pull_request.branches` 匹配的是 Pull Request 的目标分支，不是来源分支。

## 3、permissions：工作流权限

`permissions` 控制 GitHub 自动生成的 `GITHUB_TOKEN` 能做什么。只做 CI 检查时，通常只需要读取仓库内容。

示例：

```yaml
permissions:
  contents: read
```

这表示工作流可以读取仓库代码，但不能推送提交、创建 Release 或修改仓库内容。

> 注意：权限默认值可能受仓库和组织设置影响。显式写出最小权限，比依赖默认配置更稳。

## 4、env：全局环境变量

`env` 定义工作流、Job 或 Step 中可用的环境变量。

示例：

```yaml
env:
  CARGO_TERM_COLOR: always
```

对 Rust 项目来说，`CARGO_TERM_COLOR=always` 会让 Cargo 在 Actions 日志里保留彩色输出，便于区分错误、警告和构建状态。它只影响日志显示，不影响检查结果。

# 三、Job 和 Step 的执行模型

## 1、jobs：一组独立任务

一个工作流可以包含多个 Job。每个 Job 通常在独立运行器上执行。

示例：

```yaml
jobs:
  rust-checks:
    name: Rust checks
    runs-on: ubuntu-latest
```

这里的含义是：

- `rust-checks`：Job 的内部标识符。
- `name: Rust checks`：GitHub 页面上显示的 Job 名称。
- `runs-on: ubuntu-latest`：在 GitHub 提供的 Ubuntu 运行器上执行。

`ubuntu-latest` 是浮动标签，GitHub 可能随时间切换到底层更新的 Ubuntu 版本。如果项目对系统版本敏感，应改用固定运行环境。

## 2、steps：Job 内部的顺序步骤

`steps` 是 Job 中按顺序执行的动作。前一个 Step 失败时，后续 Step 默认不会继续执行。

示例：

```yaml
steps:
  - name: Checkout repository
    uses: actions/checkout@v6

  - name: Check formatting
    run: cargo fmt --all -- --check
```

Step 有两种常见写法：

- **`uses`**：调用已有 GitHub Action，例如检出代码。
- **`run`**：直接执行命令，例如运行测试。

`actions/checkout` 用于把仓库代码下载到运行器的工作目录中。没有这一步，后面的 `cargo fmt`、`cargo test` 等命令通常找不到项目文件。

> 注意：第三方 Action 版本要固定到明确版本，如 `@v6` 或具体提交 SHA。不要长期使用浮动分支名作为关键 CI 依赖。

# 四、Rust 项目的典型 CI

## 1、完整示例

下面是一份 Rust 命令行项目常见的 CI 配置：

```yaml
name: Rust CI

on:
  pull_request:
    branches:
      - main

  push:
    branches:
      - main

permissions:
  contents: read

env:
  CARGO_TERM_COLOR: always

jobs:
  rust-checks:
    name: Rust checks
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v6

      - name: Set up Rust
        run: |
          rustup toolchain install stable --profile minimal --component rustfmt,clippy
          rustup default stable

      - name: Check formatting
        run: cargo fmt --all -- --check

      - name: Run Clippy
        run: cargo clippy --all-targets --all-features --locked -- -D warnings

      - name: Run tests
        run: cargo test --all-targets --all-features --locked

      - name: Build release
        run: cargo build --release --locked
```

这份配置覆盖了四类基础质量门禁：格式、静态检查、测试和 release 构建。

## 2、安装 Rust 工具链

```yaml
- name: Set up Rust
  run: |
    rustup toolchain install stable --profile minimal --component rustfmt,clippy
    rustup default stable
```

`rustup toolchain install stable` 安装 stable Rust 工具链。`--profile minimal` 减少不必要组件下载，`--component rustfmt,clippy` 额外安装格式化和静态检查工具。

如果仓库已经有 `rust-toolchain.toml`，通常可以让 CI 读取仓库内固定的 Rust 版本，而不是在命令里手写 `stable`。

## 3、检查格式

```yaml
- name: Check formatting
  run: cargo fmt --all -- --check
```

`cargo fmt --all` 检查整个 Cargo 工作区。后面的 `-- --check` 表示把 `--check` 传给底层 `rustfmt`，只检查格式，不自动修改文件。

CI 不应该偷偷改代码。格式不对时让工作流失败，再由开发者本地运行 `cargo fmt --all` 修复。

## 4、运行 Clippy

```yaml
- name: Run Clippy
  run: cargo clippy --all-targets --all-features --locked -- -D warnings
```

这条命令做了几件事：

- **`--all-targets`**：检查库、二进制、测试、示例等目标。
- **`--all-features`**：启用所有 Cargo feature。
- **`--locked`**：禁止 CI 自动修改 `Cargo.lock`。
- **`-D warnings`**：把 warning 当作 error。

> 注意：如果项目的 feature 互相排斥，就不能简单使用 `--all-features`。这种情况下应拆成多个明确的 feature 组合。

## 5、运行测试

```yaml
- name: Run tests
  run: cargo test --all-targets --all-features --locked
```

`cargo test` 会编译并运行测试。配合 `--all-targets` 和 `--all-features`，可以发现只在测试、示例或可选功能中出现的问题。

## 6、构建 release

```yaml
- name: Build release
  run: cargo build --release --locked
```

`cargo build --release` 使用发布配置编译项目。它不会自动上传二进制产物，只是确认正式构建配置能通过。

# 五、常见配置取舍

## 1、是否固定 Rust 版本

| 方案 | 适用场景 | 代价 |
|---|---|---|
| `stable` | 希望持续跟进稳定版 Rust | CI 结果可能随 Rust 更新变化 |
| `rust-toolchain.toml` | 希望团队和 CI 使用同一版本 | 需要主动升级工具链 |
| 手写具体版本 | 临时固定环境 | 版本信息分散在 CI 文件里 |

普通项目优先使用 `rust-toolchain.toml`。这样本地和 CI 更一致，CI 文件也更少藏项目策略。

## 2、是否使用缓存

Cargo 缓存可以减少下载和编译时间，但不是最小可用 CI 的必需项。

先写无缓存版本更简单。只有当 CI 变慢且影响开发节奏时，再引入缓存，例如缓存 Cargo registry、Git 依赖和 `target/` 中可复用的部分。

## 3、是否拆分多个 Job

单 Job 的优点是配置短、执行顺序清楚。缺点是格式检查失败时，测试结果也看不到。

多个 Job 可以并行运行格式、Clippy、测试和构建，但配置会变多。项目小的时候，单 Job 足够；项目变大或 CI 时间明显变长时，再拆分。


# 六、排查 CI 失败的顺序

## 1、先看失败的 Step

GitHub Actions 日志会标出哪个 Step 失败。排查时先定位失败 Step，再看该 Step 的最后一段错误输出。

常见对应关系：

| 失败 Step | 常见原因 | 本地复现命令 |
|---|---|---|
| Check formatting | 代码格式不符合 rustfmt | `cargo fmt --all -- --check` |
| Run Clippy | Clippy lint 或 warning | `cargo clippy --all-targets --all-features --locked -- -D warnings` |
| Run tests | 测试失败或测试目标编译失败 | `cargo test --all-targets --all-features --locked` |
| Build release | release 配置编译失败 | `cargo build --release --locked` |

## 2、优先本地复现

CI 命令应该尽量能在本地直接运行。能本地复现，就不要只在网页日志里猜。

如果本地通过但 CI 失败，优先检查：

- Rust 版本是否一致。
- 操作系统是否一致。
- 环境变量是否一致。
- 是否漏提交 `Cargo.lock`。
- 是否依赖本地没有提交的文件。

# 七、小结

GitHub CI 的最小有效版本是：在 Pull Request 和主分支提交时，自动检出代码并运行项目必须通过的检查。Rust 项目通常先覆盖 `cargo fmt`、`cargo clippy`、`cargo test` 和 `cargo build --release`。

配置 CI 时先保持简单：固定最小权限、明确触发条件、能本地复现每条命令。缓存、矩阵、多 Job 和发布流程都可以等项目真的需要时再加。
