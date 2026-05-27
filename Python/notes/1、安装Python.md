
# 一、Python简介

`Python`是一门跨平台编程语言，可以运行在`Windows`、`macOS`、`Linux` 和各种类 `Unix` 系统上。

本篇笔记只关注 `macOS` 系统下的 Python 安装与基础开发环境配置。

安装`Python`最主要的就是安装**Python解释器**。Python解释器是运行Python程序的核心，编写的`.py`文件本身不能直接被操作系统执行，需要交给Python解释器读取、解析并运行。

Python曾经长期存在两个主要版本：

|版本|状态|
|---|---|
|`Python 2.x`|已经停止维护，不建议学习和使用|
|`Python 3.x`|当前主流版本，推荐安装和学习|
`Python 2`和`Python 3`并不完全兼容。同一段代码，在`Python 2`中能运行，不代表在`Python 3`中一定能运行。

现在学习 Python，应直接安装最新稳定版的 `Python 3`。

在`macOS`上，通常使用：

```shell
python3
```

运行 Python 3，而不是直接使用：

```shell
python
```

原因是 `python` 这个命令在不同环境中的含义可能不一致。它可能不存在，也可能指向旧版本或其他自定义版本。


# 二、通过Homebrew安装Python

通过`Homebrew`安装Python（Homebrew的安装参考[[2、Homebrew安装与使用|Homebrew安装与使用]]）：

```shell
brew install python
```

安装完成后，检查 Python 版本以及安装路径：

```shell 
python3 --version
which python3
```

![[Pasted image 20260527125731.png|500]]

注意，当在终端中输入`python3`时，系统会根据 `PATH` 环境变量中的目录顺序，依次查找名为 `python3` 的可执行文件。如果`Homebrew`的路径排在叫后面，可能运行的是`macOS`系统自带的`Python`。此时，推荐把 Homebrew 的环境配置写入 `~/.zprofile`：

```shell
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
source ~/.zprofile
```



# 三、运行Python

## 1、进入Python 交互式环境

打开 macOS 终端，输入：

```shell
python3
```

会看到类似输出：

![[Pasted image 20260527130236.png|500]]

其中：

```shell
>>>
```

表示已经进入 Python 交互式环境。

在这个环境中输入：

```shell
1 + 2
```

输出：

```shell
3
```

再输入：

```shell
print("Hello, Python")
```

输出：

```shell
Hello, Python
```

在 `>>>` 提示符下输入：

```shell
exit()
```

然后按回车，即可退出 Python 交互式环境。

macOS 中也可以使用快捷键`Ctrl + D`。


## 2、使用IDLE编写和运行Python

`IDLE`是 Python 自带的轻量级开发环境。

它主要包含两类窗口：

| 窗口             | 作用                     |
| -------------- | ---------------------- |
| `Python Shell` | 交互式输入 Python 代码，立即查看结果 |
| 编辑窗口           | 编写、保存、运行 `.py` 文件      |

`IDLE` 比终端交互环境稍方便，因为它可以新建和保存 `.py` 文件，也可以通过菜单直接运行当前文件。

执行`idle3`：

```shell
idle3
```

出现：

![[Pasted image 20260527130840.png|500]]

说明当前 Python 没有可用的 `Tkinter/Tk` 支持，需要安装。

因为`Python`是使用Homebrew 安装的，可以安装：

```shell
brew install python-tk
```

安装完成后，就可以执行`idle3`命令了：

![[Pasted image 20260527131056.png|400]]

打开 `IDLE` 后，一般先看到的是 `IDLE Shell`进入交互式环境，这适合临时测试代码，但不适合编写完整程序。

可以新建`.py`文件，在 `IDLE Shell` 顶部菜单中选择：

```text
File → New File
```

会打开一个新的编辑窗口。

在编辑窗口中输入：

```python
print("Hello, Python")
```

保存文件：

```text
File → Save
```

也可以使用快捷键：

```text
Command + S
```

保存后，在编辑窗口中选择：

```text
Run → Run Module
```

运行结果会显示在 `IDLE Shell` 窗口中。

运行后会看到：

```shell
Hello, Python
```

不过，`IDLE` 功能比较基础。后续正式写项目时，更常用的是 `PyCharm`、`VS Code` 这类功能更完整的开发工具。