---
title: Git 的安装与配置
date: 2026-06-05
tags: [git, version-control]
---

# 一、Git简介

`Git`是一个**分布式版本控制系统**，用于记录文件在不同时间点的变化。

`Git`管理的项目目录称为仓库，即`repository`。仓库中会保存一组提交记录，每一次提交都可以理解为项目在某个时刻的快照。

通过`Git`，可以完成以下工作：

| 功能   | 说明              |
| ---- | --------------- |
| 版本记录 | 记录文件在不同时间点的变化   |
| 版本回退 | 将代码恢复到之前的某个提交状态 |
| 差异对比 | 查看文件、提交、分支之间的差异 |
| 分支管理 | 在不同分支上并行开发功能    |
| 协同开发 | 多人通过远程仓库协作      |
| 问题追踪 | 根据提交历史定位代码变化来源  |
Git 最初由 `Linus Torvalds` 在 2005 年开发，用于管理 Linux 内核源码。现在已经广泛用于软件开发、文档管理、配置文件管理等场景。


# 二、安装Git

## 1、通过 Xcode Command Line Tools 安装

在 macOS 上，最常见的方式就是安装`Xcode Command Line Tools`。它会包含 Git、C/C++编译器、`make`、系统头文件等命令行开发工具。

执行：

```shell
xcode-select --install
```

安装完成后，查看 Git 版本：

```shell
git --version
```

![[assets/Pasted image 20260604230357.png|222]]


## 2、通过 Homebrew 安装 Git

如果已经使用`Homebrew`管理开发工具，也可以使用 `Homebrew` 安装 Git。

```shell
brew install git
```

后续升级 Git：

```shell
brew upgrade git
```

macOS 通常已经可以通过 `Xcode Command Line Tools` 获得 Git。使用 Homebrew 安装的好处是版本更新更方便，适合希望使用较新 Git 版本的场景。

# 三、初始化 Git 配置

## 1、配置用户名和邮箱

安装 Git 后，需要先设置提交使用的用户名和邮箱。

```shell
git config --global user.name "Zhang San"
git config --global user.email "zhangsan@example.com"
```

这两个配置会写入当前用户的全局 Git 配置文件：

```shell
~/.gitconfig
```

每次执行 `git commit` 时，Git 都会把当前配置的 `user.name` 和 `user.email` 写入提交记录。

提交记录中的作者信息大致类似：

```text
Author: Zhang San <zhangsan@example.com>
```

这里的邮箱建议使用 GitHub、GitLab、Gitee 等代码托管平台中绑定过的邮箱。这样平台才能把提交记录正确关联到你的账号。

如果用户名中包含空格，需要使用引号包裹：

```shell
git config --global user.name "Zhang San"
```

如果没有空格，也可以不写引号：

```shell
git config --global user.name zhangsan
```

为了保持习惯统一，用户名和邮箱都可以统一使用引号。

## 2、查看配置结果

查看全局用户名：

```shell
git config --global user.name
```

查看全局邮箱：

```shell
git config --global user.email
```

查看所有全局配置：

```shell
git config --global --list
```

示例：

![[assets/Pasted image 20260604232027.png|200]]

# 四、Git 配置级别

## 1、常见配置级别

Git 配置可以来自不同级别。常见级别有三种：

| 配置级别     | 作用范围      | 常见位置           |
| -------- | --------- | -------------- |
| `system` | 当前系统的所有用户 | 系统级 Git 配置文件   |
| `global` | 当前用户的所有项目 | `~/.gitconfig` |
| `local`  | 当前仓库      | `.git/config`  |
配置优先级通常是：

> local > global > system

也就是说，如果同一个配置项在多个级别都存在，当前仓库的本地配置优先级最高。

## 2、全局配置

使用 `--global` 设置的配置，对当前用户的所有 Git 仓库生效。

```shell
git config --global user.name "Zhang San"
git config --global user.email "zhangsan@example.com"
```

查看全局配置：

```shell
git config --global --list
```

全局配置适合保存通用设置，例如：

```shell
git config --global user.name "Zhang San"
git config --global user.email "zhangsan@example.com"
git config --global init.defaultBranch main
```


## 3、本地配置

如果不加 `--global`，并且当前目录已经是一个 Git 仓库，配置会写入当前仓库的 `.git/config` 文件。

例如：

```shell
git config user.name "Work Account"
git config user.email "work@example.com"
```

