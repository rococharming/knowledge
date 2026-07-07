
# 一、整体架构与角色

一个二进制，两种互斥角色。

`simulator_mac` 二进制由 `argv[1]` 决定扮演哪种角色，二者互斥：

1. 角色A  ——  模拟器主机

```shell
./simulator_mac --package com.xxx.xxx --rpk-root ～/apps [--id watch1]
```

- 起窗口、渲染、跑应用
- 开本地 Unix  domain  socket 监听，等 CLI 来连
- 常驻，直到 stop 或窗口关闭
- --id 指定 session id，没传默认**default**

2. 角色B  ——  控制客户端（带子命令）

```shell
./simulator_mac route /pages/Home [--id watch] [--mode push] [--query ...]
./simulator_mac screenshot ./a.png [--id watch1]
./simulator_mac status [--id watch1]
./simulator_mac stop [--id watch1]
```

- 短生命周期进程
- 连本地 socket，发一条 JSON-RPC，打印结果，退出
- --id 指定 目标 session，没传默认 default

**判别规则**：argv\[1] ∈ {route, screenshot, status, stop} → 角色 B；否则 → 角色 A。


