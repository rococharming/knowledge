---
title: Git 安装与配置
date: 2026-07-14
tags: [计算机基础, Git, Git基础, git]
aliases:
  - Git 配置
  - git config
  - Git 安装与配置
---

# 一、Git 的基本定位

Git 是一个分布式版本控制系统，用来记录项目文件在不同时间点的变化。被 Git 管理的项目目录称为仓库，也就是 repository 或 repo。

每一次提交都可以理解为项目在某个时刻的快照。后续查看历史、对比差异、切换分支、协作开发，本质上都是围绕这些快照展开。

| 能力 | 作用 |
|---|---|
| 版本记录 | 保存文件变化历史 |
| 版本回退 | 回到某个历史提交的状态 |
| 差异对比 | 查看文件、提交、分支之间的变化 |
| 分支管理 | 在多条开发线上并行工作 |
| 协同开发 | 通过远程仓库进行多人协作 |

# 二、安装 Git

## 1、通过 Xcode Command Line Tools 安装

在 macOS 上，最常见的安装方式是安装 Xcode Command Line Tools。它会同时提供 Git、编译器、`make` 和系统头文件等命令行开发工具。

```shell
xcode-select --install
```

安装完成后检查版本：

```shell
git --version
```

## 2、通过 Homebrew 安装

如果希望更方便地升级 Git，也可以使用 Homebrew：

```shell
brew install git
brew upgrade git
```

Xcode Command Line Tools 适合系统基础开发环境，Homebrew 适合希望使用较新 Git 版本的场景。

# 三、初始化用户配置

## 1、配置提交身份

Git 提交会记录作者姓名和邮箱。首次使用前应设置全局身份：

```shell
git config --global user.name "Zhang San"
git config --global user.email "zhangsan@example.com"
```

这些配置会写入当前用户的全局配置文件：

```text
~/.gitconfig
```

提交记录中的作者信息大致如下：

```text
Author: Zhang San <zhangsan@example.com>
```

邮箱最好使用 GitHub、GitLab 或 Gitee 等平台已绑定的邮箱，这样平台才能把提交正确关联到账号。

## 2、查看配置结果

```shell
git config --global user.name
git config --global user.email
git config --global --list
```

如果要排查某个配置来自哪里，可以加上来源信息：

```shell
git config --list --show-origin
```

# 四、Git 配置级别

Git 配置可以来自多个级别。越靠近当前仓库，优先级越高。

| 级别 | 作用范围 | 常见位置 |
|---|---|---|
| `system` | 当前系统所有用户 | 系统级配置文件 |
| `global` | 当前用户所有仓库 | `~/.gitconfig` |
| `local` | 当前仓库 | `.git/config` |

优先级通常是：

```text
local > global > system
```

因此，如果某个仓库提交时仍然使用旧邮箱，常见原因是该仓库存在本地配置覆盖了全局配置。

## 1、全局配置

全局配置适合保存通用偏好：

```shell
git config --global user.name "Zhang San"
git config --global user.email "zhangsan@example.com"
git config --global init.defaultBranch main
```

## 2、本地配置

在 Git 仓库中不加 `--global` 时，配置会写入当前仓库：

```shell
git config user.name "Work Account"
git config user.email "work@example.com"
git config --local --list
```

本地配置适合区分个人项目和公司项目的提交身份。

# 五、常用初始配置

## 1、默认分支名

新建仓库时，可以把默认分支设为 `main`：

```shell
git config --global init.defaultBranch main
```

之后执行 `git init` 创建的新仓库会默认使用 `main`。仓库初始化流程见 [[2、创建 Git 仓库|创建 Git 仓库]]。

## 2、默认编辑器

Git 在不带 `-m` 的 `git commit`、`git commit --amend`、合并、变基等操作中可能打开编辑器。若希望默认使用 VS Code：

```shell
git config --global core.editor "code --wait"
```

`code --wait` 的关键是 `--wait`：Git 会等待编辑器中文件保存并关闭后，再继续执行后续操作。

> [!tip] VS Code 需要安装命令行入口
> 如果终端中不能执行 `code --version`，需要在 VS Code 命令面板中运行 `Shell Command: Install 'code' command in PATH`。

## 3、凭证管理

macOS 上常见的 HTTPS 凭证管理配置是：

```shell
git config credential.helper
```

如果输出：

```text
osxkeychain
```

说明 Git 会把 HTTPS 认证凭证交给 macOS 钥匙串保存。

# 六、远程认证方式

Git 认证通常发生在访问远程仓库时，例如：

```shell
git clone https://github.com/user/repo.git
git pull
git push
```

HTTPS 地址通常使用 Personal Access Token（PAT）认证。PAT 可以理解为专门给 Git 命令使用的访问令牌，权限可控，也可以单独撤销。

SSH 地址通常形如：

```text
git@github.com:user/repo.git
```

配置好 SSH 公钥后，克隆、拉取和推送时通常不需要反复输入 Token。

# 七、小结

Git 安装后先完成三类配置：提交身份、默认分支、默认编辑器。配置问题优先用 `git config --list --show-origin` 排查，因为同一配置项可能被本地仓库覆盖。

下一步可以从 [[2、创建 Git 仓库|创建仓库]] 开始，理解 `.git` 目录如何把普通目录变成可版本控制的仓库。
