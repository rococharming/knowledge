---
title: fish shell 语法
date: 2026-05-14
tags: [shell]
source_count: 1
---

fish shell 采用与 POSIX shell（bash/zsh/sh）不同的语法设计，更强调一致性和简洁性。

## 变量赋值

POSIX shell：
```shell
NAME="ABC"
echo $NAME
```

fish：
```shell
set NAME ABC
echo $NAME
```

环境变量使用 `-x` 或 `-gx` 导出：
```shell
set -gx EDITOR code
```

| 选项 | 含义 |
|------|------|
| 无选项 | 局部变量 |
| `-x` | 导出变量（环境变量） |
| `-gx` | 全局导出变量 |

## if 条件判断

POSIX shell：
```shell
if [ -f test.txt ]; then
    echo yes
fi
```

fish：
```shell
if test -f test.txt
    echo yes
end
```

fish 不使用 `then`/`fi`，以 `end` 结束代码块。

## for 循环

POSIX shell：
```shell
for x in a b c; do
    echo $x
done
```

fish：
```shell
for x in a b c
    echo $x
end
```

同样以 `end` 替代 `done`。

## 函数定义

POSIX shell：
```shell
myfunc() {
    echo hello
}
```

fish：
```shell
function myfunc
    echo hello
end
```

调用方式相同：`myfunc`。

## 命令替换

POSIX shell：
```shell
today=$(date)
echo $today
```

fish：
```shell
set today (date)
echo $today
```

fish 使用圆括号 `()` 而非 `$()`。

## PATH 和环境变量

POSIX shell 手动追加 PATH：
```shell
export PATH="$PATH:/new/path"
```

fish 推荐：
```shell
fish_add_path /new/path
```

如需手动设置：
```shell
set -gx PATH $PATH /new/path
```

## export 兼容

fish 新版本内置 `export` 兼容函数，便于临时复制 bash 风格命令。但 `config.fish` 中仍建议使用原生写法 `set -gx`。

## alias 与 abbreviation

fish 支持 alias：
```shell
alias ll="ls -lh"
```

但更推荐使用 **abbreviation（缩写）**，输入短命令后按空格自动展开为完整命令：

```shell
abbr -a gs "git status"
```

输入 `gs` 并按空格后自动展开为 `git status`。比 alias 更直观，因为执行前能看到完整命令。

## 来源

- [[fish shell 安装与使用]]
