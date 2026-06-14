from dotenv import load_dotenv
from anthropic import Anthropic
import os


load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN")
if not api_key:
    raise RuntimeError("请设置 ANTHROPIC_AUTH_TOKEN 或 ANTHROPIC_API_KEY 环境变量")

client = Anthropic(
    base_url=os.getenv("ANTHROPIC_BASE_URL"),
    api_key=api_key,
)

model = os.getenv("MODEL_ID")


stream = client.messages.create(
    model=model,
    max_tokens=800,
    temperature=0,
    messages=[
        {
            "role": "user",
            "content": "请写一篇关于大型语言模型流式输出的短文，说明它是什么、为什么有用，以及适合哪些应用场景。"
        }
    ],
    stream=True
)

for event in stream:
    if event.type == "message_start":
        print(f"input tokens: {event.message.usage.input_tokens}")
        print("=========================")
    elif event.type == "content_block_delta":
        print(event.delta.text, flush=True, end="")
    elif event.type == "message_delta":
        print("\n=========================")
        print(f"output tokens: {event.usage.output_tokens}")

