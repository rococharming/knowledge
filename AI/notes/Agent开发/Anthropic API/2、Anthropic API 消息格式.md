---
title: Anthropic API 消息格式
date: 2026-06-11
tags: [AI, Agent, Anthropic]
aliases:
  - Anthropic API 消息格式
  - AnthropicAPI消息格式
---

# 一、Message API 的消息结构

`Messages API` 使用 `messages` 参数描述对话内容。`messages` 是一个消息列表，列表中的每个元素表示一条消息。

示例：

```python
messages = [
    {"role": "user", "content": "给我讲个笑话"}
]
```

一条消息通常由 `role` 和 `content` 两部分组成：

|字段|作用|常见取值|
|---|---|---|
|`role`|标记消息是谁说的|`user`、`assistant`|
|`content`|保存消息正文|字符串或内容块列表|

`role` 用来区分消息来源：

| `role`      | 含义         |
| ----------- | ---------- |
| `user`      | 用户发送的消息    |
| `assistant` | 模型之前生成过的消息 |

最常见的 `content` 写法是字符串：

```python
{"role": "user", "content": "给我讲个笑话"}
```

对于普通文本内容，字符串形式已经足够。更复杂的场景中，`content` 也可以写成内容块列表。Anthropic 的 Message API 把消息内容组织为一个或多个内容块。

响应中的 `content` 字段也是内容块数组。例如普通文本块通常包含 `type` 字段，值为 `text`，同时包含 `text` 字段，值为对应文本。

```python
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "请用一句话解释什么是 HTTP。"
            }
        ]
    }
]
```

入门阶段可以优先使用字符串写法；当需要混合文本、图片、工具结果等结构化内容时，再使用内容块列表。

# 二、一次完整的消息请求

## 1、发送请求

调用 `client.messages.create()` 可以向模型发送一次消息请求：

```python
response = client.messages.create(
    model="kimi-for-coding",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "你好"}
    ]
)
```

常用参数如下：

|参数|说明|
|---|---|
|`model`|指定要调用的模型|
|`max_tokens`|限制模型本次最多生成多少 token|
|`messages`|传入当前消息和必要的历史上下文|
|`system`|设置全局系统提示词|
|`temperature`|控制输出随机性|
|`stop_sequences`|指定遇到某些字符串时停止生成|
|`stream`|是否使用流式响应|

`max_tokens` 限制的是输出 token 数，不是输入 token 数；模型可能自然停止，也可能因为达到该上限而停止。

## 2、system参数

`system`用来设置模型的整体行为要求，例如角色、风格、边界和输出规范。它是 `client.messages.create()` 的顶层参数，不写进 `messages` 列表中。Anthropic Messages API 使用顶层 `system` 参数，而不是 `"role": "system"` 的消息。

示例：

```python
response = client.messages.create(
    model="kimi-for-coding",
    max_tokens=1000,
    system="你是一个简洁、准确的翻译助手。只给出翻译后的内容",
    messages=[
        {"role": "user", "content": "将你好翻译成英文。"}
    ]
)
```

上述例子中，因为增加了“只给出翻译后的内容”的全局规则，因此模型返回的只有简洁的翻译内容，而无其他无关输出。

`system` 适合放全局规则；`messages` 适合放用户输入、助手历史回答和示例上下文。

# 三、响应对象

## 1、响应示例

`client.messages.create()` 返回一个 `Message` 对象。这个对象不仅包含模型生成的文本，还包含模型、停止原因、token 使用量等信息。

```python
response = client.messages.create(  
    model=MODEL,  
    max_tokens=1000,  
    messages=[  
        {"role": "user", "content": "你好"}  
    ]  
)  
  
print(response)
```

输出：

```text
Message(
	id='msg_uFjxw6Qx263pF9FIsITrpaKb', 
	container=None, 
	content=
	[
		TextBlock(
			citations=None, 
			text='你好！很高兴见到你，有什么我可以帮助你的吗？', 
			type='text'
		)
	], 
	model='kimi-for-coding', 
	role='assistant', 
	stop_details=None, 
	stop_reason='end_turn', 
	stop_sequence=None, 
	type='message', 
	usage=Usage(
		cache_creation=None, 
		cache_creation_input_tokens=0, 
		cache_read_input_tokens=8, 
		inference_geo='not_available', 
		input_tokens=0, 
		output_tokens=15, 
		output_tokens_details=None, 
		server_tool_use=None, 
		service_tier='standard', 
		prompt_tokens=8, 
		cached_tokens=8, 
		completion_tokens=15, 
		total_tokens=23
	)
)
```

普通文本响应通常这样读取：

```python
print(response.content[0].text)
```

输出：

