# modules/listener.py
import speech_recognition as sr
import logging
from modules.triad import ask_triage

logger = logging.getLogger("Listener")

class ListenerModule:
    def __init__(self, event_bus=None):
        self.event_bus = event_bus
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.running = True

    def listen(self):
        """Listen for audio and return the transcribed text."""
        try:
            with self.microphone as source:
                logger.info("Listening for commands...")
                audio = self.recognizer.listen(source)

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
        """Run the listener loop on a separate thread."""
        while self.running:
            command = self.listen()
            if command:
                self.process_command(command)

    def process_command(self, command):
        """Process the recognized command."""
        if "triad" in command:
            message = command.split("triad", 1)[1].strip()
            if message == "help":
                help_message = ("Available commands are: describe the room, object detection, list folder, "
                                "create folder, read file, restart vm, get vm status.")
                self.event_bus.emit("speak", help_message)
            elif message:
                logger.info(f"TRIAD activated with: {message}")
                response = ask_triage(message)
                if isinstance(response, dict) and "error" in response:
                    self.event_bus.emit("speak", f"Error: {response['error']}")
                else:
                    description = response.get("description", "I couldn't describe that.")
                    self.event_bus.emit("speak", description)
            else:
                self.event_bus.emit("speak", "Yes, House?")
        else:
            logger.info(f"Ignored command: {command}")

    def shutdown(self):
        logger.info("Shutting down Listener Module...")
        self.running = False
