---
title: Git Submodule
date: 2026-07-16
tags: [计算机基础, Git, git, version-control]
aliases:
  - Git 子模块
  - git submodule
  - Git Submodule
---

# 一、Git Submodule 的核心模型

Git Submodule（Git 子模块）用于在一个 Git 仓库中引用另一个独立 Git 仓库，并把这个外部仓库锁定到一个确定提交。

简单来说：主仓库不保存子模块里的全部文件历史，只保存“这个路径对应哪个子仓库、当前指向哪个提交”。

```text
my-project/
├── .git/
├── .gitmodules
├── src/
└── third_party/
    └── ui/
```

这里 `my-project` 是主仓库，`third_party/ui` 是子模块。二者拥有独立提交历史：

```text
主仓库 commit A
│
├── src/
├── README.md
└── third_party/ui
        │
        └── 指向子模块 commit X

子模块仓库：
X --- Y --- Z
```

只要主仓库没有更新子模块引用，`third_party/ui` 就仍然指向 `X`。子模块远程仓库新增 `Y`、`Z` 不会让主仓库自动切换过去。

> Submodule 的关键价值不是“自动使用最新代码”，而是“在主仓库中精确记录外部仓库的某个版本”。

# 二、主仓库到底记录了什么

理解 Submodule 要抓住三类信息：`.gitmodules` 配置、主仓库索引里的 `gitlink`、子模块自己的 Git 数据。

## 1、`.gitmodules` 记录路径和远程地址

添加子模块后，主仓库根目录会出现 `.gitmodules`：

```ini
[submodule "third_party/ui"]
	path = third_party/ui
	url = https://github.com/example/ui.git
```

字段含义：

| 字段 | 含义 |
|---|---|
| `submodule` | 子模块名称 |
| `path` | 子模块在主仓库中的目录 |
| `url` | 子模块远程仓库地址 |

`.gitmodules` 必须提交到主仓库。团队成员克隆主仓库后，Git 依靠它知道有哪些子模块、放在哪个目录、从哪个远程仓库获取。

## 2、`gitlink` 记录子模块提交

主仓库记录的是子模块的提交哈希，不是分支名。查看主仓库索引：

```shell
git ls-files --stage
```

普通文件示例：

```text
100644 8f912abc... 0 src/main.rs
```

子模块示例：

```text
160000 a1b2c3d4... 0 third_party/ui
```

`160000` 表示这个路径是 `gitlink`，也就是“指向另一个 Git 仓库某个提交的特殊条目”。

| 模式 | 含义 |
|---|---|
| `100644` | 普通文件 |
| `100755` | 可执行文件 |
| `160000` | Git 子模块 |

因为主仓库保存的是提交哈希，所以初始化或同步子模块后，子模块工作区会检出到主仓库记录的那个提交。该提交没有本地分支名直接指向时，子模块会处于 detached HEAD（分离头指针）状态。`HEAD` 和分支指针模型见 [[通用计算机知识/notes/Git/1、Git 分支的基本概念与操作|Git 分支]]。

## 3、子模块的 Git 数据放在主仓库内部

通过 `git submodule` 创建的子模块中，`.git` 是文本文件，不是目录：

```text
gitdir: ../../.git/modules/third_party/ui
```

真正的子模块 Git 数据位于主仓库的 `.git/modules/` 下：

```text
my-project/
├── .git/
│   └── modules/
│       └── third_party/
│           └── ui/
└── third_party/
    └── ui/
        └── .git
```

这让主仓库可以统一保存子模块的仓库数据，同时子模块目录仍然表现为一个可进入、可提交、可推送的独立 Git 仓库。

# 三、添加和克隆子模块

这一部分解决两个入口问题：项目维护者如何把子模块加入主仓库，团队成员如何完整拉下带子模块的项目。

## 1、添加子模块

基本命令：

```shell
git submodule add <仓库地址> <本地目录>
```

示例：

```shell
git submodule add https://github.com/example/ui.git third_party/ui
```