```text
你好！很高兴见到你，有什么我可以帮助你的吗？
```


## 2、Message对象字段

| 字段              | 示例值                              | 说明                                                       |
| --------------- | -------------------------------- | -------------------------------------------------------- |
| `id`            | `'msg_uFjxw6Qx263pF9FIsITrpaKb'` | 本次响应对象的唯一标识，通常用于日志、排查问题或追踪请求                             |
| `container`     | `None`                           | 容器相关信息。普通文本对话中通常为 `None`；如果服务商支持代码执行、文件处理等容器能力，可能会出现相关信息 |
| `content`       | `[TextBlock(...)]`               | 模型生成的内容块列表。普通文本回复通常在第一个 `TextBlock` 中                    |
| `model`         | `'kimi-for-coding'`              | 实际生成响应的模型名称                                              |
| `role`          | `'assistant'`                    | 当前响应的角色。模型返回的消息通常是 `assistant`                           |
| `stop_details`  | `None`                           | 停止生成的扩展细节。不同服务商兼容实现可能不同，普通请求中通常为 `None`                  |
| `stop_reason`   | `'end_turn'`                     | 模型停止生成的原因                                                |
| `stop_sequence` | `None`                           | 如果因为自定义停止序列而停止，这里会记录触发停止的字符串；否则通常为 `None`                |
| `type`          | `'message'`                      | 返回对象类型，Messages API 的响应通常是 `message`                     |
| `usage`         | `Usage(...)`                     | 本次请求的 token 使用情况，包括输入、输出、缓存等统计                           |

这里最常用的字段是`content`、`stop_reason`和`usage`。

`content`用于读取模型生成内容，`stop_reason`用来判断响应是否正常结束；`usage`用来观察 token 消耗、缓存命中与请求成本。

## 3、content 内容块

返回的 Message 对象的 `content`是一个列表：

```python
content=
[
	TextBlock(
		citations=None, 
		text='你好！很高兴见到你，有什么我可以帮助你的吗？', 
		type='text'
	)
]
```

字段含义如下：

|字段|示例值|说明|
|---|---|---|
|`type`|`'text'`|内容块类型。`text` 表示普通文本块|
|`text`|`'你好！很高兴见到你，有什么我可以帮助你的吗？'`|模型生成的文本内容|
|`citations`|`None`|引用信息。普通文本回复通常为 `None`；如果模型返回带引用的内容，可能包含引用来源|
因为 `content` 是列表，所以读取文本时需要先取第一个内容块：

```python
text = response.content[0].text
```

如果响应包含多个内容块，就不能只假设`content[0]`一定包含全部内容。更稳妥的写法是把所有文本块拼接起来：

```python
texts = []  
  
for block in response.content:  
    if block.type == "text":  
        texts.append(block.text)  
  
result = "".join(texts)  
print(result)
```


## 4、usage token 统计

前面示例的返回结果中，`usage`是：

```text
Usage(
    cache_creation=None,
    cache_creation_input_tokens=0,
    cache_read_input_tokens=8,
    inference_geo='not_available',
    input_tokens=0,
    output_tokens=15,
    output_tokens_details=None,
    server_tool_use=None,
    service_tier='standard',
    prompt_tokens=8,
    cached_tokens=8,
    completion_tokens=15,
    total_tokens=23
)
```

可以分成三类理解。

第一类是 Anthropic Messages API 中常见的 token 统计字段：

| 字段                            |  示例值 | 说明                                                                             |
| ----------------------------- | ---: | ------------------------------------------------------------------------------ |
| `input_tokens`                |  `0` | 输入 token 数。这里显示为 `0`，说明 Kimi 兼容层可能没有使用 Anthropic 原字段记录输入，而是使用了 `prompt_tokens` |
| `output_tokens`               | `15` | 输出 token 数                                                                     |
| `cache_creation_input_tokens` |  `0` | 写入 prompt cache 的输入 token 数                                                    |
| `cache_read_input_tokens`     |  `8` | 从 prompt cache 读取的输入 token 数                                                   |
Anthropic 官方响应中的 `usage` 用于表示输入和输出 token 使用情况，也会包含与 prompt caching 相关的 token 统计字段。

第二类是 Kimi 兼容层或第三方兼容服务常见的补充字段：

| 字段                  |  示例值 | 说明                                                  |
| ------------------- | ---: | --------------------------------------------------- |
| `prompt_tokens`     |  `8` | 输入 prompt 消耗的 token 数，语义上接近输入 token                 |
| `completion_tokens` | `15` | 模型完成回复消耗的 token 数，语义上接近输出 token                     |
| `total_tokens`      | `23` | 总 token 数，通常约等于 `prompt_tokens + completion_tokens` |
| `cached_tokens`     |  `8` | 命中缓存的 token 数                                       |
第三类是服务侧元信息：

