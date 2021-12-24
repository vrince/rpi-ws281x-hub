import time
from abc import ABC, abstractmethod
from colour import Color as C
import random

from strip import *

class Task(ABC):
    @abstractmethod
    def tick(self):
        pass

class colorFire(Task):
    def __init__(self, from_color='orange', to_color='red'):
        self.colors = list(C(from_color).range_to(C(to_color), 100))

    def tick(self, ratio: float):
        i = int(random.uniform(0, strip.numPixels()))
        c = self.colors[int(random.uniform(0, len(self.colors)))]
        intensity = random.uniform(0, 1)
        color = C(rgb=tuple([e * intensity for e in c.rgb]))
        strip.setPixelRGB(i, color)
        strip.show()

tasks = {
    'clear': clear,
    'brighteness': brighteness,
    'colorFade': colorFade,
    'colorWipe': colorWipe,
    'colorRandom': colorRandom,
    'colorFire': colorFire,
    'colorStar': colorStar,
    'rainbow': rainbow,
    'rainbowCycle': rainbowCycle,
    'theaterChaseRainbow': theaterChaseRainbow,
    'theaterChase': theaterChase
}
