---
title: Fish
date: 2026-05-14
tags: [shell, terminal, homebrew]
source_count: 1
---

Fish（friendly interactive shell）是一个面向交互式使用的命令行 shell，以易用性和开箱即用的体验著称。

## 特点

- **自动建议**：根据历史记录实时建议命令
- **Tab 自动补全**：覆盖命令、路径、参数
- **语法高亮**：命令有效性、路径存在性通过颜色即时反馈
- **简洁一致的语法**：设计更现代化，但**不兼容 POSIX shell**

> 注意：fish 定位为交互式 shell。执行现有 bash/zsh/sh 脚本时，应使用对应解释器直接运行，无需改写。

## macOS 安装

通过 Homebrew 安装：

```shell
brew install fish
```

Apple Silicon Mac 上默认安装路径通常为 `/opt/homebrew/bin/fish`。

![[Pasted image 20260513215534.png|400]]

查看版本：

```shell
fish --version
```

## 配置

- [[将 fish 设为默认 Shell]]
- [[fish 环境变量配置]]

## 语法

fish 语法与 bash/zsh 等 POSIX shell 差异较大。主要区别见 [[fish shell 语法]]。

## 主题与插件管理

fish 内置配置工具：

```shell
fish_config
```

提供 Web 界面调整提示符、颜色主题、函数等。

第三方框架可选：

- **[[Oh My Fish]]**：fish shell 框架，用于安装主题和插件
- **Fisher**：轻量级插件管理器
- **Starship**：跨 shell 的轻量提示符工具

## 来源

- [[fish shell 安装与使用]]
