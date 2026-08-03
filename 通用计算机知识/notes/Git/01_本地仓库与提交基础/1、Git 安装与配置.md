---
title: Git 安装与配置
date: 2026-07-21
tags: [计算机基础, Git, Git基础]
aliases:
  - Git 配置
  - git config
---

# 一、Git 的定位

Git 是一个 **分布式版本控制系统**，用来记录项目文件在不同时间点的变化。被 Git 管理的项目目录称为仓库（repository 或 repo）。

![[assets/Pasted image 20260722001502.png|600]]


每一次提交都可以理解为项目在某个时刻的快照。查看历史、对比差异、切换分支和协作开发，本质上都是围绕这些快照展开。

| 能力 | 作用 |
|---|---|
| 版本记录 | 保存文件变化历史 |
| 版本回退 | 回到某个历史提交的状态 |
| 差异对比 | 查看文件、提交、分支之间的变化 |
| 分支管理 | 在多条开发线上并行工作 |
| 协同开发 | 通过远程仓库进行多人协作 |

# 二、安装 Git

本篇以 macOS 为例。安装完成后，先确认终端实际调用的是哪一份 Git；系统的 [[macOS/notes/1、Xcode与命令行工具|Xcode Command Line Tools]] 与 [[macOS/notes/2、Homebrew安装与使用|Homebrew]] 可以同时提供 Git。

## 1、Xcode 工具链

[[macOS/notes/1、Xcode与命令行工具|Xcode Command Line Tools]] 是 macOS 上最常见的安装方式。它会同时提供 Git、编译器、`make` 和系统头文件等命令行开发工具。

```shell
xcode-select --install
```

## 2、Homebrew

如果希望更方便地升级 Git，或需要较新的版本，可以使用 [[macOS/notes/2、Homebrew安装与使用|Homebrew]]：

```shell
brew install git
```

日后升级已安装的 Git：

```shell
brew upgrade git
```

## 3、确认版本

安装后执行：

```shell
command -v git
git --version
```

`command -v git` 用来确认当前终端会调用的可执行文件路径；当 Xcode 与 Homebrew 的 Git 共存时，它能帮助定位“安装了新版但仍在使用旧版”的问题。

# 三、配置作用域

Git 的配置来自不同作用域。越接近当前命令或当前仓库的配置，通常优先级越高。

## 1、常用层级

| 级别 | 作用范围 | 常见位置 |
|---|---|---|
| `system` | 当前系统所有用户 | 系统级配置文件 |
| `global` | 当前用户的所有仓库 | `~/.gitconfig` |
| `local` | 当前仓库 | `.git/config` |
| `worktree` | 当前工作树（启用多工作树配置时） | 当前工作树的专属配置 |

日常最常见的覆盖关系可以理解为：

```text
local > global > system
```

此外，`git -c 键=值 ...` 提供的命令行配置只对本次命令生效，优先级更高。它适合临时试验，不适合保存个人习惯。

## 2、排查来源

配置结果不符合预期时，不要只看值；还要看它来自哪个文件、属于哪个作用域：

```shell
git config --list --show-origin --show-scope
```

其中：

| 参数 | 作用 | 用来判断 |
|---|---|---|
| `--show-origin` | 显示每条配置来自哪个文件或命令来源 | 是 `~/.gitconfig` 生效，还是当前仓库的 `.git/config` 生效 |
| `--show-scope` | 显示每条配置属于哪个作用域 | 是 `global`、`local`、`system`，还是其他作用域 |

输出通常类似：

```text
global  file:/Users/zhangsan/.gitconfig   user.email=old@example.com
local   file:.git/config                  user.email=project@example.com
```

这表示同一个配置项在 `global` 和 `local` 中都存在。由于 `local` 更接近当前仓库，所以当前仓库实际会使用 `project@example.com`。

例如，某个仓库提交时仍使用旧邮箱，通常是该仓库的 `local` 配置覆盖了全局设置。

# 四、首次配置

完成下面三项设置后，新建本地仓库就可以正常开始提交。

## 1、提交身份

每次提交都会记录作者姓名和邮箱。首次使用前，设置全局身份：

```shell
git config --global user.name "Zhang San"
git config --global user.email "zhangsan@example.com"
```

这些设置通常写入：

```text
~/.gitconfig
```

以后，提交记录中的作者信息大致如下：

```text
Author: Zhang San <zhangsan@example.com>
```

若希望 GitHub、GitLab 或 Gitee 将提交关联到账号，应使用该平台已验证或认可的邮箱。Git 本身不限制邮箱地址；个人项目与公司项目需要不同身份时，可在对应仓库设置 `local` 配置。

示例：

```shell
git config user.name "Work Account"
git config user.email "work@example.com"
```

## 2、默认分支

新建仓库时，可以把默认初始分支设为 `main`：

```shell
git config --global init.defaultBranch main
```

这只影响之后执行 `git init` 创建的新仓库。仓库初始化流程见 [[2、创建 Git 仓库|创建 Git 仓库]]。

## 3、默认编辑器

Git 在不带 `-m` 的 `git commit`、`git commit --amend`、合并和变基等操作中可能打开编辑器。若希望默认使用 VS Code：

```shell
git config --global core.editor "code --wait"
```

`--wait` 会让 Git 等待文件保存并关闭后再继续。若终端不能执行 `code --version`，需先在 VS Code 命令面板中运行 `Shell Command: Install 'code' command in PATH`将`code`加入 PATH 环境变量。

不使用 VS Code 时，也可以指定已熟悉的终端编辑器，例如：

```shell
git config --global core.editor nano
```

# 五、验证与排错

配置完成后，先检查保存的值和来源；再在下一篇创建仓库并进行一次提交，确认身份真正写入提交记录。

## 1、检查配置

```shell
git config --global user.name
git config --global user.email
git config --global init.defaultBranch
git config --list --show-origin --show-scope
```

## 2、验证提交身份

在空目录中按 [[2、创建 Git 仓库|创建 Git 仓库]] 的步骤初始化仓库并完成一次提交后，可以查看最近一次提交：

```shell
git log -1 --format=fuller
```

输出中的 `Author` 应与预期姓名、邮箱一致。若不一致，先检查当前仓库的配置来源：

```shell
git config --show-origin --get user.email
git config --show-origin --get user.name
```

然后根据来源决定是修改全局配置，还是为当前仓库设置正确的本地身份。

# 六、本地练习

起点：在一个已经初始化、且当前处于干净状态的本地仓库中。

```shell
git --version
git config --global user.name
git config --global user.email
git config --global init.defaultBranch
git status
```

本课只确认环境和配置，不创建新提交，也不修改文件。目标状态是：仓库仍然保持 clean，下一课可以继续观察 `.git/` 和仓库结构。

# 七、小结

本篇的最小检查清单：

- 安装后用 `command -v git` 和 `git --version` 确认实际使用的 Git。
- 设置提交身份 `user.name` 与 `user.email`。
- 设置新仓库的默认分支 `init.defaultBranch`。
- 选择 Git 需要打开编辑器时使用的 `core.editor`。
- 遇到配置异常时，用 `git config --list --show-origin --show-scope` 定位覆盖来源。

下一步阅读 [[2、创建 Git 仓库|创建仓库]]，理解 `.git` 目录如何把普通目录变成可版本控制的仓库。完成本地基础后，可继续阅读 [[通用计算机知识/notes/Git/03_远程仓库与团队协作/1、远程仓库与第一次推送|远程仓库与第一次推送]]，为访问远程仓库做准备。
