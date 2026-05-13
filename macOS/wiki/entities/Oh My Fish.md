---
title: Oh My Fish
date: 2026-05-14
tags: [shell]
source_count: 1
---

Oh My Fish（简称 OMF）是一个 fish shell 框架，用于安装和管理 fish 的主题、插件和扩展。

## 安装

```shell
curl -L https://raw.githubusercontent.com/oh-my-fish/oh-my-fish/master/bin/install | fish
```

安装完成后 fish 提示符可能会发生变化。

## 常用命令

### 查看已安装包

```shell
omf list
```

### 主题管理

查看可用主题：
```shell
omf theme
```

安装主题（如 `clearance`）：
```shell
omf install clearance
```

切换主题：
```shell
omf theme clearance
```

移除主题或插件：
```shell
omf remove clearance
```

### 更新

```shell
omf update          # 更新所有包
omf update omf      # 仅更新 OMF 本身
omf update clearance # 更新指定包
```

### 卸载

```shell
omf destroy
```

## 来源

- [[fish shell 安装与使用]]
