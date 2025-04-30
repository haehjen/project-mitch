from core.logger import setup_logger

class ModuleBase:
    def __init__(self, name, event_bus):
        self.name = name
        self.event_bus = event_bus
        self.logger = setup_logger(name)

    def run(self):
        raise NotImplementedError

    def shutdown(self):
        self.logger.info("Shutting down")