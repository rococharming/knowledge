
> rust-ui 基线：`feat/hot-restart-app-reload`
> bdb 基线：`adapt-rust-uipreviewer`

# 1、BDB 现在如何控制 Previewer

`bdb preview` 用于在本机启动和控制 `uipreviewer`。BDB 负责启动进程、管理会话和转发命令；Previewer 负责读取应用、启动 PMS/AMS、渲染页面并执行命令。

```text
bdb preview 命令
  → BDB Server（本机 127.0.0.1:9900）
  → 启动 uipreviewer，并传入 --app、设备参数、Session Root
  → uipreviewer 通过 WebSocket 连接回 BDB
  → preview.ready 后，BDB 才转发 route/screenshot/fold/stop/update
```

`--app` 必须是直接包含 `manifest.json` 的应用目录，支持 JS 应用和 Rust Native 应用。Previewer 从 manifest 中读取包名和应用类型，统一走 PMS/AMS 启动。

## 启动会话

```shell
bdb preview launch \
  --app <APP_DIR> \
  --device-type <TYPE> \
  [--headless] \
  [--width <WIDTH> --height <HEIGHT>]
```

| 参数                     | 说明                          |
| ---------------------- | --------------------------- |
| `--app <APP_DIR>`      | 必填。目录根下必须有 `manifest.json`。 |
| `--device-type <TYPE>` | 必填。指定预览设备类型。                |
| `--headless`           | 不显示窗口，但仍会渲染，供自动化使用。         |
| `--width` / `--height` | 可选物理像素尺寸，必须同时提供。            |

首次 launch 成功时 BDB 返回类似 `preview-1` 的会话 ID；后续操作都应使用该 ID。

注意：不传--width，--height时对于指定设备有默认分辨率：

|设备类型|默认物理分辨率|
|---|---|
|`watch-round`|`466x466`|
|`watch-square`|`390x450`|
|`phone`|`1290x2796`|
|`foldable`|`2200x2480`|
|`camera`|`318x564`|

只传 `--device-type` 时使用上表默认值。物理尺寸会在 Previewer 内按 DPR 转成 Runtime Size；截图是 Runtime Size，不是 Host Window 的尺寸。


## 控制已启动会话

```shell
# JS 页面路由；路径必须以 / 开头，query 不加 ?。
bdb preview route --id preview-1 /pages/DemoDetail --mode push --query 'id=1'

# 保存最近一次已渲染画面；没有首帧会失败。
bdb preview screenshot --id preview-1 /tmp/demo.png

# 切换折叠屏展开和折叠状态，仅支持 --device-type 为 foldable 可用。
bdb preview fold --id preview-1 --state folded

# 只停止指定会话。
bdb preview stop --id preview-1
```

当前能力按应用类型不同：

| 应用 | 当前 BDB 能力 |
| --- | --- |
| JS | route、screenshot、stop；foldable 另有 fold |
| Rust Native | screenshot、stop、update

Native 目前不支持 BDB route；不要对 Native 会话发送 route。`route` / `screenshot` / `fold` / `stop` 必须显式传 launch 返回的 `preview-N`。


## Native 热更新怎样触发

BDB 没有 `bdb preview update` 子命令，这样设计的目的是为了方便 Agent 在应用重新构建好之后，执行和启动时同样的launch参数命令直接对已有窗口进行热更新。对同一个应用路径、device type、宽高和 headless 状态重复执行 `launch`，BDB 会复用该会话并发送 `preview.update`。

例如`bdb preview launch --app xxx --device-type camera`首次启动了应用，后续应用重新构建后，仍通过`bdb preview launch --app xxx --device-type camera`在同一窗口进行热更新。

注意：当前热更新只支持 Rust Native 应用且只支持 `restart-app`热更新策略，成功时 Previewer 的 PID、窗口、Session ID 和 Session Data Root 不变，但应用 dylib 和应用内存已经替换。JS 应用热更新需要后续实现。

# 2、 Rust Native 热更新的开发操作

开发时让 BDB 使用当前 rust-ui 编出的 Previewer：

```shell
export BDB_PREVIEW_COMMAND=/Users/11185032/work/rust-ui/target/debug/uipreviewer
```

>正式安装的 BDB 从自身同级 `preview-runtime/uipreviewer` 使用随包发布的 Previewer；开发时可通过 `BDB_PREVIEW_COMMAND` 覆盖为本地编译产物。

改了这个环境变量后要重启 BDB Server。这个变量只指定二进制位置，BDB 不会自动编译 rust-ui。

## JS 应用的运行时资源

JS Preview 还依赖 Previewer 可执行文件旁的 `quickruntime/gui/js`。资源源文件已在仓库的 `crates/ui_previewer/quickruntime/gui/js/`；新 clone 或清理 `target/` 后，开发者需同步到 debug 输出目录：

```bash
cd /Users/11185032/work/rust-ui
rsync -a \
  crates/ui_previewer/quickruntime/gui/js/ \
  target/debug/quickruntime/gui/js/
```

