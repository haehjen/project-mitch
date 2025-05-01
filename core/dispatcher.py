# core/dispatcher.py

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from modules.vision_ai import VisionAI
from modules.vision import VisionModule
from modules.proxmon import ProxMonModule
from core.event_bus import EventBus
import threading
import logging
import os
import asyncio

app = FastAPI()
logger = logging.getLogger("Dispatcher")

# Init
os.makedirs("/tmp", exist_ok=True)
app.mount("/static", StaticFiles(directory="/tmp"), name="static")

event_bus = EventBus()
vision_ai = VisionAI()
vision_module = VisionModule()
proxmon = ProxMonModule(event_bus)

# Start ProxMon polling thread
proxmon_thread = threading.Thread(target=proxmon.run, daemon=True)
proxmon_thread.start()

# HTTP fallback (still usable)
@app.post("/dispatch")
async def dispatch_api(request: Request):
    data = await request.json()
    return await dispatch_router(data)

# Main dispatch logic
async def dispatch_router(data):
    logger.info(f"Dispatching from event bus: {data}")
    function_name = data.get("function_name")
    args = data.get("args", {})

    try:
        if function_name == "capture_and_describe":
            description = await vision_ai.capture_and_describe()
            event_bus.emit("speak", description)
            return {"description": description}

        elif function_name == "object_detection":
            objects = await vision_ai.detect_objects()
            event_bus.emit("speak", objects)
            return {"objects": objects}

        elif function_name == "restart_vm":
            vmid = args.get("vmid")
            if vmid is not None:
                result = proxmon.restart_vm(vmid)
                event_bus.emit("speak", result)
                return {"result": result}
            else:
                return {"error": "Missing vmid"}

        elif function_name == "get_vm_status":
            vmid = args.get("vmid")
            if vmid is not None:
                status = proxmon.get_vm_status(vmid)
                event_bus.emit("speak", str(status))
                return {"status": status}
            else:
                return {"error": "Missing vmid"}

        else:
            return {"error": f"Unknown function: {function_name}"}

    except Exception as e:
        logger.error(f"Dispatch failed: {e}")
        event_bus.emit("speak", f"Dispatch error: {e}")
        return {"error": str(e)}

# Called from interpreter or TRIAD via EventBus
def handle_dispatch_event(payload):
    try:
        asyncio.run(dispatch_router(payload))
    except Exception as e:
        logger.error(f"Error in dispatch thread: {e}")

event_bus.subscribe("dispatch", handle_dispatch_event)
# core/dispatcher.py

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from modules.vision_ai import VisionAI
from modules.vision import VisionModule
from modules.proxmon import ProxMonModule
from core.event_bus import EventBus
import threading
import logging
import os
import asyncio

app = FastAPI()
logger = logging.getLogger("Dispatcher")

# Init
os.makedirs("/tmp", exist_ok=True)
app.mount("/static", StaticFiles(directory="/tmp"), name="static")

event_bus = EventBus()
vision_ai = VisionAI()
vision_module = VisionModule()
proxmon = ProxMonModule(event_bus)

# Start ProxMon polling thread
proxmon_thread = threading.Thread(target=proxmon.run, daemon=True)
proxmon_thread.start()

# HTTP fallback (still usable)
@app.post("/dispatch")
async def dispatch_api(request: Request):
    data = await request.json()
    return await dispatch_router(data)

# Main dispatch logic
async def dispatch_router(data):
    logger.info(f"Dispatching from event bus: {data}")
    function_name = data.get("function_name")
    args = data.get("args", {})

    try:
        if function_name == "capture_and_describe":
            description = await vision_ai.capture_and_describe()
            event_bus.emit("speak", description)
            return {"description": description}

        elif function_name == "object_detection":
            objects = await vision_ai.detect_objects()
            event_bus.emit("speak", objects)
            return {"objects": objects}

        elif function_name == "restart_vm":
            vmid = args.get("vmid")
            if vmid is not None:
                result = proxmon.restart_vm(vmid)
                event_bus.emit("speak", result)
                return {"result": result}
            else:
                return {"error": "Missing vmid"}

        elif function_name == "get_vm_status":
            vmid = args.get("vmid")
            if vmid is not None:
                status = proxmon.get_vm_status(vmid)
                event_bus.emit("speak", str(status))
                return {"status": status}
            else:
                return {"error": "Missing vmid"}

        else:
            return {"error": f"Unknown function: {function_name}"}

    except Exception as e:
        logger.error(f"Dispatch failed: {e}")
        event_bus.emit("speak", f"Dispatch error: {e}")
        return {"error": str(e)}

# Called from interpreter or TRIAD via EventBus
def handle_dispatch_event(payload):
    try:
        asyncio.run(dispatch_router(payload))
    except Exception as e:
        logger.error(f"Error in dispatch thread: {e}")

event_bus.subscribe("dispatch", handle_dispatch_event)
