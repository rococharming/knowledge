# 一、概述

Python 内置了两种常用的哈希集合类型：`dict`和`set`。

| 类型     | 中文名称 | 存储内容            | 主要用途                  |
| ------ | ---- | --------------- | --------------------- |
| `dict` | 字典   | `key-value` 键值对 | 根据 `key` 快速查找 `value` |
| `set`  | 集合   | 不重复的 `key`      | 去重、成员判断、集合运算          |

`dict`和`set`的底层都依赖哈希机制，因此查找速度很快。但也正因为如此，它们对元素有一个重要要求：**`dict`的`key`和`set`中的元素必须是可哈希对象，通常也就是不可变对象**。

> 不可变对象：对象一旦创建，它自身的内容就不能被修改。
> 注意变量和对象的区别。
> 变量是一个名字，它指向某个对象。


# 二、dict

## 1、dict的基本含义

`dict`全称为 dictionary，中文通常叫字典。在其他语言中，也常被称为`map`。

`dict` 使用 `key-value` 形式存储数据：

```python
d = {
	"Michael": 95,
	"Bob": 75,
	"Tracy": 85,
}

print(d["Michael"])
```

输出：95

这里 `"Michael"` 是 `key`，`95` 是对应的 `value`。

## 2、dict的查找特点

如果用两个 `list` 保存名字和成绩：

```python
names = ["Michael", "Bob", "Tracy"]  
scores = [95, 75, 85]
```

查找某个同学的成绩时，需要先在 `names` 中找到位置，再到 `scores` 中取对应位置的值。

如果使用 `dict`：

```python
scores = {  
	"Michael": 95,  
	"Bob": 75,  
	"Tracy": 85,  
}
```

就可以直接根据名字取成绩：

```python
print(scores["Bob"])
```

`dict` 适合做“根据某个标识快速查找对应数据”的场景。

## 3、dict常用操作

### （1）添加和修改元素

除了初始化时直接写入，也可以通过`key`增加元素：

```python
d = {
    "Michael": 95,
    "Bob": 75,
    "Tracy": 85,
}

d["Adam"] = 67

print(d)
```

输出：

```text
{'Michael': 95, 'Bob': 75, 'Tracy': 85, 'Adam': 67}
```

**如果 `key` 已经存在，再次赋值会覆盖原来的 `value`**。


### （2）访问不存在的key

如果直接访问不存在的`key`，例如：

```python
d = {
    "Michael": 95,
    "Bob": 75,
    "Tracy": 85,
}

print(d["Thomas"])
```

会抛出`KeyError`异常：

![[Pasted image 20260528164446.png|400]]

常见处理方式有两种：

- 使用`in`判断：

```python
if "Thomas" in d:
    print(d["Thomas"])
else:
    print("not found")
```

- 使用 `get()`：

```python
print(d.get("Thomas"))  
print(d.get("Thomas", -1))
```

`get(key)` 在 `key` 不存在时默认返回 `None`；`get(key, default)` 可以指定默认值。

### （3）删除元素

使用 `pop(key)` 可以删除指定 `key`，并返回对应的 `value`。

```python
d = {
    "Michael": 95,
    "Bob": 75,
    "Tracy": 85,
}

score = d.pop("Bob")

print(score)
print(d)
```

如果 `key` 不存在，`pop(key)` 会抛出 `KeyError`。

可以指定默认值：

```python
score = d.pop("Thomas", None)  
  
print(score)
```


### （4）遍历dict

可以遍历 `dict` 的 `key`：

```python
d = {
    "Michael": 95,
    "Bob": 75,
    "Tracy": 85,
}

for name in d:
    print(name)
```

也可以明确写成：

```python
for name in d.keys():
    print(name)
```

遍历 `value`：

```python
for score in d.values():  
	print(score)
```

同时遍历 `key` 和 `value`：

```python
for name,score in d.items():
	print(name, score)
```

`items()` 在实际代码中很常用，适合处理键值对。

## 4、dict的特点

- 查找和插入速度快
- 空间换时间
- 字典顺序：现代Python中，`dict`会保留插入顺序

## 5、key必须可哈希

`dict` 的 `key` 必须是可哈希对象。

常见可以作为 `key` 的类型：

| 类型      | 示例            |
| ------- | ------------- |
| `str`   | `"name"`      |
| `int`   | `1001`        |
| `float` | `3.14`        |
| `bool`  | `True`        |
| `tuple` | `("Tom", 18)` |
> 需要注意，`tuple` 只有在内部元素也都可哈希时，才能作为 `dict` 的 `key`。

常见不能作为 `key` 的类型：

|类型|原因|
|---|---|
|`list`|可变|
|`dict`|可变|
|`set`|可变|

`dict` 需要根据 `key` 的哈希值定位数据。如果一个对象作为 `key` 后还能被修改，它的哈希结果就可能变化，`dict` 内部结构会失去稳定性。

