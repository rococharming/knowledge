
```shell
cargo run --bin uipreviewer-mac
```

默认启动的是内置 launcher：`com.blueos.launcher`。整个过程不是 main 函数直接读取 JS然后画窗口，而是现在桌面进程中模拟出 BlueOS 的 PMS、AMS、IMS和应用进程生命周期，再由 AMS 驱动 UI/JS 线程加载 launcher，最后将 BlueOS 渲染树接到 macOS 的 OpenGL 窗口上。

![[assets/Pasted image 20260725143418.png]]

不带 `--app`：

```shell
cargo run --bin uipreviewer-mac
```

流程：

```
Cargo 编译并启动 previewer
    ↓
previewer 准备本地运行环境和窗口
    ↓
启动内置的 Launcher
    ↓
显示 Launcher 页面
```

## 带 `--app <path>`

```
cargo run --bin uipreviewer-mac -- --app /path/to/app
```

流程：

```
Cargo 编译并启动 previewer
    ↓
previewer 准备本地运行环境和窗口
    ↓
识别你指定的应用目录
    ↓
直接启动这个应用
```

也就是：**不进入默认 Launcher，直接预览你的快应用项目。**


## 带 `--native`

```
cargo run --bin uipreviewer-mac -- --native
```

`--native` 的目标又不同：它不是启动一个快应用目录，而是加载一个已经编译好的 **原生动态库应用**（native demo）。

流程：

```
Cargo 编译并启动 previewer
    ↓
previewer 准备窗口和本地 UI 环境
    ↓
加载原生动态库中的应用
    ↓
显示这个原生应用
```