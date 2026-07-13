---
title: Python字符串
date: 2026-06-27
tags: [Python, Python基础]
---

# 一、定义字符串

Python 中的字符串是由**单引号**或**双引号**包围的一系列字符。在某些编程语言中，被单引号包围的字符与被双引号包围的字符处理方式不同，但在 Python 中，它们被视为相等。

因此，在处理字符串时，你可以使用任意一种。

示例：

```python
my_str_1 = "Hello"
my_str_2 = '你好'
```

```python
print("Hello, 世界")
```

如果需要**多行字符串**，可以使用三重双引号或单引号：

```python
my_str_3 = """多行  
文本  
字符串"""  
  
my_str_4 = '''另一个  
文本  
字符串'''  
  
print(my_str_3)  
print(my_str_4)
```

结果：

![[assets/Pasted image 20260615224325.png|50]]

如果字符串内容中包含单引号或双引号，此时有两种方式显示它们：

1. 使用相反类型的引用，即如果字符串包含单引号，则用双引号包裹；如果字符串包含双引号，则用单引号包裹

```python
msg = "It's a beautiful girl"
quote = 'He said "Hello"'
```

2. 使用反斜杠`\`转义字符转义字符串中的单引号或双引号

```python
msg = 'It\'s a beautiful girl'
quote = "He said \"Hello\""
```


# 二、字符串的不可变性

Python 中的所有数据都成为对象，有些对象是可变的，有些对象是不可变的。

不可变的数据类型一旦声明后就不能被修改，但可以将它们的变量指向新的内容，这称为赋值。但你不能通过添加、删除或替换任何元素更改原始对象本身。

![[assets/Pasted image 20260615230144.png|400]]

字符串就是 Python 典型的不可变类型。

对字符串变量重新赋值：

```python
greeting = 'hi'
greeting = 'hello'
print(greeting) # hello
```

但不允许直接修改字符串：

```python
greeting = 'hi'
greeting[0] = 'H' # TypeError: 'str' object does not support item assignment
```

整数、浮点数、布尔、元组和范围也是不可变数据类型。


# 三、字符串常见操作

## 1、判断字符或子串是否存在

有时，你可能需要查看一个字符串中是否包含一个或多个字符，Python 提供了`in`操作符，它返回一个布尔值，判断字符或子串是否存在于某个字符串中。

```python
my_str = "Hello world"  
  
print("Hello" in my_str)  # True  
print("Python" in my_str) # False  
print('a' in my_str)   # False
```

## 2、获取字符串的长度

获取字符串的长度，你可以使用内置的 `len()` 函数。

示例：

```python
my_str = 'Hello world'
print(len(my_str))  # 11
```

这里输出的是**字符数而非字节数**。

## 3、字符串索引

字符串中的每个字符都有一个称为索引的位置。索引是从零开始的，这意味着字符串中第一个字符的索引是 `0`，第二个字符的索引是 `1`，依此类推。

通过`[]`访问指定位置的字符：

```python
my_str = "Hello world"

print(my_str[0])  # H
print(my_str[6])  # w
```

除了正向索引外，Python 也允许负向索引，即从字符串的最后一个位置开始。用 `-1` 获取任何字符串的最后一个字符，用 `-2` 获取倒数第二个字符，依此类推：

```python
my_str = 'Hello world'
print(my_str[-1])  # d
print(my_str[-2]) # l
```


## 4、字符串拼接

在 Python 中，可以使用加号（`+`）操作符将多个字符串串接在一起，这个过程称为字符串拼接。

```python
my_str_1 = 'Hello'
my_str_2 = "World"

str_plus_str = my_str_1 + ' ' + my_str_2
print(str_plus_str) # Hello World
```

需要注意，`+`操作符仅适用于字符串之间的拼接，不能拼接字符串和数字，如果这样操作会得到`TypeError`：

```python
name = 'Tom'
age = 25

name_and_age = name + age
print(name_and_age)
```

结果：

![[assets/Pasted image 20260615230640.png|300]]

这是因为 Python 在连接时不会自动将其他数据类型如整数转换为字符串。Python 要求所有元素必须是字符串才能进行连接。

为了解决这个问题，可以使用内置的 `str()` 函数将数字转换为字符串，该函数返回给定对象的字符串表现形式，而不修改原始对象：

```python
name = 'Tom'  
age = 25  
  
