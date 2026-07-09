# 一、winit 定位

## 1、winit 简介

`winit` 是 Rust 生态中最主流的**跨平台窗口创建与事件处理库**。它负责两件事：

- **创建窗口**：在各个平台上弹出一个系统原生窗口。
- **跑事件循环**：持续接收系统发来的事件（键盘、鼠标、窗口缩放、关闭请求等），交给你的代码处理。

它**只负责开窗口和收事件，不负责画图**。把窗口画上像素是 GPU 渲染库（如 `wgpu`、`vulkano`、`glutin`）或即时模式 GUI（如 `egui`）的工作。winit 通过 `raw-window-handle` 把底层窗口句柄"递"给渲染库。

`winit` 是一个跨平台窗口库，每个操作系统平台的窗口系统完全不同，`winit`必须调用操作系统原生的窗口 API。因此，后端就是 `winit` 在某个平台上实际调用的底层系统 API。

各个平台的后端如下表所示：

| 平台      | 后端                   |
| ------- | -------------------- |
| Windows | Win32                |
| macOS   | AppKit               |
| Linux   | X11 / Wayland        |
特别需要注意的是，Linux 上没有唯一的窗口系统。`X11`是老牌显示协议，几乎所有的 Linux 桌面都支持。Wayland 是新一代替代协议，现在发行版（如 Ubuntu较新版本）默认用它。`winit`编译时两个都支持，运行时自动检测该用哪个。

## 2、核心三件套

| 概念                   | 含义                      |
| -------------------- | ----------------------- |
| `EventLoop`          | 事件循环，程序的心脏，不断派发事件       |
| `Window`             | 一个窗口对象                  |
| `ApplicationHandler` | 你实现的 trait，事件循环把事件回调到这里 |

![[winit-core-three.png]]

> winit `0.30` 相比 `0.29` 做了较大重构：旧的 `Event` 大枚举 + 闭包式 `run` 被替换成 `ApplicationHandler` trait + `run_app`，事件按生命周期、窗口、设备等分类回调。两套 API 不兼容。本文基于 `0.30`。

# 二、安装依赖

新建项目：

```shell
cargo new winit-demo
cd winit-demo
```

添加依赖：

```shell
cargo add winit
```

`Cargo.toml` 中大致是：

```toml
[dependencies]
winit = "0.30"
```

> 如果只跑 Linux X11 后端，可以 `cargo add winit --no-default-features --features x11`；如果同时需要把窗口交给 GPU 库渲染，通常还要加 `--features rwh_06`（启用 `raw-window-handle` 0.6 接口）。

# 三、最小示例

先写一个能弹出窗口、点关闭按钮退出的程序：

```rust
use winit::application::ApplicationHandler;
use winit::event::WindowEvent;
use winit::event_loop::{ActiveEventLoop, EventLoop};
use winit::window::{Window, WindowId};

#[derive(Default)]
struct App {
    window: Option<Window>,
}

impl ApplicationHandler for App {
    fn resumed(&mut self, event_loop: &ActiveEventLoop) {
        let attrs = Window::default_attributes().with_title("Hello winit");
        let window = event_loop.create_window(attrs).unwrap();
        self.window = Some(window);
    }

    fn window_event(
        &mut self,
        event_loop: &ActiveEventLoop,
        _window_id: WindowId,
        event: WindowEvent,
    ) {
        if let WindowEvent::CloseRequested = event {
            event_loop.exit();
        }
    }
}

fn main() {
    let event_loop = EventLoop::new().unwrap();
    let mut app = App::default();
    event_loop.run_app(&mut app).unwrap();
}
```

运行：

```shell
cargo run
```

会弹出一个标题为 `Hello winit` 的空窗口；点击窗口的关闭按钮，程序退出。

![[Pasted image 20260708023809.png|500]]

核心关系：

| 写法                                | 作用                            |
| --------------------------------- | ----------------------------- |
| `EventLoop::new()`                | 创建事件循环                        |
| `impl ApplicationHandler for App` | 让 `App` 成为事件回调对象              |
| `event_loop.run_app(&mut app)`    | 启动事件循环，把事件派发给 `App`           |
| `fn resumed`                      | 窗口可创建时回调，通常在此 `create_window` |
| `fn window_event`                 | 窗口收到事件时回调                     |
| `event_loop.exit()`               | 请求退出事件循环                      |

