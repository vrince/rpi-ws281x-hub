import time
from abc import ABC, abstractmethod
from colour import Color as C
import random
from enum import Enum
import math
from operator import add
from pydantic import BaseModel
from easing_functions import *

from rpi_ws281x_hub.strip import ColorPixelStrip

RAINBOW = list(C('#FF0000').range_to(C('#00FFFE'), 128)) + list(C('#00FFFF').range_to(C('#FF0001'), 128))
STAR = list(C('yellow').range_to(C('white'), 128))
WAVE = list(C('blue').range_to(C('cyan'), 128))

def roll_index(position, max_position):
    if position > max_position:
        return position - max_position
    elif position < 0:
        return position + max_position
    return position


def dim_color(color, intensity):
    return C(rgb=tuple([max(0,min(e * intensity,1)) for e in color.rgb]))


def rotate(array, position):
    return array[position:len(array)] + array[0:position]


def add_color(c1, c2):
    color = list(map(add, c1.rgb, c2.rgb))
    return C(rgb=tuple([max(0,min(e,1)) for e in color]))


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
        rotate_colors = RAINBOW[d:255] + RAINBOW[0:d]
        for i in range(self.strip.numPixels()):
            self.strip.setPixelRGB(i, rotate_colors[int((i/self.strip.numPixels())*255)])
        self.strip.show()


class RaindowChase():
    def __init__(self, strip: ColorPixelStrip, **kwargs):
        self.strip = strip
        self.index = 0

    @task
    def __call__(self, ratio: float):
        d = int(ratio*255)
        rotate_colors = RAINBOW[d:255] + RAINBOW[0:d]
        for i in range(self.strip.numPixels()):
            self.strip.setPixelRGB(i, rotate_colors[int((i/self.strip.numPixels())*255)])
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
            self.strip.setPixelRGB(i,dim_color(self.strip.getPixelRGB(i), 0.75))
        for i in range(self.count):
            self.positions[i] += self.speeds[i]
            self.positions[i] = roll_index(self.positions[i],numPixels)
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
            self.strip.setPixelRGB(i, dim_color(self.color,r))
        self.strip.show()


class Sparkles():
    def __init__(self, strip: ColorPixelStrip, **kwargs):
        self.strip = strip

    @task
    def __call__(self, ratio: float):
        numPixels = self.strip.numPixels()
        for i in range(numPixels):
            self.strip.setPixelRGB(i, dim_color(self.strip.getPixelRGB(i), 0.75))
        if random.choice(range(10)) < 2:
            index = random.choice(range(numPixels))
            color = random.choice(STAR)
            self.strip.setPixelRGB(index, color)
        self.strip.show()


class RainbowStar():
    def __init__(self, strip: ColorPixelStrip, **kwargs):
        self.strip = strip
        num = self.strip.numPixels()
        self.position = random.choice(range(num))
        self.size = random.choice(range(int(num/8),int(num/4)))
        self.speed = random.uniform(0.5, 2)
        self.easing = CubicEaseIn()

    @task
    def __call__(self, ratio: float):
        num = self.strip.numPixels()
        if random.uniform(0,1) < 0.1:
            self.speed = random.uniform(0.5, 2)
        if random.uniform(0,1) < 0.1:
            self.size = random.choice(range(int(num/8),int(num/4)))            

        self.position = roll_index( self.position + self.speed, num)
        fraction = self.position % 1
        indexes = [ int(((i + fraction) / self.size)*254) for i in range(self.size)]
        start_tail = [ dim_color(RAINBOW[p],0.75 * (1-self.easing(i/len(indexes)))) for i,p in enumerate(indexes) ]
        # extend to stip size (fill with black)
        start_tail = start_tail + [C('black')]*(num - len(start_tail))
        start_tail = rotate(start_tail, int(self.position))
        
        for i in range(0,len(start_tail)):
            self.strip.setPixelRGB(i, start_tail[i])

        self.strip.show()


class Wave():
    def __init__(self, strip: ColorPixelStrip, **kwargs):
        self.strip = strip
        self.count = int(random.uniform(3, 6))
        self.phases = [random.uniform(0, 2*math.pi) for w in range(self.count)]
        self.period = [random.uniform(0.01, 0.5) for w in range(self.count)]
        self.speeds = [random.uniform(-2, 2) for w in range(self.count)]
        self.intensities = [random.uniform(0.5, 1) for w in range(self.count)]

    @task
    def __call__(self, ratio: float):
        numPixels = self.strip.numPixels()
        numWaves = self.count

        for i in range(numPixels):
            self.strip.setPixelRGB(i, dim_color(self.strip.getPixelRGB(i), 0.1))

        for w in range(numWaves):
            self.phases[w] += self.speeds[w]
            for i in range(numPixels):
                value = self.intensities[w] * (1 + math.sin(self.phases[w] + self.period[w]*i)) / 2
                color = WAVE[int(value*len(WAVE))]
                self.strip.setPixelRGB(i, add_color(self.strip.getPixelRGB(i), dim_color(color,1/numWaves)))
        
        self.strip.show()


class TaskName(str, Enum):
    fire = "fire"
    rainbow = "rainbow"
    rainbowChase = "rainbowChase"
    fallingStars = "fallingStars"
    colorWheel = "colorWheel"
    sparkles = "sparkles"
    rainbowStar = "rainbowStar"
    wave = "wave"


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
        elif name == 'rainbowStar':
            return RainbowStar(self.strip, **kwargs)
        elif name == 'wave':
            return Wave(self.strip, **kwargs)
        else:
            return None
