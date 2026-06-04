---
title: Git 配置
date: 2026-06-05
tags: [git, configuration]
source_count: 1
---

# Git 配置

Git 提供多级配置体系，控制提交身份、默认行为、凭证管理等。

## 配置级别

Git 配置按作用范围分为三级：

| 级别 | 命令标志 | 作用范围 | 配置文件位置 |
|------|----------|----------|--------------|
| system | `--system` | 当前系统所有用户 | 系统级路径（如 `/etc/gitconfig`） |
| global | `--global` | 当前用户所有仓库 | `~/.gitconfig` |
| local | `--local`（默认） | 仅当前仓库 | `.git/config` |

优先级规则：**local > global > system**。同一配置项在多个级别存在时，local 优先级最高。

查看当前最终生效的所有配置：

```shell
git config --list
```

查看配置来源（排查配置被覆盖时很有用）：

```shell
git config --list --show-origin
```

## 提交身份配置

每次 `git commit` 都会将配置的 `user.name` 和 `user.email` 写入提交记录：

```shell
git config --global user.name "Zhang San"
git config --global user.email "zhangsan@example.com"
```

建议使用代码托管平台（GitHub、GitLab、Gitee）绑定的邮箱，以便平台正确关联提交记录到个人账号。

## 默认分支名

设置新仓库的默认初始分支为 `main`：

```shell
git config --global init.defaultBranch main
```

早期 Git 默认使用 `master`，现在主流平台已迁移到 `main`。

## 凭证管理

macOS 上 Git 默认使用系统钥匙串管理凭证：

```shell
git config credential.helper
# 输出: osxkeychain
```

远程仓库的访问凭证（如 HTTPS 的 PAT）会安全存储在 macOS 钥匙串中。

## 本地配置的应用场景

不同项目使用不同提交身份时，可在仓库内设置 local 配置：

```shell
git config user.name "Work Account"
git config user.email "work@example.com"
```

这样个人项目与公司项目的提交作者可以自动区分。

## 相关页面

- [[Git 认证]] — 远程仓库访问的认证配置
- [[Git 仓库]] — 仓库级别的本地配置存储在 `.git/config`

## 来源

- [[Git的安装与配置]]
