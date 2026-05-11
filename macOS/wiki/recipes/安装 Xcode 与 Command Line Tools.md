---
title: 安装 Xcode 与 Command Line Tools
date: 2026-05-12
tags: [devtools, toolchain, macos-tips]
source_count: 1
---

# 安装 Xcode 与 Command Line Tools

## 方案一：安装 Xcode Command Line Tools（轻量）

适用于仅需命令行开发场景，如编译 C/C++、运行 [[Homebrew]]、使用 `make` 等。

### 步骤

1. 在终端执行：

```shell
xcode-select --install
```

2. 系统弹出安装提示，点击"安装"
3. 等待下载完成（约 1GB）

### 验证

```shell
xcode-select --print-path
```

预期输出：
```
/Library/Developer/CommandLineTools
```

## 方案二：安装完整 Xcode（完整功能）

适用于 iOS/macOS/watchOS/tvOS/visionOS App 开发、使用模拟器、图形化调试等场景。

### 方式 A：App Store（推荐）

1. 打开 App Store
2. 搜索 "Xcode"
3. 点击"获取"并安装（约 10GB+，下载时间较长）

### 方式 B：Apple Developer 网站

1. 访问 [Apple Developer 下载页面](https://developer.apple.com/download/all/)
2. 登录 Apple Developer 账号
3. 搜索并下载所需版本的 `.xip` 文件
4. 解压后拖拽到 `/Applications`

**适用场景**：需要安装旧版本 Xcode、或 App Store 版本与当前 macOS 版本不兼容时。

### 验证

```shell
xcode-select --print-path
```

预期输出：
```
/Applications/Xcode.app/Contents/Developer
```

## 切换工具链

若同时安装了 Command Line Tools 和完整 Xcode，可通过 [[xcode-select]] 切换：

```shell
# 切换到完整 Xcode
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer

# 重置为默认
sudo xcode-select --reset
```

## 常见问题

| 问题 | 解决 |
|---|---|
| `xcode-select: error: tool 'xcodebuild' requires Xcode` | 当前激活的是 Command Line Tools，未安装完整 Xcode |
| Homebrew 提示需要 Command Line Tools | 执行 `xcode-select --install` |
| 多版本 Xcode 共存 | 使用 `xcode-select --switch` 指定具体版本路径 |
