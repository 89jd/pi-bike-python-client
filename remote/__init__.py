import evdev
import threading
import time

class RemoteControlThread(threading.Thread):
    def __init__(self, device_id:str, on_key, debug: bool = False) -> None:
        super().__init__(daemon=True)
        self.device_id = device_id
        self.on_key = on_key
        self.debug = debug

    def print_debug_log(self, s: str):
        if self.debug:
            print(s)

    def run(self) -> None:
        while True:
            try:
                device = evdev.InputDevice(self.device_id)
                self.print_debug_log('Input device found')
                for event in device.read_loop():
                    if event.type == evdev.ecodes.EV_KEY:
                        self.on_key(event.code, event.value)
            except FileNotFoundError:
                if self.debug:
                    self.print_debug_log('Input device not found')
                time.sleep(1)


if __name__ == "__main__":
    RemoteControlThread(print).start()
    while True:
        time.sleep(1)
