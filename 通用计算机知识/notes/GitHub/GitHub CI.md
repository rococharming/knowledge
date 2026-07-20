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

![[assets/Pasted image 20260720154919.png|600]]

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

## 5、jobs：一组独立任务

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

`ubuntu-latest` 是一个别名，不是固定系统版本。它当前指向 GitHub 认为最新稳定的 Ubuntu runner 镜像。GitHub 官方说明 `-latest` 标签会逐步迁移，迁移期可能持续 1-2 个月；如果不想被自动迁移影响，应写固定标签，比如`ubuntu-24.04`。

## 6、steps：Job 内部的顺序步骤

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

# 三、Rust 项目的典型 CI

## 1、跨平台完整示例

下面是一份 Rust 命令行项目常见的跨平台 CI 配置。它会在 Linux x64、Windows x64、macOS ARM64 和 macOS Intel x64 四种环境里运行同一组检查，并构建 release 产物。

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
  build:
    name: Build ${{ matrix.name }}
    runs-on: ${{ matrix.os }}

    strategy:
      fail-fast: false
      matrix:
        include:
          - name: Linux x64
            os: ubuntu-24.04
            target: x86_64-unknown-linux-gnu
            artifact: release-linux-x64

          - name: Windows x64
            os: windows-2025
            target: x86_64-pc-windows-msvc
            artifact: release-windows-x64

          - name: macOS ARM64
            os: macos-15
            target: aarch64-apple-darwin
            artifact: release-macos-arm64

          - name: macOS Intel x64
            os: macos-15-intel
            target: x86_64-apple-darwin
            artifact: release-macos-intel-x64

    steps:
      - name: Checkout repository
        uses: actions/checkout@v6

      - name: Set up Rust
        run: |
          rustup toolchain install stable --profile minimal --component rustfmt,clippy
          rustup default stable
          rustup target add ${{ matrix.target }}

      - name: Check formatting
        run: cargo fmt --all -- --check

      - name: Run Clippy
        run: cargo clippy --all-targets --all-features --locked --target ${{ matrix.target }} -- -D warnings

      - name: Run tests
        run: cargo test --all-targets --all-features --locked --target ${{ matrix.target }}

      - name: Build release
        run: cargo build --release --locked --target ${{ matrix.target }}

      - name: Upload release artifact
        uses: actions/upload-artifact@v7
        with:
          name: ${{ matrix.artifact }}
          path: target/${{ matrix.target }}/release
          if-no-files-found: error
          retention-days: 7
```

这份配置覆盖了四类基础质量门禁：格式、静态检查、测试和 release 构建。它还通过 `strategy.matrix` 把同一个 Job 展开成四个平台版本，用同一套步骤验证项目在不同操作系统和 CPU 架构上的表现。最后的 `Upload release artifact` 会把每个平台的 release 构建目录上传到本次 Actions 运行记录里，方便在 CI 页面下载。

## 2、Job 与 matrix

```yaml
jobs:
  build:
    name: Build ${{ matrix.name }}
    runs-on: ${{ matrix.os }}
```

`build` 是 Job 的内部标识符。它主要给工作流内部引用使用，例如其他 Job 可以通过 `needs: build` 表示“等 build 这个 Job 完成后再运行”。

`name: Build ${{ matrix.name }}` 是 GitHub Actions 页面上显示的名称。`${{ matrix.name }}` 会被替换为当前 matrix 项里的 `name`，所以最终会显示成 `Build Linux x64`、`Build Windows x64`、`Build macOS ARM64` 等。

`runs-on: ${{ matrix.os }}` 表示当前 Job 要在哪种 GitHub-hosted runner 上执行。`${{ matrix.os }}` 会被替换为 `ubuntu-24.04`、`windows-2025`、`macos-15` 或 `macos-15-intel`。

## 3、strategy 与 fail-fast

```yaml
strategy:
  fail-fast: false
  matrix:
    include:
      - name: Linux x64
        os: ubuntu-24.04
        target: x86_64-unknown-linux-gnu