## 1、程序启动顺序

这个例子不是从上到下一次性执行完的程序，而是典型的**事件驱动**程序。真正的执行顺序大致是：

1. `main` 创建 `EventLoop`。
2. `main` 创建一个空的 `App`。
3. `run_app` 启动事件循环，并把 `App` 交给 winit。
4. winit 在合适的生命周期时机调用 `App::resumed`。
5. `resumed` 中创建真正的系统窗口，并保存到 `App.window`。
6. 用户操作窗口时，系统产生 `WindowEvent`。
7. winit 把这些窗口事件派发给 `App::window_event`。
8. 如果收到 `CloseRequested`，调用 `event_loop.exit()` 请求结束事件循环。
9. 事件循环结束后，`run_app` 返回，`main` 结束。

所以，`run_app` 之后程序会进入事件循环，不是立即继续往下跑。窗口程序的大部分逻辑都发生在 winit 回调你的方法时。

## 2、导入的类型

```rust
use winit::application::ApplicationHandler;
use winit::event::WindowEvent;
use winit::event_loop::{ActiveEventLoop, EventLoop};
use winit::window::{Window, WindowId};
```

这几行把示例需要的核心类型引入当前文件：

| 类型 | 作用 |
| --- | --- |
| `ApplicationHandler` | 需要由你的应用状态实现的 trait，winit 通过它回调你的代码 |
| `WindowEvent` | 窗口相关事件枚举，例如关闭、缩放、鼠标、键盘、重绘 |
| `EventLoop` | 事件循环对象，负责接收系统事件并派发回调 |
| `ActiveEventLoop` | 事件循环运行期间传给回调的句柄，可用于创建窗口、退出循环等 |
| `Window` | 一个系统窗口对象 |
| `WindowId` | 窗口 ID，用于区分多个窗口 |

这里同时出现 `EventLoop` 和 `ActiveEventLoop`，容易混淆：`EventLoop` 是你在 `main` 中创建并启动的事件循环本体；`ActiveEventLoop` 是事件循环已经跑起来之后，winit 在回调中临时交给你的操作句柄。

## 3、App 保存应用状态

```rust
#[derive(Default)]
struct App {
    window: Option<Window>,
}
```

`App` 是这个 GUI 程序自己的状态对象。winit 不要求你必须叫它 `App`，这里只是一个常见命名。

`window` 使用 `Option<Window>`，是因为程序一开始还没有窗口。窗口不能在结构体初始化时直接创建，而要等事件循环启动后，在 `resumed` 回调里通过 `ActiveEventLoop` 创建。因此初始状态是 `None`，创建成功后再变成 `Some(window)`。

`#[derive(Default)]` 的作用是让 Rust 自动生成 `App::default()`。由于 `Option<Window>` 的默认值是 `None`，所以这个派生刚好等价于创建一个“还没有窗口”的 `App`。

## 4、实现 ApplicationHandler

```rust
impl ApplicationHandler for App {
    fn resumed(&mut self, event_loop: &ActiveEventLoop) {
        let attrs = Window::default_attributes().with_title("Hello winit");
        let window = event_loop.create_window(attrs).unwrap();
        self.window = Some(window);
    }

    fn window_event(
        &mut self,
        event_loop: &ActiveEventLoop,
        _window_id: WindowId,
        event: WindowEvent,
    ) {
        if let WindowEvent::CloseRequested = event {
            event_loop.exit();
        }
    }
}
```

`ApplicationHandler` 是 winit `0.30` 的核心入口。你不再把一个大闭包传给事件循环，而是实现一个 trait，让 winit 在不同事件发生时调用对应方法。

`resumed` 表示应用进入可运行状态。很多平台要求窗口必须在事件循环启动后创建，所以窗口创建代码通常放在这里：

```rust
let attrs = Window::default_attributes().with_title("Hello winit");
```

这行先构造窗口属性。`Window::default_attributes()` 给出一组默认窗口配置，`with_title("Hello winit")` 在默认配置基础上设置窗口标题。

```rust
let window = event_loop.create_window(attrs).unwrap();
```