name_and_age = name + str(age)  
print(name_and_age)
```

还可以使用扩充赋值操作符来进行串接。它表现为加号和等号（`+=`），并在一步中执行串接和赋值。下面是它的示例：

```python
name = 'Tom'  
age = 25  
  
name_and_age = name  
name_and_age += str(age)  
print(name_and_age)
```

内存示意图如下：

![[assets/Pasted image 20260615231320.png|500]]

## 5、字符串插值

将变量和表达式插入到字符串中的过程称为**字符串插值**。Python 中有一类称为`f-strings`（格式化字面值）的字符串，它允许你使用简洁可读的语法处理插值。

f-strings 以 `f`（小写或大写）开头，紧跟引号，允许你在由花括弧（`{}`）表示的替换字段中嵌入变量或表达式。示例如下：

示例：

```python
name = 'Tom'  
age = 25  
  
name_and_age = f"My name is  {name}, I am {age} years old"
print(name_and_age)
```

注意你不需要使用 `str()` 函数转换非字符串类型。在上面的示例中，`age`变量的值在插值过程中在底层被转换为字符串。

## 6、转换为大小写

### （1）upper()

`upper()`方法用于将字符串中的所有字符都转换为大写的新建字符串。

```python
my_str = 'hello world'

uppercase_my_str = my_str.upper()
print(uppercase_my_str)  # HELLO WORLD
```

### （2）lower()

`lower()`方法用于将字符串中的所有字符都转换为小写的新建字符串。

```python
my_str = 'Hello World'

lowercase_my_str = my_str.lower()
print(lowercase_my_str)  # hello world
```


## 7、判断字符串是否全大写或小写

### （1）isupper()

`isupper()`方法判断当前字符串是否为全大写字母。

示例：

```python
my_str = 'HELLO WORLD'

print(my_str.isupper())  # True
```
### （2）islower()

`islower()`方法判断当前字符串是否为全小写字母。

示例：

```python
my_str = 'hello world'

print(my_str.islower())  # True
```


## 8、移除前导和尾随字符

`strip()`方法返回一个新建字符串，移除指定的前导和尾随字符。如果未传入参数，则移除前导和尾随空白字符。

示例：

```python
my_str = '  hello world  '

trimmed_my_str = my_str.strip()
print(trimmed_my_str)  # "hello world"
```

## 9、替换旧子串为新子串

`replace(old, new)`方法返回一个新建字符串，其中所有的 `old` 都被替换为 `new`。

示例：

```python
my_str = 'hello world'

replaced_my_str = my_str.replace('hello', 'hi')
print(replaced_my_str)  # hi world
```

## 10、分隔字符串

`split(separator)`方法将字符串按指定分隔符拆分成字符串列表。如果未指定分隔符，则按空白字符拆分。

示例：

```python
my_str = 'hello world'

split_words = my_str.split()
print(split_words)  # ['hello', 'world']
```


## 11、指定分隔符连接字符串

`join(iterable)`方法用于将可迭代对象的元素用分隔符连接成一个新的字符串。

示例：

```python
my_list = ['hello', 'world']

joined_my_str = ' '.join(my_list)
print(joined_my_str)  # hello world
```

这里表示用空格分隔每个字符串形成新的字符串。


## 12、判断是否以某个字符串为前缀或后缀

### （1）startswith

`startswith(prefix)`方法用于判断字符串是否以指定前缀开头，它返回布尔值。

示例：

```python
my_str = 'hello world'

starts_with_hello = my_str.startswith('hello')
print(starts_with_hello)  # True
```

### （2）endswith

- `endswith(suffix)`方法用于判断字符串是否以指定的后缀结尾，它返回布尔值。

示例：

```python
my_str = 'hello world'

ends_with_world = my_str.endswith('world')
print(ends_with_world)  # True
```


## 13、查找子串

`find(substring)`方法返回子串第一次出现的索引，如果没有找到返回-1。

示例：

```python
my_str = 'hello world'

world_index = my_str.find('world')
print(world_index)  # 6
```

## 14、统计子串在字符串中出现的次数

 `count(substring)`方法返回子串在字符串中出现的次数。

```python
my_str = 'hello world'

