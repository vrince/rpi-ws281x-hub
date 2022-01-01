import time
from abc import ABC, abstractmethod
from colour import Color as C
import random
from enum import Enum

from strip import ColorPixelStrip


class colorFire():
    def __init__(self, strip: ColorPixelStrip, **kwargs):
        self.strip = strip
        colors = kwargs.get('colors', ['orange', 'red'])
        self.colors = list(C(colors[0]).range_to(C(colors[1]), 100))

    def __call__(self, ratio: float):
        i = int(random.uniform(0, self.strip.numPixels()))
        c = self.colors[int(random.uniform(0, len(self.colors)))]
        intensity = random.uniform(0, 1)
        color = C(rgb=tuple([e * intensity for e in c.rgb]))
        self.strip.setPixelRGB(i, color)
        self.strip.show()


class colorRaindow():
    def __init__(self, strip: ColorPixelStrip, **kwargs):
        self.strip = strip
        self.colors = list(C('#FF0000').range_to(C('#00FFFE'), 128))
        self.colors += list(C('#00FFFF').range_to(C('#FF0001'), 128))

    def __call__(self, ratio: float):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelRGB(i, self.colors[int(ratio*255)])
        self.strip.show()


class TaskName(str, Enum):
    fire = "fire"
    rainbow = "rainbow"


class TaskFactory():
    def __init__(self, strip: ColorPixelStrip):
        self.strip = strip

    def get(self, name: str, **kwargs):
        print(name, kwargs)
        if name == 'fire':
            return colorFire(self.strip, **kwargs)
        elif name == 'rainbow':
            return colorRaindow(self.strip, **kwargs)
        else:
            return None