这行通过 `ActiveEventLoop` 创建窗口。创建窗口可能失败，所以返回的是 `Result`；示例里用 `unwrap()` 简化处理，真实项目里可以改成更明确的错误处理。

```rust
self.window = Some(window);
```

这行把窗口保存到 `App` 中。这个保存动作很重要：如果不保存 `Window`，窗口对象会在 `resumed` 结束时被丢弃，窗口也就无法作为应用状态继续存在。

`window_event` 负责处理窗口事件。参数里的 `_window_id` 前面带下划线，表示这个示例暂时不用它；如果程序有多个窗口，就可以用 `WindowId` 判断事件来自哪个窗口。

```rust
if let WindowEvent::CloseRequested = event {
    event_loop.exit();
}
```

这段只关心一种事件：用户点击关闭按钮时产生的 `CloseRequested`。收到它以后调用 `event_loop.exit()`，意思是请求事件循环退出。注意它不是直接杀掉进程，而是告诉 winit：事件循环可以结束了。

## 5、main 只负责搭建和启动

```rust
fn main() {
    let event_loop = EventLoop::new().unwrap();
    let mut app = App::default();
    event_loop.run_app(&mut app).unwrap();
}
```

`EventLoop::new()` 创建事件循环。它也可能失败，所以返回 `Result`，示例里继续用 `unwrap()` 简化。

`let mut app = App::default();` 创建应用状态。这里必须是 `mut`，因为 winit 调用 `resumed` 时需要修改 `app.window`，调用其他回调时也可能修改应用状态。

`event_loop.run_app(&mut app)` 启动事件循环。这里传入的是 `&mut app`，表示 winit 在事件循环运行期间可以反复通过可变引用回调并修改这个 `App`。

这一行通常会阻塞很久：只要窗口程序还在运行，事件循环就会持续等待系统事件。只有调用 `event_loop.exit()` 之后，它才会结束并返回。

## 6、最重要的心智模型

- `App` 用 `#[derive(Default)]`，省得手写构造；`window` 用 `Option<Window>` 是因为窗口在 `resumed` 里才创建，初始为 `None`。
- `ApplicationHandler` 中**只有 `resumed` 和 `window_event` 是必须实现**的，其余方法都有默认实现。
- `create_window` 返回 `Result<Window, OsError>`，这里用 `unwrap()` 是示例简化。
- `main` 不是窗口逻辑的主战场，真正的窗口逻辑在 `ApplicationHandler` 的回调里。
- `EventLoop` 像调度器：它等系统事件，然后在合适的时候调用你的 `App`。
- `Window` 是系统窗口对象，通常要保存在 `App` 里，否则创建出来的窗口无法稳定地作为程序状态存在。
- `window_event` 是处理用户输入、窗口关闭、窗口缩放、重绘请求等事件的主要入口。

# 四、窗口的创建与配置

## 1、在 resumed 中创建

窗口创建通常放在`resumed`回调里。对于桌面程序，可以把它理解为事件循环启动后、适合创建窗口的时机；对于 Android、iOS等平台，它还可能对应应用从挂起或缓存状态恢复。

例如在 Android 上，用户按 Home 键把 App 切到后台，系统可能会销毁底层的渲染表面；当用户重新打开 App 时，应用会再次进入恢复状态，`resumed` 可能被重新调用。

由于 `resumed` 可能被调用多次，这里需要做幂等处理：只有 `self.window` 为 `None` 时才创建窗口，避免重复创建多个 `Window`。

```rust
fn resumed(&mut self, event_loop: &ActiveEventLoop) {
    if self.window.is_none() {
        let attrs = Window::default_attributes().with_title("Hello winit");
        self.window = Some(event_loop.create_window(attrs).unwrap());
    }
}
```

需要注意，这里的判断只保证窗口对象不会重复创建；如果程序还持有渲染表面或图形资源，移动端恢复时还需要额外处理这些资源的释放与重建。