o_count = my_str.count('o')
print(o_count)  # 2
```


## 15、首字母大写

`capitalize()`方法返回一个新字符串，首个字符大写，其余字符小写。

示例：

```python
my_str = 'hello world'

capitalized_my_str = my_str.capitalize()
print(capitalized_my_str)  # Hello world
```

## 16、每个单词首字母大写

`title()`方法返回一个新字符串，每个单词首字母均大写。

示例：

```python
my_str = 'hello world'

title_case_my_str = my_str.title()
print(title_case_my_str)  # Hello World
```


# 四、str 类型和 bytes 类型

## 1、str类型

### （1）Unicode 字符序列

在 Python 中，字符串的类型是`str`，它是 Unicode 文本序列。

示例：

```python
my_str = "中文"
```

这里的 `my_str` 是一个 `str`，它包含两个字符：中、文，对应的Unicode码点为：

|字符|Unicode 码点|
|---|---|
|`中`|`U+4E2D`|
|`文`|`U+6587`|

>注意，Python中的`str`不是UTF-8字节序列，而是Unicode文本序列。只有在编码时，`str`才会变成UTF-8、GBK或其他编码形式的字节。

### （2）`ord()`和`chr()`

Python 提供了`ord()`和`chr()`用于字符和Unicode码点之间的转换。

`ord()`用于获取单个字符对应的整数码点：

```python
print(ord('A'))
print(ord('中'))
```

输出：

```text
65
20013
```

如果想看十六进制形式，可以使用`hex()`：

```python
print(hex(ord('中')))
```

输出：

```text
0x4e2d
```

`chr()`用于把整数码点转换为对应字符：

```python
print(chr(65))
print(chr(0x4e2d))
```

输出：

```text
A
中
```

### （3）\u转义写法

如果知道字符的`Unicode`码点，也可以使用`\u`转义字符序列表示字符串。它表示一个Unicode字符，由4位16进制表示。

```python
print("\u4e2d\u6587")
```

输出：

```text
中文
```

这和直接写中文是等价的。


## 2、bytes

### （1）bytes 的基本含义

`bytes`表示字节序列。它不是文本，而是由一个个字节组成的二进制数据。

Python 中使用`b`前缀创建`bytes`：

```python
my_bytes = b"ABC"
```

这里的 `my_bytes`类型是 `bytes`而不是 `str`。

使用`type()`查看类型：

```python
print(type("ABC"))  
print(type(b"ABC"))
```

结果：

![[assets/Pasted image 20260528001823.png]]


### （2）str 和 bytes 区别
`str`和`bytes`类型区别如下：

|表达式|类型|含义|
|---|---|---|
|`"ABC"`|`str`|Unicode 文本字符串|
|`b"ABC"`|`bytes`|字节序列|

### （3）bytes中的元素是整数

`bytes`本质上是一串字节，每个字节的取值范围是`0`到`255`。

例如：

```python
my_bytes = b"ABC"
print(my_bytes[0])
```

输出：

```text
65
```

因为字符 `A` 的 ASCII 值是 `65`。

### （4）\x转义写法

 `b'...'`字面量必须是 ASCII 字符，而不是其他非 ASCII 字符：
 
```python
print(b"ABC")  # 正确
print(b"中文")  # 错误
```

报错：

![[assets/Pasted image 20260615233850.png|300]]

可以使用`\x##`十六进制序列表示`bytes`字面值。

```python
my_bytes = b'\xe4\xb8\xad\xe6\x96\x87'
print(my_bytes)
```

输出：

```text
b'\xe4\xb8\xad\xe6\x96\x87'  
```

## 3、编码和解码

### （1）编码

编码（`encode`）是指将`str`转换为`bytes`。

Python中使用 `encode` 将`str`（Unicode文本序列）转换为`bytes`（二进制字节序列）。

`encode`需要传入字符编码的方式，例如`ascii`、`utf-8`、`gbk`等。

示例1：

```python
my_str = "ABC"  
print(my_str)  
my_bytes = my_str.encode('ascii')  
print(my_bytes)
```

输出：

```text
ABC
b'ABC'
```

示例2：

```python
my_str = "中文"  
print(my_str)  
my_bytes = my_str.encode('utf-8')  
print(my_bytes)
```