```

`strategy` 定义 Job 的运行策略。最常见的策略是 `matrix`，表示“用多组参数展开同一个 Job”。

`matrix.include` 用对象列表显式描述每一种构建组合。这里每一项都有三个字段：

- `name`：人类可读的平台名称，用在页面显示里。
- `os`：GitHub runner 标签，决定 CI 在哪种机器上运行。
- `target`：Rust 编译目标，决定 Cargo 生成给哪个平台和架构运行的二进制。
- `artifact`：上传到 GitHub Actions 页面时使用的产物名称。

`fail-fast: false` 表示 matrix 中某个平台失败时，不要提前取消其他平台。例如 Linux 失败后，Windows 和 macOS 仍然会继续运行。跨平台 CI 通常建议这样写，因为它能一次看出到底是单个平台失败，还是所有平台都失败。

## 4、Rust target

`target` 的名字是 Rust 工具链约定好的固定名称，不能随便起。常见 target 如下：

| target | 含义 |
|---|---|
| `x86_64-unknown-linux-gnu` | Linux x64，使用 GNU libc |
| `x86_64-pc-windows-msvc` | Windows x64，使用 MSVC 工具链 |
| `aarch64-apple-darwin` | macOS ARM64，也就是 Apple Silicon |
| `x86_64-apple-darwin` | macOS Intel x64 |

`runs-on` 和 `target` 不是一回事。`runs-on` 决定“CI 在哪台机器上跑”，`target` 决定“编译出来的程序给哪个平台运行”。

```yaml
os: macos-15
target: aarch64-apple-darwin
```

这表示在 GitHub 提供的 macOS ARM64 runner 上运行，并构建 macOS ARM64 二进制。

如果不写 `--target`，Cargo 会默认使用当前 runner 自己的平台。显式写 `target` 的好处是产物平台更清楚，后续上传二进制 artifact 或发布 Release 时也更容易命名和区分。

## 5、Checkout repository

```yaml
- name: Checkout repository
  uses: actions/checkout@v6
```

这一步使用 `actions/checkout` 把当前仓库代码下载到 runner 的工作目录中。没有这一步，后面的 `cargo fmt`、`cargo clippy`、`cargo test` 和 `cargo build` 通常找不到项目文件。

`uses` 表示调用一个已有 Action。`actions/checkout@v6` 中：

- `actions/checkout` 是 Action 名称。
- `@v6` 是版本引用，表示使用该 Action 的 v6 版本。

关键 CI 依赖不要长期写成 `@main` 或 `@master` 这样的浮动分支名。浮动分支名会随着分支最新提交变化，今天和明天运行的代码可能不同。更严格的做法是固定到明确版本标签，甚至固定到完整提交 SHA。

## 6、Set up Rust

```yaml
- name: Set up Rust
  run: |
    rustup toolchain install stable --profile minimal --component rustfmt,clippy
    rustup default stable
    rustup target add ${{ matrix.target }}
```

这一步安装并选择 Rust 工具链，同时安装当前平台要用的编译目标。

第一行：

```bash
rustup toolchain install stable --profile minimal --component rustfmt,clippy
```

参数含义：

- `rustup toolchain install stable`：安装 Rust stable 工具链。
- `--profile minimal`：使用最小安装配置，减少 CI 下载和安装时间。
- `--component rustfmt,clippy`：额外安装 `rustfmt` 和 `clippy` 组件。

`rustfmt` 是 Rust 官方格式化工具，供 `cargo fmt` 使用。`clippy` 是 Rust 官方静态检查工具，供 `cargo clippy` 使用。

第二行：

```bash
rustup default stable
```

把当前 runner 的默认 Rust 工具链切换为 `stable`。后续执行 `cargo`、`rustc` 时会默认使用 stable。

第三行：

```bash
rustup target add ${{ matrix.target }}
```

安装当前 matrix 指定的 Rust 编译目标。例如在 `macOS ARM64` 这一项里，`${{ matrix.target }}` 会替换成 `aarch64-apple-darwin`。

如果仓库已经有 `rust-toolchain.toml`，通常可以让 CI 读取仓库内固定的 Rust 版本，而不是在命令里手写 `stable`。

## 7、Check formatting

```yaml
- name: Check formatting
  run: cargo fmt --all -- --check
```

这一步检查代码格式。

参数含义：

- `cargo fmt`：通过 Cargo 调用 `rustfmt`。
- `--all`：检查整个 Cargo workspace 中的所有 package。
- `--`：Cargo 参数和 `rustfmt` 参数的分隔符。前面的参数给 `cargo fmt`，后面的参数转交给底层 `rustfmt`。
- `--check`：只检查格式是否正确，不自动修改文件。

CI 不应该偷偷改代码。格式不对时让工作流失败，再由开发者本地运行 `cargo fmt --all` 修复。

## 8、Run Clippy

```yaml
- name: Run Clippy
  run: cargo clippy --all-targets --all-features --locked --target ${{ matrix.target }} -- -D warnings
