
## 当前代码基线

| 仓库      | 地址                                                 | 分支                     |
| ------- | -------------------------------------------------- | ---------------------- |
| bdb     | https://gitblueos.vivo.xyz/BlueOS/System/tools_bdb | adapt-rust-uipreviewer |
| rust-ui | https://gitblueos.vivo.xyz/BlueOS/System/rust-ui   | fix/windows-msvc-link  |

## 当前已经实现的功能

```shell
bdb preview launch
bdb preview route
bdb preview screenshot
bdb preview fold
bdb preview stop
```

当前 launch 参数：

| 参数                 | 当前行为                                                           |
| ------------------ | -------------------------------------------------------------- |
| `--id`             | 可选，默认 `default`；由调用方指定，同一活动 ID 再次 launch 会失败                   |
| `--app`            | 必选，JavaScript 应用目录                                             |
| `--device-type`    | 必选，支持 `watch-round`、`watch-square`、`phone`、`foldable`、`camera` |
| `--width/--height` | 可选，但必须成对提供；含义是设备物理分辨率                                          |
| `--headless`       | 可选；隐藏交互窗口但保留渲染、route 和截图能力                                     |
