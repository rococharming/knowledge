
>`tools_uipreview` 是 vivo BlueOS 快应用框架的桌面端 UI 模拟器。使用纯 Rust 在 Windows 平台把整套 BlueOS 应用运行时（PMS / AMS / IMS 三大系统服务 + 应用生命周期 + Skia 渲染 + 输入事件）“单进程模拟”跑起来，让快应用（RPK包）无需真机即可在 PC 上预览。

# 一、整体功能

BlueOS（vivo的手表/折叠屏等设备的操作系统）的快应用使用 RPK 包格式、JS 框架、自有 UI 渲染栈（sglui/Skia）。在设备上调试 UI 成本高 、迭代慢。本项目把 BlueOS 应用框架的核心部分 “搬” 到 主机桌面，让开发者直接 `cargo run` 拉起一个窗口预览快应用效果。

# 二、核心能力

| 能力       | 实现方式                                                                   |
| -------- | ---------------------------------------------------------------------- |
| 快应用加载与运行 | 启动内置 launcher，AMS 调度应用生命周期，UI Thread Manager 执行 JS/DOM/渲染              |
| 触摸交互     | 鼠标/触屏事件经 IMS 注入，坐标缩放到 layout 分辨率                                       |
| 按键交互     | Backspace→Back、Home→Home，500ms 按键重复                                    |
| 折叠屏模拟    | F1 切换开合盖（2200×2480 <-> 1172×2748），双通道通知（Hall 传感器 + DisplayInfoChanged） |
| 系统服务     | PMS（包管理）、AMS（应用管理）、IMS（输入管理）本地桩实现                                      |
| 渲染       | sglui（Skia）+ glutin（EGL）、winit 窗口                                      |
| 字体       | 31 个字体文件（vivo/Hanyi/Roboto/Emoji/表盘字体）                                 |


# 三、项目定位和边界

## 1、monorepo 子项目

本项目不是自包含的——`Cargo.toml`通过`path = "../../system/core"` 引用了约 15 个外部`crate`（ui_frontend、pkgmgr、appmgr、ui、feature、graphic/sglui 等）。这些属于 BlueOS 主仓库。

## 2、Cargo.toml

是本项目最特别的地方：Cargo.toml 里有 170+ 行注释，把整个 BlueOS app_fwk 的依赖分层、Windows 编译策略、暂未启用的模块都写清楚了。它本身就是一个高质量的架构说明文档



# 四、系统架构

## 1、分层总览

![[Pasted image 20260626153726.png|400]]


## 2、入口层

| 入口                | 状态                                                                                       |
| ----------------- | ---------------------------------------------------------------------------------------- |
| `main_windows.rs` | 完整可用：窗口创建、GL 上下文、渲染注册、输入注入、折叠屏、按键重复、日志配置                                                 |
| `main_mac.rs`     | 骨架：只启动服务 + `UIThreadManager::loop_run()`，无窗口、渲染、输入；注释 TODO：`integrate with Cocoa/AppKit` |
| `main_linux.rs`   | 骨架：同上；注释 TODO：`integrate with xcb/wayland`                                               |
三者共享：服务启动序列、register_ready_callbacks、init_app、set_app_thread_factory、SimAppThread 工厂。差异只在"窗口系统 + 渲染表面 + 事件循环"这一层——这正是平台适配的工作量所在。

## 3、服务层

aidl_stub 是本项目的灵魂。 BlueOS 用 binder + AIDL 做跨进程 IPC，桌面环境没有 binder  驱动。aidl_stub crate 用纯 Rust 把整套 AIDL / binder 机制降级为同进程函数调用：

```
AIDL interface     →  Rust trait (Send + Sync)
AIDL parcelable    →  Rust struct
binder::Strong<T>  →  Arc<T>
binder::Result<T>  →  Result<T, Box<dyn Error>>
binder::get_interface →  ServiceLocator::get
binder::add_service   →  ServiceLocator::register
```

aidl_stub 定义了 BlueOS 三大系统服务的 AIDL 接口对应的 trait：

