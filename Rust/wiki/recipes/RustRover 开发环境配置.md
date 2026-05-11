---
title: RustRover 开发环境配置
date: 2026-05-12
tags: [rust, ide, rustrover, setup]
source_count: 1
---

# RustRover 开发环境配置

## 问题

在 RustRover（JetBrains 出品的专用 Rust IDE）中配置 Rust 开发环境，获得开箱即用的代码补全、错误提示、Cargo 集成、运行、测试和调试等功能。

## 前置条件

- 已安装 [RustRover](https://www.jetbrains.com/rust/)
- 已安装 Rust 工具链（[[rustup]]）

## 步骤

### 步骤 1：打开现有项目

如果已使用 `cargo new` 创建了 Rust 项目，直接用 RustRover 打开项目目录即可。RustRover 会自动识别 `Cargo.toml` 并将目录作为 Cargo 项目加载。

### 步骤 2：新建项目（可选）

也可以通过 RustRover 的菜单新建项目：`File → New → Project`，选择 Rust 项目类型，按向导完成创建。

## 核心功能

### 1. 代码补全与错误提示

RustRover 内置 Rust 代码分析引擎，提供：

- **代码补全**：输入前几个字符后自动弹出补全提示，按 `Enter` 或 `Tab` 接受
- **类型提示**：变量和表达式旁显示推断类型
- **错误诊断**：语法错误、类型错误、借用检查问题直接在编辑器中标记
- **Quick Fix**：部分场景下提供快速修复建议

### 2. Cargo 工具窗口

RustRover 对 Cargo 有内置支持。打开项目后，在 IDE 侧边栏可以看到 Cargo 工具窗口（如未显示，通过 `View → Tool Windows → Cargo` 打开）。

Cargo 工具窗口中通常列出项目中的各类 target：

- bin target
- lib target
- test target
- example target
- benchmark target

可直接在工具窗口中运行对应目标，或在终端执行 `cargo` 命令。

### 3. 运行代码

打开 `src/main.rs` 后，`main` 函数左侧会出现绿色运行按钮。点击可选择运行当前程序，或使用顶部工具栏的运行按钮、快捷键运行。

### 4. 调试代码

RustRover 提供完整调试器，支持断点、变量查看、单步执行、内存视图和反汇编视图。

使用方式：

1. 在代码行号左侧点击设置断点
2. 点击 `main` 函数左侧的运行图标
3. 选择 `Debug`
4. 程序运行到断点处暂停
5. 在 Debug 窗口中查看变量、调用栈，并进行单步执行

## 关联

- [[rustup]] — 提供 Rust 编译器和工具链
- [[Cargo]] — RustRover 底层调用 cargo 命令
- [[VS Code Rust 开发环境配置]] — 另一种 IDE 配置方案