输出：

```text
中文
b'\xe4\xb8\xad\xe6\x96\x87'
```

示例3：

```python
my_str = "中文"  
print(my_str)  
my_bytes = my_str.encode('gbk')  
print(my_bytes)
```

输出：

```text
中文
b'\xd6\xd0\xce\xc4'
```

### （2）解码

解码（`decode`）是指把`bytes`转为`str`。

Python中使用 `decode` 将`bytes`（二进制字节序列）转换为`str`（Unicode文本序列）。

示例1：

```python
my_bytes = b"ABC"  
print(my_bytes)  
my_str = my_bytes.decode('ascii')  
print(my_str)
```

输出：

```text
b'ABC'
ABC
```

示例2：

```python
my_bytes = b'\xe4\xb8\xad\xe6\x96\x87'  
print(my_bytes)  
my_str = my_bytes.decode('utf-8')  
print(my_str)
```

输出：

```text
b'\xe4\xb8\xad\xe6\x96\x87'
中文
```

如果指定错误的字符编码：

```python
my_bytes = b'\xe4\xb8\xad\xe6\x96\x87'  
print(my_bytes)  
my_str = my_bytes.decode('gbk')  
print(my_str)
```

这里`my_bytes`是UTF-8字节序列，但错误使用了`gbk`解码，会报错：

![[assets/Pasted image 20260615235134.png|500]]

### （3）解码错误处理

如果使用错误的字符编码来解码，就可能报错或产生乱码。

但如果`bytes`中只有一小部分无效的字节，可以传入`errors='ignore'`忽略错误的字节：

```python
print(b'\xe4\xb8\xad\xff'.decode('utf-8', errors='ignore'))
```

输出：

```text
中
```

`0xff`属于UTF-8的非法字节，这里忽略了该错误字节。

其他常见处理方式：

|写法|含义|
|---|---|
|`errors="strict"`|默认方式，遇到错误直接报错|
|`errors="ignore"`|忽略无法解码的字节|
|`errors="replace"`|用替代字符替换无法解码的字节|

> 编码和解码必须匹配

### （4）Python源文件编码

Python 源代码文件（`.py`）本身也是一个文本文件。

如果源代码中包含中文、日文、Emoji 等非 ASCII 字符，需要确保 `.py` 文件本身使用正确的文本编码保存。

例如：

```python
print("中文")
```

现代 Python 3 项目通常统一使用 UTF-8 保存源文件。

有时会在 Python 脚本文件开头看到这两行：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```

第一行是 `Shebang`，主要用于 Linux、macOS 等类 Unix 系统，含义是：

> 去环境变量 PATH 中查找 python3，然后用找到的 python3 执行这个脚本

这样，把 Python 文件增加了可执行权限后，可直接输入 Python 文件名执行：

```shell
chmod +x hello.py
./hello.py
```

不一定要写成：

```python
python3 hello.py
```

第二行是代码文件编码声明。含义是：

> 解释器读取这个 `.py` 文件时，应当按 `UTF-8` 来理解里面的字符。

需要注意的是：

代码文件编码声明只是告诉 Python 解释器按照什么编码来理解源文件，并不是自动改变文件本身的编码。因此，如果 `.py` 文件实际不是 UTF-8 编码，即使写了`# -*- coding: utf-8 -*-`，也仍然可能报错。

因此正确关系应该是编辑器保存编码为UTF-8，Python 解释器按 UTF-8 读取源代码。

不过在 Python 3 中，源码文件默认就是 `UTF-8`，所以这行通常不是必须的。

# 五、字符串格式化

## 1、字符串格式化的作用

字符串格式化用于把变量或表达式插入到字符串中。

Python 中常见的字符串格式化方式有三种：

| 方式         | 示例                         | 说明                |
| ---------- | -------------------------- | ----------------- |
| `%格式化`     | `"Hello, %s" % name`       | 旧式格式化方式           |
| `format()` | `"Hello, {}".format(name)` | 字符串方法             |
| `f-string` | `f"Hello, {name}"`         | Python 3.6 以后推荐使用 |

## 2、%格式化

% 格式化和 C语言风格比较接近。

示例：

```python
print("Hello, %s" % "world")
```

输出：

```text
Hello, world
```

多个值需要使用元组传入：

