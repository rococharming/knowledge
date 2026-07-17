---
title: Rust UI 预览架构
date: 2026-07-09
tags: [BlueOS, Rust]
aliases:
  - Rust UI 预览架构
  - RustUI预览架构
---

# 一、基础知识

## 1、应用与 PMS/AMS/IMS

PMS/AMS/IMS 这三个系统服务各司其职。

服务：PMS
全称：Package Manager Service 包管理服务
管什么：装了哪些应用——解析 rpk 包、维护已安装应用清单、查询应用信息（包名、图标、入口等）

---

服务：AMS
全称：App Manager Service 应用管理服务
管什么：应用怎么跑——启动/切换/销毁应用进程、管理应用生命周期（创建、前台、后台、结束）

---

服务：IMS
全称：Input Manager Service 输入管理服务
管什么：用户操作发给谁——收集触摸/按键事件，分发给当前焦点窗口

应用和它们的关系：

- 应用不知道自己装在哪、怎么启动自己，这些是 PMS / AMS 的职责。一个快应用想跑起来，得先有人把它从 rpk 解析成可执行单元，再分配进程让它运行。这件事应用自己做不了，必须仰仗 PMS + AMS。
- 应用需要查询别的应用（例如 launcher 需要列出所有应用图标），此时依靠 PMS。
- 应用需要接收用户点击——靠 IMS 把事件派发过来。

因此，PMS/AMS/IMS 是系统级的基础设施服务，地位在应用之下。应用启动、运行、交互，全程都依赖它们，离开它们，应用寸步难行。

## 2、AIDL
AIDL（Android Interface Definition Language，Android接口定义语言）。它是一种接口描述语言，本身不是可运行代码，而是一份契约文件。

例如，BlueOS 里真实的 IQrReadyCallBack.aidl 长这样：

```
interface IQrReadyCallBack {
	void onReady(int sys);
}
```

它的作用是：让不同进程之间能调用彼此的方法，就像调用本地对象一样自然。

Android/BlueOS 上系统服务（PMS、AMS、IMS）和应用跑在不同进程里，进程之间内存隔离，不能直接`obj.method()`调用对方的方法。AIDL 解决的是 跨进程方法调用（RPC/IPC）。

AIDL 文件经过编译器处理，会自动生成两段代码：

- Stub（桩）：服务端持有的接线板。它将客户端传来的字节流解析成参数，调用真正的实现方法，再把返回值打包成字节流送回去。
- Proxy（代理）：客户端持有的假对象。例如调用 proxy.onReady(1)，它内部其实是把参数序列化字节流，通过内核驱动送到服务端，等返回结果再反序列化给你。对你而言就像调用了真实对象。

`stub`的含义就是一个替身/接线板。它本身不实现业务逻辑，只是转接调用。在服务端那侧的转接叫`Stub`，客户端那侧的转接叫 `Proxy`。


## 3、Binder
Binder 是 Android/BlueOS 的内核级 IPC（进程间通信）机制，是 AIDL 背后真正搬运数据的“管道”。

AIDL 是接口契约语言，Binder 是传输管道。两者的关系：

- AIDL：定义了有哪些方法，参数怎么序列化
- Binder：负责把序列化后的字节流从一个进程送到另一个进程，并唤醒对方线程处理

下图展示了一个跨进程通信方式：

![[assets/Pasted image 20260708165926.png|500]]

## 4、桌面预览也需要 PMS/AMS/IMS

桌面预览器的定位不是一个能画 rpk 的渲染器，而是一台 BlueOS 设备在 PC 上的软件模拟。

快应用的 UI 不是静态画面，而是被运行时驱动的活东西。一个 rpk 要变成屏幕上的画面，必须经历：

![[assets/Pasted image 20260708172635.png|400]]

条链路是 BlueOS 定义的标准运行时,快应用框架就是按这套链路写的。其中 PMS/AMS/IMS 不是可选配件,而是链路的前两环——没有 PMS 解析 rpk、没有 AMS 启动应用,后面的 UI 引擎根本拿不到东西可渲染。


# 二、ui-previewer 整体机制

现在桌面的 `ui-previewer` 是一个“BlueOS 单进程虚拟机”：不模拟硬件，而是把 BlueOS 的系统服务软件层整个搬进一个进程，外面套一层PC 窗口。分四层：

![[assets/Pasted image 20260708174028.png|400]]