|字段|示例值|说明|
|---|---|---|
|`cache_creation`|`None`|缓存创建信息。这里没有返回具体值|
|`output_tokens_details`|`None`|输出 token 的扩展细节。普通请求中可能为空|
|`server_tool_use`|`None`|服务端工具使用信息。未使用工具时通常为空|
|`service_tier`|`'standard'`|服务等级|
|`inference_geo`|`'not_available'`|推理所在区域信息。这里表示不可用或未提供|

本次输出中，主要关注：

```text
prompt_tokens=8
completion_tokens=15
total_tokens=23
cached_tokens=8
```

也就是说，这次请求输入侧大约消耗 `8` 个 token，输出侧消耗 `15` 个 token，总计 `23` 个 token，并且输入 token 命中了缓存。

如果想单独读取 token 信息，可以根据实际返回字段访问：

```python
usage = response.usage

print("输入 token:", getattr(usage, "prompt_tokens", None))
print("输出 token:", getattr(usage, "completion_tokens", None))
print("总 token:", getattr(usage, "total_tokens", None))
print("缓存 token:", getattr(usage, "cached_tokens", None))
```

因为当前调用的是 Kimi 的 Anthropic 兼容接口，`usage` 中同时出现了 Anthropic 风格字段和兼容层扩展字段。写正式代码时，不要假设所有服务商都会返回完全相同的字段；可以使用 `getattr()` 读取可选字段，避免字段不存在时报错。
## 5、stop_reason

`stop_reason`表示模型为什么停止生成，例如：

```text
stop_reason='end_turn'
```

说明模型自然完成了这一轮回复。

常见值如下：

|`stop_reason`|含义|常见场景|
|---|---|---|
|`end_turn`|模型自然结束本轮回复|普通问答正常完成|
|`max_tokens`|达到 `max_tokens` 输出上限|输出被截断，需要调大 `max_tokens` 或缩短任务|
|`stop_sequence`|命中自定义停止序列|请求中设置了 `stop_sequences`|
|`tool_use`|模型决定调用工具|使用 tools / function calling 场景|
|`pause_turn`|模型暂停当前轮次，等待继续|长任务或服务端工具相关场景中可能出现|
|`refusal`|模型拒绝回答|请求触发安全边界或模型拒答策略|
处理时可以按 `stop_reason` 做分支：

```python
if response.stop_reason == "end_turn":
	print(response.content[0].text)
elif response.stop_reason == "max_tokens":
	print("输出可能被截断，可以增大 max_tokens 或缩短提示词")
	print(response.content[0].text)
elif response.stop_reason == "stop_sequence":
	print("模型命中了自定义停止序列。")  
	print(response.content[0].text)	
elif response.stop_reason == "tool_use":  
	print("模型请求调用工具，需要读取 tool_use 内容块并执行对应工具。")
elif response.stop_reason == "refusal":  
	print("模型拒绝回答，需要根据业务场景处理。")
else:
	print(f"未知停止原因：{response.stop_reason}")
```

普通脚本里，可以先只读取 `response.content[0].text`；正式项目中，建议同时检查 `stop_reason`。尤其是 `max_tokens`，它通常意味着回复可能没有生成完整。


# 四、消息列表的组织方式

## 1、单轮回答

单轮问答只需要传入当前用户消息：

```python
response = client.messages.create(
    model="kimi-for-coding",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "用一句话解释什么是递归。"}
    ]
)
print(response.content[0].text)
```

这种结构适合一次性问答、翻译、摘要、分类、格式转换等任务。


## 2、带历史的多轮对话

`Message API`不会自动保存应用中的对话历史。如果希望模型理解上下文，需要把相关历史一起传入`messages`。

```python
messages = [
    {"role": "user", "content": "你好，什么是机器学习"},
    {"role": "assistant", "content": "机器学习是人工智能的一个分支，它让计算机从数据中学习规律，从而做出预测或决策"},
    {"role": "user", "content": "那深度学习和机器学习有什么区别？"}
]
```

模型会基于这个列表生成下一条 `assistant` 消息：

![[assets/Pasted image 20260611102836.png|400]]

这里的 `assistant` 消息不是让程序现场生成回答，而是把模型之前的回答作为上下文重新传给模型。

## 3、预填充 assistant 消息

有时可以把最后一条消息写成 `assistant`，让模型从这段内容后继续生成。这种方式适合控制输出开头。