执行后，Git 完成三件事：

1. 克隆子模块仓库到 `third_party/ui`。
2. 创建或更新 `.gitmodules`。
3. 在主仓库索引中记录 `third_party/ui` 当前指向的提交。

查看状态：

```shell
git status
```

会看到主仓库新增两个待提交条目：

```text
new file:   .gitmodules
new file:   third_party/ui
```

随后在主仓库提交：

```shell
git add .gitmodules third_party/ui
git commit -m "chore: add ui submodule"
```

这里提交的是 `.gitmodules` 和子模块提交指针，不是子模块内部的完整文件历史。`git add`、`git status`、`git commit` 的基础流程见 [[通用计算机知识/notes/Git/01_本地仓库与提交基础/4、查看状态、暂存和提交|查看状态、暂存和提交]]。

## 2、克隆带子模块的仓库

推荐在克隆时递归拉取子模块：

```shell
git clone --recurse-submodules https://github.com/example/my-project.git
```

这等价于：

```shell
git clone https://github.com/example/my-project.git
cd my-project
git submodule update --init --recursive
```

如果已经普通克隆了主仓库，进入仓库后补执行：

```shell
git submodule update --init --recursive
```

各参数含义：

| 参数 | 作用 |
|---|---|
| `--init` | 根据 `.gitmodules` 注册本地子模块配置 |
| `--recursive` | 同步嵌套子模块 |
| `update` | 克隆缺失的子模块，并检出主仓库记录的提交 |

# 四、查看和同步子模块状态

Submodule 的日常判断重点是：主仓库记录的提交、子模块工作区当前提交、子模块远程最新提交，这三者是不是同一个概念。

## 1、查看子模块状态

执行：

```shell
git submodule status
```

输出示例：

```text
 a1b2c3d4 third_party/ui
```

提交哈希前的字符表示状态：

| 前缀 | 含义 | 处理 |
|---|---|---|
| 空格 | 子模块已检出到主仓库记录的提交 | 无需处理 |
| `-` | 子模块尚未初始化 | `git submodule update --init` |
| `+` | 子模块当前提交与主仓库记录不同 | 决定回到记录版本，或在主仓库提交新指针 |
| `U` | 子模块引用存在合并冲突 | 手动选择正确提交后重新提交 |

也可以用 `git status` 查看主仓库视角：

```text
modified: third_party/ui (new commits)
```

这表示子模块目录已经指向新提交，但主仓库还没有把这个新指针提交下来。

## 2、同步到主仓库记录的版本

当其他人更新了主仓库里的子模块指针，本地拉取主仓库后，需要把子模块工作区同步到主仓库记录的提交。

```shell
git pull
git submodule update --init --recursive
```

示例：

```text
主仓库原记录：third_party/ui -> A
其他人提交后：third_party/ui -> B

本地 git pull 后：
主仓库记录：B
本地子模块：A

执行 git submodule update --init --recursive 后：
主仓库记录：B
本地子模块：B
```

这个操作只让本地子模块回到主仓库指定版本，不会主动追踪子模块远程仓库的最新提交。

## 3、让 pull 自动递归处理子模块

一次性命令：

```shell
git pull --recurse-submodules
git submodule update --init --recursive
```

如果不想手写`--recurse-submodules`，可以配置：

仓库级配置：

```shell
git config submodule.recurse true
```

全局配置：

```shell
git config --global submodule.recurse true
```

启用 `submodule.recurse` 后，支持递归行为的 Git 命令会进入子模块执行对应操作。团队项目中是否全局启用取决于个人习惯；更稳妥的做法是在关键脚本或文档中显式写出 `--recurse-submodules`。

# 五、更新子模块到新版本

“更新子模块”有两种含义：一种是同步到主仓库已经记录的版本，上一节已经覆盖；另一种是把主仓库记录的子模块指针推进到子模块仓库的新提交。

## 1、手动进入子模块更新

进入子模块：

```shell
cd third_party/ui
```

切换到要跟进的分支并拉取：

