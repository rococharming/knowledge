## PE
PE（Portable Executable），即可移植可执行文件格式。

PE 文件中会保存：

- 程序代码
- 程序中使用的数据
- 需要加载哪些 DLL
- 需要调用 DLL 中的哪些函数
- 图标、版本号等资源

例如，`myapp.exe`需要调用`kernel32.dll`中的`CreateFileW`。

那么这个信息会记录在`myapp.exe`自己的 PE 导入表中：

```
myapp.exe
└── 导入信息
    └── kernel32.dll
        └── CreateFileW
```

运行`myapp.exe`，Windows 会：

```
读取 myapp.exe
    ↓
发现它需要 kernel32.dll
    ↓
加载 kernel32.dll
    ↓
找到 CreateFileW 的地址
    ↓
让 myapp.exe 可以调用它
```

## ordinal

DLL 导出的函数，可以通过两种方式查找：

- 按名称查找：CreateFileW
- 按序号查找：ordinal 123

`ordinal`就是DLL为导出函数分配的一个对外序号。

示例：

|ordinal|函数名|
|--:|---|
|1|`add`|
|2|`subtract`|
|3|`multiply`|

程序即可以按名称查找，也可以按 ordinal 查找。

有些函数没有导出名称，只能通过 ordinal 查找。

## ordinal 索引

PE 内部会使用一个数组保存函数的地址：

```
函数地址表：

索引 0 → add
索引 1 → subtract
索引 2 → multiply
```

这里的`0、1、2`就是 ordinal 索引，本质上是数组洗