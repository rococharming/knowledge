# 一、本节概览 
  
本节介绍 AI 编码智能体最小可运行内核：**一个模型循环加一个 `bash` 工具**。

模型本身只负责判断下一步要做什么；真正把命令跑起来、收集结果、再喂回模型的是 harness。

没有这个循环时，模型只能给出命令；有了这个循环后，模型可根据工具结果继续推理和行动。

核心判断只有一个：

| 条件                                   | 含义         | 行为                                   |
| ------------------------------------ | ---------- | ------------------------------------ |
| `response.stop_reason == "tool_use"` | 模型请求调用工具   | 执行工具，把结果作为 `tool_result` 追加进消息，再继续循环 |
| `response.stop_reason != "tool_use"` | 模型没有继续请求工具 | 退出本轮 agent loop                      |
  
# 二、消息流  
  
一次完整的交互可以理解为：  

1. 用户输入任务，形成第一条`user`消息
2. harness 将历史消息、系统提示词和工具定义一起发给模型
3. 模型返回普通文本，或者返回`tool_use`块
4. 如果有`tool_use`，harness 执行对应工具
5. harness 把工具输出包装成`tool_result`，作为新的 `user` 消息追加到历史中
6. 回到第 2 步，直到模型不再调用工具
  
关键点是：工具结果不是直接打印给模型，而是作为对话历史的一部分回传。模型因此可以看到刚才命令执行后的真实结果。  

如下图所示：

![[Pasted image 20260602181738.png|600]]

# 三、代码结构  
  
## 1、环境与客户端  
  
先加载 `.env`，再从环境变量里读取 API Key、Base URL 和模型：  
  
```python  
api_key = os.getenv("ANTHROPIC_AUTH_TOKEN") or os.getenv("ANTHROPIC_API_KEY")  
client = Anthropic(  
    base_url=os.getenv("ANTHROPIC_BASE_URL"),    api_key=api_key,)  
MODEL = os.environ["MODEL_ID"]  
```  
  
这里支持 `ANTHROPIC_BASE_URL`，所以它不只绑定 Anthropic 官方服务，也可以接兼容服务商。  
  
## 2、系统提示词  
  
```python  
SYSTEM = f"You are a coding agent at {os.getcwd()}. Use bash to solve tasks. Act, don't explain."  
```  
  
它告诉模型当前工作目录，并要求模型用 bash 行动。这是一个很强的行为约束：本课不是让模型解释方案，而是让模型真的通过工具完成任务。  
  
## 3、工具定义  
  
本课只有一个工具：`bash`。  
  
```python  
TOOLS = [{
	"name": "bash",
	"description": "Run a shell command.",
	"input_schema": {
		"type": "object",
		"properties": {"command": {"type": "string"}},
		"required": ["command"],
	}
}]
```  

这是在定义“给模型看的工具说明书”。模型不会直接知道你的 Python 里有什么函数，所以要用这种JSON-like的格式告诉它：你可以调用一个叫 bash 的工具，调用时必须传什么参数。

```json
"name": "bash"
```

工具名。模型之后如果想用它，会生成一个`tool_use`，里面的名字就是`bash`。

```json
"description": "Run a shell command."
```

工具描述。给模型看的，帮助模型判断什么时候该用这个工具。

```json
"input_schema": {
	"type": "object",
	"properties": {"command": {"type": "string"}},
	"required": ["command"],
}
```

`input_schema`定义工具参数的结构。

```json
"type": "object"
```

表示调用`bash`时，输入必须是一个对象，类似：

```json
{
	"command": "ls -la"
}
```

```json
"properties": {"command": {"type": "string"}},
```

表示这个对象里允许有一个字段`command`，它的值必须是字符串。

所以模型应该生成：

```json
{
	"command": "pwd"
}
```

而不是：

```json
{
	"command": 123
}
```

```json
"required": ["command"],
```

表示`command`是必填字段。模型不能只说“我要用 bash”，必须明确给出要执行的命令。

整体等价于告诉模型：

> 有一个工具叫 bash，它可以运行 shell 命令。调用它时，请传入一个对象，里面必须有字段 command，其值必须为字符串。

模型调用后，大概会返回类似这种内容：

```json
{
	"type": "tool_use",
	"name": "bash",
	"input": {
		"command": "ls -la"
	}
}
```

然后 Python 通过：

```python
block.input["command"]
```

拿到命令"ls -la"，在执行：

