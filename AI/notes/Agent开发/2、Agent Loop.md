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

```python
def run_bash(command: str)  -> str {
	
	# 危险命令列表
	dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
	
	# 判断命令是否危险，危险则直接返回不执行命令
	if any(d in command for d in dangerous):
		return "Error: Dangerous command blocked"
	
	try:
		r = subprocess.run(command, shell=True, cwd=os.getcwd(),
						  capture_output=True, text=True, timeout=120)
		out = (r.stdout + r.stderr).strip();
		return out[:50000] if out else "(no output)"
	except subprocess.TimeoutExpired:
		return "Error: Timeout (120s)"
	except (FileNotFoundError, OsError) as e:
		return f"Error: {e}"
	
}
```
  
这是教学版的轻量保护，不是完整权限系统。
  
## 5、Agent Loop 逐行理解  
  
核心函数是：  
  
```python  
def agent_loop(messages: list):
	
	while True:
	
		# 用 Anthropic Messages API，让模型根据当前对话历史生成下一步响应。
		response = client.messages.create(
			model=MODEL, system=SYSTEM, messages=messages,
			tools=TOOLS, max_tokens=8000,
		)
		
		# 把模型这次回复加入对话历史。
		messages.append({"role": "assistant", "content": response.content})
	
		# 如果模型不需要调用工具，结束循环
		if response.stop_reason != "tool_use":
			return 
		
	
		results = []
		for block in response.content:
			if block.type = "tool_use":
				print(f"\033[33m$ {block.input['command']}\033[0m")
				output = run_bash(block.input["command"])
				print(output[:200])
				results.append({
					"type": "tool_result",
					"tool_use_id": block.id,
					"content": output
				})
	
	
		# 把工具执行结果作为一条新的 `user` 消息写回对话历史。	
		messages.append({"role": "user", "content": results})
	

```  

参数`messages`用于保存整个对话历史，例如：

```python
[
	{"role": "user", "content": "帮我查看当前目录"},
	{"role": "assistant", "content": ...},
	{"role": "user", "content": ...},
]
```

注意，`response.content` 不一定只是普通文本，也可能包含工具调用请求。

例如模型想执行命令时，`response.content` 里可能包含类似：

```python
{
	"type": "tool_use",
	"name": "bash",
	"input": {
		"command": "ls"
	}
}
```

将工具执行结果加入列表时，需要按照 Anthropic 工具调用协议组织：

```python
results.append({  
	"type": "tool_result",  
	"tool_use_id": block.id,  
	"content": output,  
})
```

字段含义：

| 字段                        | 含义                 |
| ------------------------- | ------------------ |
| `"type": "tool_result"`   | 表示这是工具执行结果         |
| `"tool_use_id": block.id` | 对应模型刚才发出的那个工具调用 ID |
| `"content": output`       | 工具执行输出             |

其中 `tool_use_id` 很重要，它把某个工具结果和模型发出的某个工具调用对应起来。模型一次可能请求多个工具调用，结果需要能准确匹配回去。  
  
## 6、入口交互  
  
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
  

# 四、观察现象
  
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
  

# 五、回答问题
  
学完本课后，应该能回答：  
  
1. 为什么只让模型输出命令还不算 agent？  
2. `tool_use` 和 `tool_result` 分别表示什么？  
3. 为什么工具结果要追加回 `messages`？  
4. `stop_reason` 在这个教学实现里起什么作用？  
5. harness 和模型的职责边界是什么？  
6. 为什么本课的 bash 工具需要后续权限系统补强？  
  