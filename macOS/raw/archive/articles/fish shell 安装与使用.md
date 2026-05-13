
`fish shell`是一个强调易用性和交互体验的`shell`。它的全称是 friendly interactive shell，主要面向日常命令行交互使用。

常见特点包括：

- 自动建议：根据历史记录实时建议可能要输入的命令
- Tab 自动补全：支持命令、路径、参数等补全
- 内置语法高亮：命令是否存在、路径是否有效，可以直接通过颜色反馈；
- 开箱即用：不需要复杂配置也能有较好的交互体验
- 语法更简洁一致，但**不兼容 POSIX shell**

> 需要注意的是，fish 更适合作为交互式 shell使用。

如果你经常运行别人写的 sh、zsh、bash 脚本，不需要把这些脚本改为 fish 语法，直接用对应解释器运行即可。

例如：

```shell
bash install.sh
zsh script.zsh
sh script.sh
```

# 二、macOS安装 fish shell

macOS建议使用 Homebrew 安装fish，Homebrew安装参考：[[2、Homebrew安装与使用|Homebrew安装与使用]]。

```shell
brew install fish
```

安装完成后，可以查看 fish 的安装路径：

```shell
which fish
```

Apple Silicon Mac 安装的 fish 通常位于：

![[Pasted image 20260513215534.png|400]]

如果想查看 fish 版本，可以执行：

```shell
fish --version
```


# 三、将 fish 设为默认shell

如果只是想临时体验 fish ，可以直接执行：

```shell
fish
```

这样只会在当前终端会话中进入 fish。退出 fish 可以执行：

```shell
exit
```

如果确认要把 fish 设置为默认 shell，需要分两步：先把 fish 路径加入 `/etc/shells`，再用 `chsh -s` 修改默认 shell。

### 1、确认 fish 路径

先执行：

```shell
which fish
```

如果输出是：

```shell
/opt/homebrew/bin/fish
```

说明后续命令中应该使用这个路径。

### 2、加入允许的 shell 列表

执行：

```shell
echo /opt/homebrew/bin/fish | sudo tee -a /etc/shells
```

将 /opt/homebrew/bin/fish 追加到 `/etc/shells`。

可以检查是否已经加入成功：

```shell
cat /etc/shells
```


## 3、切换默认shell

执行：

```shell
chsh -s /opt/homebrew/bin/fish
```

执行后，关闭终端并重新打开。重新打开后，终端应该会自动进入 fish。

![[Pasted image 20260513220811.png|400]]

可以用下面的命令验证当前默认 shell：

```shell
echo $SHELL
```

如果输出类似：

```test
/opt/homebrew/bin/fish
```

说明默认 shell 已经切换成功。

不过要注意，`echo $SHELL` 表示登录 shell，不一定等于当前正在运行的 shell。想查看当前进程实际运行的 shell，可以执行：

```shell
ps -p $fish_pid
```

查看 fish shell 进程：

![[Pasted image 20260513221124.png|200]]

# 四、fish配置文件

macOS 默认 shell 通常是 zsh，zsh 常见的用户配置文件主要有两个：

```text
~/.zprofile
~/.zshrc
```

`.zprofile` 通常用于登录 shell 启动时执行，适合放一些偏“环境初始化”的配置，例如 `PATH`、`JAVA_HOME`、`ANDROID_HOME`、`Homebrew` 初始化等。

`.zshrc` 通常用于交互式 shell 启动时执行，适合放一些偏”交互体验”的配置，例如 alias、主题、提示符、自动补全、快捷函数等。

fish 不会读取 `~/.zprofile`，也不会读取 `~/.zshrc`。fish 的用户配置文件是：

```text
~/.config/fish/config.fish
```

所以，如果从 zsh 切换到 fish，之前写在 `.zprofile` 或 `.zshrc` 里的配置不会自动生效。需要把真正需要在 fish 中生效的配置改写成 fish 语法，并写入 `~/.config/fish/config.fish`。

例如 zsh 中的写法：

```shell
export EDITOR="code"
export PATH="$HOME/.cargo/bin:$PATH"
```

在 fish 中可以改成：

```shell
set -gx EDITOR code
fish_add_path $HOME/.cargo/bin
```

# 五、Homebrew路径配置

如果你前面在 zsh 中安装过 Homebrew，现在把 fish 设置成默认 shell，需要确保 fish 能找到 Homebrew 安装的软件。

如果你之前在 zsh 的 `~/.zprofile` 设置过：

```shell
eval "$(/opt/homebrew/bin/brew shellenv)"
```

那么在 fish 的配置文件 `~/.config/fish/config.fish` 里也可以加入：

```shell
eval "$(/opt/homebrew/bin/brew shellenv)"
```

`/opt/homebrew/bin/brew shellenv`会根据当前 shell 生成匹配当前 shell 的设置环境变量语法。

如果你不想添加 `eval "$(/opt/homebrew/bin/brew shellenv)"`，那么也可以在 `~/.config/fish/config.fish` 里加入：

```shell
fish_add_path /opt/homebrew/bin
```

