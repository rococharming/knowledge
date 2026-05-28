# 一、概述

Python 中常用的有序集合类型主要有两种：`list`和`tuple`。

|类型|中文名称|是否可变|常见用途|
|---|---|---|---|
|`list`|列表|可变|保存一组需要增删改的元素|
|`tuple`|元组|不可变|保存一组确定后不希望修改的元素|
`list` 和 `tuple` 都是有序集合，都可以通过索引访问元素，也都支持正向索引和负向索引。它们的主要区别在于：

> `list` 创建后可以修改，`tuple` 创建后不能修改自身保存的元素引用。


# 二、list

## 1、list的基本含义

`list`是 Python 内置的一种有序集合，可以保存多个元素。

示例：

```python
a = [1, 2, 3]

print(a)
```

输出：`[1, 2, 3]`

其内存示意图如下：

![[Pasted image 20260528170441.png|300]]

可以使用 `len()` 获取列表中元素的个数：

```python
print(len(a))
```

输出：3

## 2、通过索引访问元素

`list` 中的元素按照顺序排列，索引从 `0` 开始。

```python
classmates = ["Michael", "Bob", "Tracy"]

print(classmates[0])
print(classmates[1])
print(classmates[2])
```

如果索引超出范围，例如：

```python
print(classmates[3])
```

会抛出 `IndexError`：

![[Pasted image 20260528151118.png|600]]

Python 支持使用**负向索引**从列表末尾访问元素。

```python
classmates = ["Michael", "Bob", "Tracy"]

print(classmates[-1])
print(classmates[-2])
print(classmates[-3])
```

常见索引关系如下：

```text
元素：   Michael     Bob     Tracy
正向索引：   0         1        2
负向索引：  -3        -2       -1
```

负向索引同样不能越界：

```python
print(classmates[-4])
```

同样报错：`IndexError: list index out of range`


## 3、常用操作

### （1）追加元素

`list` 是可变的，可以使用 `append()` 在末尾追加元素。

```python
classmates = ["Michael", "Bob", "Tracy"]

classmates.append("Adam")

print(classmates)
```

`append()` 总是把新元素添加到列表末尾。

### （2）插入元素

可以使用 `insert()` 把元素插入到指定位置。

```python
classmates = ["Michael", "Bob", "Tracy"]

classmates.insert(1, "Jack")

print(classmates)
```

`insert(1, "Jack")` 表示把 `"Jack"` 插入到索引 `1` 的位置，原来索引 `1` 及其后面的元素会向后移动。


### （3）删除末尾元素

可以使用 `pop()` 删除列表末尾的元素。

```python
classmates = ["Michael", "Bob", "Tracy"]

name = classmates.pop()

print(name)
print(classmates)
```

结果：

```text
Tracy
['Michael', 'Bob']
```

`pop()` 会删除元素，并返回被删除的元素。


### （4）删除指定位置的元素

可以使用 `pop(i)` 删除指定索引位置的元素。

```python
classmates = ["Michael", "Jack", "Bob", "Tracy"]

name = classmates.pop(1)

print(name)
print(classmates)
```

### （5）修改元素

可以直接给指定索引位置重新赋值。

```python
classmates = ["Michael", "Bob", "Tracy"]

classmates[1] = "Sarah"

print(classmates)
```


## 4、list中的元素类型

Python 的 `list` 可以保存不同类型的元素。

```python
L = ["Apple", 123, True]

print(L)
```

不过在实际代码中，列表通常会存放同一类数据，这样更便于理解和处理。


## 5、嵌套列表

`list`中的元素也可以是另一个`list`。

```python
s = ["python", "java", ["asp", "php"], "scheme"]

print(len(s))
print(s[2])
print(s[2][1])
```

结果：

```text
4
['asp', 'php']
php
```

嵌套列表可以表示二维结构，但如果层级过深，代码会变得不易阅读。


## 6、空列表

空列表使用`[]`表示。

空列表常用于先创建一个容器，后续再逐步添加元素。

```python
names = []

names.append("Michael")
names.append("Bob")

print(names)
```


# 三、tuple

## 1、tuple的基本含义

`tuple` 是另一种有序集合，中文通常称为元组。

它和 `list` 很相似，也可以通过索引访问元素，但 `tuple` 一旦创建，就不能修改。

```python
a = (1, 2, 3)

print(a[0])
print(a[-1])
```

输出：

```
1
3
```

其内存示意图如下：

![[Pasted image 20260528170529.png|300]]

## 2、tuple的不可变性

`tuple` 创建后，不能替换其中某个位置的元素。

```python
classmates = ("Michael", "Bob", "Tracy")

classmates[1] = "Sarah"
```

报错：

![[Pasted image 20260528152712.png|600]]

由于tuple无法修改，因此没有 `append()`、`insert()`、`pop()` 这类修改方法。

如果一组数据创建后不希望被修改，可以优先使用 `tuple`。

例如：

```python
point = (3, 5)
rgb = (255, 128, 0)
```

这类数据更强调“整体固定”，使用 `tuple` 比 `list` 更合适。



## 3、tuple的定义细节

定义一个普通元组：

```python
t = (1, 2)
print(t)
```

空元组使用 `()` 表示。

```python
t = ()
print(t)
```

定义只有一个元素的`tuple`时，必须在元素后面加逗号。

```python
t = (1,)
print(t)
```

如果写成`t = (1)`，那么`(1)`会被Python 当作普通数学括号，而不是 `tuple`。

因此，判断单元素元组的关键不是括号，而是逗号：

```python
t = 1,
print(t)
```

输出：

```python
(1,)
```

不过为了可读性，通常写成：

```python
t = (1,)
```

## 4、tuple中包含可变对象

**`tuple`的不可变指的是`tuple`中每个位置保存的对象引用不能改变**。

例如：

```python
t = ("a", "b", ["A", "B"])
```

这个 `tuple` 有 3 个元素：

```text
t
├── "a"
├── "b"
└── list ["A", "B"]
```

![[Pasted image 20260528153502.png|300]]

不能把 `t[0]` 改成其他对象，也不能把 `t[2]` 改成另一个列表：

```python
t[0] = "x"
t[2] = ["X", "Y"]
```

这两种写法都会报错。

但**可变元素本身仍然可以修改**，如果 `tuple` 中保存的是一个 `list`，这个 `list` 自身仍然可以修改：

```python
t = ("a", "b", ["A", "B"])

t[2][0] = "X"
t[2][1] = "Y"

print(t)
```

输出：

```text
('a', 'b', ['X', 'Y'])
```

![[Pasted image 20260528153544.png|300]]

`t[2]` 仍然指向原来的那个 `list`，只是这个 `list` 内部的元素变了。

> 如果希望`tuple`的内容也真正保持不变，需要保证它包含的每个元素本身也是不可变对象。