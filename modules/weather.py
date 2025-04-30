# modules/weather.py
from core.module_base import ModuleBase
import time

class WeatherModule(ModuleBase):
    def __init__(self, event_bus):
        super().__init__("WeatherModule", event_bus)
        self.running = True  # <-- ADD THIS

    def run(self):
        self.logger.info("Weather module online.")
        while self.running:
            time.sleep(10)

    def shutdown(self):
        self.logger.info("Shutting down Weather Module.")
        self.running = False
