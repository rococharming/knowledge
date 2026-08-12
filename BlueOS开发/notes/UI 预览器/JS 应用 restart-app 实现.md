## 概要

复用现有 BDB “同一条 `preview launch` → `preview.update`”协议。JS Preview Session 在 `preview.ready` 中声明更新能力；更新时替换完整 JS 应用产物，销毁旧前台 JS App，再从 manifest 入口创建新 App。进程、窗口、Session ID、Session Data Root 均保持不变。

## 实现

- 复用 `generations/slots/a|b/<package>`、`current`、`candidate` 角色链接；`data/app/<package>` 始终指向 `generations/current/<package>`。
- 首次 BDB 启动把完整 JS `--app` 目录部署到 `current`；独立 `uipreviewer --app` 保持现有直接启动行为，不支持热更新。
- 将应用树复制和内容指纹泛化为 JS/Native 共用能力。JS 指纹覆盖 `build/foldable` 下实际运行的完整产物；内容未变化时更新成功但不重启。
- 为 pkgmgr 增加只读候选检查：解析 manifest、确认包名和 JS 类型，但不得改动 `data/app` 链接或已注册元数据。
- JS Session 在 Ready 能力中加入 `preview.update`；BDB 不按 JS/Native 分支，只按该能力决定复用 Session 并发送更新。
- 更新顺序固定为：候选复制与校验 → 暂停输入/隐藏旧前台页面 → 销毁全部旧页面与 JS Application，并等待 Runtime 确认完成 → 原子切换 `current` → 注册新的 current 路径 → 重置 RPK 已加载状态 → 走正常 `prepare_load_rpk` / `load_finish` → 从 manifest entry 启动。
- 成功条件是新入口页首帧出现后再额外确认一帧；不能以 JSON-RPC 已返回、RPK 加载完成或 Page 已创建作为成功。
- 候选校验失败时保留旧 App 继续运行；旧 App 已销毁后的切换、加载、目标帧失败时终止整个 Preview Session，不做回滚。
- v1 仅支持前台 JS App。检测到活动 Service/Background Context 时，在切换前明确拒绝更新；不保存、恢复或重建这些上下文。
- 旧 JS 工作树只参考其“销毁旧 Application、重载 RPK、目标帧”经验；不迁入页面栈快照、query 恢复、逐页回放、复杂 revision fence 或 Service 重建。

## 测试与验收

- 单元测试：JS Session 宣告 `preview.update`；候选检查不改注册路径；相同指纹不重启；候选错误不影响 Gen1；旧 App 完成销毁后才允许切换；切换后失败使 Session 结束。
- Runtime 集成测试：Gen1 入口页 → JS 更新 → Gen2 入口页；更新前停在 `DemoDetail` 时，更新后必须回到 manifest entry `pages/Demo`，证明是 `restart-app` 而非刷新当前页。
- BDB 回归：同 Launch Key 的 Ready Session 且带 `preview.update` 时，第二次 `preview launch` 转发更新；能力缺失、更新中、超时保持现有错误语义。
- 真实 GUI 验收使用：
    - 应用目录：`/Users/11185032/BlueOSProjects/my-application-5/build/foldable`
    - 源码：`/Users/11185032/BlueOSProjects/my-application-5/src/pages/Demo/index.ux`
    - BDB：`~/tools_bdb/bdb_cli` 构建出的 `bdb`
    - 固定使用同一条 `bdb preview launch --app /Users/11185032/BlueOSProjects/my-application-5/build/foldable --device-type foldable`。
    - 首次显示明确的 Gen1 文案并记录 PID、窗口、Session ID、Session Data Root；在 BlueOS Studio 修改 `src/pages/Demo` 为 Gen2 并保存，等待 Studio 更新 `build/foldable`；再次执行完全相同的 launch。
    - 截图证明 Gen2 已显示，且四项身份信息均未变；再做一次包名错误/产物破损验证旧 App 仍在，以及一次切换后超时验证 Session 被终止。

## 默认约束

- 仅 macOS Preview / `std_local` 路径改动，不影响真机运行。
- 不新增 BDB 命令、参数或文件监听；Studio 负责构建，BDB 负责在下一次相同 launch 时触发更新。
- 以现有 Native 的 current/candidate 改造完成并稳定为前提，JS 共享其布局与通用 staging 能力，不并行改同一段平台代码。