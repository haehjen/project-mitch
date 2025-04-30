# modules/triad.py

import requests
import openai
import logging
import json

# Initialize OpenAI client (v1 syntax)
client = openai.OpenAI(api_key="Open Api Key")

dispatcher_url = "http://127.0.0.1:9000/dispatch"
logger = logging.getLogger("TRIAD")

# Tool definitions for GPT-4o function calling
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
            "parameters": {
                "type": "object",
                "properties": {}
            },
            "required": []
        }
    },
    {
        "type": "function",
        "function": {
            "name": "object_detection",
            "description": "Capture an image and detect objects using AI",
            "parameters": {
                "type": "object",
                "properties": {}
            },
            "required": []
        }
    }
]

def ask_triage(user_input: str):
    logger.info(f"Sending input to GPT-4o: {user_input}")

    try:
        chat_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are TRIAD, a helpful assistant for House. Use tools when appropriate to take action."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            tools=tools,
            tool_choice="auto"
        )

        choice = chat_response.choices[0]

        # If GPT-4 wants to call a function
        if choice.finish_reason == "tool_calls":
            tool_call = choice.message.tool_calls[0]
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            logger.info(f"Dispatching to: {function_name} with args: {arguments}")

            result = requests.post(dispatcher_url, json={
                "function_name": function_name,
                "args": arguments
            })

            if result.status_code == 200:
                return result.json()
            else:
                return {"error": f"Dispatcher error: {result.status_code} - {result.text}"}

        # Otherwise, just reply normally
        return {"description": choice.message.content}

    except Exception as e:
        logger.error(f"TRIAD failed: {e}")
        return {"description": f"Error: {e}"}
