from config import properties
from typing import Callable

class ButtonSensor():
    def __init__(self, pin_and_mode_pairs, on_pin: Callable[[int], None]) -> None:
        import RPi.GPIO as GPIO
        for button in pin_and_mode_pairs:
            if button.mode == 'pull_up':
                GPIO.setup(button.pin, GPIO.IN, GPIO.PUD_UP)
                GPIO.add_event_detect(button.pin, GPIO.RISING, lambda _: on_pin(button.pin), bouncetime=300)
            elif button.mode == 'pull_down':
                GPIO.setup(button.pin, GPIO.IN, GPIO.PUD_DOWN)
                GPIO.add_event_detect(button.pin, GPIO.FALLING, lambda _: on_pin(button.pin), bouncetime=300)