- IQrAppManager（AMS）：~50 方法，含 startApp/attachProcess/notifyCreated/updateSettings 等完整生命周期。当前用 DefaultAms 占位，真实实现来自外部 app_manager crate。
- IQrPackageManager（PMS）：install/uninstall/queryAppInfo/getInstallApp 等。真实实现来自外部 package_manager crate。
- IQrInputManager（IMS）：registerInputListener/injectInputEvent/setFocusWindow + Hall 传感器监听。ImsStubService 是本项目自己实现的（313 行，最完整），承担输入事件分发枢纽。

辅助 trait：IQrAppThread（应用线程回调，含 create/running/stop/destroy 等 16 方法）、IQrReadyCallBack（系统就绪回调）、IQrInputCallBack/IQrInputHallStateCallBack（输入回调）。

## 4、应用线程模拟器

BlueOS 真机上每个快应用跑在独立子进程，AMS 通过 binder 调用子进程的 IQrAppThread。桌面模拟器不可能也不需要真起子进程，于是用 SimAppThread 在同进程内模拟：

AMS 启动应用 → create_app_thread(pid, pkg)
            → 工厂回调返回 SimAppThread
            → ams.attachProcess(SimAppThread, pid, LaunchInfo)
AMS 生命周期回调 → SimAppThread::notifyCreate/Running/Stop/Destroy
              → 委托 UIThreadManager::on_create/on_running/...

SimAppThread 全部 16 个方法都是"转发器"，把 AIDL LaunchInfo 转成内部 StartInfo（convert_launch_info，处理 URI/params/data/language/screen 等字段），再交给 UIThreadManager。这与真机上 app_thread_binder.rs 的 IQrAppThreadBinder 委托 UIThreadManager 的路径完全一致——模拟器刻意保持与 native 路径同构。

工厂模式为何必要？ 因为 appmgr crate 不能依赖 UIThreadManager（那是 qr_ui_rs 里的，依赖方向反过来），所以 aidl_stub 提供 set_app_thread_factory，让主程序注册一个能访问 UIThreadManager 的工厂，appmgr 通过 create_app_thread 回调拿到实现。这是典型的"依赖反转 + 工厂"解耦。


## 5、启动流程

以 main_windows.rs 的 main 函数 为例：

1. 日志初始化（默认 stdout，UIPREVIEWER_LOG_TO_FILE=1 写 full_log.txt）
2. 环境初始化：
	- 定位 data_root（exe 同级 data/ 或 exe 目录）
	- package_manager::Env::init
	- Environment 配置 10+ 路径（intrpk/prerpk/rpk/js/fonts/appinfo/permission...）
	- launcher 包名 = "com.blueos.launcher"，字体族 = "Hanyi-vivo"
3. 启动三大服务：start_package_manager_service / start_app_manager_service / start_input_manager_service
4. set_app_thread_factory（注册 SimAppThread 工厂）
5. register_ready_callbacks（向 AMS/PMS 注册就绪回调）
6. init_app（给 UIThreadManager/AppWindowManager/RenderOpManager/LanguageUtils 注入 Context，初始化字体集合）
7. UIThreadManager::get_instance().run()  ← 独立线程跑 UI 运行时
8. 主线程跑 winit EventLoop（窗口系统必须在主线程）

系统就绪握手：AmsPmsReadyCallback::onReady 收到 AMS(0)/PMS(1) 两个就绪信号后，两者都 ready 才 start_launcher() 启动桌面应用。AMS ready 时还会立刻 updateSettings 推送初始显示分辨率（2200×2480）。

## 6、渲染管线

![[Pasted image 20260626155344.png|500]]

两套坐标缩放（关键设计，避免缩放混乱）：
- scale_x/scale_y = layout / window：触摸输入用，把窗口坐标放大到 layout 坐标（2200×2480 体系）
- render_scale_x/y = min(win/layout, win/layout) 统一值：渲染用，保持纵横比，选较小值确保内容完整 fit

窗口尺寸按 layout 纵横比（2200:2480≈0.887）取屏幕高度 80% 反推宽度，并禁用 resize。