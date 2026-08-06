
## 整体方案

uipreviewer 定义为 BDB 的私有 UI Preview Runtime，而不是独立安装和使用的命令。用户只安装`@blueos/bdb`，UI预览功能使用`bdb preview`。`BDB_PREVIEW_COMMAND` 仅保留给源码开发和测试选择本机uipreviewer二进制。


## 单包 -> 入口包 + 平台载荷包

```text
@blueos/bdb
├── @blueos/bdb-darwin-arm64
├── @blueos/bdb-darwin-x64
├── @blueos/bdb-linux-x64
└── @blueos/bdb-win32-x64
```

设计如下：

- `@blueos/bdb`：只包含公共 `bdb` 命令入口和文档。
- macOS 载荷：包含对应架构的 BDB，以及完整 UI Preview Runtime Bundle。
- Windows/Linux 载荷：现阶段只包含 BDB；执行 `bdb preview` 时明确提示尚不支持。
- 入口包通过精确版本的 `optionalDependencies` 引用所有载荷。
- 每个载荷用 `os`、`cpu` 限定平台，npm 只安装当前平台匹配的载荷。这是 npm 官方支持的机制。

```json
{
  "optionalDependencies": {
    "@blueos/bdb-darwin-arm64": "2.0.0",
    "@blueos/bdb-darwin-x64": "2.0.0",
    "@blueos/bdb-linux-x64": "2.0.0",
    "@blueos/bdb-win32-x64": "2.0.0"
  }
}
```

> 选择 `optionalDependencies` 有一个必须接受的代价：用户可以使用 --omit=optional 跳过所有 `optionalDependencies`，不把它们实际安装到 `node_modules` 中，因此，载荷安装失败也不会让根包安装失败，所以 bdb 启动器必须检测缺失载荷并给出准确错误。
> 



