---
title: Git 远程仓库
date: 2026-06-05
tags: [git, repository, remote]
source_count: 1
---

# Git 远程仓库

远程仓库（remote repository）是托管在服务器上的 Git 仓库，用于多人协作和代码备份。

## 克隆远程仓库

```shell
git clone <远程仓库URL>
```

例如：

```shell
git clone https://github.com/user/repo.git
```

执行后会在当前目录创建 `repo/` 目录，内含完整项目文件和 `.git` 仓库。

### git clone 的内部操作

`git clone` 不是简单下载代码，它会自动完成：

1. 创建本地目录（默认使用远程仓库名）
2. 下载项目文件
3. 下载完整的提交历史
4. 初始化 `.git` 目录
5. 获取远程分支和标签引用
6. 添加远程别名 `origin`

### 自定义本地目录名

```shell
git clone https://github.com/user/repo.git my-project
```

会生成 `my-project/` 而非 `repo/`。

## 查看远程仓库地址

```shell
git remote -v
```

输出示例：

```shell
origin  https://github.com/user/repo.git (fetch)
origin  https://github.com/user/repo.git (push)
```

| 字段 | 含义 |
|------|------|
| `origin` | 远程仓库的默认别名 |
| `fetch` | 从远程获取数据使用的地址 |
| `push` | 向远程推送数据使用的地址 |

## 远程别名

`origin` 是 Git 给克隆来源自动设置的默认远程仓库名称。一个本地仓库可以关联多个远程仓库，每个都有自己的别名。

后续学习远程仓库操作时，会详细展开 `origin`、`fetch`、`pull`、`push` 之间的关系。

## 相关页面

- [[Git 仓库]] — 本地仓库的创建与管理
- [[Git 认证]] — 访问远程仓库的认证方式

## 来源

- [[创建Git仓库]]
