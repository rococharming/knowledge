---
title: Xcode Command Line Tools
date: 2026-05-12
tags: [devtools, toolchain]
source_count: 1
---

# Xcode Command Line Tools

Xcode Command Line Tools 是 Apple 提供的一套轻量级命令行开发工具包，面向 Terminal / UNIX 风格的命令行开发场景。

## 包含组件

- `clang` — C / C++ / Objective-C 编译器
- `git` — 版本管理工具
- `make` — 构建工具
- `lldb` — 调试器
- 部分 SDK、系统头文件和开发相关工具
- 与 [[xcodebuild]] 等 Apple 开发工具相关的命令行支持

## 与完整 [[Xcode]] 的区别

| 能力 | Command Line Tools | 完整 Xcode |
|---|---|---|
| C/C++/Obj-C 编译 | ✅ | ✅ |
| `make` / `CMake` / `Ninja` 构建 | ✅ | ✅ |
| Homebrew 等包管理器依赖 | ✅ | ✅ |
| 图形界面开发 | ❌ | ✅ |
| iOS/macOS GUI App 开发 | ❌ | ✅ |
| 模拟器 | ❌ | ✅ |
| 工程管理（.xcodeproj） | 仅命令行 | 图形化 + 命令行 |
| 代码签名与发布 | ❌ | ✅ |

## 典型使用场景

- 编译 C / C++ 程序
- 使用 `make` / `CMake` / `Ninja` 构建项目
- 让 [[Homebrew]] 等包管理工具正常工作
- 命令行下的基础开发工作

## 安装

```shell
xcode-select --install
```

安装后 developer directory 通常指向 `/Library/Developer/CommandLineTools`。