```rust
struct App {  
	window: Option<Window>,  
	renderer: Option<Renderer>,  
}

impl ApplicationHandler for App {
	fn resumed(&mut self, event_loop: &ActiveEventLoop) {
	    if self.window.is_none() {
	        let attrs = Window::default_attributes().with_title("Hello winit");
	        self.window = Some(event_loop.create_window(attrs).unwrap());
	    }
	
	    if self.renderer.is_none() {
	        // 基于 window 重新创建 renderer / surface
	    }
	}
	
	fn suspended(&mut self, _event_loop: &ActiveEventLoop) {
	    // Android 上需要释放和 surface 相关的图形资源
	    self.renderer = None;
	}
}
```


## 2、常用窗口属性

`Window::default_attributes()` 返回一个 `WindowAttributes`，通过链式 `with_xxx` 配置：

| 方法                                        | 作用             |
| ----------------------------------------- | -------------- |
| `with_title("...")`                       | 设置窗口标题         |
| `with_inner_size(LogicalSize::new(w, h))` | 设置窗口内部尺寸（逻辑像素） |
| `with_position(Position::Logical(...))`   | 设置窗口位置         |
| `with_visible(bool)`                      | 是否可见           |
| `with_resizable(bool)`                    | 是否允许缩放         |
| `with_maximized(bool)`                    | 是否最大化          |

带尺寸和标题的例子：

```rust
use winit::dpi::LogicalSize;
use winit::window::Window;

fn resumed(&mut self, event_loop: &ActiveEventLoop) {
    if self.window.is_none() {
        let attrs = Window::default_attributes()
            .with_title("Hello winit")
            .with_inner_size(LogicalSize::new(800.0, 600.0));
        self.window = Some(event_loop.create_window(attrs).unwrap());
    }
}
```

> 尺寸单位用 `LogicalSize`（逻辑像素，跟随系统缩放）或 `PhysicalSize`（物理像素）。跨平台建议优先用逻辑像素。

# 五、常用窗口事件

`window_event` 回调收到的 `WindowEvent` 是一个枚举，覆盖与窗口相关的事件。常见变体：

| 事件 | 触发时机 |
| --- | --- |
| `CloseRequested` | 用户点击关闭按钮 |
| `Resized(PhysicalSize)` | 窗口大小改变 |
| `Focused(bool)` | 窗口获得/失去焦点 |
| `CursorMoved { position, .. }` | 鼠标在窗口内移动 |
| `MouseInput { state, button, .. }` | 鼠标按键按下/抬起 |
| `KeyboardInput { event, .. }` | 键盘按键 |
| `RedrawRequested` | 窗口需要重绘 |

先看 `RedrawRequested` 之前这些常见事件。它们都出现在 `window_event` 的 `event: WindowEvent` 参数里，通常用 `match` 分支逐个处理：

```rust
use winit::event::{ElementState, MouseButton, WindowEvent};
use winit::keyboard::{KeyCode, PhysicalKey};

fn window_event(
    &mut self,
    event_loop: &ActiveEventLoop,
    _window_id: WindowId,
    event: WindowEvent,
) {
    match event {
        WindowEvent::CloseRequested => {
            event_loop.exit();
        }
        WindowEvent::Resized(size) => {
            println!("new size: {} x {}", size.width, size.height);
        }
        WindowEvent::Focused(is_focused) => {
            println!("focused: {is_focused}");
        }
        WindowEvent::CursorMoved { position, .. } => {
            println!("cursor: {}, {}", position.x, position.y);
        }
        WindowEvent::MouseInput { state, button, .. } => {
            if button == MouseButton::Left && state == ElementState::Pressed {
                println!("left mouse pressed");
            }
        }
        WindowEvent::KeyboardInput { event, .. } => {
            if event.state == ElementState::Pressed {
                if let PhysicalKey::Code(KeyCode::Escape) = event.physical_key {
                    event_loop.exit();
                }
            }
        }
        _ => {}
    }
}
```

逐个理解：

| 事件 | 典型用途 | 示例里的处理 |
| --- | --- | --- |
| `CloseRequested` | 用户点窗口关闭按钮时触发 | 调用 `event_loop.exit()` 退出程序 |
| `Resized(size)` | 窗口尺寸变化时触发 | 读取 `size.width` 和 `size.height`，实际项目里常用来更新渲染 surface |
| `Focused(is_focused)` | 窗口获得或失去焦点时触发 | `true` 表示窗口获得焦点，`false` 表示失去焦点 |
| `CursorMoved { position, .. }` | 鼠标在窗口内部移动时触发 | 读取鼠标位置 `position.x`、`position.y` |
| `MouseInput { state, button, .. }` | 鼠标按键按下或松开时触发 | 判断左键是否被按下 |
| `KeyboardInput { event, .. }` | 键盘输入时触发 | 判断 `Esc` 是否按下，并用它退出程序 |

