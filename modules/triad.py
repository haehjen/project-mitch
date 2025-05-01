# modules/triad.py

import requests
import openai
import logging
import json
import os
from dotenv import load_dotenv
from core.event_bus import EventBus

# Init
load_dotenv("mitchskeys")
event_bus = EventBus()
logger = logging.getLogger("TRIAD")

# OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
dispatcher_url = "http://127.0.0.1:9000/dispatch"

# Tool definitions
tools = [
    {
        "type": "function",
        "function": {
            "name": "restart_vm",
            "description": "Restart a VM by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "vmid": {
                        "type": "integer",
                        "description": "The ID of the VM to restart"
                    }
                },
                "required": ["vmid"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_vm_status",
            "description": "Get the status of a VM by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "vmid": {
                        "type": "integer",
                        "description": "The ID of the VM"
                    }
                },
                "required": ["vmid"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "capture_and_describe",
            "description": "Capture an image and generate a description using AI",
            "parameters": {"type": "object", "properties": {}},
            "required": []
        }
    },
    {
        "type": "function",
        "function": {
            "name": "object_detection",
            "description": "Capture an image and detect objects using AI",
            "parameters": {"type": "object", "properties": {}},
            "required": []
        }
    }
]

def handle_triage(user_input: str):
    logger.info(f"Sending to GPT-4o: {user_input}")

    try:
        chat_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are TRIAD, a helpful assistant for House. Use tools when appropriate."},
                {"role": "user", "content": user_input}
            ],
            tools=tools,
            tool_choice="auto"
        )

        choice = chat_response.choices[0]

        if choice.finish_reason == "tool_calls":
            tool_call = choice.message.tool_calls[0]
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            logger.info(f"Dispatching tool: {function_name} with args: {arguments}")
            event_bus.emit("dispatch", {"function_name": function_name, "args": arguments})

        else:
            event_bus.emit("speak", choice.message.content)

    except Exception as e:
        logger.error(f"TRIAD failed: {e}")
        event_bus.emit("speak", f"Error: {e}")

# Hook into the bus
event_bus.subscribe("triad_request", handle_triage)
