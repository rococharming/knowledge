---
title: Homebrew 安装与使用
date: 2026-05-13
tags: [homebrew, devtools]
source_count: 1
---

# Homebrew 安装与使用

本文是关于 Homebrew 安装与使用的完整入门指南摘要，涵盖从安装前准备到常用命令操作的完整流程。

## 核心内容

1. **Homebrew 简介**：macOS 上最常用的包管理器，支持命令行工具和图形界面应用（通过 Cask）的统一管理
2. **安装前准备**：需要先安装 [[Xcode Command Line Tools]]，提供 `clang`、`git`、`make` 等基础工具
3. **安装方式**：官方脚本（从 GitHub 下载）或国内镜像脚本（第三方维护）
4. **环境变量配置**：Apple Silicon（`/opt/homebrew`）与 Intel（`/usr/local`）芯片的路径差异
5. **验证安装**：`brew --version` 和 `brew doctor`
6. **常用命令**：搜索、安装、列出、更新、升级、清理、卸载等 `brew` 子命令

## 关键要点

- Homebrew 的核心价值在于将 macOS 软件安装标准化，省去手动处理依赖和环境变量的步骤
- Cask 机制使 Homebrew 不仅限于命令行工具，还能管理日常 GUI 应用
- `brew update` 只更新索引，`brew upgrade` 才实际升级软件
- `brew cleanup` 配合 `-n` 预演模式，可安全释放旧版本占用的磁盘空间

## 相关页面

- [[Homebrew]] — Homebrew 实体页面，含核心概念（Formula、Cask、Tap）和完整命令参考
- [[Homebrew 安装与配置]] — 分步安装指南，含芯片差异和常见问题排查
- [[Xcode Command Line Tools]] — 安装 Homebrew 的前置依赖
