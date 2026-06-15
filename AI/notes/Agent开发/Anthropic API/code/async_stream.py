from anthropic import AsyncAnthropic
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN")
if not api_key:
    raise RuntimeError("请设置 ANTHROPIC_AUTH_TOKEN 或 ANTHROPIC_API_KEY 环境变量")

model = os.getenv("MODEL_ID")

client = AsyncAnthropic(
    base_url=os.getenv("ANTHROPIC_BASE_URL"),
    api_key=api_key
)

blue = "\033[34m"
reset = "\033[0m"





async def streaming_with_helpers():
    async with client.messages.stream(
        max_tokens=800,
        model=model,
        messages=[
            {
                "role": "user",
                "content": "请写一篇关于大型语言模型流式输出的短文，说明它是什么、为什么有用，以及适合哪些应用场景。"
            }
        ]
    ) as stream:
        async for event in stream:
            if event.type == "content_block_delta":
                print(blue + event.delta.text + reset, end="", flush=True)


    final_message = await stream.get_final_message()
    print("\n\nSTREAMING IS DONE. FINAL MESSAGE:")
    print(final_message.to_json())


if __name__ == "__main__":
    asyncio.run(streaming_with_helpers())