---
title: Xcode 与命令行工具
date: 2026-05-12
tags: [devtools, toolchain]
source_count: 1
---

# Xcode 与命令行工具

本文介绍 macOS 上 Apple 开发者工具链的核心组成：完整 [[Xcode]] IDE、轻量级的 [[Xcode Command Line Tools]]，以及命令行管理工具 [[xcode-select]] 和构建工具 [[xcodebuild]]。

## 核心内容

### 工具链层次

| 工具 | 定位 | 适用场景 |
|---|---|---|
| [[Xcode Command Line Tools]] | 轻量命令行工具包 | 终端编译、Homebrew、基础开发 |
| [[Xcode]] | 完整 IDE | GUI App 开发、模拟器、调试、发布 |
| [[xcode-select]] | 工具链切换器 | 管理多套开发者工具路径 |
| [[xcodebuild]] | 命令行构建器 | 终端编译 Xcode project/workspace |

### 关键要点

- Command Line Tools 包含 `clang`、`git`、`make`、`lldb` 等核心工具，体积约 1GB
- Xcode 在 Command Line Tools 基础上增加了图形编辑器、模拟器、Instruments、代码签名和 App Store 发布能力，体积约 10GB+
- `xcode-select` 用于查看和切换当前激活的 developer directory，典型路径为 `/Library/Developer/CommandLineTools`（仅 CLT）或 `/Applications/Xcode.app/Contents/Developer`（完整 Xcode）
- `xcodebuild` 支持对 `.xcodeproj` 和 `.xcworkspace` 执行 `build`、`test`、`archive`、`clean` 等操作

### 相关页面

- [[Xcode]] — 完整 IDE 功能详解
- [[Xcode Command Line Tools]] — 轻量工具包组成与使用
- [[xcode-select]] — 工具链路径管理
- [[xcodebuild]] — 命令行构建详解
- [[安装 Xcode 与 Command Line Tools]] — 分步安装指南
