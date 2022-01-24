import os
import time
import random
import json

from pydantic import BaseModel

from timeit import default_timer as timer

from colour import Color as C

from rpi_ws281x import *

class ColorPixelStripConfig(BaseModel):
    num: int = 12
    pin: int = 18
    freq_hz: int = 800000
    dma: int = 10
    invert: bool = False
    brightness: int = 255
    channel: int = 0
    strip_type: int = None
    gamma: int = None

class ColorPixelStrip(PixelStrip):
    def __init__(self, config: ColorPixelStripConfig = ColorPixelStripConfig()):
        super().__init__(config.num, config.pin, config.freq_hz, config.dma,
                         config.invert, config.brightness, config.channel,
                         config.strip_type, config.gamma)
        self.config = config

    def clear(self):
        for i in range(self.numPixels()):
            self.setPixelRGB(i, C('black'))
        self.show()

    def brighteness(value=0.5):
        value = int(max(0, min(value, 1)) * 255)
        self.setBrightness(value)
        self.show()

    def getConfig(self):
        return self.config

    def setPixelRGB(self, n, color):
        rgb = tuple([int(c * 255) for c in color.rgb])
        self.setPixelColor(n, Color(*rgb))

    def getPixelRGB(self, n):
        return C(rgb=((self._led_data[n] >> 16 & 0xff) / 255,
                      (self._led_data[n] >> 8 & 0xff) / 255,
                      (self._led_data[n] & 0xff) / 255))

