---
title: VS Code Rust 开发环境配置
date: 2026-05-10
tags: [rust, ide, vscode, setup]
source_count: 2
---

# VS Code Rust 开发环境配置

## 问题

在 VS Code 中配置 Rust 开发环境，获得代码补全、类型推导、错误提示、一键运行和调试等功能。

## 前置条件

- 已安装 [VS Code](https://code.visualstudio.com/)
- 已安装 Rust 工具链（[[rustup]]）

## 步骤

### 步骤 1：安装 `code` 命令到 PATH

确保 VS Code 的 `code` 命令已在系统 PATH 中。若终端提示 `code: command not found`，在 VS Code 中打开命令面板（`Cmd+P`），搜索 `> Shell Command` 并选择 `Shell Command: Install 'code' command in PATH`。

### 步骤 2：用 VS Code 打开 Rust 项目

```bash
cargo new my_project
cd my_project
code .
```

### 步骤 3：安装 Rust 插件

在 VS Code 左侧 Extensions（插件）面板中搜索并安装：

1. **rust-analyzer**（必装）
   - 提供代码补全、类型推导、错误提示、跳转到定义等功能
   - 是官方推荐的 Rust 语言服务器

2. **Error Lens**（推荐）
   - 将编译错误和警告直接内嵌显示在代码行旁边
   - 无需查看底部面板即可定位问题

### 步骤 4：验证功能

创建或打开 `src/main.rs`，输入以下内容测试自动补全：

```rust
fn main() {
    let v = vec![1, 2, 3];
    v.    // 输入点后应弹出 Vec 的方法列表
}
```

## 使用方法

### 运行代码

打开 `main.rs`，点击 `main` 函数上方的 **Run** 按钮（▶️），或直接按 `Ctrl+F5`（macOS: `Cmd+F5`）。

### 调试代码

点击 `main` 函数上方的 **Debug** 按钮（🐛），或使用快捷键 `F5`。VS Code 会自动启动调试会话，支持断点、变量查看、单步执行等功能。

### 检查代码

```bash
cargo check
```

或使用 VS Code 命令面板（`Ctrl+Shift+P`）搜索 **Rust Analyzer: Run Cargo Check**。

## 关联

- [[rustup]] — 提供 Rust 编译器和工具链
- [[Cargo]] — VS Code 的 Run/Debug 按钮底层调用 cargo 命令
