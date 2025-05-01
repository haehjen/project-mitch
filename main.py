# main.py

import threading
import signal
import sys
import logging
from core.event_bus import EventBus
from modules.listener import ListenerModule
from modules.tts import TTSModule

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
)

# Load event-driven modules (each subscribes to EventBus)
import modules.interpreter
import modules.triad
import core.dispatcher
import modules.proxmon

def main():
    event_bus = EventBus()

    # Start TTS
    tts = TTSModule(event_bus)
    tts_thread = threading.Thread(target=tts.run, daemon=True)
    tts_thread.start()

    # Start Listener
    listener = ListenerModule(event_bus)
    listener_thread = threading.Thread(target=listener.run, daemon=True)
    listener_thread.start()

    # Handle Ctrl+C clean shutdown
    def shutdown_handler(sig, frame):
        print("\n[MITCH] Shutting down cleanly...")
        listener.shutdown()
        tts.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)

    print("MITCH 1.0 event-driven system online. Press Ctrl+C to exit.")
    listener_thread.join()

if __name__ == "__main__":
    main()