```shell
git switch main
git pull --ff-only
```

返回主仓库：

```shell
cd ../..
git status
```

主仓库会显示：

```text
modified: third_party/ui (new commits)
```

提交新的子模块指针：

```shell
git add third_party/ui
git commit -m "chore: update ui submodule"
```

这次提交只改变主仓库中的 `gitlink`，让 `third_party/ui` 从旧提交指向新提交。

## 2、使用 `--remote` 按远程分支更新

也可以让 Git 根据子模块的远程分支更新：

```shell
git submodule update --remote third_party/ui
```

更新所有子模块：

```shell
git submodule update --remote --recursive
```

可以在 `.gitmodules` 中声明默认跟踪分支：

```ini
[submodule "third_party/ui"]
	path = third_party/ui
	url = https://github.com/example/ui.git
	branch = main
```

提交配置和新指针：

```shell
git add .gitmodules third_party/ui
git commit -m "chore: track ui submodule main"
```

`branch = main` 只告诉 `git submodule update --remote` 从哪个远程分支取新提交。主仓库仍然锁定一个确定提交，不会因为配置了 `branch = main` 就自动使用 `main` 的最新提交。

# 六、在子模块中开发与常见取舍

子模块本身是独立 Git 仓库。进入子模块目录后，可以按普通仓库方式创建分支、提交、推送；回到主仓库后，再提交新的子模块指针。

## 1、完整开发流程

进入子模块：

```shell
cd third_party/ui
```

创建开发分支并提交：

```shell
git switch -c feature/new-button
git add .
git commit -m "feat: add new button"
git push -u origin feature/new-button
```

返回主仓库：

```shell
cd ../..
git status
```

主仓库显示：

```text
modified: third_party/ui (new commits)
```

提交子模块指针：

```shell
git add third_party/ui
git commit -m "chore: update ui submodule"
```

一次完整的子模块开发包含两次提交：

| 提交位置 | 提交内容 |
|---|---|
| 子模块仓库 | 子模块代码修改 |
| 主仓库 | 子模块路径指向的新提交 |

提交顺序不能反过来。主仓库引用的子模块提交必须已经存在于子模块远程仓库中，否则其他人拉取主仓库后无法检出该提交。

## 2、适用场景

Submodule 适合这些情况：

- **依赖项目需要独立版本历史**：例如第三方库、共享组件库、内部 SDK。
- **主仓库必须锁定精确版本**：例如构建、发布、回滚要求可复现。
- **子项目可被多个主仓库复用**：一个子模块仓库被多个产品或平台引用。

不适合这些情况：

- **希望依赖代码跟随主项目一起频繁改动**：放在同仓库或 monorepo 更直接。
- **团队不愿处理双仓库提交和同步成本**：Submodule 要求开发者理解主仓库指针和子模块仓库提交的区别。
- **只想管理大文件**：优先考虑 Git LFS 或制品仓库，而不是 Submodule。

## 3、常用命令速查

| 目标 | 命令 |
|---|---|
| 添加子模块 | `git submodule add <url> <path>` |
| 克隆时拉取子模块 | `git clone --recurse-submodules <url>` |
| 初始化并同步子模块 | `git submodule update --init --recursive` |
| 查看子模块状态 | `git submodule status` |
| 按远程分支更新子模块 | `git submodule update --remote <path>` |
| 拉取主仓库并递归处理子模块 | `git pull --recurse-submodules` |

# 七、小结

Git Submodule 的核心是两层提交关系：子模块仓库提交真实代码，主仓库提交子模块路径指向哪个提交。

日常使用时只要分清两类动作，就不容易混乱：

- **同步到主仓库指定版本**：`git submodule update --init --recursive`。
- **推进主仓库中的子模块版本**：先更新子模块仓库，再在主仓库提交新的 `gitlink`。

Submodule 牺牲了一部分操作简单性，换来跨仓库复用和精确版本锁定。它适合依赖边界清晰、版本可复现要求明确的项目。
