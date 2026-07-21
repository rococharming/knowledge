---
title: Homebrew 安装与使用
date: 2026-07-21
tags: [macOS, Homebrew, package-manager]
aliases:
  - Homebrew安装与使用
  - brew
  - Homebrew
---

# 一、定位

Homebrew 是 macOS 上常用的软件包管理器，也支持 Linux。它通过 `brew` 命令安装、更新、查看和卸载软件，适合管理开发工具、命令行程序以及部分图形界面应用。

没有 Homebrew 时，很多开发工具需要手动下载安装包、配置环境变量、处理依赖。使用 Homebrew 后，大部分工具都可以通过统一命令维护。

示例：

```shell
brew install node
brew install python
brew install --cask visual-studio-code
```

# 二、安装准备

## 1、系统要求

Homebrew 官方支持的 macOS 版本会随时间变化。当前官方安装文档建议使用受支持硬件上的较新 macOS，并要求安装 [[1、Xcode与命令行工具|Xcode Command Line Tools]] 或完整 Xcode。

> CLT 主要用于构建源码包和本地依赖。部分瓶装包（bottle）或图形应用（cask）可能不直接编译源码，但把 CLT 作为 macOS 开发环境基础仍然最稳妥。

## 2、默认路径

Homebrew 建议安装在默认前缀，方便直接使用官方预编译包：

| Mac 类型 | 默认路径 |
|---|---|
| Apple Silicon | `/opt/homebrew` |
| Intel | `/usr/local` |

不要把 Homebrew 随意安装到自定义路径。偏离默认路径后，许多预编译包可能无法直接使用，安装速度和稳定性都会变差。

# 三、安装 Homebrew

## 1、官方脚本

Homebrew 官方安装命令使用 `/bin/bash` 执行安装脚本：

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

这条命令会从 Homebrew 官方仓库下载安装脚本，并在执行前说明它将要修改哪些内容。即使当前默认 shell 是 fish，也仍然可以直接运行这条命令，因为它显式调用的是 `/bin/bash`。

## 2、谨慎使用镜像

如果网络访问 GitHub 较慢，可以考虑可信镜像或代理，但核心笔记里不建议长期记录来源不明的一键脚本。安装包管理器相当于把后续软件安装入口交给它，脚本来源必须可验证。

更稳妥的做法是优先使用官方脚本；确实需要镜像时，单独记录镜像来源、维护者、更新时间和回退方式。

# 四、环境变量

## 1、查看前缀

安装完成后，可以查看 Homebrew 前缀：

```shell
brew --prefix
```

如果终端提示 `brew: command not found`，说明 shell 还没有把 Homebrew 的 `bin` 目录加入 `PATH`。

## 2、配置 zsh

Apple Silicon 常见配置：

```shell
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Intel 常见配置：

```shell
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/usr/local/bin/brew shellenv)"
```

`brew shellenv` 会输出适合当前 Homebrew 安装位置的环境变量设置，包括 `PATH`、`MANPATH`、`INFOPATH` 以及 `HOMEBREW_PREFIX` 等变量。

## 3、配置 fish

如果使用 [[3、fish shell 安装与使用|fish shell]]，可以把下面一行写入 `~/.config/fish/config.fish`：

```fish
/opt/homebrew/bin/brew shellenv | source
```

Intel Mac 通常改成：

```fish
/usr/local/bin/brew shellenv | source
```

如果只想让 fish 找到 Homebrew 命令，也可以使用：

```fish
fish_add_path /opt/homebrew/bin
```

不过 `brew shellenv` 更完整，因为它不仅处理 `PATH`，还会设置 Homebrew 相关环境变量。

# 五、验证安装

## 1、版本检查

检查 Homebrew 版本：

```shell
brew --version
```

检查当前环境状态：

```shell
brew doctor
```

如果输出 `Your system is ready to brew.`，说明环境基本正常。`brew doctor` 的警告不一定都是致命错误，但安装路径、权限、CLT 缺失这类问题应优先处理。

## 2、路径检查

查看 `brew` 实际路径：

```shell
command -v brew
```

查看 Homebrew 前缀：

```shell
brew --prefix
```

Apple Silicon 上通常应看到 `/opt/homebrew`，Intel Mac 上通常应看到 `/usr/local`。

# 六、常用命令

## 1、查询与安装

搜索软件：

```shell
brew search node
```

查看软件信息：

```shell
brew info node
```

安装命令行软件包：

```shell
brew install node
```

安装图形界面应用：

```shell
brew install --cask visual-studio-code
```

这里的 `--cask` 表示安装图形界面应用或预编译应用包，不是 `-cask`。

## 2、更新与升级

更新 Homebrew 自身和软件包索引：

```shell
brew update
```

升级已安装软件：

```shell
brew upgrade
```

只升级某一个软件：

```shell
brew upgrade node
```

可以把两者理解为：`brew update` 先更新“软件目录”，`brew upgrade` 再升级“已经安装的软件”。

## 3、列表与清理

查看已安装软件：

```shell
brew list
```

只查看 cask 应用：

```shell
brew list --cask
```

预览清理内容：

```shell
brew cleanup -n
```

真正清理旧版本和缓存：

```shell
brew cleanup
```

## 4、卸载软件

卸载命令行软件包：

```shell
brew uninstall node
```

卸载图形界面应用：

```shell
brew uninstall --cask visual-studio-code
```

# 七、术语

| 术语 | 含义 |
|---|---|
| formula | 命令行软件包定义，通常通过 `brew install` 安装 |
| cask | 图形界面应用或预编译应用包，通常通过 `brew install --cask` 安装 |
| bottle | Homebrew 提供的预编译二进制包 |
| prefix | Homebrew 安装前缀，例如 `/opt/homebrew` |
| Cellar | Homebrew 存放具体软件版本的目录 |
| tap | 第三方或额外的软件包仓库 |

# 八、排错

## 1、命令找不到

如果出现：

```text
zsh: command not found: brew
```

或 fish 中提示找不到 `brew`，优先检查：

```shell
command -v brew
brew --prefix
```

如果 `command -v brew` 没有输出，通常是 shell 环境变量没有配置好。回到“环境变量”一节，根据当前 shell 写入 `brew shellenv`。

## 2、权限异常

日常不要使用 `sudo brew install ...`。Homebrew 的设计是安装后不需要用 `sudo` 管理普通软件包；如果频繁需要 `sudo`，通常说明安装路径或权限被改坏了。

遇到权限问题时，先看 `brew doctor` 的提示，再判断是否需要修复目录所有者或重新安装。

# 九、延伸

Homebrew 是 macOS 开发环境的基础设施之一。安装语言工具链、终端工具、编辑器、数据库和 CLI 时，都可以先考虑 Homebrew；涉及 Apple 开发工具链时，再回到 [[1、Xcode与命令行工具|Xcode 与命令行工具]] 检查 CLT 或完整 Xcode 是否就绪。

参考：

- [Homebrew Documentation：Installation](https://docs.brew.sh/Installation)
- [Homebrew Documentation：Manpage](https://docs.brew.sh/Manpage)
- [Homebrew Documentation：FAQ](https://docs.brew.sh/FAQ)
