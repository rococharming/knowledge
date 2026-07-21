---
title: Git 安装与首次配置
date: 2026-07-22
tags: [git, macos, setup]
source_count: 1
---

# Git 安装与首次配置

本配方面向 macOS 的 Git 安装、身份配置和配置来源排错。Git 的基本定位与能力见 [[Git 版本控制系统]]。

## 1. 安装并确认实际使用的 Git

可通过 Xcode Command Line Tools 安装系统工具链：

```shell
xcode-select --install
```

若希望较方便地升级 Git，也可以使用 Homebrew：

```shell
brew install git
brew upgrade git
```

安装后检查终端实际调用的可执行文件及版本：

```shell
command -v git
git --version
```

当系统工具链与 Homebrew 同时提供 Git 时，第一条命令可确认当前 PATH 选择的是哪一份程序。

## 2. 设置全局提交身份和默认行为

```shell
git config --global user.name "Zhang San"
git config --global user.email "zhangsan@example.com"
git config --global init.defaultBranch main
git config --global core.editor "code --wait"
```

- `user.name` 与 `user.email` 会写入提交作者信息；若需要与 Git 托管平台账户关联，应使用该平台认可的邮箱。
- `init.defaultBranch` 只影响之后执行 `git init` 新建的仓库。
- `core.editor` 是 Git 在提交、变基或合并需要输入说明时打开的编辑器。使用 VS Code 时，`--wait` 会让 Git 等待编辑器关闭后继续执行。

如果 `code --version` 不能运行，需要先在 VS Code 中将 `code` 命令加入 PATH；也可以改用熟悉的终端编辑器，例如 `nano`。

## 3. 为单个仓库覆盖身份

个人项目和工作项目需要不同身份时，在目标仓库目录运行不带 `--global` 的配置命令：

```shell
git config user.name "Work Account"
git config user.email "work@example.com"
```

这会写入该仓库的 `.git/config`，并覆盖同名的全局配置。

## 4. 检查配置来源

配置不符合预期时，先同时查看值、作用域和来源：

```shell
git config --list --show-origin --show-scope
```

常见优先级可概括为 `local > global > system`。此外，`git -c 键=值 ...` 只对当前命令临时生效，优先级更高，不适合保存长期偏好。

若某仓库仍使用旧邮箱，可进一步定位两项身份配置：

```shell
git config --show-origin --get user.email
git config --show-origin --get user.name
```

输出指向 `~/.gitconfig` 时修改全局配置；指向 `.git/config` 时在当前仓库更新本地配置。

## 5. 验证一次提交

在新建仓库完成一次提交后，检查最近提交记录：

```shell
git log -1 --format=fuller
```

确认 `Author` 显示的姓名和邮箱符合预期。若不一致，回到上一步检查实际生效的配置来源。

## 来源

- [[Git 安装与配置]]
