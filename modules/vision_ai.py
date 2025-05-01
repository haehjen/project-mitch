# modules/vision_ai.py

import openai
import os
import time
import base64
import requests
from modules.vision import VisionModule
from dotenv import load_dotenv

# Load secrets
load_dotenv(dotenv_path="mitchskeys")

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Imgur Client ID
imgur_client_id = os.getenv("IMGUR_CLIENT_ID")

class VisionAI:
    def __init__(self):
        self.vision_module = VisionModule()

    async def capture_and_describe(self):
        image_path = self.vision_module.capture_image()
        time.sleep(2)
        image_url = self.upload_to_imgur(image_path)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Please describe this image."},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
            max_tokens=800,
            temperature=0.7
        )

        return response.choices[0].message.content

    async def detect_objects(self):
        image_path = self.vision_module.capture_image()
        time.sleep(2)
        image_url = self.upload_to_imgur(image_path)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Please list all objects you can see."},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
            max_tokens=800,
            temperature=0.7
        )

        return response.choices[0].message.content

    def upload_to_imgur(self, image_path):
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read())

        headers = {
            "Authorization": f"Client-ID {imgur_client_id}"
        }
        data = {
            "image": image_data,
            "type": "base64"
        }

        response = requests.post("https://api.imgur.com/3/image", headers=headers, data=data)

        if response.status_code == 200:
            return response.json()["data"]["link"]
        else:
            raise RuntimeError(f"Imgur upload failed: {response.text}")
