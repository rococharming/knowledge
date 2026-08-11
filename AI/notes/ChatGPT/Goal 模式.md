
# 一、什么是 Goal 模式

普通 Codex 模式是单回合任务：你给 prompt，Codex 给响应，做完就停。如果任务没有完成，需要你手动追问、手动指出问题、手动让它继续。

而 Goal 模式是持久化目标驱动：定义一个可验证完成的目标，Codex 自动循环执行，直到它自己评估目标已达成或 Token 预算耗尽。

真正的自主智能体循环：plan -> act -> test -> review -> iterate。


# 二、核心特性

- 持久化目标：目标状态保存到 app-server 中，跨会话、跨终端都能 resume 
- 预算感知： Token 预算耗尽时是 "soft stop"，会被标记为 `budget_limited`，并触发 wrap-up steering 而不是粗暴中断
- **TUI 控制台**: TUI 中可直接 create / pause / resume / clear 当前目标
- **运行时延续 (Runtime Continuation)**: 不需要每个回合敲键盘，CLI 会自动延续工作
- **中断友好**：你可以 Ctrl+C 中断，Goal 状态自动保留，重新进 TUI 后会自动恢复

# 三、Goal 模式的工作原理

## 1、5 阶段循环

OpenAI 内部把 Goal 模式的循环叫做 Ralph Loop，它不是简单的失败重试，而是一个带评估、带规划、带测试的闭环。

每一轮循环 Codex 都会走完以下 5 个阶段：

![[assets/Pasted image 20260811153445.png]]

每个阶段的具体工作如下：

- Plan（规划）：Codex 把高层目标拆成可执行的子任务列表，并标注成功判定标准
- Act（执行）：按照计划修改代码、安装依赖、调用 shell 命令
- Test（测试）：运行单元测试、lint、构建命令，收集失败信息
- Review（评审）：评估当前进展是否接近目标，识别新出现的阻塞
-  Iterate (迭代)：基于 Review 结果生成下一轮 Plan，回到第一步

## 2、Goal 模式的终止条件

不是所有循环都会无限跑下去。Goal 模式有 3 个明确的终止条件：

1. 目标达成：Codex 自评 success criteria 全部通过 → 输出最终总结后退出
2. Token 运算耗尽：触发 `budget_limited` soft stop，Codex 会用剩余 Token 做 wrap-up，写一个进度报告再退出
3. 手动 clear：TUI 中输入 `/goal clear` 或 `Ctrl + C` 选择终止。

> 预算控制 Tips：默认 Token 运算在大型项目下很快耗尽。建议通过 `/goal budget <tokens>` 显式设置预算上限，避免某个错误判断导致 Codex 在错误方向上消耗大量 Token。


# 四、Goal 快速上手

## 1、定义目标

示例：

```
/goal Migrate this codebase from Pydantic v1 to v2, fix all type errors, and ensure all tests pass.
```

写好 Goal 的 3 个原则：

1. 目标必须可验证：例如所有测试通过、无 lint 错误
2. 明确边界：例如"只动 src/ 目录，不动 tests/"，避免 Codex 自由发挥过度
3. 给出退出条件：