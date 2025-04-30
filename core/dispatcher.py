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

app = FastAPI()
logger = logging.getLogger("dispatcher")

# Ensure /tmp exists for captured images
os.makedirs("/tmp", exist_ok=True)

# Serve /tmp/ folder as /static
app.mount("/static", StaticFiles(directory="/tmp"), name="static")

# Initialize modules
event_bus = EventBus()
vision_ai = VisionAI()
vision_module = VisionModule()
proxmon = ProxMonModule(event_bus)

# Start ProxMon polling in a background thread
proxmon_thread = threading.Thread(target=proxmon.run, daemon=True)
proxmon_thread.start()

@app.post("/dispatch")
async def dispatch(request: Request):
    data = await request.json()
    logger.info(f"Dispatcher received data: {data}")

    function_name = data.get("function_name")
    args = data.get("args", {})

    if function_name == "capture_and_describe":
        return await capture_and_describe(args)
    elif function_name == "object_detection":
        return await object_detection(args)
    elif function_name == "restart_vm":
        return await restart_vm(args)
    elif function_name == "get_vm_status":
        return await get_vm_status(args)
    else:
        return {"error": f"Unknown function: {function_name}"}

# Vision tools
async def capture_and_describe(args):
    description = await vision_ai.capture_and_describe()
    return {"description": description}

async def object_detection(args):
    objects = await vision_ai.detect_objects()
    return {"objects": objects}

# ProxMon / VM management
async def restart_vm(args):
    vmid = args.get("vmid")
    if not vmid:
        return {"error": "Missing vmid"}

    result = proxmon.restart_vm(vmid)
    return {"description": f"Restarted VM {vmid}. Result: {result}"}

async def get_vm_status(args):
    vmid = args.get("vmid")
    if not vmid:
        return {"error": "Missing vmid"}

    status = proxmon.get_vm_status(vmid)
    return {"status": status}