## 首次完整构建

macOS 上需要执行一步：

```shell
# 1. 安装依赖（自动下载 NDK + jax 构建工具）  
pnpm install  
  
# 2. 构建并运行 hello 示例  
cargo run --bin run -- examples/hello
```

但 Windows 上的 JAX Windows local-ABI 有些问题，因此没有用 jax 构建应用，而是临时采用裸 rustc 
构建 app.dll，所以只需要：

```shell
cargo run --bin run -- examples/hello
```

这不是只打开 hello。`run` 会：

1. 编译 `uipreviewer` 和 `libsystem_framework.dylib`。
2. 将完整 runtime bundle 复制到 `examples/hello/src/libs/local/`。
3. 用 `jax buildndk` 编译 hello，生成 `dist/libs/local/libapp.dylib`。
4. 将 manifest 和 dylib 部署到：
```text
target/debug/system/app/com.application.hello/
├── manifest.json
└── libs/aarch64-apple-darwin/libapp.dylib
```


关闭首次打开的窗口后，该目录`target/debug/system/app/com.application.hello/` 就是 BDB launch 要传的 `--app`。

>Windows 上为解决 MSVC Link 导出表符号超限问题，对system_framework.dll进行了分层串联。Windows 下保留 system_framework.dll 作为唯一入口，下面按依赖链拆成多个 sf_*.dll，预览器和 App 仍只依赖同一个 system_framework


## 只重编 app 并更新 dylib

macOS：

```shell
cd /Users/11185032/work/rust-ui/crates/ui_previewer/examples/hello

JAX_ABI=local /Users/11185032/work/rust-ui/node_modules/.bin/jax buildndk --clean-only

JAX_ABI=local \
JAX_USE_SYSTEM_RUST=1 \
RUSTFLAGS='-L dependency=/Users/11185032/work/rust-ui/target/debug/deps --cfg feature="std_local"' \
/Users/11185032/work/rust-ui/node_modules/.bin/jax buildndk

cp dist/libs/local/libapp.dylib \
  /Users/11185032/work/rust-ui/target/debug/system/app/com.application.hello/libs/aarch64-apple-darwin/libapp.dylib
```

Windows 与 macOS/Linux 的构建流程要彻底分开  
“`run` 会用 jax buildndk 编译 hello、产出 `libapp.dylib`”只适用于 macOS/Linux。Windows 当前由 runner 直接调用 `rustc` 编译 `app.dll`，不调用 jax；部署路径也是 `libs/<host-triple>/app.dll`。

# 3、当前已完成的 Rust Native 实现

- `--app` 读取 manifest，区分 JS 和 Native；二者都通过 PMS/AMS 启动。
- Native 首次启动和更新都会在 BDB Session Root 内生成独立 dylib 副本，避免动态库缓存到旧 image。
- 更新时先销毁旧 Native 生命周期和 entry route，再加载新 dylib，从新的 manifest entry 启动。
- 旧 dylib handle 会保留到旧 runtime 退出后，不会过早 `dlclose`。
- Runtime 在新 generation 的目标帧后才回复 BDB update 成功。

现有 Native 更新语义是 **`restart-app`**：只启动新的 entry page，不恢复旧页面栈。



# 4、后续工作

### A. Windows 上的 BDB 控制 Previewer

Windows 当前已有 Native AMS/PMS 启动和分层 DLL runner，但没有 BDB 自动化适配：`platform_windows.rs` 仍是旧 `--native` 启动方式，没有 `--app`、WebSocket、ready、screenshot、route、fold、stop 或 update。

目标是让 Windows Previewer 和 macOS 一样接收 BDB 的 launch 参数并上报 capability。建议顺序：

1. Windows 接入统一 `PreviewConfig` 和 WebSocket automation，先完成 ready、screenshot、stop。
2. 完成 JS 的 route、fold 和 headless。
3. 接入 Native update，处理 Windows `.dll` staging、文件锁和加载器缓存。
4. 以 BDB 实测五类设备、截图、路由、fold、stop、headless、重复 launch update；不能只做 Windows 编译检查。

### B. Rust `refresh-page`

当前 Rust 只有 `restart-app`。还需要支持`refresh-page` ，
可参考 BlueOS Studio 的内置模拟器两种热更新策略行为。

但当前 Rust Native 应用还不支持页面栈能力，需要确定一下是否依赖该前置条件才能实现

### C. JS 热更新

当前 JS 只支持 BDB route/screenshot/stop/fold，不支持 update。JS 热更新不能复用 Native 的 `dlopen` 逻辑：它需要退休 QuickJS runtime、JS page/component、timer、callback 和旧 generation 的异步渲染工作，再加载新的 manifest、JS 和 template。

可以复用 BDB transport、Session Root、capability、单飞 update 和“目标帧后回复”的规则；Native handle / dylib staging 不能复用。
