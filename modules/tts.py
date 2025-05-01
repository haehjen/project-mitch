# modules/tts.py
import time
import pyttsx3
from core.logger import setup_logger

logger = setup_logger("TTS")

class TTSModule:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        self.running = True

        # Set British voice if available
        for voice in self.engine.getProperty('voices'):
            if 'english' in voice.id.lower() and 'gb' in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                break

        # Subscribe to TTS events
        self.event_bus.subscribe("speak", self.handle_speak)

    def handle_speak(self, message):
        logger.info(f"Speaking: {message}")
        self.engine.say(message)
        self.engine.runAndWait()

    def run(self):
        while self.running:
            time.sleep(0.5)

    def shutdown(self):
        logger.info("Shutting down TTS module")
        self.running = False