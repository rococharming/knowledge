---
title: Homebrew 安装与配置
date: 2026-05-13
tags: [homebrew, devtools, shell]
source_count: 1
---

# Homebrew 安装与配置

## 前置条件

安装 Homebrew 前，需要先安装 [[Xcode Command Line Tools]]：

```shell
xcode-select --install
```

若已安装，系统会提示 `command line tools are already installed`。

## 安装步骤

### 官方安装脚本

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

该脚本从 Homebrew 官方 GitHub 仓库下载并执行安装。

### 国内网络替代方案

若访问 GitHub 较慢，可使用第三方镜像脚本（**注意**：非官方维护，使用前应确认来源可信）：

```shell
/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
```

## 配置环境变量

安装完成后，终端通常会提示将 Homebrew 加入 shell 环境变量。根据芯片架构选择对应路径：

### Apple Silicon（M1/M2/M3）

```shell
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### Intel

```shell
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/usr/local/bin/brew shellenv)"
```

> `brew shellenv` 输出一组 `export` 命令，`eval` 将其解析执行，使当前终端立即识别 `brew`。

若未配置环境变量，执行 `brew` 时会提示 `zsh: command not found: brew`。

## 验证安装

```shell
brew --version
```

正常输出类似：

![[Pasted image 20260513013040.png]]

进一步检查环境健康：

```shell
brew doctor
```

若输出 `Your system is ready to brew.`，说明环境正常。

## 常见问题

| 问题 | 原因 | 解决 |
|---|---|---|
| `command not found: brew` | 环境变量未配置 | 执行对应芯片的 `brew shellenv` 配置 |
| 安装脚本下载失败 | 网络问题 | 尝试镜像脚本或代理 |
| `brew doctor` 报错 | 权限或路径问题 | 按提示修复，通常是目录权限 |

## 参考

- 完整命令参考：[[Homebrew]]
- 前置工具：[[Xcode Command Line Tools]]

## 来源

- [[Homebrew安装与使用]]