```python
name = "Michael"
money = 1000000

print("Hi, %s, you have $%d." % (name, money))
```

输出：

```text
Hi, Michael, you have $1000000.
```

常见占位符如下：

| 占位符 | 含义         |
| ------ | ------------ |
| `%d`   | 整数         |
| `%x`   | 十六进制整数 |
| `%f`   | 浮点数       |
| `%s`   | 字符串       |

如果字符串中有多个占位符，后面的值需要按顺序一一对应。

格式化整数时，可以指定宽度和是否补零：

```python
print("%2d-%02d" % (3, 1))
```

其中：

- `%2d`表示整数至少占2位，不足时用空格补全
- `%02d`表示整数至少占2位，不足时用0补全

输出：

```text
 3-01
```

格式化浮点数时，可以指定小数位数：

```python
print("%.2f" % 3.1415926)
```

输出：

```text
3.14
```

`%s`具有通用性，可以将对象转换成字符串形式。如果不确定使用哪个占位符，`%s`通常可以作为兜底选择。

```python
print("Age: %s. Gender: %s" % (25, True))
```

如果字符串里要输出普通的 `%`，需要写成 `%%`：

```python
print("growth rate: %d %%" % 7)
```

输出：growth rate: 7 %


## 3、format()格式化

`format()`是字符串对象的方法，会把传入的参数填入字符串中的`{}`占位符。

示例：

```python
print("Hello, {}".format("world"))
```

多个参数会按顺序填入：

```python
print("Hello, {}, your score is {}.".format("小明", 95))
```

`format()` 可以通过 `{0}`、`{1}` 指定参数位置：

```python
print("Hello, {0}, 成绩提升了 {1:.1f}%".format("小明", 17.125))
```

其中 `{1:.1f}` 表示取第 2 个参数，并按浮点数格式保留 1 位小数。

`format()`也可以使用命名参数：

```python
print("姓名：{name}，成绩：{score}".format(name="小明", score=95))
```

这种写法在模板较长、变量较多时更清晰。

## 4、f-string格式化

`f-string`是 Python 3.6 引入的字符串格式化方法。

写法是在字符串前加 `f`，然后在字符串中使用 `{}` 插入变量或表达式。

示例：

```python
name = "小明"
score = 95

print(f"姓名：{name}，成绩：{score}")
```

`f-string` 的 `{}` 中不仅可以写变量，也可以写表达式。

```python
a = 3
b = 5

print(f"{a} + {b} = {a + b}")
```

也可以调用方法：

```python
name = "python"

print(f"{name.upper()}")
```

`f-string` 可以使用格式化参数：

```python
r = 2.5
s = 3.14 * r ** 2

print(f"The area of a circle with radius {r} is {s:.2f}")
```

其中 `{s:.2f}` 表示按浮点数格式显示，并保留 2 位小数。

# 六、字符串切片

字符串切片允许你提取字符串的一部分，仅处理其中的特定部分。

基本语法：

```python
string[start:stop]
```

含义：提取 string 从索引 start 开始到 stop-1 （不含stop）的字符序列。

示例：

```python
my_str = 'Hello world'
my_slice = my_str[1:4]
print(my_slice) # ell
```

内存示意图如下：
![[assets/Pasted image 20260616003704.png|500]]

可以省略`start`，此时表示从索引0开始：

```python
my_str = 'Hello world'
print(my_str[:4]) # Hell
```

也可以省略`stop`，此时表示一直到末尾：

```python
my_str = 'Hello world'
print(my_str[4:]) # o world
```

还可以同时省略`start`和`stop`，此时表示全量切片。

除了`start`和`stop`索引外，还有一个可选的`step`参数，用于指定切片中每个索引之间的增量。

语法：

```python
string[start:stop:step]
```

示例：

```python
my_str = 'Hello world'
print(my_str[0:11:2])  # Hlowrd
```

含义：切片从索引 `0` 开始，在 `11` 之前停止，并提取每隔一个的字符。

一个比较有用的技巧是通过将 step 设置为 `-1`，并将 `start` 和 `stop` 留空来反转一个字符串：

```python
my_str = 'Hello world'
print(my_str[::-1]) # dlrow olleH
```

step 为`-1`表示从右往左，每次移动一个位置。