因此，`dict` 的 `key` 必须稳定、可哈希。


# 三、set

## 1、set的基本含义

`set`是一组不重复元素的集合。

它和`dict`类似，但只保存 `key`，不保存 `value`。

创建 `set` 可以使用 `{}`：

```python
s = {1, 2, 3}

print(s)
```

输出：

```text
{1, 2, 3}
```

也可以使用 `set()` 从其他可迭代对象创建：

```python
s = set([1, 2, 3])

print(s)
```


## 2、自动去重

`set` 中不会保留重复元素。

```python
s = {1, 1, 2, 2, 3, 3}

print(s)
```

输出：

```text
{1, 2, 3}
```

这一点常用于列表去重：

```python
nums = [1, 1, 2, 2, 3, 3]

unique_nums = set(nums)

print(unique_nums)
```

> 需要注意，转成 `set` 后通常不会保留原列表顺序。

如果需要再转回列表，使用`list()`：

```python
nums = list(set(nums))
```


## 3、常用操作

### （1）增加元素

使用 `add()` 添加元素：

```python
s = {1, 2, 3}

s.add(4)
s.add(4)

print(s)
```

输出：

```text
{1, 2, 3, 4}
```

重复添加已有元素不会产生变化。


### （2）删除元素

使用 `remove()` 删除元素：

```python
s = {1, 2, 3, 4}

s.remove(4)

print(s)
```

输出：

```text
{1, 2, 3}
```

如果元素不存在，例如

```python
s.remove(5)
```

则程序会抛`KeyError`异常：

![[Pasted image 20260528171308.png|400]]

如果不希望元素不存在时报错，可以使用 `discard()`：

```python
s.discard(5)
```

`discard()` 删除不存在的元素时不会报错。

### （3）成员判断

`set` 很适合做成员判断。

示例：

```python
s = {"apple", "banana", "orange"}

print("apple" in s)
print("pear" in s)
```


### （4）集合运算

`set` 可以进行数学意义上的集合运算。

示例：

```python
s1 = {1, 2, 3}
s2 = {2, 3, 4}
```

- 交集

```python
print(s1 & s2)
```

结果：

```text
{2, 3}
```

也可以写成：

```python
print(s1.intersection(s2))
```

- 并集

```python
print(s1 | s2)
```

输出：

```text
{1, 2, 3, 4}
```

也可以写成：

```python
print(s1.union(s2))
```

- 差集

差集表示存在于左边集合，但不存在于右边集合的元素。

```python
print(s1 - s2)  
print(s2 - s1)
```

输出：

```text
{1}
{4}
```

也可以写成：

```python
print(s1.difference(s2))
```

- 对称差集

对称差集表示只存在于其中一个集合，而不是两个集合共有的元素。

```python
print(s1 ^ s2)
```

输出：

```text
{1, 4}
```

也可以写成：

```python
print(s1.symmetric_difference(s2))
```

常见集合运算如下：

|运算|符号|方法|
|---|---|---|
|交集|`s1 & s2`|`s1.intersection(s2)`|
|并集|`s1 \| s2`|`s1.union(s2)`|
|差集|`s1 - s2`|`s1.difference(s2)`|
|对称差集|`s1 ^ s2`|`s1.symmetric_difference(s2)`|

## 4、set元素要求

`set` 的元素和 `dict` 的 `key` 一样，也必须是可哈希对象。

可以放入 `set`：

```python
s = {"a", 1, (2, 3)}
```

不能放入`set`：

```python
s = {[1, 2, 3]}
```

原因和 `dict` 类似：`set` 需要判断元素是否已经存在，如果元素本身可变，就无法稳定地完成哈希和去重。


# 四、可变对象和不可变对象

## 1、可变对象

可变对象是指对象创建后，内部内容可以被修改。

典型例子是 `list`：

```python
a = ["c", "b", "a"]

a.sort()

print(a)
```

`sort()` 会直接修改原来的列表。

常见可变对象：

|类型|示例|
|---|---|
|`list`|`[1, 2, 3]`|
|`dict`|`{"name": "Tom"}`|
|`set`|`{1, 2, 3}`|

## 2、不可变对象

不可变对象是指对象创建后，自身内容不能被修改。

典型例子是 `str`：

```python
a = "abc"

b = a.replace("a", "A")

print(a)
print(b)
```

输出：

```text
abc
Abc
```

`replace()` 返回的是一个新字符串，原字符串不会改变。

常见不可变对象：

| 类型      | 示例       |
| ------- | -------- |
| `int`   | `1`      |
| `float` | `3.14`   |
| `bool`  | `True`   |
| `str`   | `"abc"`  |
| `tuple` | `(1, 2)` |
> 需要注意，`tuple` 本身不可变，但如果内部包含可变对象，可变对象内部仍然能变。