`fish_add_path` 是 fish 中专门用于添加 PATH 的命令，适合替代手动修改 `PATH`。它会把路径加入 fish 的路径列表，并避免重复添加。

# 六、fish shell 基础语法

## 1、fish shell 和 POSIX shell 语法差异

POSIX shell 指的是 `sh` 这一套标准化 shell 语法。`bash`、`zsh`、`ksh` 在很多基础语法上和 POSIX shell 接近，而 fish 是另一套设计，语法明显不同。

## 2、变量赋值

POSIX shell 写法：

```shell
NAME="ABC"
echo $NAME
```

fish shell写法：

```shell
set NAME ABC
echo $NAME
```

如果要设置环境变量，也就是让子进程可以读取这个变量，fish 中使用 `-x` 或 `-gx`：
```shell
set -gx EDITOR code
```

其中：

```shell
set NAME ABC       设置普通变量
set -x NAME ABC    设置导出变量
set -gx NAME ABC   设置全局导出变量
```

## 3、if条件判断

例如判断当前目录下是否存在 test.txt 文件。

POSIX shell 写法：

```shell
if [ -f test.txt ]; then
	echo yes
fi
```

fish shell 语法：

```
if test -f test.txt
	echo yes
end
```

fish 不使用 `then` 和 `fi`，而是使用 `end` 结束代码块。

## 4、for循环

POSIX shell 写法：

```shell
for x in a b c; do
	echo $x
done	
```

fish shell 写法：

```shell
for x in a b c
	echo $x
end	
```

fish 不使用 `do` 和 `done`，而是使用 `end`。

## 5、函数定义

POSIX shell 写法：

```shell
myfunc() {
	echo hello
}
```

fish shell 写法：

```shell
function myfunc
	echo hello
end
```

定义后可以直接调用：`myfunc`。

## 6、命令替换

命令替换是指：***先执行一个命令，把这个命令的输出结果拿回来，再放到另一个命令或变量中使用**。

POSIX shell 常见写法：

```shell
today=$(date)
echo $today
```

fish shell 常见写法：

```shell
set today (date)
echo $today
```

fish 使用圆括号 `()` 做命令替换，而不是 `$()`。

## 7、PATH和环境变量写法

在 POSIX shell 中，经常这样修改 PATH：

```shell
export PATH="$PATH:/new/path"
```

fish 中更推荐使用：

```shell
fish_add_path /new/path
```

如果手动写，也可以写成：

```shell
set -gx PATH $PATH /new/path
```

但对于 PATH 这种变量，优先使用 `fish_add_path` 更清晰。

## 8、关于 fish 中的 export

fish 的新版本中提供了 export 兼容函数，方便用户在交互式场景下临时复制一些 bash 风格命令。

可以执行：

```shell
type export
```

如果输出显示 `export` 是一个 function，说明它是 fish 提供的兼容函数。

不过在 `config.fish` 中，仍然建议使用 fish 原生写法：

```shell
set -gx EDITOR code
fish_add_path /opt/homebrew/bin
```

## 9、fish的别名和缩写

fish 中可以使用 alias：

```shell
alias ll="ls -lh"
```

但 fish 中更推荐使用 `abbreviation`，也就是缩写。缩写的特点是：**输入短命令后，按空格自动展开为完整命令**。

例如：

```shell
abbr -a gs "git status"
```

输入：

```shell
gs
```

按空格后会自动展开为：

```
git status
```

这种方式比 alias 更直观，因为最终执行前你能看到完整命令。


# 七、fish 主题和插件管理

fish 本身已经内置了不错的交互体验。如果只是想要更好看的提示符，有两种常见选择：

1. 使用 fish 自带配置工具
2. 使用 OMF、Fisher、Starship 等工具

如果你只是想换主题，可以使用 OMF；如果你更偏向轻量插件管理，也可以了解 Fisher；如果你希望跨 shell 使用统一提示符，可以了解 Starship。

fish 自带一个 Web 配置界面，可以执行：

```shell
fish_config
```

它可以用来调整提示符、颜色主题、函数等配置。


# 八、On My Fish

## 1、简介

On My Fish 简称 OMF。它是一个**fish shell 框架**，用来安装和管理 fish 的主题、插件和扩展。OMF 官方仓库说明，它提供基础设施，让用户安装可以扩展或修改 shell 外观的包。

## 2、安装OMF

安装 OMF 的命令如下：

```shell
curl -L https://raw.githubusercontent.com/oh-my-fish/oh-my-fish/master/bin/install | fish
```

安装完成后，fish 提示符可能会发生变化。

## 3、查看已安装的主题和插件

```shell
omf list
```


## 4、查看主题

```shell
omf theme
```


## 5、安装主题

例如安装`clearance`：

```shell
omf install clearance
```

## 6、切换主题

```shell
omf theme clearance
```

## 7、移除主题或插件

```shell
omf remove clearance
```

## 8、更新

```shell
omf update omf      # 更新 omf 本身
omf update           # 更新 omf 所有包
omf update clearance # 更新指定包
```

## 9、更新所有OMF包

```shell
omf update
```

## 10、卸载 OMF

```shell
omf destroy
```