其中 `state` 通常是 `ElementState::Pressed` 或 `ElementState::Released`。也就是说，鼠标和键盘事件一般都要同时判断“哪个键”和“按下还是松开”。

`CursorMoved` 和 `MouseInput` 经常配合使用：前者告诉你鼠标在哪里，后者告诉你鼠标按钮发生了什么。例如做拖拽时，通常会在鼠标左键按下时记录状态，在移动时根据当前位置更新对象。

对 `RedrawRequested` 做个说明：当窗口需要重绘（首次显示、从遮挡中露出、手动 `request_redraw`）时，系统会发送这个事件。**渲染代码应该写在这里**，因为这是真正画图的时机。

```rust
fn window_event(
    &mut self,
    event_loop: &ActiveEventLoop,
    _window_id: WindowId,
    event: WindowEvent,
) {
    match event {
        WindowEvent::CloseRequested => event_loop.exit(),
        WindowEvent::Resized(size) => {
            println!("window resized: {size:?}");
        }
        WindowEvent::RedrawRequested => {
            // 这里调用渲染库把画面画到 self.window 上
            // 例：self.window.as_ref().unwrap().request_redraw(); // 持续重绘
        }
        _ => (),
    }
}
```

# 六、键盘输入

## 1、基本处理

`KeyboardInput` 变体携带一个 `KeyEvent`，里面有按键的 `physical_key`（物理键位）、`state`（`Pressed`/`Released`）等信息：

```rust
use winit::event::{ElementState, KeyEvent};
use winit::keyboard::{KeyCode, PhysicalKey};

fn window_event(
    &mut self,
    event_loop: &ActiveEventLoop,
    _window_id: WindowId,
    event: WindowEvent,
) {
    if let WindowEvent::KeyboardInput {
        event: KeyEvent {
            state: ElementState::Pressed,
            physical_key: PhysicalKey::Code(code),
            ..
        },
        ..
    } = event
    {
        if let KeyCode::Escape = code {
            event_loop.exit();
        }
    }
}
```

按 `Esc` 退出程序。

## 2、物理键与逻辑键

| 概念  | 类型               | 含义                                |
| --- | ---------------- | --------------------------------- |
| 物理键 | `PhysicalKey`    | 键盘上的物理位置，与布局无关（如 `KeyCode::KeyW`） |
| 逻辑键 | `Key<Character>` | 经过输入法/布局映射后的字符（如输入"中"）            |

做游戏、快捷键（如 WASD 移动）用物理键；做文本输入用逻辑键，通常配合 `WindowEvent::KeyboardInput` 之外的 `WindowEvent::Ime` 处理中文输入。

# 七、其他生命周期回调

`ApplicationHandler` 还有几个带默认实现的回调，按需覆写：

| 方法 | 触发时机 |
| --- | --- |
| `about_to_wait` | 事件循环即将阻塞等待新事件（适合驱动每帧逻辑） |
| `new_events` | 一批新事件到来时 |
| `suspended` | 应用被挂起（如移动端切到后台） |
| `exiting` | 事件循环即将退出 |
| `device_event` | 设备级事件（如全局鼠标移动） |

最常见的补充是 `about_to_wait`：在桌面端如果你想做"持续动画"，可以在 `about_to_wait` 里调用 `window.request_redraw()`，从而持续触发 `RedrawRequested`：

```rust
fn about_to_wait(&mut self, _event_loop: &ActiveEventLoop) {
    if let Some(window) = &self.window {
        window.request_redraw();
    }
}
```

这样窗口会不断被请求重绘，形成渲染循环。

# 八、与渲染库配合

winit 本身不画图，它只负责创建系统窗口、运行事件循环、接收输入和窗口事件。真正把像素画到窗口里的，是 `wgpu`、`vulkano`、`glutin`、`softbuffer`、`egui` 这类渲染或 GUI 库。两者的关系可以先理解成：