```python
run_bash("ls -la")
```

## 4、工具执行  
  
`run_bash()` 做了四件事：  
  
1. 拦截明显危险的命令片段，例如 `rm -rf /`、`sudo`、`shutdown`。  
2. 用 `subprocess.run(..., shell=True)` 执行命令。  
3. 捕获 stdout 和 stderr。  
4. 对超时、无输出和系统错误做简单兜底。  
  
这是教学版的轻量保护，不是完整权限系统。README 也明确提示：真实权限控制会在后续课程展开。  
  
## Agent Loop 逐行理解  
  
核心函数是：  
  
```python  
def agent_loop(messages: list):  
    while True:        response = client.messages.create(            model=MODEL, system=SYSTEM, messages=messages,            tools=TOOLS, max_tokens=8000,        )  
        messages.append({"role": "assistant", "content": response.content})  
        if response.stop_reason != "tool_use":            return  
        results = []        for block in response.content:            if block.type == "tool_use":                output = run_bash(block.input["command"])                results.append({                    "type": "tool_result",                    "tool_use_id": block.id,                    "content": output,                })  
        messages.append({"role": "user", "content": results})  
```  
  
理解时可以抓住三个动作：  
  
- `client.messages.create(...)`：让模型基于当前历史决定下一步。  
- `run_bash(...)`：harness 替模型执行真实世界动作。  
- `messages.append({"role": "user", "content": results})`：把执行结果回灌给模型，让下一轮推理有依据。  
  
其中 `tool_use_id` 很重要，它把某个工具结果和模型发出的某个工具调用对应起来。模型一次可能请求多个工具调用，结果需要能准确匹配回去。  
  
## 入口交互  
  
主程序维护一个 `history`：  
  
```python  
history = []  
```  
  
每次用户输入后，都会追加到同一个历史里：  
  
```python  
history.append({"role": "user", "content": query})  
agent_loop(history)  
```  
  
这意味着同一进程内的多轮输入共享上下文。用户上一轮让模型创建的文件、查询过的信息、模型回答过的内容，都可能影响下一轮。  
  
## 本课要观察什么  
  
运行时重点看两个现象：  
  
1. 模型何时选择调用 `bash`。  
2. 工具输出回来后，模型如何决定下一步。  
  
例如：  
  
```text  
Create a file called hello.py that prints "Hello, World!"  
```  
  
模型通常会先调用 bash 创建文件，可能再读取或运行它验证，然后才停止。  
  
再比如：  
  
```text  
What is the current git branch?  
```  
  
模型会调用类似 `git branch --show-current` 的命令，拿到结果后用自然语言回答。  
  
## 安全边界  
  
这一课的安全能力很有限：  
  
- 危险命令只靠字符串黑名单拦截。  
- `shell=True` 允许复杂 shell 语法。  
- 没有用户确认机制。  
- 没有按工具、目录、命令类型做细粒度权限控制。  
- 没有完整的错误恢复、压缩、hooks、任务管理等生产级机制。  
  
因此它适合教学和临时测试，不适合直接拿来执行高风险任务。学习时最好在临时目录或干净仓库中运行。  
  
## 和生产级 Agent 的关系  
  
README 里提到，Claude Code 生产实现远比本课复杂，但核心仍然是这个循环。  
  
教学版：  
  
```text  
模型返回 tool_use -> 执行工具 -> tool_result 回传 -> 继续  
```  
  
生产版会额外叠加：  
  
- 流式响应处理。  
- 并发工具执行。  
- 权限系统。  
- hooks。  
- 上下文压缩。  
- 错误恢复。  
- 最大轮次和 token 预算控制。  
- 后台任务、子 agent、MCP 等机制。  
  
所以 s01 的价值不是功能完整，而是把 agent harness 的最小骨架单独拎出来：后续所有能力都围绕这个骨架扩展。  
  
## 学习检查点  
  
学完本课后，应该能回答：  
  
1. 为什么只让模型输出命令还不算 agent？  
2. `tool_use` 和 `tool_result` 分别表示什么？  
3. 为什么工具结果要追加回 `messages`？  
4. `stop_reason` 在这个教学实现里起什么作用？  
5. harness 和模型的职责边界是什么？  
6. 为什么本课的 bash 工具需要后续权限系统补强？  
  
一句话总结：s01 展示的是最小 agent loop，模型负责决策，harness 负责执行和回灌结果；循环继续还是停止，取决于模型是否继续请求工具调用。