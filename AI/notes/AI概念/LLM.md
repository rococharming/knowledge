
# LLM：一种学会语言规律的模型


**LLM** 是 Large Language Model，中文即大语言模型。“语言”指它处理语言，“模型”指从数据中训练出来、能根据输入计算输出的系统。“大”通常描述模型规模，并没有一个适用于所有场合的固定门槛。

你可以把它暂时理解为：**通过大量训练，获得处理和生成语言能力的计算模型。** 训练让它学到语言表达、知识关联和一些任务规律。

例如，看它怎样把一段会议纪要变成待办：

输入：

```plain
会议纪要：小李负责修改首页文案，周五前完成。请整理成一条待办
```

输出：

```plain
待办：修改首页文案  
负责人：小李  
截止时间：周五前
```

模型把自然语言中的任务、负责人和时间组织成了结构化内容。因此，它能把这次没见过的会议纪要整理成待办。

# 训练和推理

对于 LLM，需要分开看两个时刻。

## 训练：形成能力

训练程序用大量数据和反馈调整模型内部的数值，也叫“参数”。模型逐渐学会语言和任务规律。

## 推理：使用能力

你提交会议纪要，系统运行已训练的模型，根据当前输入生成回答。这种运行称为“推理”（Inference）。

平时我们与大语言模型聊天时，使用的就是已经训练过的模型，并不会修改模型参数。

# 回答怎么生成？一步步生成

常见聊天语言模型会根据你的输入和已经生成的内容，计算后续文字片段的可能性，再逐步生成回答。这些片段就称为 [[AI/notes/AI概念/Token|Token]]，中文就是词元。

下图展示了一条待办是怎么逐步形成的：

![[assets/Pasted image 20260930153134.png|600]]


# 常见模型

| 模型家族 / 官方资料                                                                                        | 开发方                   | 代表型号示例                                                      |
| -------------------------------------------------------------------------------------------------- | --------------------- | ----------------------------------------------------------- |
| [**GPT**](https://developers.openai.com/api/docs/models/all)                                       | OpenAI                | GPT-6 Astra  <br>GPT-6.1 Sol  <br>GPT-6 Luna                |
| [**Claude**](https://platform.claude.com/docs/en/models/overview)                                  | Anthropic             | Claude Opus 5.5  <br>Claude Sonnet 5.5 <br>Claude Haiku 4.5 |
| [**Gemini**](https://ai.google.dev/gemini-api/docs/models)                                         | Google                | Gemini 3.8 Flash  <br>Gemini 3.1 Pro（预览）                    |
| [**DeepSeek**](https://api-docs.deepseek.com/quick_start/pricing/)                                 | DeepSeek              | DeepSeek-V4.1-Flash  <br>DeepSeek-V4-Pro                    |
| [**Qwen / 千问**](https://help.aliyun.com/zh/model-studio/models)                                    | 阿里巴巴                  | Qwen3.8-Max  <br>Qwen3.7-Plus  <br>Qwen3.8-Flash            |
| [**Kimi**](https://www.kimi.ai/ai-models/kimi-k3)                                                  | Moonshot AI  <br>月之暗面 | Kimi K3                                                     |
| [**GLM**](https://docs.bigmodel.cn/cn/guide/start/model-overview)                                  | 智谱 AI                 | GLM-5.3  <br>GLM-5.3-Flash                                  |
| [**Doubao / 豆包**](https://docs.volcengine.com/docs/ark/coding-plan-personal-model-release?lang=zh) | 字节跳动                  | Doubao-Seed-2.1-Pro  <br>Doubao-Seed-2.1-Lite               |
。

