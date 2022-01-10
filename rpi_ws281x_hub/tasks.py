import time
from abc import ABC, abstractmethod
from colour import Color as C
import random
from enum import Enum
from pydantic import BaseModel
from easing_functions import *

from strip import ColorPixelStrip

RAINBOW = list(C('#FF0000').range_to(C('#00FFFE'), 128)) + list(C('#00FFFF').range_to(C('#FF0001'), 128))
STAR = list(C('yellow').range_to(C('white'), 128))

def task(func):
    """task decorator (wrap `__call__` method of tasks)

    Returns:
        actual color array of the strip
    """
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return [ self.strip.getPixelRGB(i).hex for i in range(self.strip.numPixels()) ]
    return wrapper

class Fire():
    def __init__(self, strip: ColorPixelStrip, **kwargs):
        self.strip = strip
        colors = kwargs.get('colors', ['orange', 'red'])
        self.colors = [C(color) for color in colors]

    @task
    def __call__(self, ratio: float):
        i = int(random.uniform(0, self.strip.numPixels()))
        c = self.colors[int(random.uniform(0, len(self.colors)))]
        intensity = random.uniform(0, 1)
        color = C(rgb=tuple([e * intensity for e in c.rgb]))
        self.strip.setPixelRGB(i, color)
        self.strip.show()


class Raindow():
    def __init__(self, strip: ColorPixelStrip, **kwargs):
        self.strip = strip

    @task
    def __call__(self, ratio: float):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelRGB(i, RAINBOW[int(ratio*255)])
        self.strip.show()


class RaindowChase():
    def __init__(self, strip: ColorPixelStrip, **kwargs):
        self.strip = strip
        self.index = 0

    def __call__(self, ratio: float):
        d = int(ratio*255)
        rotateColors = RAINBOW[d:255] + RAINBOW[0:d]
        for i in range(self.strip.numPixels()):
            self.strip.setPixelRGB(i, rotateColors[int((i/self.strip.numPixels())*255)])
        self.strip.show()


class RaindowChase():
    def __init__(self, strip: ColorPixelStrip, **kwargs):
        self.strip = strip
        self.index = 0

    @task
    def __call__(self, ratio: float):
        d = int(ratio*255)
        rotateColors = RAINBOW[d:255] + RAINBOW[0:d]
        for i in range(self.strip.numPixels()):
            self.strip.setPixelRGB(i, rotateColors[int((i/self.strip.numPixels())*255)])
        self.strip.show()

class FallingStars():

    def __init__(self, strip: ColorPixelStrip, **kwargs):
        self.strip = strip
        self.count = int(random.uniform(2, 4))
        self.positions = random.choices( list(range(self.strip.numPixels())), k=self.count)
        self.speeds = [random.uniform(-1, 1) for s in range(self.count)]
        self.colors = random.choices( STAR, k=self.count)
        print(self.count, self.positions, self.speeds, self.colors)

    @task
    def __call__(self, ratio: float):
        numPixels = self.strip.numPixels()
        for i in range(self.strip.numPixels()):
            self.strip.setPixelRGB(i, C(rgb=tuple([e * 0.75 for e in self.strip.getPixelRGB(i).rgb])))
        for i in range(self.count):
            self.positions[i] += self.speeds[i]
            self.positions[i] = self.positions[i] - numPixels if self.positions[i] > numPixels else self.positions[i]
            self.positions[i] = self.positions[i] + numPixels if self.positions[i] < 0 else self.positions[i]
            self.strip.setPixelRGB(int(self.positions[i]), self.colors[i])
        self.strip.show()

class ColorWheel():
    def __init__(self, strip: ColorPixelStrip, **kwargs):
        self.strip = strip
        self.colors = random.choices(RAINBOW, k=6)
        self.color = random.choice(self.colors)
        self.easing = CubicEaseInOut()

    @task
    def __call__(self, ratio: float):
        r = self.easing(ratio if ratio < 0.5 else 1 - ratio)
        if r < 0.01:
            self.color = random.choice(self.colors)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelRGB(i, C(rgb=tuple([e * r for e in self.color.rgb])))
        self.strip.show()

class Sparkles():
    def __init__(self, strip: ColorPixelStrip, **kwargs):
        self.strip = strip

    @task
    def __call__(self, ratio: float):
        numPixels = self.strip.numPixels()
        for i in range(self.strip.numPixels()):
            self.strip.setPixelRGB(i, C(rgb=tuple([e * 0.75 for e in self.strip.getPixelRGB(i).rgb])))
        if random.choice(range(10)) < 2:
            index = random.choice(range(numPixels))
            color = random.choice(STAR)
            self.strip.setPixelRGB(index, color)
        self.strip.show()


class TaskName(str, Enum):
    fire = "fire"
    rainbow = "rainbow"
    rainbowChase = "rainbowChase"
    fallingStars = "fallingStars"
    colorWheel = "colorWheel"
    sparkles = "sparkles"


class TaskFactory():
    def __init__(self, strip: ColorPixelStrip):
        self.strip = strip

    def get(self, name: str, **kwargs):
        print(name, kwargs)
        if name == 'fire':
            return Fire(self.strip, **kwargs)
        elif name == 'rainbow':
            return Raindow(self.strip, **kwargs)
        elif name == 'rainbowChase':
            return RaindowChase(self.strip, **kwargs)
        elif name == 'fallingStars':
            return FallingStars(self.strip, **kwargs)
        elif name == 'colorWheel':
            return ColorWheel(self.strip, **kwargs)
        elif name == 'sparkles':
            return Sparkles(self.strip, **kwargs)
        else:
            return None
