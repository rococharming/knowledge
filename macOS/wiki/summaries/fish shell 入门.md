---
title: fish shell 入门
date: 2026-05-14
tags: [shell, terminal, homebrew]
source_count: 1
---

fish（friendly interactive shell）是一个强调易用性和交互体验的 shell，主要面向日常命令行交互使用。

## 核心特点

- **自动建议**：根据历史记录实时建议可能要输入的命令
- **Tab 自动补全**：支持命令、路径、参数等补全
- **内置语法高亮**：命令是否存在、路径是否有效，可直接通过颜色反馈
- **开箱即用**：不需要复杂配置也能有较好的交互体验
- **语法更简洁一致**，但不兼容 POSIX shell

> fish 更适合作为交互式 shell 使用。运行 bash/zsh/sh 脚本时，直接用对应解释器运行即可，无需改写为 fish 语法。

## 安装与配置

macOS 建议通过 Homebrew 安装：

```shell
brew install fish
```

安装后需要了解：
- [[将 fish 设为默认 Shell]] — 系统级默认 shell 切换流程
- [[fish 环境变量配置]] — config.fish 配置文件、PATH 设置、从 zsh 迁移

## 语法差异

fish 语法与 POSIX shell（bash/zsh）有明显不同。详见 [[fish shell 语法]]，涵盖变量赋值、条件判断、循环、函数定义、命令替换、PATH 处理、alias 与 abbreviation 等。

## 主题与插件

fish 自带 Web 配置界面：

```shell
fish_config
```

如需更丰富的主题和插件管理，可使用 [[Oh My Fish]]（OMF）框架。

## 来源

- [[fish shell 安装与使用]]
