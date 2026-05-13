---
title: 将 fish 设为默认 Shell
date: 2026-05-14
tags: [shell, system-config]
source_count: 1
---

将 fish 设为 macOS 默认 shell 需要三个步骤：确认路径、加入 `/etc/shells`、执行 `chsh`。

## 临时体验

仅在当前终端会话进入 fish：

```shell
fish
```

退出：

```shell
exit
```

## 设为默认 shell

### 1. 确认 fish 路径

```shell
which fish
```

Apple Silicon Mac 通常输出 `/opt/homebrew/bin/fish`，后续命令使用该路径。

### 2. 加入允许的 shell 列表

```shell
echo /opt/homebrew/bin/fish | sudo tee -a /etc/shells
```

验证：

```shell
cat /etc/shells
```

### 3. 切换默认 shell

```shell
chsh -s /opt/homebrew/bin/fish
```

关闭终端并重新打开，应自动进入 fish。

![[Pasted image 20260513220811.png|400]]

## 验证

查看登录 shell：

```shell
echo $SHELL
```

期望输出 `/opt/homebrew/bin/fish`。

> `echo $SHELL` 反映登录 shell，不一定等于当前运行的 shell。查看当前进程实际运行的 shell：

```shell
ps -p $fish_pid
```

![[Pasted image 20260513221124.png|200]]

## 来源

- [[fish shell 安装与使用]]
