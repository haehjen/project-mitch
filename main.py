import threading
import time
from core.event_bus import EventBus
from modules.tts import TTSModule
from modules.listener import ListenerModule
from modules.folder_access import FolderAccessModule
from modules.proxmon import ProxMonModule
from modules.weather import WeatherModule

def main():
    print("Starting MITCH...")
    event_bus = EventBus()

    tts_module = TTSModule(event_bus)
    listener_module = ListenerModule(event_bus)
    folder_access_module = FolderAccessModule(event_bus)
    proxmon_module = ProxMonModule(event_bus)
    weather_module = WeatherModule(event_bus)

    modules = [tts_module, listener_module, proxmon_module, weather_module]
    threads = []

    for module in modules:
        thread = threading.Thread(target=module.run, daemon=True)
        threads.append(thread)
        thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutdown requested...exiting.")
        for module in modules:
            module.shutdown()

if __name__ == "__main__":
    main()