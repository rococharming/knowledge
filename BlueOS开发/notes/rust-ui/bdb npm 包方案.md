
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

| 序号  | 任务                      | 主要工作                                                                                                                        | 预估工作量        |
| --- | ----------------------- | --------------------------------------------------------------------------------------------------------------------------- | ------------ |
| 1   | BDB Preview Launch 会话编排 | LaunchKey 匹配；自动生成 SessionId；`--new-instance`；批量热更新；`preview list`；`--session-id`；更新策略命令；跨 Session 并行、单 Session 串行；结果汇总与固定超时 | **3～4 人天**   |
| 2   | rust-ui JS 应用热更新内核      | 重新读取 `--app` 构建产物；仅刷新页面；重启应用；路由与参数恢复；无效路由回入口页；保留持久化数据；`update_id`；新版本首帧 ready；失败诊断与 E2E                                     | **3～4 人天**   |
| 3   | 用户操作 UI 层               | 底部工具栏；返回首页；返回上一页；截图及系统保存对话框；切换设备；物理分辨率预设；同窗口动态调整尺寸、DPR、画布和触摸映射；Session 更新策略选择                                               | **4～5 人天**   |
| 4   | Runtime Diagnostics     | frontend 稳定诊断日志；`page_show_settled`；BDB 增量日志监测；结构化 JS 诊断；source map 映射 `.ux`；launch/route 错误门禁；                             | **6～7 人天**   |
|     | **合计**                  |                                                                                                                             | **16～20 人天** |