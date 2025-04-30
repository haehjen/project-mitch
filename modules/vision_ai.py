# modules/vision_ai.py
import openai
import os
import time
import base64
import requests
from modules.vision import VisionModule

# Initialize OpenAI client
client = openai.OpenAI(api_key="Open API Key")

# Imgur Client ID
imgur_client_id = "c9fbb400c7e9968"

class VisionAI:
    def __init__(self):
        self.vision_module = VisionModule()

    async def capture_and_describe(self):
        # Capture the image
        image_path = self.vision_module.capture_image()

        # Wait to ensure filesystem is flushed
        time.sleep(2)

        # Upload the image to Imgur
        image_url = self.upload_to_imgur(image_path)

        # Now ask OpenAI to describe it
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

        description = response.choices[0].message.content
        return description

    async def detect_objects(self):
        # Capture the image
        image_path = self.vision_module.capture_image()

        time.sleep(2)

        # Upload the image to Imgur
        image_url = self.upload_to_imgur(image_path)

        # Ask OpenAI to detect objects
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

        objects = response.choices[0].message.content
        return objects

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
            imgur_link = response.json()["data"]["link"]
            return imgur_link
        else:
            raise RuntimeError(f"Imgur upload failed: {response.text}")
