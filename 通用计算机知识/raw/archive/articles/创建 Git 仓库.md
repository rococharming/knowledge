---
title: 创建 Git 仓库
date: 2026-07-22
tags: [计算机基础, Git, Git基础]
aliases:
  - Git 仓库
  - git init
  - git clone
---

# 一、Git 仓库

Git 仓库是被 Git 纳入版本控制的项目目录。普通目录执行 `git init` 后，Git 会创建隐藏目录 `.git`；它保存提交历史、分支引用、暂存区和仓库配置等信息。

创建仓库有两条起点，应按项目的来源选择：

| 起点 | 命令 | 适合场景 |
|---|---|---|
| 本地初始化 | `git init` | 从本地目录开始一个新项目 |
| 克隆已有仓库 | `git clone <repository-url>` | 获取已有项目及其版本历史 |

> [!note] 创建仓库不等于提交文件
> Git 不会自动把目录中的所有文件写入历史。文件还要经过 `git add` 和 `git commit`，才会成为提交的一部分。

# 二、初始分支

## 1、单次指定

现代项目通常把主分支命名为 `main`。创建仓库时可以直接指定初始分支：

```shell
mkdir learngit
cd learngit
git init -b main
```

这样无需在仓库创建后再重命名分支。

## 2、全局默认

如果希望以后新建的仓库都使用 `main`，可以设置全局默认值：

```shell
git config --global init.defaultBranch main
```

查看当前设置：

```shell
git config --global init.defaultBranch
```

Git 的用户名、邮箱与其他配置见 [[1、Git 安装与配置|Git 安装与配置]]。

# 三、本地初始化

## 1、新建项目

对一个新目录，可以使用上面的 `git init -b main`。若默认分支已经通过全局配置设置，也可以只执行：

```shell
git init
```

初始化后，Git 会在项目根目录创建 `.git`。普通项目文件仍在工作区，尚未进入历史。

## 2、已有项目

`git init` 不要求目录为空。在已有文件的项目目录中执行它，不会删除或修改原有文件，只会让当前目录具备 Git 仓库能力。

要把已有文件作为第一版历史保存下来：

```shell
git add .
git commit -m "initial commit"
```

暂存和提交流程见 [[通用计算机知识/notes/Git/01_本地仓库基础/4、查看状态、暂存和提交|查看状态、暂存和提交]]。

# 四、克隆仓库

## 1、克隆已有项目

当项目已经有远程仓库时，使用 `git clone`。它会下载工作区文件和提交历史，配置克隆来源为默认远程别名 `origin`，并检出远程默认分支对应的本地分支。

```shell
git clone https://github.com/user/repo.git
cd repo
```

其他远程分支会作为远程跟踪分支保存；创建本地分支、推送和同步属于后续的协作主题。

## 2、自定义目录

默认本地目录名来自远程仓库名。若要指定目录名，在命令末尾附加目标目录：

```shell
git clone https://github.com/user/repo.git my-project
```

## 3、查看来源

克隆后可以检查远程地址：

```shell
git remote -v
```

输出通常类似：

```text
origin  https://github.com/user/repo.git (fetch)
origin  https://github.com/user/repo.git (push)
```

`origin` 只是克隆来源的默认别名，不是特殊的服务器。认证、远程地址和协作流程见 [[1、远程仓库认证与凭证管理|远程仓库认证与凭证管理]]。

# 五、验证仓库

## 1、确认身份

在项目目录或任意子目录中执行以下命令，可以确认当前仓库和它的根目录：

```shell
git rev-parse --show-toplevel
```

`git rev-parse` 是 Git 的底层查询命令，常用于解析修订版本、路径和仓库相关信息。

这里的 `--show-toplevel` 是 `rev-parse` 的一个选项，作用是显示当前工作区的顶层目录。若命令成功，输出的是仓库根目录的绝对路径。也可以用 `git status` 查看工作区状态。

其他常见用法：

```shell
git rev-parse HEAD       # 当前提交的完整哈希
git rev-parse main~2     # main 向前第 2 个提交的哈希
git rev-parse --git-dir  # Git 元数据目录的位置
```


## 2、查看分支

初始化后，用下面的命令查看当前分支：

```shell
git branch --show-current
```

如果输出 `main`，说明当前位于 `main` 分支。若当前目录及其父目录都找不到 Git 仓库，`git status` 等命令会报错：

```text
fatal: not a git repository (or any of the parent directories): .git
```

# 六、`.git` 目录

## 1、保存内容

`.git` 是 Git 的内部数据库。普通仓库中，它是项目根目录下的隐藏目录，常见内容包括：

| 内容 | 作用 |
|---|---|
| `objects/` | 保存 Git 对象，包括文件内容、目录树和提交 |
| `refs/` | 保存分支、标签和远程跟踪分支等引用 |
| `HEAD` | 记录当前检出位置 |
| `index` | 保存暂存区的底层数据 |
| `config` | 保存当前仓库的本地配置 |
| `hooks/` | 存放 Git 钩子脚本 |
| `info/exclude` | 保存仅对本仓库生效的本地忽略规则 |

`.gitignore` 与 `info/exclude` 的适用场景见 [[8、忽略规则文件|忽略规则文件]]。

## 2、工作方式

在仓库子目录中执行 Git 命令时，Git 会从当前目录向上查找 `.git`：

```text
learngit/
  ├── .git/
  └── src/
      └── main.rs
```

因此即使当前位于 `src/`，执行 `git status` 仍属于 `learngit` 仓库。

> [!warning] 不要删除或手动修改 `.git`
> 删除 `.git` 后，项目文件仍在，但仓库配置和提交历史会丢失。linked worktree、submodule 等进阶场景中，`.git` 也可能是指向实际 Git 目录的文件；本篇以普通仓库为例。

# 七、小结

新项目使用 `git init`，已有项目使用 `git clone`。初始化或克隆后，先确认仓库根目录和当前分支，再通过 [[3、工作区域与文件状态|工作区域与文件状态]] 理解修改如何经过工作区、暂存区进入提交历史。
