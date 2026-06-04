---
title: Git 认证
date: 2026-06-05
tags: [git, authentication, security]
source_count: 1
---

# Git 认证

访问远程仓库时，代码托管平台需要验证用户身份和权限。Git 支持多种认证方式。

## 使用场景

以下操作会触发认证：

```shell
git clone https://github.com/xxx/yyy.git
git pull
git push
```

私有仓库或需要写入权限的操作，平台会要求认证。常见平台包括 GitHub、GitLab、Gitee。

## HTTPS 认证与 PAT

使用 HTTPS 地址访问远程仓库时，远程平台要求认证。远程地址格式：

```text
https://github.com/xxx/yyy.git
```

### Personal Access Token (PAT)

GitHub 等平台已不再支持直接使用账号密码进行 Git 认证，转而使用 **Personal Access Token**（PAT）。

PAT 是专门给 Git 命令使用的访问令牌：
- 可以单独设置权限范围
- 可以随时撤销
- 比直接使用账号密码更安全

在 Git 操作中，当平台要求密码时，输入 PAT 代替密码即可。

## SSH 认证

除 HTTPS 外，也可以使用 SSH 协议访问远程仓库。远程地址格式：

```shell
git@github.com:xxx/yyy.git
```

### SSH 密钥配置

配置好 SSH 公钥后，执行 `git clone`、`git pull`、`git push` 时无需反复输入凭证。

SSH 认证的优势：
- 一次配置，长期免密
- 安全性高于密码传输
- 适合频繁推送的开发者

## 方式对比

| 方式 | 地址格式 | 认证方式 | 适用场景 |
|------|----------|----------|----------|
| HTTPS | `https://...` | PAT / 密码 | 临时克隆、防火墙限制 SSH 时 |
| SSH | `git@...` | SSH 密钥 | 日常开发、频繁推送 |

## 相关页面

- [[Git 配置]] — 凭证管理的配置方式
- [[Git 远程仓库]] — 远程仓库的地址与别名

## 来源

- [[Git的安装与配置]]
