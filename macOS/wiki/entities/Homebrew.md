---
title: Homebrew
date: 2026-05-13
tags: [homebrew, devtools, toolchain]
source_count: 1
---

# Homebrew

Homebrew 是 macOS（及 Linux）上的软件包管理器，通过统一的 `brew` 命令完成安装、更新、搜索、卸载等操作，省去手动下载安装包、配置环境变量和处理依赖的繁琐步骤。

Homebrew 官方定位是「macOS 缺失的软件包管理器」，核心解决的是软件安装和维护的标准化问题。

## 核心概念

### Formula

Homebrew 使用 **Formula**（配方）来定义命令行软件的安装规则。每个 Formula 是一个 Ruby 脚本，描述如何下载、编译、安装某个软件。

```shell
brew install node
brew install python
```

### Cask

**Cask** 扩展了 Homebrew 的能力，使其可以安装图形界面应用（GUI apps）。Cask 同样使用 Ruby 脚本定义，但面向的是 `.app`、`.dmg`、`.pkg` 等 macOS 应用包格式。

```shell
brew install --cask google-chrome
brew install --cask visual-studio-code
```

Cask 与 Formula 的区别在于：Formula 通常安装到 `/opt/homebrew/Cellar/`（或 Intel 的 `/usr/local/Cellar/`），而 Cask 安装到 `/Applications/`。

### Tap

**Tap** 是 Homebrew 的第三方软件源机制。除了官方仓库 `homebrew/core` 和 `homebrew/cask`，用户可以添加社区维护的 Tap 来安装更多软件。

```shell
brew tap user/repo
```

## 常用命令

| 命令 | 作用 |
|---|---|
| `brew search <name>` | 搜索软件包 |
| `brew install <name>` | 安装命令行软件 |
| `brew install --cask <name>` | 安装图形界面应用 |
| `brew list` | 列出已安装软件 |
| `brew list --cask` | 列出已安装的 GUI 应用 |
| `brew info <name>` | 查看软件详细信息 |
| `brew update` | 更新本地软件包索引 |
| `brew upgrade` | 升级已安装软件 |
| `brew cleanup` | 清理旧版本和缓存 |
| `brew uninstall <name>` | 卸载软件 |
| `brew doctor` | 检查环境健康状况 |

## 安装路径差异

Homebrew 的安装前缀因芯片架构而异：

- **Apple Silicon**（M1/M2/M3 等）：`/opt/homebrew`
- **Intel**：`/usr/local`

这一差异直接影响环境变量配置和某些软件的路径引用。详见 [[Homebrew 安装与配置]]。

## 与其他工具的关系

- 安装 Homebrew 前通常需要先安装 [[Xcode Command Line Tools]]，提供 `clang`、`git`、`make` 等基础编译工具
- Homebrew 是 macOS 开发环境搭建的首选包管理器，与 [[Xcode]] 共同构成完整的工具链
