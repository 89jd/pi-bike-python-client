from typing import Callable
import socketio
import config

class SocketClient():
    def __init__(self) -> None:
        super().__init__()

        self.on_exercise_data_received: Callable[[dict], None] = None
        self.on_duration_received: Callable[[int], None] = None
        self.on_idle_received: Callable[[bool], None] = None
        
        sio = socketio.Client()
        
        self.sio = sio
        
        @sio.event
        def exercise_data(data):
            self.on_exercise_data_received(data)

        @sio.event
        def idle_state(is_idle):
            self.on_idle_received(is_idle)
            
        @sio.event
        def duration(duration):
            self.on_duration_received(duration)

    def emit(self, event: str):
        self.sio.emit(event)

    def start(self):
        self.sio.connect(config.properties.server_address)
