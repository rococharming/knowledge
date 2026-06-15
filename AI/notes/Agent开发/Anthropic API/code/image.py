import requests
from dotenv import load_dotenv
from anthropic import Anthropic
import os
import base64
import mimetypes
from pathlib import Path
import httpx
from urllib.parse import urlparse




load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN")
if not api_key:
    raise RuntimeError("请设置 ANTHROPIC_AUTH_TOKEN 或 ANTHROPIC_API_KEY 环境变量")

client = Anthropic(
    base_url=os.getenv("ANTHROPIC_BASE_URL"),
    api_key=api_key,
)

model = os.getenv("MODEL_ID")

def create_image_message(image_path: str) -> dict:
    path = Path(image_path)

    with path.open("rb") as image_file:
        binary_data = image_file.read()

    base64_string = base64.b64encode(binary_data).decode("utf-8")
    mime_type, _ = mimetypes.guess_type(path)

    if mime_type == None:
        raise ValueError(f"Cannot determine MIME type for image: {image_path}")

    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": mime_type,
            "data": base64_string,
        }
    }

def get_image_dict_from_url(image_url: str) -> dict:

    response = httpx.get(image_url)
    response.raise_for_status()

    mime_type = response.headers.get("content-type")

    if mime_type:
        mime_type = mime_type.split(";")[0].strip()
    else:
        path = urlparse(image_url).path
        mime_type, _ = mimetypes.guess_type(path)

    if mime_type not in {"image/jpeg", "image/png", "image/gif", "image/webp"}:
        raise ValueError(f"Unsupported or unknown image MIME type: {mime_type}")

    base64_string = base64.b64encode(response.content).decode("utf-8")

    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": mime_type,
            "data": base64_string,
        },
    }



response = client.messages.create(
    model=model,
    max_tokens=800,
    messages=[
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "图像1：" },
                get_image_dict_from_url("https://www.wikihow.com/images/thumb/e/e9/Draw-Pikachu-Step-14.jpg/v4-728px-Draw-Pikachu-Step-14.jpg"),
                { "type": "text", "text": "图像2：" },
                get_image_dict_from_url("https://preview.redd.it/what-makes-pikachu-an-amazing-mascot-v0-bf4hcwmio6vg1.jpg?width=640&crop=smart&auto=webp&s=636ffada5a470c4b18202873815b8798061b5899"),
                {
                    "type": "text",
                    "text": "请识别每张图片的宝可梦是什么"
                }
            ]
        }
    ]
)


print(response.content[0].text)


