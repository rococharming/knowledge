---
title: 安装Python
date: 2026-06-27
tags: [Python, Python基础]
aliases:
  - 安装Python
---

# 一、简介

Python 是一种以**简洁**和**易用**著称的通用编程语言。它被用于许多领域，包括机器学习、网页开发、脚本编写与自动化、嵌入式系统、物联网等。

本篇笔记关注 `macOS` 系统下的 Python 安装与基础开发环境配置。

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

![[assets/Pasted image 20260527125731.png|500]]

注意，当在终端中输入`python3`时，系统会根据 `PATH` 环境变量中的目录顺序，依次查找名为 `python3` 的可执行文件。如果`Homebrew`的路径排在较后面，可能运行的是`macOS`系统自带的`Python`。此时，推荐把 Homebrew 的环境配置写入 `~/.zprofile`：

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

![[assets/Pasted image 20260527130236.png|500]]

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

macOS 中也可以使用快捷键<kbd>Ctrl</kbd> + <kbd>D</kbd>。


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

![[assets/Pasted image 20260527130840.png|500]]

说明当前 Python 没有可用的 `Tkinter/Tk` 支持，需要安装。

因为`Python`是使用Homebrew 安装的，可以安装：

```shell
brew install python-tk
```

安装完成后，就可以执行`idle3`命令了：

![[assets/Pasted image 20260527131056.png|400]]

打开 `IDLE` 后，一般先看到的是 `IDLE Shell`，进入交互式环境，这适合临时测试代码，但不适合编写完整程序。

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

也可以使用快捷键 <kbd>Command</kbd> + <kbd>S</kbd>。

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


## 3、直接运行Python文件

平时运行 Python 文件，一般是这样：

```shell
python3 hello.py
```

即启动 python3 解释器，让它去执行 hello.py。

在`macOS`或`Linux`中，可以直接运行：

```shell
./hello.py
```

但需要在`hello.py`文件的第一行加上一个特殊的注释：

```python
#!/usr/bin/env python3
print('Hello World')
```

然后给`hello.py`加上可执行权限；

```shell
chmod +x hello.py
```

这个原理涉及Unix可执行文件机制和`Shebang`行。`#!/usr/bin/env python3`就是`Shebang`行。

之后直接运行：

```shell
./hello.py
```

表面上看像是在运行 `.py` 文件，实际上并不是操作系统直接理解 Python 代码。操作系统先读取`hello.py`第一行，根据第一行找到 `python` 解释器，再用`python3`去执行`hello.py`。


# 四、安装 PyCharm

## 1、PyCharm的作用

`PyCharm` 是 JetBrains 提供的 Python IDE，提供代码编写、项目管理、运行调试等能力。

相比 `IDLE`，它更适合正式编写 Python 项目，常见能力包括：

- 项目管理：管理多个`.py`文件和目录
- 代码补全：根据上下文提示变量、函数、模块
- 语法检查：提前发现常见错误
- 调试器：设置断点，逐步执行代码
- 虚拟环境管理：为不同项目创建独立 Python 环境
- 包管理：安装和管理第三方依赖

## 2、安装PyCharm

进入[PyCharm官网](https://www.jetbrains.com/pycharm/download)下载安装。


## 3、PyCharm中配置 Homebrew Python

### （1）打开项目

打开 PyCharm 后，选择：

```
Open
```

然后选择某个目录，PyCharm 会把这个目录作为一个项目打开。

### （2）选择 Python 解释器

PyCharm 需要知道当前项目使用哪个Python 解释器。

进入设置：

```text
Settings → Python → Interpreter
```

之后，一般会看到当前项目解释器。

![[assets/Pasted image 20260527143446.png|600]]

如果还没有配置，选择`Add Interpreter`，然后选择：`Add Local Interpreter`。

或者点击`PyCharm`右下角：

![[assets/Pasted image 20260527151421.png|300]]

弹出如下界面：

![[assets/Pasted image 20260527152200.png|500]]

这里可以在项目目录下创建一个新的虚拟环境 `.venv`，并且用 Homebrew Python 作为基础解释器。以后在这个项目里安装包，会安装到 `.venv` 里，而不是污染全局 Homebrew Python。

### （3）创建并运行Python文件

在项目中创建文件：

```text
hello.py
```

写入：

```python
print("Hello, PyCharm")
```

运行方式：

```text
右键 hello.py → Run 'hello'
```

或者点击顶部运行按钮。

如果控制台输出：

```shell
Hello, PyCharm
```

说明 PyCharm 已经可以正确使用 Python 解释器运行代码。


# 五、pip包管理工具

## 1、pip的作用

`pip`是 Python 的包管理工具，用来安装、升级、卸载和查看第三方 Python 包。

Python 本身只提供了标准库，例如字符串处理、文件读写、时间日期、JSON解析等基础能力。如果需要使用其他开发者发布的第三方库，通常就需要通过 `pip` 安装。

例如，`requests`是常用的 HTTP 请求库，可通过如下命令安装：

```shell
python3 -m pip install requests
```

> `python3 -m pip`的含义：使用`python3`这个解释器，运行`pip`模块。系统中可能同时存在多个`Python`，如果直接执行`pip`或`pip3`，有时不容易看出这个`pip`属于哪个Python。因此，使用`python3 -m pip`明确告诉系统使用这个`python3`对应的`pip`。

安装后，就可以在 Python 代码中导入并使用：

```python
import requests
```


## 2、常用pip操作

- 查看`pip`版本

```shell
python3 -m pip --version
```

- 安装第三方包

```shell
python3 -m pip install 包名
```

- 升级第三方包

```shell
python3 -m pip install --upgrade 包名
```

- 卸载第三方包

```shell
python3 -m pip uninstall 包名
```

- 查看已安装的包

```shell
python3 -m pip list
```


## 3、全局Python与虚拟环境中的pip

### （1）使用 Homebrew 全局 Python 时

如果当前终端中的 `python3` 指向：

```shell
/opt/homebrew/bin/python3
```

那么执行：

```shell
python3 -m pip install requests
```

通常会把包安装到 Homebrew Python 对应的环境中。

这种方式可以用，但不建议所有项目都直接依赖全局环境。


### （2）使用 PyCharm 项目虚拟环境时

如果项目使用的是：

```shell
~/projects/hello_python/.venv/bin/python
```

那么在 PyCharm 的 Terminal 中执行：

```shell
python -m pip install requests
```

会把`requests`安装到当前项目的`.venv`中。

因为虚拟环境激活后，`python` 已经指向当前项目的虚拟环境解释器，因此不必写`python3 -m pip`。

注意：

在 PyCharm 终端下，如果虚拟环境没有激活，可在项目目录执行：

- fish

```shell
source .venv/bin/activate.fish
```

- zsh / bash

```shell
source .venv/bin/activate
```

激活后，命令行前面会出现`(.venv)`。

如果要退出虚拟环境，在当前终端输入：

```shell
deactivate
```
