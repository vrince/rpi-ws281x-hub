import time
from abc import ABC, abstractmethod
from colour import Color as C
import random
from enum import Enum

from strip import ColorPixelStrip


class colorFire():
    def __init__(self, strip: ColorPixelStrip, from_color='orange', to_color='red'):
        self.strip = strip
        self.colors = list(C(from_color).range_to(C(to_color), 100))

    def __call__(self, ratio: float):
        i = int(random.uniform(0, self.strip.numPixels()))
        c = self.colors[int(random.uniform(0, len(self.colors)))]
        intensity = random.uniform(0, 1)
        color = C(rgb=tuple([e * intensity for e in c.rgb]))
        self.strip.setPixelRGB(i, color)
        self.strip.show()


class colorRaindow():
    def __init__(self, strip: ColorPixelStrip):
        self.strip = strip
        self.colors = list(C('red').range_to(C('blue'), 128))
        self.colors += list(C('blue').range_to(C('red'), 128))

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
        if name == 'fire':
            return colorFire(self.strip, **kwargs)
        elif name == 'rainbow':
            return colorRaindow(self.strip, **kwargs)
        else:
            return None
