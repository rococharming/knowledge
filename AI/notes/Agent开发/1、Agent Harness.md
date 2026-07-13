
# 一、Claude Code

将`Claude Code`拆到最本质的形态：

```text
Claude Code = 一个 agent loop
            + 工具（bash、read、write、edit、glob、grep、browser...）
            + 按需加载 skill
            + 上下文压缩
            + 启动 subagent
            + 带依赖图的任务系统
            + 用于团队协作的异步 mailbox
            + 基于 worktree 隔离的并行执行
            + 权限治理
            + hooks 扩展系统
            + 持久化 memory
            + MCP 外部能力路由
```

真正的`agent`本身是`Claude`模型或第三方模型。

`harness`没有让模型变聪明，因为模型本身已经很智能。`harness` 只是给了模型手、眼睛和一个可以工作的空间。


# 二、核心模式

![[assets/Pasted image 20260527104340.png|600]]

```python
def agent_loop(messages):
	
	# Agent Loop
    while True:
        # 调用模型
        response = client.messages.create(
            model=MODEL, system=SYSTEM,
            messages=messages, tools=TOOLS,
        )
        
        # 保存模型回复
        messages.append({
            "role": "assistant",
            "content": response.content
        })
		
		# 判断模型是否需要调用工具
        if response.stop_reason != "tool_use":
            return
		
		# 准备保存工具执行结果
        results = []
        
        # 遍历模型返回的内容块
        for block in response.content:
            if block.type == "tool_use":   # 筛选工具调用块
                output = TOOL_HANDLERS[block.name](**block.input)  # 执行对应工具
                results.append({      # 将工具结果整理成模型能理解的格式
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })

        messages.append({   # 把工具结果放回 messages
            "role": "user",
            "content": results
        })
```

之后在这个循环之上叠加一种`harness`机制，但这个循环本身从不改变。循环本身是`agent`，机制属于`harness`。循环是固定的，会变化的是工具、知识、权限。

```text
Agent = 模型(LLM) + 通用操作环境（Harness）
```

更直白地说，`agent loop`是整个智能体运行的核心骨架。无论后面加入工具调用、权限控制、上下文压缩、知识加载、任务系统、子代理，底层都还是这个循环。

真正做判断的是模型，`harness`负责给模型提供可操作的环境，比如：

- 工具：Bash、Read、Write、Edit等
- 知识：文档、规则、Skills等
- 权限：哪些文件能改、哪些命令要确认、哪些操作被禁止