\
# 一、简介

`Homebrew`是macOS上常用的软件包管理工具，也支持Linux。它可以通过命令行安装、更新、搜索、卸载软件，适合管理开发工具、命令行程序以及部分图形界面应用。

例如，可以用`Homebrew`安装：

```shell
brew install node
brew install python
```

也可以通过 Homebrew Cask 安装图形界面应用，例如：

```shell
brew install --cask google-chrome
brew install --cask visual-studio-code
```

Homebrew 本质上解决的是软件安装和维护问题。没有 Homebrew 时，很多软件需要手动下载安装包、配置环境变量、处理依赖；使用 Homebrew 后，大部分操作可以通过统一的 `brew` 命令完成。Homebrew 官方也把它定位为 macOS 或 Linux 的软件包管理器。

# 二、安装前准备

在 macOS 上安装`Homebrew`之前，通常需要先安装 Xcode Command Line Tools。详见[[1、Xcode与命令行工具|Xcode命令行工具]]。

Xcode Command Line Tools 是 Apple 提供的一组命令行开发工具，包含 `clang`、`git`、`make` 等工具。Homebrew 在安装或编译某些软件时可能会依赖这些工具。

执行命令：

```shell
xcode-select --install
```

如果系统弹出安装窗口，按照提示安装即可。

如果已经安装过，系统可能会提示：

```shell
xcode-select: error: command line tools are already installed
```

这说明命令行工具已经存在，不需要重复安装。

# 三、安装Homebrew

Homebrew 官方安装命令是：

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

这条命令会从 Homebrew 官方 GitHub 仓库下载安装脚本并执行。

如果在国内网络环境下访问 GitHub 较慢，可以使用镜像源或第三方安装脚本。但这类脚本不属于 Homebrew 官方维护，使用前应确认来源可信。

例如：

```shell
/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
```

# 四、配置环境变量

安装完成后，终端通常会提示你执行类似下面的命令，把 Homebrew 加入 shell 环境变量。

Apple Silicon 芯片的 Mac，Homebrew 默认安装路径通常是：

```shell
/opt/homebrew
```

常见配置命令：

```shell
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

> `/opt/homebrew/bin/brew shellenv` 本质上是生成一组 `export` 命令，用来配置 Homebrew 所需的环境变量；`eval` 则会把这组输出结果当作 Shell 命令重新解析并执行。因此，这条命令的作用就是执行 Homebrew 生成的环境变量配置，让当前终端立即识别并使用 `brew`。

Intel 芯片的 Mac，Homebrew 默认安装路径通常是：

```shell
/usr/local
```

常见配置命令：

```shell
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/usr/local/bin/brew shellenv)"
```

这一步的作用是让系统能在终端中找到 `brew` 命令。否则可能会出现：

```shell
zsh: command not found: brew
```

# 五、验证安装

安装完成后，可以使用下面的命令验证 Homebrew 是否安装成功：

```shell
brew --version
```

如果能看到类似输出，说明安装成功：

![[Pasted image 20260513013040.png|300]]

还可以使用下面的命令检查 Homebrew 当前状态：

```shell
brew doctor
```

`brew doctor` 会检查当前 Homebrew 环境是否存在潜在问题。如果输出：

```shell
Your system is ready to brew.
```

说明环境基本正常。

# 六、常用命令

## 1、搜索软件

```shell
brew search node
```

用于搜索 Homebrew 中是否有某个软件包。

## 2、安装软件

```shell
brew install node
```

用于安装命令行软件包。

如果要安装图形用户界面应用，可以使用`-cask`：

```shell
brew install --cask visual-studio-code
```

## 3、查看已经安装的软件

```shell
brew list
```

用于查看当前通过 Homebrew 安装了哪些软件包。

如果只想查看图形界面应用，可以使用：

```shell
brew list --cask
```

## 4、查看某个软件的信息

```shell
brew info node
```

用于查看某个软件包的版本、安装路径、依赖关系、是否已安装等信息。

## 5、更新Homebrew软件包索引

```shell
brew update
```

`brew update` 用来更新 Homebrew 本地的软件包索引。

它不会直接升级已经安装的软件，而是让本地 Homebrew 知道：

- 哪些软件有新版本；
- 哪些软件包规则发生了变化；
- 哪些 formula 或 cask 被新增、删除或修改。

可以把它理解为：**先更新软件目录，但不真正升级软件。**

## 6、升级已安装软件

```shell
brew upgrade
```

`brew upgrade` 用来升级已经安装的软件包。

如果不指定软件名，它会尝试升级所有可升级的软件：

```shell
brew upgrade
```

如果只想升级某一个软件，可以写软件名：

```shell
brew upgrade node
```

`brew upgrade` 通常会先需要有最新的软件包索引。实际使用时，可以先执行：

```shell
brew update
brew upgrade
```

不过 Homebrew 在一些情况下也会自动更新索引，所以你不一定每次都必须手动执行 `brew update`。

## 7、清理旧版本和缓存

```shell
brew cleanup
```

`brew cleanup` 用来清理 Homebrew 产生的旧版本文件和缓存文件。

Homebrew 升级软件时，可能会保留旧版本文件。例如你之前安装过 `node 22.x`，后来升级到 `node 23.x`，旧版本的一些文件可能还留在本地。

`brew cleanup` 的作用就是清理这些不再需要的旧文件，释放磁盘空间。

如果你想先看看它会清理什么，但不真的删除，可以使用：

```
brew cleanup -n
```

这里的 `-n` 表示 dry run，也就是预演模式。它只显示将要清理的内容，不会真正删除文件。

确认没问题后，再执行：

```
brew cleanup
```


## 8、卸载软件

```shell
brew uninstall node
```

用于卸载指定软件包。

卸载图形界面应用可以使用：

```shell
brew uninstall --cask visual-studio-code
```