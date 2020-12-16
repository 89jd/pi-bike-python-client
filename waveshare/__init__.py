import config
import sys

if hasattr(config.properties, 'waveshare_lib_dir'):
    sys.path.append(config.properties.waveshare_lib_dir)
    
    from waveshare_2inch_LCD import ST7789
    from waveshare_2inch_LCD.config import RaspberryPi
    import RPi.GPIO as GPIO
    from frontend import Output, DISPLAYS
    from threading import Lock

    class WaveshareST7789(Output):
        def __init__(self) -> None:
            super().__init__()
            self.lock = Lock()
            self.disp = ST7789.ST7789()
            
            self.disp.Init()
        
        @property
        def width(self) -> float:
            return self.disp.height

        @property
        def height(self) -> float:
            return self.disp.width

        def clear(self):
            self.disp.clear()

        def show(self, image):
            with self.lock:
                self.disp.ShowImage(image)

        def switch_backlight(self, on: bool):
            GPIO.output(RaspberryPi.BL_PIN, 1 if on else 0)

    DISPLAYS["ST7789"] = WaveshareST7789()