---
title: xcodebuild
date: 2026-05-12
tags: [devtools, toolchain]
source_count: 1
---

# xcodebuild

`xcodebuild` 是 Apple 提供的命令行构建工具，用于在终端中对 [[Xcode project]] 或 [[Xcode workspace]] 执行构建、测试、归档等操作。

## 核心概念

- `.xcodeproj` — Xcode project 文件，包含单个项目的构建配置
- `.xcworkspace` — Xcode workspace 文件，可包含多个 project，常见于 CocoaPods / Swift Package Manager 等依赖管理场景
- `scheme` — 构建方案，定义了要构建的 target、配置和动作

## 常用命令

### 查看 Xcode 版本

```shell
xcodebuild -version
```

### 构建 project

```shell
xcodebuild -project Demo.xcodeproj -scheme Demo build
```

### 构建 workspace

```shell
xcodebuild -workspace Demo.xcworkspace -scheme Demo build
```

### 其他常见动作

| 动作 | 说明 |
|---|---|
| `build` | 编译构建 |
| `test` | 运行测试 |
| `archive` | 归档（用于分发） |
| `clean` | 清理构建产物 |

## 完整命令格式

```shell
xcodebuild -project <项目名>.xcodeproj \
           -scheme <方案名> \
           -configuration <Debug|Release> \
           -destination <设备指定> \
           <动作>
```

## 前置条件

`xcodebuild` 依赖当前激活的 developer directory（由 [[xcode-select]] 管理）。确保路径指向正确的 [[Xcode]] 或 [[Xcode Command Line Tools]] 安装位置。
