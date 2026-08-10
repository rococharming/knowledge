

## 任务背景

用户操作 UI 面向 macOS `uipreviewer` 的日常手动操作，目标是在预览窗口底部提供宿主工具栏，方便返回、截图、调整当前设备分辨率和选择应用更新策略。

任务1 BDB Preview Launch 会话编排的目的，是为了方便 Agent 操作，统一使用 bdb preview launch 完成首次启动新窗口运行应用和复用已有窗口完成热更新。例如首次使用`bdb preview launch --app ~/app --device-type foldable`打开一个预览窗口，再次执行`bdb preview launch --app ~/app --device-type phone`尽管是同一构建目录，但其他参数不同，因此会新开一个预览窗口。而后续执行`bdb preview launch --app ~/app --device-type foldable`则会找到已有的窗口并对应用进行热更新。因此任务1依赖任务2的实现。

任务 2 热更新的目的，是在同一 `uipreviewer` 进程内完成 JS 应用热更新，并提供“仅刷新页面”和“重启应用”两个接口。任务 3 的更新策略下拉框最终接入这两个接口。


# 仓库和分支

| 仓库        | 地址                                                 | 分支                     |
| --------- | -------------------------------------------------- | ---------------------- |
| rust-ui   | https://gitblueos.vivo.xyz/BlueOS/System/rust-ui   | fix/windows-msvc-link  |
| tools_bdb | https://gitblueos.vivo.xyz/BlueOS/System/tools_bdb | adapt-rust-uipreviewer |

`rust-ui` 是用户操作 UI 的主实现仓库，主要完成 macOS `uipreviewer` 底部工具栏，以及 Home、Back、截图、当前设备下的物理分辨率选择和应用更新策略选择。物理分辨率变化还需要在同一进程内同步调整 Runtime Size（应用布局、截图和输入坐标使用的逻辑尺寸）、应用画布、Runtime 显示信息和触摸映射。

`tools_bdb` 不作为 用户操作 UI 独立开发的运行依赖，但后续由BDB 启动一个UI预览会话时时，可能需要配合 查询或展示该预览窗口的有效物理分辨率和更新策略。

# 当前已有实现

现有的 `uipreviewer` 已经能加载 `--app <build-directory>`。如果独立启动`uipreviewer`而不走 BDB 控制，它只是一个直接运行的 `uipreviewer` 进程，不会向 BDB 注册预览会话，也没有 Session ID（BDB 用来标识某个预览实例的编号）。

## 两类运行目录

`--session-data-root <absolute-path>` 指定当前预览实例的可写运行数据目录，主要保存应用安装内容、应用数据和数据库、应用信息及文件日志。每个UI预览窗口使用独立可写运行数据目录的目的是为了让不同窗口运行同一构建应用的数据互不干扰。

`UIPREVIEWER_RESOURCE_ROOT` 指向只读的 Runtime Assets 根目录，提供 `quickruntime/gui/js`、字体等框架资源。Cargo debug 生成的可执行文件旁通常没有这套完整资源，因此独立启动时需要显式指定。它只负责“运行时需要加载哪些框架文件”，不应与 `--session-data-root` 混用，也不保存应用业务数据。

`headless` 是隐藏渲染窗口、供自动化控制的模式，只由 BDB 启动并要求 BDB Server 地址和 Session ID；独立开发不使用该模式。

## 可复用代码和设备模型

- `src/preview_config.rs`：启动参数及资源目录解析；
- `src/device_config.rs`：设备类型、物理尺寸、Pixel Factor 和 Runtime Size；
- `src/platform_mac.rs`：macOS 窗口、渲染、输入和截图；
- `src/preview_automation.rs`：BDB 与 Runtime 之间的控制协议。

当前已有五类设备预设：

|设备|默认物理尺寸|Pixel Factor|Runtime Size|
|---|---|---|---|
|watch-round|466×466|1|466×466|
|watch-square|390×450|1|390×450|
|phone|1290×2796|3|430×932|
|foldable|2200×2480|3.25|677×763|
|camera|318×564|3|106×188|

物理尺寸是设备硬件像素；Pixel Factor 用于换算 Runtime Size，应用布局和截图使用 Runtime Size。`std_local` 已接收换算后的尺寸，框架内 DPR 固定为 1，不能再次设置 3 或 3.25 造成重复缩放。

现有 macOS 基础包括 OpenGL 预览窗口、窗口和画布缩放、鼠标到 Runtime 坐标的映射、键值注入、画布截图读回，以及 foldable 的同进程设备配置更新。`preview.ready`、`preview.route`、`preview.screenshot`、`preview.fold` 和 `preview.stop` 已有对应协议入口。

