---
title: xcode-select
date: 2026-05-12
tags: [devtools, toolchain]
source_count: 1
---

# xcode-select

`xcode-select` 是 Apple 提供的命令行工具，用于查看或切换当前激活的 developer directory——即告诉系统"当前命令行环境应该使用哪一套 Apple 开发者工具"。

## 常用命令

### 查看当前激活路径

```shell
xcode-select --print-path
```

### 切换到完整 Xcode

```shell
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
```

### 安装 Xcode Command Line Tools

```shell
xcode-select --install
```

### 重置为默认路径

```shell
sudo xcode-select --reset
```

## 路径说明

| 安装类型 | 典型路径 |
|---|---|
| 仅 Command Line Tools | `/Library/Developer/CommandLineTools` |
| 完整 Xcode | `/Applications/Xcode.app/Contents/Developer` |
| 多版本 Xcode（示例） | `/Applications/Xcode-15.4.app/Contents/Developer` |

## 关联工具

- [[Xcode]] — 完整 IDE，安装后路径如上
- [[Xcode Command Line Tools]] — 轻量级工具包，独立安装时路径如上
- [[xcodebuild]] — 使用当前激活的 developer directory 进行构建
