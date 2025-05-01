# modules/listener.py

import speech_recognition as sr
import logging

logger = logging.getLogger("Listener")

class ListenerModule:
    def __init__(self, event_bus=None):
        self.event_bus = event_bus
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.running = True

    def listen(self):
        try:
            with self.microphone as source:
                logger.info("Listening for commands...")
                audio = self.recognizer.listen(source)
                logger.info("Captured audio")

            command = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized command: {command}")
            return command.lower()

        except sr.UnknownValueError:
            logger.warning("Could not understand audio.")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service failed; {e}")
            return None

    def run(self):
        while self.running:
            command = self.listen()
            if command:
                self.process_command(command)

    def process_command(self, command):
        if self.event_bus:
            logger.info(f"Emitting speech_input: {command}")
            self.event_bus.emit("speech_input", command)
        else:
            logger.warning("No event bus available to emit command.")

    def shutdown(self):
        logger.info("Shutting down Listener Module...")
        self.running = False