![[assets/winit-window-render-flow.png|500]]

这里最容易混淆的是：**winit 的 `Window` 不是渲染画布本身，而是系统窗口的 Rust 包装对象**。它代表“这个窗口存在”，可以设置标题、查询大小、请求重绘、拿到窗口 ID，也负责在 drop 时关闭窗口。渲染库不会接管这个 `Window`，通常只是通过它拿到底层句柄，然后创建自己的渲染目标。

`raw-window-handle` 就是这中间的“通用身份证”。不同平台的窗口系统完全不同：Windows 有 Win32 窗口句柄，macOS 有 AppKit / Cocoa 对象，Linux 有 X11 / Wayland surface。渲染库如果要跨平台，就不能只认识某一种平台句柄，所以 Rust 生态用 `raw-window-handle` 把这些底层窗口信息包装成统一接口。

`raw-window-handle`（rwh）是一个纯接口 crate，它只定义 trait 和平台句柄类型。`winit`和渲染库都依赖它，但两者没有直接依赖。

![[Pasted image 20260708102632.png]]

注意：`winit` 和 `wgpu` 之间没有箭头。`wgpu` 的代码里根本没有 `winit` 这个依赖，它不知道 `winit` 是什么。它们俩唯一的共同语言是 `rwh` 的 trait。

也就是说：

| 对象                         | 谁创建                 | 谁持有                  | 作用                   |
| -------------------------- | ------------------- | -------------------- | -------------------- |
| `Window`                   | winit               | 通常保存在你的 `App` 里      | 代表系统窗口，处理窗口级操作       |
| raw window/display handle  | winit 从 `Window` 暴露 | 临时借给渲染库使用            | 告诉渲染库底层窗口在哪里         |
| `Surface` / OpenGL context | 渲染库                 | 通常保存在你的 `Renderer` 里 | 表示“可以往这个窗口呈现画面”的渲染目标 |

所以 `Window` 和 `Surface` 不是同一个东西：`Window` 是系统窗口，`Surface` 是渲染库基于它创建的”呈现目标”，`Surface` 依赖窗口存在，要让 `Window` 活得更久。以 `wgpu` 为例，核心一行是 `instance.create_surface(&window)`——`&window` 只是借用，wgpu 通过它读到底层句柄再创建 `Surface`，窗口所有权仍归你的 `App`。

要让 winit 的 `Window` 暴露 `raw-window-handle` 0.6 接口，依赖里通常要打开 `rwh_06` feature：

```toml
winit = { version = "0.30", features = ["rwh_06"] }
```

如果你关闭默认 feature，只启用某个平台后端，也可以写成：

```toml
winit = { version = "0.30", default-features = false, features = ["rwh_06", "x11"] }
```

和渲染库配合后，`window_event` 里的几个事件就会有明确分工：

| winit 信号 | 通常做什么 |
| --- | --- |
| `resumed` | 创建 `Window`，然后用 `&Window` 初始化渲染器 |
| `WindowEvent::Resized(size)` | 窗口大小变了，通知渲染器重新配置 surface 尺寸 |
| `WindowEvent::RedrawRequested` | 现在需要画一帧，调用 `renderer.render()` |
| `window.request_redraw()` | 请求 winit 稍后再发一次 `RedrawRequested` |
| `suspended` | 移动端常用来释放或暂停 surface 相关资源 |

放在代码结构里，以 wgpu 填充关键部分如下：

