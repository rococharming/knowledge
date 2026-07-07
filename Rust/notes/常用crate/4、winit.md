# 一、winit 定位

## 1、winit 简介

`winit` 是 Rust 生态中最主流的**跨平台窗口创建与事件处理库**。它负责两件事：

- **创建窗口**：在各个平台上弹出一个系统原生窗口。
- **跑事件循环**：持续接收系统发来的事件（键盘、鼠标、窗口缩放、关闭请求等），交给你的代码处理。

它**只负责开窗口和收事件，不负责画图**。把窗口画上像素是 GPU 渲染库（如 `wgpu`、`vulkano`、`glutin`）或即时模式 GUI（如 `egui`）的工作。winit 通过 `raw-window-handle` 把底层窗口句柄"递"给渲染库。

| 平台      | 后端                   |
| ------- | -------------------- |
| Windows | Win32                |
| macOS   | AppKit               |
| Linux   | X11 / Wayland        |


`winit` 在生态中是很多图形/GUI 框架的**底座**，可以理解成"Rust 版的 GLFW/SDL 窗口部分"。

## 2、核心三件套

| 概念                   | 含义                      |
| -------------------- | ----------------------- |
| `EventLoop`          | 事件循环，程序的心脏，不断派发事件       |
| `Window`             | 一个窗口对象                  |
| `ApplicationHandler` | 你实现的 trait，事件循环把事件回调到这里 |

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

![[Pasted image 20260630160322.png|600]]

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

核心关系：

| 写法 | 作用 |
| --- | --- |
| `EventLoop::new()` | 创建事件循环 |
| `impl ApplicationHandler for App` | 让 `App` 成为事件回调对象 |
| `event_loop.run_app(&mut app)` | 启动事件循环，把事件派发给 `App` |
| `fn resumed` | 窗口可创建时回调，通常在此 `create_window` |
| `fn window_event` | 窗口收到事件时回调 |
| `event_loop.exit()` | 请求退出事件循环 |

几个关键点：

- `App` 用 `#[derive(Default)]`，省得手写构造；`window` 用 `Option<Window>` 是因为窗口在 `resumed` 里才创建，初始为 `None`。
- `ApplicationHandler` 中**只有 `resumed` 和 `window_event` 是必须实现**的，其余方法都有默认实现。
- `create_window` 返回 `Result<Window, OsError>`，这里用 `unwrap()` 是示例简化。

# 四、窗口的创建与配置

## 1、在 resumed 中创建

窗口创建必须发生在事件循环启动之后，因此放在 `resumed` 回调里。`resumed` 会在应用启动、以及从挂起状态恢复时被调用，所以这里要做"幂等"处理：只在还没有窗口时才创建。

```rust
fn resumed(&mut self, event_loop: &ActiveEventLoop) {
    if self.window.is_none() {
        let attrs = Window::default_attributes().with_title("Hello winit");
        self.window = Some(event_loop.create_window(attrs).unwrap());
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

| 概念 | 类型 | 含义 |
| --- | --- | --- |
| 物理键 | `PhysicalKey` | 键盘上的物理位置，与布局无关（如 `KeyCode::KeyW`） |
| 逻辑键 | `Key<Character>` | 经过输入法/布局映射后的字符（如输入"中"） |

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

winit 本身不画图。典型搭配是：

```text
winit（开窗口 + 收事件）
        ↓ 通过 raw-window-handle 交出窗口句柄
渲染库（wgpu / vulkano / glutin / egui）
        ↓ 把画面画到窗口上
```

要让 winit 实现 `raw-window-handle` 0.6 接口，依赖里要带 `rwh_06` feature：

```toml
winit = { version = "0.30", default-features = false, features = ["rwh_06", "x11"] }
```

随后 `Window` 就能作为 `HasWindowHandle` 交给渲染库使用。具体的渲染集成属于 `wgpu` 等库的范畴，超出 winit 入门范围。

# 九、常见使用模式

一个"持续重绘 + Esc 退出"的最小骨架，可以直接作为后续接入渲染库的起点：

```rust
use winit::application::ApplicationHandler;
use winit::event::{ElementState, KeyEvent, WindowEvent};
use winit::event_loop::{ActiveEventLoop, EventLoop};
use winit::keyboard::{KeyCode, PhysicalKey};
use winit::window::{Window, WindowId};

struct App {
    window: Option<Window>,
}

impl App {
    fn new() -> Self {
        Self { window: None }
    }
}

impl ApplicationHandler for App {
    fn resumed(&mut self, event_loop: &ActiveEventLoop) {
        if self.window.is_none() {
            let attrs = Window::default_attributes().with_title("winit demo");
            self.window = Some(event_loop.create_window(attrs).unwrap());
        }
    }

    fn window_event(
        &mut self,
        event_loop: &ActiveEventLoop,
        _window_id: WindowId,
        event: WindowEvent,
    ) {
        match event {
            WindowEvent::CloseRequested => event_loop.exit(),
            WindowEvent::KeyboardInput {
                event:
                    KeyEvent {
                        state: ElementState::Pressed,
                        physical_key: PhysicalKey::Code(KeyCode::Escape),
                        ..
                    },
                ..
            } => event_loop.exit(),
            WindowEvent::RedrawRequested => {
                // 渲染逻辑写在这里
                // 画完一帧后，若需要持续动画，在 about_to_wait 中 request_redraw
            }
            _ => (),
        }
    }

    fn about_to_wait(&mut self, _event_loop: &ActiveEventLoop) {
        if let Some(window) = &self.window {
            window.request_redraw();
        }
    }
}

fn main() {
    let event_loop = EventLoop::new().unwrap();
    let mut app = App::new();
    event_loop.run_app(&mut app).unwrap();
}
```

要点回顾：

- 事件循环通过 `EventLoop::new()` 创建，`run_app` 启动，事件回调进 `ApplicationHandler`。
- 窗口在 `resumed` 里 `create_window`，用 `Option` 持有。
- 退出用 `event_loop.exit()`，可由 `CloseRequested` 或按键触发。
- 渲染写在 `RedrawRequested`，持续动画靠 `about_to_wait` 里 `request_redraw`。
- 真正画图交给渲染库，winit 只通过 `rwh_06` 交出窗口句柄。