# 用户操作 UI 要做什么

底部工具栏预期规划为五项：Home、Back、Screenshot、Physical Resolution 和 Update Strategy。

宿主 UI 是 `uipreviewer` 管理的 macOS 原生区域；应用画布才是实际渲染、接收触摸和被截图的区域。工具栏不能改变应用的 Runtime Size、截图尺寸或 BDB 自动化坐标，也不能成为 `headless` 的启动前提。建议增加一个小型进程内 Preview 操作层，让工具栏只表达操作意图，平台代码负责执行。

### Home 和 Back

Back 先交给应用或页面处理；未处理时返回上一层；根页不退出 Preview。现有共享 `RouterUtils::back` 在部分应用根页会触发 finish，因此需要增加仅对桌面 Preview 生效的导航边界，不能直接改变真实设备共用语义。

Home 返回当前应用页面栈根页，不切换到 BlueOS Launcher、不重读 `manifest.json`、不重启应用。需要用至少包含两页的真实应用验证页面栈行为。

### Screenshot

复用现有画布捕获能力，提供两个入口：工具栏弹出 macOS Save 对话框并默认保存到 Downloads；BDB 继续使用调用方给出的绝对路径，不弹对话框。两者都只输出 Runtime Size 的应用画布 PNG，取消保存时不创建文件。

### Physical Resolution

设备类型由启动时的 `--device-type` 决定，工具栏不切换设备，只展示当前设备已确认的固定分辨率预设。跨设备预览需要通过`bdb preview launch`指定`--device-type`重新启动另一个UI窗口。

切换当前设备的物理分辨率时，保持进程、窗口、运行数据目录和当前更新策略不变，同时更新 Runtime 显示信息、Runtime Size、画布、窗口比例和触摸映射。随后通过一次性 Restart App 让应用重新读取屏幕信息并回到 `manifest.json` 入口页；这一接入点依赖任务 2。窗口拖动只改变桌面显示比例，不改变设备配置。

### Update Strategy

参考 BlueOS Studio，下拉框保留两种策略：

|UI 文案|内部值|下一次应用更新后的行为|
|---|---|---|
|仅刷新页面|`refresh-page`|重建应用后恢复仍有效的导航路径|
|重启应用|`restart-app`|重建应用后停留在 `manifest.json` 入口页|

每个预览实例默认使用“仅刷新页面”。切换选项只修改当前实例的 Effective Settings，不立即触发更新；不同实例的选择互不影响。两种策略都会重新读取应用产物、重建 JS 内存，并保留进程、窗口和运行数据。正式接口接入前，可用测试替身验证下拉框；生产路径的最终状态应由 Runtime 保存。

# 后续接口边界

1. 任务 2 提供 Restart App：保留 Runtime 进程、窗口和持久化数据，重建应用内存并在入口页首帧完成后返回；
2. 任务 2 提供 Effective Settings：读取和设置 `refresh-page` 或 `restart-app`，设置本身不触发更新；
3. 任务 1 通过 Runtime 协议同步 BDB 需要展示的当前分辨率和更新策略，不改变原始启动参数或 BDB 会话身份。

任务 3 的工具栏外壳可先独立开发；Physical Resolution 的完整切换和 Update Strategy 的生产接入，待上述接口具备后再完成跨模块验收。

# 开发和验收

独立开发可直接启动一个不连接 BDB 的可见预览窗口：

```bash
cd /Users/11185032/work/rust-ui
cargo build --bin uipreviewer

UIPREVIEWER_RESOURCE_ROOT=/Users/11185032/work/rust-ui/crates/ui_previewer \
  /Users/11185032/work/rust-ui/target/debug/uipreviewer \
  --app /absolute/path/to/app/build/foldable \
  --device-type foldable \
  --session-data-root /tmp/uipreviewer-task3-foldable
```

`--app` 应指向包含 `manifest.json` 的已构建应用目录。

复用 `--session-data-root` 可验证持久化数据，使用新路径可得到干净实例或同时运行多个实例

`UIPREVIEWER_RESOURCE_ROOT` 只提供只读框架资源。独立启动不需要 BDB 环境变量或参数。

建议验收顺序：先验证工具栏和独立启动，再验证 Home/Back、截图、当前设备分辨率重配置，最后接入两种更新策略及任务 2 接口；BDB 状态查询放到任务 1 的跨仓集成阶段验证。
