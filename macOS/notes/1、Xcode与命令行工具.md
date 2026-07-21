---
title: Xcode 与命令行工具
date: 2026-07-21
tags: [macOS, Xcode, toolchain]
aliases:
  - Xcode与命令行工具
  - Xcode Command Line Tools
  - CLT
---

# 一、定位

Xcode 与 Xcode Command Line Tools 都是 Apple 提供的开发工具链，但它们服务的场景不同：前者是完整 IDE 和平台开发套件，后者是更轻量的命令行开发工具包。

日常命令行开发、安装 [[2、Homebrew安装与使用|Homebrew]]、编译 C / C++ 依赖、使用 Git 时，通常只需要 Xcode Command Line Tools。开发 iOS、macOS、watchOS、tvOS、visionOS 应用时，通常需要完整 Xcode。

# 二、工具组成

## 1、Command Line Tools

Xcode Command Line Tools 常简称为 CLT，主要面向 Terminal / UNIX 风格的开发场景。它通常安装在：

```text
/Library/Developer/CommandLineTools
```

CLT 常见内容包括：

- `clang`：C、C++、Objective-C 编译器
- `git`：版本控制工具
- `make`：构建工具
- `lldb`：调试器
- macOS SDK、man pages、系统头文件和其他命令行工具

CLT 的重点是让终端中的开发命令可用，例如编译本地依赖、运行 `make`、让 Homebrew 能构建某些软件包。它适合基础命令行开发，但不能替代完整 Xcode。

> 注意：Apple 官方文档说明，`xcodebuild`、`xctrace` 等命令只随完整 Xcode 提供，不属于单独的 Command Line Tools 包。

## 2、完整 Xcode

Xcode 是 Apple 平台开发的完整工具套件，本质上是 IDE 加开发平台工具集合。它通常安装在：

```text
/Applications/Xcode.app
```

完整 Xcode 包含：

- 图形化代码编辑器和工程管理工具
- Apple 平台 SDK
- iOS、watchOS、tvOS、visionOS 模拟器
- `xcodebuild`、`xcrun`、`xctrace` 等开发命令
- 调试、测试、性能分析、签名、归档和发布能力

如果已经安装完整 Xcode，通常不必再单独安装 CLT；但可以通过 `xcode-select` 指定当前命令行环境使用哪一套开发者目录。

# 三、安装

## 1、安装 CLT

在终端执行：

```shell
xcode-select --install
```

系统会弹出安装窗口，按提示安装即可。新系统上第一次运行 `git`、`clang` 等命令时，也可能触发 CLT 安装提示。

安装完成后，可以查看 CLT 包版本：

```shell
pkgutil --pkg-info=com.apple.pkg.CLTools_Executables
```

## 2、安装 Xcode

完整 Xcode 可以通过 App Store 安装。需要旧版本或特定版本时，可以从 Apple Developer 的下载页面获取。

安装完整 Xcode 后，建议先打开一次 Xcode 接受许可协议并完成初始组件安装。某些命令行构建或模拟器功能依赖这一步。

# 四、选择工具链

## 1、查看路径

`xcode-select` 用来查看或切换当前激活的 developer directory。简单来说，它告诉系统：当前终端命令应该使用哪一套 Apple 开发者工具。

查看当前路径：

```shell
xcode-select --print-path
```

如果当前使用 CLT，路径通常类似：

```text
/Library/Developer/CommandLineTools
```

如果当前使用完整 Xcode，路径通常类似：

```text
/Applications/Xcode.app/Contents/Developer
```

## 2、切换路径

切换到完整 Xcode：

```shell
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
```

切换回 CLT：

```shell
sudo xcode-select --switch /Library/Developer/CommandLineTools
```

如果遇到路径状态异常，也可以重置为系统默认选择：

```shell
sudo xcode-select --reset
```

# 五、验证与排错

## 1、版本检查

检查当前 `clang`：

```shell
clang --version
```

检查当前 `git`：

```shell
git --version
```

如果安装了完整 Xcode，可以检查 Xcode 版本：

```shell
xcodebuild -version
```

如果只安装了 CLT，`xcodebuild` 可能不可用或无法完成完整 Xcode 项目构建，这是正常边界，不应把它当成 CLT 损坏。

## 2、常见问题

| 现象 | 常见原因 | 处理方式 |
|---|---|---|
| `xcode-select: error: command line tools are already installed` | CLT 已安装 | 不需要重复安装，直接验证版本 |
| `invalid active developer path` | 系统升级后开发者目录失效 | 重新运行 `xcode-select --install` |
| Homebrew 编译依赖失败 | CLT 缺失或版本不匹配 | 安装或更新 CLT |
| `xcodebuild` 不可用 | 只安装了 CLT | 安装完整 Xcode 并切换路径 |

# 六、延伸

CLT 是 macOS 开发环境的地基，[[2、Homebrew安装与使用|Homebrew]]、Git、许多语言工具链都会间接依赖它。后续如果开始频繁构建 Apple 平台应用，再安装完整 Xcode 并用 `xcode-select` 明确当前工具链。

参考：

- [Apple Developer：Installing the command-line tools](https://developer.apple.com/documentation/xcode/installing-the-command-line-tools/)
