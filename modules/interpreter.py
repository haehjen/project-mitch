# modules/interpreter.py

import re
import logging
from core.event_bus import EventBus

logger = logging.getLogger("Interpreter")
event_bus = EventBus()

def extract_number(text):
    match = re.search(r"\b\d+\b", text)
    return int(match.group()) if match else None

def handle_input(command):
    logger.info(f"Interpreter received: {command}")
    command = command.strip().lower()

    if command in ("help", "what can you do"):
        logger.info("Matched help command")
        help_text = (
            "You can say things like: restart vm 105, get vm status 105, describe the room, "
            "list objects, or ask general questions."
        )
        event_bus.emit("speak", help_text)

    elif command.startswith("restart vm"):
        vmid = extract_number(command)
        if vmid:
            logger.info(f"Matched restart_vm for vmid: {vmid}")
            event_bus.emit("dispatch", {
                "function_name": "restart_vm",
                "args": {"vmid": vmid}
            })
        else:
            logger.warning("Restart command received but no VM ID found")
            event_bus.emit("speak", "I didn't catch the VM ID.")

    elif command.startswith("get vm status"):
        vmid = extract_number(command)
        if vmid:
            logger.info(f"Matched get_vm_status for vmid: {vmid}")
            event_bus.emit("dispatch", {
                "function_name": "get_vm_status",
                "args": {"vmid": vmid}
            })
        else:
            logger.warning("Get status command received but no VM ID found")
            event_bus.emit("speak", "I didn't catch the VM ID.")

    elif "describe the room" in command:
        logger.info("Matched 'describe the room'")
        event_bus.emit("dispatch", {
            "function_name": "capture_and_describe",
            "args": {}
        })

    elif "list objects" in command or "object detection" in command:
        logger.info("Matched object detection command")
        event_bus.emit("dispatch", {
            "function_name": "object_detection",
            "args": {}
        })

    else:
        logger.info("Passing to TRIAD as unknown command")
        event_bus.emit("triad_request", command)

event_bus.subscribe("speech_input", handle_input)
