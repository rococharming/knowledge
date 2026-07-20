---
title: Rust IDE 环境配置
date: 2026-07-20
tags: [rust, ide, tooling]
source_count: 1
---

# Rust IDE 环境配置

Rust 项目通常围绕 [[Cargo]] 组织，因此 IDE 或编辑器需要识别 `Cargo.toml`、调用 Cargo 命令，并接入 Rust 语言服务器能力。素材主要介绍 VS Code 和 RustRover 两条路径。

## VS Code

创建 Cargo 项目后，可以在项目目录执行：

```shell
code .
```

如果终端提示 `code: command not found`，需要在 VS Code 命令面板中搜索并执行 `Shell Command: Install 'code' command in PATH`。

![[Pasted image 20260511163624.png|600]]

推荐插件：

- `rust-analyzer`：Rust 官方推荐的语言服务器插件，提供补全、类型提示、错误诊断、跳转定义、查找引用和重构等能力。
- `Error Lens`：把错误、警告和提示直接显示在代码行旁边，对初学者更直观。

![[Image 13.png|600]]

安装后，VS Code 可以在编辑 Rust 代码时提供补全，并在 Cargo 项目中显示运行和调试入口。

![[Image 14.png|600]]

## RustRover

RustRover 是 JetBrains 推出的 Rust 专用 IDE。相比 VS Code，它更偏完整 IDE：安装后内置 Rust 项目识别、代码补全、错误提示、Cargo 集成、运行、测试、Git 集成和调试能力。

如果已有 Cargo 项目，可以直接用 RustRover 打开项目目录。RustRover 会识别 `Cargo.toml`，并以它为入口加载 Cargo 项目。

![[Pasted image 20260511224024.png|600]]

Cargo 工具窗口可以展示项目中的 bin target、lib target、test target、example target 和 benchmark target。运行程序时，可以从 `main` 函数旁的运行按钮、顶部工具栏或快捷键启动。

![[Pasted image 20260511225507.png]]

调试时，常见流程是设置断点，点击运行图标并选择 Debug，然后在 Debug 窗口查看变量、调用栈并单步执行。

![[Pasted image 20260511231034.png|600]]

## 选择建议

VS Code 更轻量，适合已经熟悉编辑器扩展生态、希望保持工具链可组合的开发者。RustRover 更完整，适合偏好集成 IDE、希望开箱即用获得 Cargo、运行、测试和调试支持的场景。

## 相关页面

- [[Cargo]]
- [[Rust 安装与镜像源配置]]

## 来源

- [[Rust安装与开发环境配置]]
