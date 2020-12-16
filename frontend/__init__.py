#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
from abc import ABCMeta, abstractproperty, abstractmethod
import config

debug_image_location = config.properties.debug_image_location

import logging
from PIL import Image,ImageDraw
from threading import Lock
from typing import Callable

logging.basicConfig(level=logging.WARNING)

current_routine_state = {}

class Output(metaclass=ABCMeta):
    def __init__(self) -> None:
        super().__init__()
        self.lock = Lock()
    
    @abstractproperty
    def width(self) -> float:
        pass

    @abstractproperty
    def height(self) -> float:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def show(self, image):
        pass

    @abstractmethod
    def switch_backlight(self, on: bool):
        pass

class LcdDebug(Output):
    def __init__(self) -> None:
        super().__init__()

    @property
    def width(self) -> float:
        return 320

    @property
    def height(self) -> float:
        return 240

    def clear(self):
        pass

    def switch_backlight(self, on: bool):
        pass

    def show(self, image):
        with self.lock:
            image.save(f"{debug_image_location}/lcd-image-tmp.png")
            os.rename(f"{debug_image_location}/lcd-image-tmp.png", f"{debug_image_location}/lcd-image.png")

DISPLAYS = {
    "debug": LcdDebug()
}

class Canvas():
    def __init__(self, width, height, lock: Lock) -> None:
        super().__init__()

        self.width = width
        self.height = height
        self.lock = lock

        self.image = Image.new('RGB', (width, height), (255,255,255))
        self._draw = ImageDraw.Draw(self.image)

    def draw(self, do_draw: Callable[[ImageDraw.Draw], None]): 
        with self.lock:
            do_draw(self._draw)