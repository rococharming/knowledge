# 一、简介

## 1、Xcode Command Line Tools

Xcode Command Line Tools，即Xcode命令行工具，是Apple提供的一个**轻量级命令行开发工具包**，主要面向 Terminal / UNIX 风格的命令行开发场景。

它通常包含：

- `clang`：C / C++ / Object-C 编译器
- `git`：版本管理工具
- `make`：构建工具
- `lldb`：调试器
- 部分SDK、系统头文件和开发相关工具
- 与`xcodebuild`等Apple开发工具相关的命令行支持  

Xcode Command Line Tools 适合在终端中进行基础开发工作，例如编译 C / C++ 程序、使用 `make` / `CMake` / `Ninja` 构建项目，以及让 Homebrew 等包管理工具正常工作。

它可以满足很多命令行开发需求，但并不能完全替代完整 Xcode。比如开发 iOS / macOS 图形界面 App、使用模拟器、管理 Xcode 工程、签名、归档和发布应用，通常仍然需要安装完整 Xcode。

## 2、Xcode

Xcode 是 Apple 提供的完整开发工具套件，本质上是一个 IDE。

除了命令行工具以外，Xcode 还包含：

- 图形化代码编辑器
- 工程管理工具
- 调试器
- iOS / watchOS / tvOS / visionOS 模拟器
- 性能分析工具
- 代码签名和证书管理
- App 打包、归档和发布能力

Xcode 适合开发 iOS、macOS、watchOS、tvOS、visionOS 等 Apple 平台应用，也适合管理 Xcode 工程、运行模拟器、调试、测试、归档和发布应用。

## 3、xcode-select命令

`xcode-select`命令用来**查看或切换当前激活的developer directory**。

> 可以理解为：告诉系统“当前命令行环境应该使用哪一套 Apple 开发者工具”

常见用途如下：

- 查看当前激活路径：

```shell
xcode-select --print-path
```

- 切换到完整`Xcode`

```shell
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
```

- 安装 Xcode Command Line Tools

```shell
xcode-select --install
```

如果只安装了 Command Line Tools，当前路径通常类似：

```text
/Library/Developer/CommandLineTools
```

如果切换到了完整 Xcode，当前路径通常类似：

```text
/Applications/Xcode.app/Contents/Developer
```

## 4、xcodebuild命令

`xcodebuild`是Apple提供的**命令行构建工具**。可以在终端对`Xcode project`或`workspace`执行构建、测试、归档等操作。

常见用途如下：

- 查看 Xcode 版本

```shell
xcodebuild -version
```

或者：

```shell
xcodebuild --version
```

- 命令行编译 Xcode 工程

```shell
xcodebuild -project Demo.xcodeproj -scheme Demo build
```

- 命令行编译 workspace：

```shell
xcodebuild -workspace Demo.xcworkspace -scheme Demo build
```

其中：

- `.xcodeproj` 是 Xcode project 文件；
- `.xcworkspace` 是 Xcode workspace 文件，常见于 CocoaPods 等依赖管理场景；
- `scheme` 表示要构建的方案；
- `build` 表示执行构建操作。

# 二、安装

## 1、安装 Xcode Command Line Tools

可以在终端执行：

```
xcode-select --install
```

执行后，系统会弹出安装提示，根据提示安装即可。

## 2、安装 Xcode

可以在 App Store 中搜索并下载安装 Xcode。

也可以从 Apple Developer 网站下载指定版本的 Xcode，适合需要安装旧版本或特定版本 Xcode 的场景。