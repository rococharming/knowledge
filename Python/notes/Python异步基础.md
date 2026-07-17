---
title: Python异步基础
date: 2026-06-15
tags: [Python, 异步编程]
aliases:
  - Python异步基础
---

# 一、async def 

`async def`用来定义异步函数。异步函数被调用时，不会立即执行函数体，而是返回一个协程对象。

```python
async def func():
	...
```

调用`func()`时得到的是一个`coroutine`，而不是普通函数的返回值。

要真正执行它，需要放到事件循环中运行，例如在 Jupyter / IPython 中可以直接：

```python
await func()
```

在普通 Python 脚本中通常写成：

```python
import asyncio

asyncio.run(func())
```


# 二、await等待异步操作完成

`await` 用来等待一个异步操作完成。它不会像普通阻塞调用那样一直占住当前执行流程，而是把控制权交还给事件循环，让事件循环可以继续调度其他异步任务。

例如：

```python
final_message = await stream.get_final_message()
```

`await` 只能出现在 `async def` 定义的异步函数内部，或者支持顶层 `await` 的交互环境中。

# 三、async with上下文管理器

`with`语句是 Python 的上下文管理器语法。

它的作用是：进入代码块时获取资源，离开代码块时自动清理资源。

示例：

```python
with open("a.txt") as f:
	content = f.read()  
	print(content)
```

等价于下面更啰嗦的写法：

```python
f = open("a.txt")

try:
	content = f.read()  
	print(content)
finally:
	f.close()
```

使用`with`语句的好处是避免我们忘记关闭资源（如这里的文件句柄）。