```python
response = client.messages.create(
    model=MODEL,
    max_tokens=500,
    messages=[
        {
            "role": "user",
            "content": "请生成一个用户信息 JSON，包含 name、age、city 三个字段。"
        },
        {
            "role": "assistant",
            "content": "{\n  \"name\":"
        }
    ]
)

print("{\n  \"name\":" + response.content[0].text)
```

这相当于告诉模型：助手已经输出了下面这段内容：

```json
{
  "name":
```

模型会从这个位置继续补全后面的内容。

这种方式的重点不是“让模型回答某个问题”，而是**把模型输出的起始部分固定住**。它常用于需要稳定输出格式的场景，例如：

| 场景             | 预填充内容示例       |
| -------------- | ------------- |
| 固定 JSON 开头     | `{\n "name":` |
| 固定 Markdown 标题 | `#`           |
| 固定标签结果         | `结果：`         |
| 固定代码块开头        | ```python     |
需要注意，预填充内容只是约束模型从某个前缀后继续生成，不等于严格保证完整 JSON 一定合法。正式项目中仍然需要对返回内容做解析和校验。

## 4、少样本提示

`messages`可以放入几组示例输入和示例输出，让模型按照示例模式处理新输入。

例如，希望模型判断用户反馈的类型，并且只返回`BUG`、`FEATURE` 或 `QUESTION`：

```python
response = client.messages.create(
    model=MODEL,
    max_tokens=100,
    temperature=0,
    messages=[
        {
            "role": "user",
            "content": "登录后页面一直空白，刷新也没用。"
        },
        {
            "role": "assistant",
            "content": "BUG"
        },

        {
            "role": "user",
            "content": "希望可以支持深色模式。"
        },
        {
            "role": "assistant",
            "content": "FEATURE"
        },

        {
            "role": "user",
            "content": "这个工具支持导出 PDF 吗？"
        },
        {
            "role": "assistant",
            "content": "QUESTION"
        },

        {
            "role": "user",
            "content": "点击保存按钮后提示成功，但重新打开数据没有了。"
        }
    ]
)

print(response.content[0].text)
```


输出可能是：

```text
BUG
```

这里前面的三组 `user` / `assistant` 消息不是普通聊天，而是在给模型提供示例：

```text
登录后页面空白              -> BUG
希望支持深色模式            -> FEATURE
询问是否支持导出 PDF         -> QUESTION
新的用户反馈                -> 按示例继续分类
```

少样本提示适合让模型输出更稳定、更标准化的结果。

对于分类类任务，通常可以把 `temperature` 设置得低一些，让结果更稳定。`temperature` 是一个数字参数，用来控制模型输出的随机性，取值范围为`0.0 ~ 1.0`。默认值是`1.0`。



# 五、消息列表的约束

`messages` 的结构需要符合对话顺序。一般情况下，列表从 `user` 消息开始，并按照 `user` / `assistant` 交替组织。

正确结构：

```python
messages = [
    {"role": "user", "content": "Hey there!"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user", "content": "Can you help me translate a word?"}
]
```

错误结构：

```python
messages = [
    {"role": "assistant", "content": "Hello there!"}
]
```

错误原因是第一条消息不能是 `assistant`。

另一个错误结构：

```python
messages = [
    {"role": "user", "content": "Hey there!"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "assistant", "content": "How can I help you?"}
]
```

错误原因是连续出现了两条 `assistant` 消息。


# 六、简单多轮聊天示例

下面示例用 `conversation_history` 保存本地对话历史。每轮用户输入后，把用户消息加入历史，再把完整历史发送给模型；模型返回后，再把助手响应追加回历史。

```python
from dotenv import load_dotenv  
from anthropic import Anthropic  
import os  
  
load_dotenv()  
  
client = Anthropic(  
    base_url=os.getenv("ANTHROPIC_BASE_URL"),  
    api_key=os.getenv("ANTHROPIC_API_KEY"),  
)  
  
MODEL = os.getenv("MODEL_ID")  
  
conversation_history = []  
  
while True:  
    user_input = input("用户：")  
  
    if user_input.lower() == "quit":  
        print("对话结束")  
        break  
  
    conversation_history.append({  
        "role": "user", "content": user_input  
    })  
  
    response = client.messages.create(  
        model=MODEL,  
        max_tokens=1000,  
        messages=conversation_history,  
    )  
  
    assistant_response = response.content[0].text  
    print(f"助手：{assistant_response}")  
  
    conversation_history.append({  
        "role": "assistant", "content": assistant_response  
    })
```

![[assets/Pasted image 20260611115750.png|300]]


结果演示：

![[assets/Pasted image 20260611115738.png|600]]


这个脚本能实现最基本的多轮对话，但还没有处理异常、历史裁剪、流式输出、超时和停止原因。正式项目中通常还需要根据 `usage` 和上下文窗口管理历史长度。