```

这一步运行 Clippy 静态检查。

参数含义：

- `cargo clippy`：运行 Rust 官方 Clippy 检查器。
- `--all-targets`：检查库、二进制、测试、示例和 benchmark 等目标。
- `--all-features`：启用所有 Cargo feature。
- `--locked`：要求使用现有 `Cargo.lock`，不允许 CI 自动解析出新版本并改动锁文件。
- `--target ${{ matrix.target }}`：针对当前 matrix 指定的平台进行检查。
- `--`：Cargo/Clippy 参数分隔符。后面的参数传给 Clippy。
- `-D warnings`：deny warnings，把所有 warning 当作 error。

`-D warnings` 的好处是避免 warning 长期堆积；代价是 Rust 或 Clippy 升级后，新出现的 warning 可能让 CI 失败。

> 注意：如果项目的 feature 互相排斥，就不能简单使用 `--all-features`。这种情况下应拆成多个明确的 feature 组合。

## 9、Run tests

```yaml
- name: Run tests
  run: cargo test --all-targets --all-features --locked --target ${{ matrix.target }}
```

这一步编译并运行测试。

参数含义：

- `cargo test`：编译并运行 Rust 测试。
- `--all-targets`：测试库、二进制、示例等目标中可测试的部分。
- `--all-features`：启用所有 Cargo feature 后运行测试。
- `--locked`：使用现有 `Cargo.lock`，防止 CI 隐式更新依赖版本。
- `--target ${{ matrix.target }}`：为当前平台 target 编译和运行测试。

在这份配置里，每个 target 都在对应的原生 runner 上测试：Windows target 在 Windows runner 上，macOS ARM target 在 macOS ARM runner 上，macOS Intel target 在 macOS Intel runner 上。因此测试可以真正运行，而不是只做交叉编译检查。

## 10、Build release

```yaml
- name: Build release
  run: cargo build --release --locked --target ${{ matrix.target }}
```

这一步构建 release 版本。

参数含义：

- `cargo build`：编译项目。
- `--release`：使用 release profile 编译，通常会开启优化，产物更接近正式发布版本。
- `--locked`：要求依赖版本完全符合 `Cargo.lock`。
- `--target ${{ matrix.target }}`：为当前 matrix 指定的平台生成二进制。

`cargo build --release` 本身不会自动发布，也不会自动上传二进制。它只确认正式构建配置能通过，并在 runner 的临时工作目录里生成 release 产物。要在 CI 页面下载产物，需要继续使用 `actions/upload-artifact` 上传。

## 11、Upload release artifact

```yaml
- name: Upload release artifact
  uses: actions/upload-artifact@v7
  with:
    name: ${{ matrix.artifact }}
    path: target/${{ matrix.target }}/release
    if-no-files-found: error
    retention-days: 7
```

这一步把 release 构建结果上传为 GitHub Actions artifact。工作流完成后，可以在对应的 Actions run 页面下载这些 artifact。

参数含义：

- `uses: actions/upload-artifact@v7`：调用 GitHub 官方的 artifact 上传 Action。
- `with`：给 Action 传入参数。
- `name: ${{ matrix.artifact }}`：artifact 在 Actions 页面显示的名称。例如 `release-linux-x64`、`release-windows-x64`。
- `path: target/${{ matrix.target }}/release`：要上传的文件或目录。这里上传当前 target 的 release 构建目录。
- `if-no-files-found: error`：如果路径没有匹配到文件，就让 step 失败。这样可以避免 CI 看起来成功，但实际没有上传任何产物。
- `retention-days: 7`：artifact 保留 7 天。这个值可以按需要调大，但保留时间越长，占用的存储配额越久。

上传整个 `release` 目录最通用，因为示例不需要提前知道二进制名称。实际项目里，如果只想上传最终二进制，可以把 `path` 收窄到具体文件，例如 Linux/macOS 的 `target/${{ matrix.target }}/release/your_binary_name`，Windows 的 `target/${{ matrix.target }}/release/your_binary_name.exe`。

artifact 只是给 CI 页面下载用，不等于正式发布。若要发布到 GitHub Release，还需要额外的 release job、标签触发条件，以及能写入 Release 的权限。
