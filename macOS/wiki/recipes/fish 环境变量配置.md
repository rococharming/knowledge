---
title: fish 环境变量配置
date: 2026-05-14
tags: [shell, dotfiles, homebrew]
source_count: 1
---

fish 的用户配置文件为 `~/.config/fish/config.fish`，不读取 `~/.zprofile` 或 `~/.zshrc`。

## 配置文件路径

```text
~/.config/fish/config.fish
```

## 从 zsh 迁移

zsh 中的写法：
```shell
export EDITOR="code"
export PATH="$HOME/.cargo/bin:$PATH"
```

fish 中的等价写法：
```shell
set -gx EDITOR code
fish_add_path $HOME/.cargo/bin
```

## Homebrew 路径配置

若之前在 zsh 的 `~/.zprofile` 中设置过：
```shell
eval "$(/opt/homebrew/bin/brew shellenv)"
```

在 `config.fish` 中可直接沿用：
```shell
eval "$(/opt/homebrew/bin/brew shellenv)"
```

`brew shellenv` 会根据当前 shell 生成匹配的环境变量语法。

或者使用 fish 原生命令：
```shell
fish_add_path /opt/homebrew/bin
```

`fish_add_path` 会避免重复添加路径，是修改 PATH 的推荐方式。

## 变量作用域

| 命令 | 含义 |
|------|------|
| `set NAME VALUE` | 局部变量 |
| `set -x NAME VALUE` | 导出变量 |
| `set -gx NAME VALUE` | 全局导出变量 |

## 来源

- [[fish shell 安装与使用]]