```rust
use std::sync::Arc;

// wgpu 的核心对象集中存在 Renderer 里
struct Renderer {
    surface: wgpu::Surface<'static>, // Arc<Window> 持有引用 → 'static
    device: wgpu::Device,
    queue: wgpu::Queue,
    config: wgpu::SurfaceConfiguration,
}

impl Renderer {
    fn new(window: Arc<Window>) -> Self {
        // ① Instance：wgpu 入口，决定图形后端（Vulkan / Metal / DX12 / WebGPU）
        let instance = wgpu::Instance::default();

        // ② Surface —— winit ↔ raw-window-handle ↔ wgpu 的关键一行：
        //    wgpu 通过 rwh 的 trait 从 Window 借出底层句柄创建呈现目标。
        //    传 Arc\<Window\> 而非 &Window，让 Surface 拿到 'static 生命周期。
        let surface = instance.create_surface(window).unwrap();

        // ③ Adapter：选一块兼容该 surface 的物理 GPU
        let adapter = pollster::block_on(instance.request_adapter(
            &wgpu::RequestAdapterOptions {
                compatible_surface: Some(&surface),
                ..Default::default()
            },
        ))
        .unwrap();

        // ④ Device + Queue：逻辑设备 + 命令提交队列
        let (device, queue) = pollster::block_on(
            adapter.request_device(&wgpu::DeviceDescriptor { ..Default::default() }),
        )
        .unwrap();

        // ⑤ 配置 surface 格式与尺寸后 configure（具体字段略）
        let config = wgpu::SurfaceConfiguration { /* format/width/height/present_mode ... */ };
        surface.configure(&device, &config);

        Self { surface, device, queue, config }
    }

    fn resize(&mut self, size: PhysicalSize<u32>) {
        self.config.width = size.width;
        self.config.height = size.height;
        self.surface.configure(&self.device, &self.config);
    }

    fn render(&mut self) {
        // 取当前帧纹理 → 编码绘制命令 → 提交 → present（细节略）
    }
}

struct App {
    window: Option<Arc<Window>>, // Arc：让 Surface 拿到 'static，避免 App 自引用
    renderer: Option<Renderer>,
}

impl ApplicationHandler for App {
    fn resumed(&mut self, event_loop: &ActiveEventLoop) {
        if self.window.is_none() {
            let attrs = Window::default_attributes().with_title("Render demo");
            let window = Arc::new(event_loop.create_window(attrs).unwrap());

            // Renderer 通过 Window 创建 surface / device / pipeline。
            // 注意：Window 仍由 App 保存（Arc 共享），Renderer 不独占窗口本身。
            let renderer = Renderer::new(Arc::clone(&window));

            self.window = Some(window);
            self.renderer = Some(renderer);
        }
    }

    fn window_event(
        &mut self,
        event_loop: &ActiveEventLoop,
        _window_id: WindowId,
        event: WindowEvent,
    ) {
        match event {
            WindowEvent::CloseRequested => {
                event_loop.exit();
            }
            WindowEvent::Resized(size) => {
                if let Some(renderer) = &mut self.renderer {
                    renderer.resize(size);
                }
            }
            WindowEvent::RedrawRequested => {
                if let Some(renderer) = &mut self.renderer {
                    renderer.render();
                }
            }
            _ => {}
        }
    }
}
```

这里 `Renderer::new`、`resize`、`render` 都是你自己封装出来的方法名，不是 winit 固定 API：`new` 用窗口 handle 创建 surface 并初始化 GPU 资源，`resize` 重新配置 surface，`render` 编码绘制命令提交到 GPU 呈现一帧。

其中 `Resized` 很关键：窗口大小变了，渲染库的 surface 尺寸必须同步，否则画面拉伸甚至呈现失败。`RedrawRequested` 则是”现在该画一帧”的信号——动画/游戏会在画完一帧后调用 `request_redraw()`，形成”画一帧 → 请求下一帧”的循环：

```rust
WindowEvent::RedrawRequested => {
    renderer.render();
    if let Some(window) = &self.window {
        window.request_redraw();
    }
}
```

静态界面不需要这个循环，只在状态变化时请求重绘即可。

如果直接操作底层图形 API，在真正提交画面前还可以调用：

```rust
window.pre_present_notify();
```

它的作用是通知 winit：马上要把这一帧提交给窗口系统了。某些后端可以借此更好地调度 `RedrawRequested`。

`egui` 也可以放进这个模型里理解。`egui` 负责 UI 逻辑，但它仍然需要 winit 提供窗口和输入事件，也需要某个渲染后端把 UI 画出来：

```text
winit
  负责窗口和输入事件
egui-winit
  把 winit 的鼠标/键盘事件翻译成 egui 输入
egui
  计算 UI 形状和交互结果
egui-wgpu / 其他后端
  把 egui 输出画到 wgpu surface 上
```

所以 `egui` 并不是替代 winit，而是通常站在 winit 和渲染后端之上：winit 决定什么时候该处理事件、什么时候该画，渲染库决定这一帧具体怎么画。
