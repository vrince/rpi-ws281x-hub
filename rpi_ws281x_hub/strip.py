import os
import time
import random
import json
from timeit import default_timer as timer

from colour import Color as C

from rpi_ws281x import *

class ColorPixelStrip(PixelStrip):
    def __init__(self,
                 num=12,
                 pin=18,
                 freq_hz=800000,
                 dma=10,
                 invert=False,
                 brightness=255,
                 channel=0,
                 strip_type=None,
                 gamma=None):
        super().__init__(num, pin, freq_hz, dma, invert, brightness, channel,
                         strip_type, gamma)

    def clear(self):
        for i in range(self.numPixels()):
            self.setPixelRGB(i, C('black'))
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



with open('config.json') as f:
    config = json.load(f)
print(config)

frame_time = 30  # ms

# PWM pins
# 12 --> https://pinout.xyz/pinout/pin32_gpio12#
# 18 --> https://pinout.xyz/pinout/pin12_gpio18#

# Create NeoPixel object with appropriate configuration.
strip = ColorPixelStrip(
    config["led_count"],  # Number of LED pixels.
    config["pin"],  # GPIO pin connected to the pixels (18 uses PWM!).
    config["frequency"],  # LED signal frequency in hertz (usually 800khz)
    config["dma"],  # DMA channel to use for generating signal (try 10)
    # True to invert the signal (when using NPN transistor level shift)
    config["invert"],
    config["brightness"],  # Set to 0 for darkest and 255 for brightest
    config["channel"])  # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Initialize the library (must be called once before other functions).
try:
    strip.begin()
except RuntimeError:
    pass

#####


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


#####


def clear():
    for i in range(strip.numPixels()):
        strip.setPixelRGB(i, C('black'))
    strip.show()
    print('clear done')


def brighteness(value=0.5):
    value = int(max(0, min(value, 1)) * 255)
    strip.setBrightness(value)
    strip.show()


def colorFade(wait_ms=20, duration_s=1):
    start = timer()
    initColors = []
    for i in range(strip.numPixels()):
        initColors.append(strip.getPixelRGB(i))
    while True:
        elasped = (timer() - start)
        if elasped >= duration_s:
            break
        ratio = max(0, (duration_s - elasped) / duration_s)
        for i in range(strip.numPixels()):
            initColor = initColors[i]
            color = C(rgb=tuple([e * ratio for e in initColor.rgb]))
            strip.setPixelRGB(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def colorWipe(color, wait_ms=50, duration_s=1):
    """Wipe color across display a pixel at a time."""
    j = 0
    start = timer()
    while (timer() - start) < duration_s:
        for i in range(strip.numPixels()):
            print(f'colorWipe')
            # strip.setPixelRGB(i, C(color) if j % 2 else C('black'))
            # strip.show()
            time.sleep(wait_ms / 1000)
        j += 1
    print('colorWipe done')


def colorRandom(wait_ms=10, duration_s=1):
    """Wipe color across display a pixel at a time."""
    start = timer()
    while (timer() - start) < duration_s:
        i = int(random.uniform(0, strip.numPixels()))
        strip.setPixelRGB(
            i, C(rgb=(random.random(), random.random(), random.random())))
        strip.show()
        time.sleep(random.uniform(0, 2 * wait_ms / 1000))


def colorFire(from_color='orange', to_color='red', wait_ms=20, duration_s=10):
    """Simulate uniform fire between two colors"""
    colors = list(C(from_color).range_to(C(to_color), 100))
    start = timer()
    while (timer() - start) < duration_s:
        i = int(random.uniform(0, strip.numPixels()))
        c = colors[int(random.uniform(0, len(colors)))]
        intensity = random.uniform(0, 1)
        color = C(rgb=tuple([e * intensity for e in c.rgb]))
        strip.setPixelRGB(i, color)
        strip.show()
        time.sleep(random.uniform(0, 2 * wait_ms / 1000))


def colorStar(color='white', wait_ms=100, duration_s=10):
    """Draw randow stars"""
    start = timer()
    clear()
    while (timer() - start) < duration_s:
        i = int(random.uniform(0, strip.numPixels()))
        intensity = random.uniform(0.5, 1)
        life = random.uniform(0.99, 0.999)
        speed = random.uniform(-0.1, 0.1)
        position = i
        c = C(rgb=tuple([e * intensity for e in C(color).rgb]))
        while c.rgb != (0, 0, 0):
            strip.setPixelRGB(i, C('black'))
            position = position + speed
            speed = speed * random.uniform(1, 1.01)
            i = int(position) % strip.numPixels()
            c = C(rgb=tuple([max(0, e * life - 0.01) for e in C(c).rgb]))
            strip.setPixelRGB(i, c)
            strip.show()
            time.sleep(random.uniform(0, wait_ms / 1000))
        time.sleep(random.uniform(0, 100 * wait_ms / 1000))


def rainbow(wait_ms=20, duration_s=10):
    """Draw rainbow that fades across all pixels at once."""
    start = timer()
    j = 0
    while (timer() - start) < duration_s:
        j = 0 if j >= 255 else j + 1
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000)


def rainbowCycle(wait_ms=20, duration_s=10):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    start = timer()
    j = 0
    while (timer() - start) < duration_s:
        j = 0 if j >= 255 else j + 1
        for i in range(strip.numPixels()):
            strip.setPixelColor(
                i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000)


def theaterChaseRainbow(wait_ms=50, duration_s=10):
    """Rainbow movie theater light style chaser animation."""
    start = timer()
    j = 0
    while (timer() - start) < duration_s:
        j += 1
        j = 0 if j >= 256 else j
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelRGB(i + q, C('black'))


def theaterChase(color, wait_ms=50, duration_s=10):
    """Movie theater light style chaser animation."""
    start = timer()
    while (timer() - start) < duration_s:
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelRGB(i + q, C(color))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelRGB(i + q, C('black'))


clear()