查看当前仓库的本地配置：

```shell
git config --local --list
```

本地配置适合用于区分不同项目的提交身份，例如个人项目使用个人邮箱，公司项目使用公司邮箱。

## 4、查看当前生效配置

查看当前目录下最终生效的 Git 配置：

```shell
git config --list
```

这个命令会综合显示 `system`、`global`、`local` 等多个来源的配置。

如果想查看每一项配置来自哪个文件，可以使用：

```shell
git config --list --show-origin
```

输出可能类似：

![[assets/Pasted image 20260604233634.png|500]]

`--show-origin` 很适合排查配置来源问题。例如明明全局邮箱已经改了，但某个仓库提交时仍然使用旧邮箱，就可以用这个命令检查是否被本地配置覆盖。


# 五、常用初始配置

## 1、默认分支名

新建仓库时，可以设置默认分支名 `main`：

```shell
git config --global init.defaultBranch main
```

之后执行 `git init` 创建仓库时，默认分支会使用 `main` 而不是 `master`。

查看配置：

```shell
git config --global init.defaultBranch
```


## 2、默认编辑器

Git 在某些操作中需要打开文本编辑器，例如：

- 执行不带 `-m` 的 `git commit`
- 使用 `git commit --amend` 修改提交信息
- 执行某些需要编辑提交信息的合并、变基或撤销操作

如果希望 Git 默认使用 VS Code，可以配置：

```shell
git config --global core.editor "code --wait"
```

查看当前配置：

```shell
git config --global core.editor
```

配置值中的两部分分别表示：

| 内容 | 作用 |
| --- | --- |
| `code` | 调用 VS Code 的命令行工具打开 Git 生成的临时编辑文件 |
| `--wait` | 让 `code` 命令继续等待，直到该编辑文件被关闭，再将控制权交还给 Git |

Git 启动编辑器后，会等待编辑器退出，然后读取保存后的内容继续操作。普通 `code` 命令在打开文件后往往会立即返回；如果不加 `--wait`，Git 可能在还没来得及编辑和保存时就继续执行，导致提交信息为空或操作被取消。

> [!tip] 完成编辑后需要关闭文件
> 在 VS Code 中保存 Git 打开的临时文件后，还需要关闭该文件的编辑器标签页。此时 `code --wait` 才会结束等待，Git 也才会继续执行，不需要退出整个 VS Code。

使用该配置前，需要确保终端中可以正常执行：

```shell
code --version
```

如果终端提示找不到 `code` 命令，需要先在 VS Code 的命令面板中执行 `Shell Command: Install 'code' command in PATH`。

## 3、凭证管理

`macOS`上常见的凭证管理配置是：

```shell
credential.helper=osxkeychain
```

它表示 Git 需要保存远程仓库访问凭证时，会把凭证交给 macOS 钥匙串管理。

可以查看当前凭证管理配置：

```shell
git config credential.helper
```

如果输出：

```
osxkeychain
```

说明 Git 会使用 macOS 钥匙串保存 HTTPS 认证凭证。


# 六、Git 认证

## 1、认证的使用场景

Git 认证发生在访问远程仓库时。

例如：

```shell
git clone https://github.com/xxx/yyy.git
git pull
git push
```

如果当前仓库是私有仓库，或者当前操作需要写入远程仓库，代码托管平台就需要确认当前用户是否有权限。

常见代码托管平台包括：

- GitHub
- GitLab
- Gitee

## 2、HTTPS 认证与 Token

使用 HTTPS 地址访问远程仓库时，远程平台通常会要求认证。

远程地址类似：

```text
https://github.com/xxx/yyy.git
```

以前可以直接使用账号密码进行 Git 操作，但现在 GitHub 等平台通常不再支持使用账号密码直接完成 Git 认证，而是使用访问令牌。

访问令牌通常称为 `Personal Access Token`，简称 `PAT`。

可以把 `PAT` 理解为专门给 Git 命令使用的一串密码。它可以单独设置权限，也可以随时撤销，比直接使用账号密码更安全。


## 3、SSH 认证

除了 HTTPS，也可以使用 SSH 访问远程仓库。

远程地址类似：

```shell
git@github.com:xxx/yyy.git
```

SSH 认证通常需要 SSH 密钥完成。配置好 SSH 公钥后，执行 `git clone`、`git pull`、`git push` 时就不需要反复输入 Token。
