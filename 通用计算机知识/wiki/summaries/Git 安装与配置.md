---
title: Git 安装与配置
date: 2026-06-05
tags: [git, version-control, tools]
source_count: 1
---

# Git 安装与配置

本文围绕 [[Git]] 在 macOS 上的安装、初始配置与认证方式展开。

## 核心内容

### Git 简介

Git 是一个**分布式版本控制系统**，由 Linus Torvalds 于 2005 年开发。它记录文件在不同时间点的变化，支持版本回退、差异对比、分支管理和协同开发。

### 安装方式

macOS 上两种主要安装途径：

| 方式 | 命令 | 特点 |
|------|------|------|
| Xcode Command Line Tools | `xcode-select --install` | 系统自带，包含 Git 及其他开发工具 |
| Homebrew | `brew install git` | 版本更新更灵活，适合需要新版 Git 的场景 |

### 初始配置

安装后需配置提交身份：

```shell
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

更多配置内容见 [[Git 配置]]。

### 配置级别

Git 配置分三级，优先级为 **local > global > system**：

| 级别 | 作用范围 | 位置 |
|------|----------|------|
| system | 当前系统所有用户 | 系统级配置文件 |
| global | 当前用户所有项目 | `~/.gitconfig` |
| local | 当前仓库 | `.git/config` |

### 认证方式

访问远程仓库时的两种认证方案：

- **HTTPS + PAT**：使用 Personal Access Token 替代密码
- **SSH**：配置 SSH 密钥后免密操作

详见 [[Git 认证]]。

## 来源

- [[Git的安装与配置]]
