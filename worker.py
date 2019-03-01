#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
import argparse
import random
import json
from timeit import default_timer as timer

from colour import Color as C
from rpi_ws281x import *

from celery import Celery

celery = Celery('tasks', broker='redis://localhost')

class MyPixelStrip(PixelStrip):
    def __init__(self, num=12, pin=18, freq_hz=800000, dma=10, invert=False, brightness=255, channel=0, strip_type=None, gamma=None):
        super().__init__(num, pin, freq_hz, dma, invert, brightness, channel, strip_type, gamma)

    def getConfig(self):
        return self.config

    def setPixelRGB(self, n, color):
        rgb = tuple([int(c * 255) for c in color.rgb])
        self.setPixelColor(n, Color(*rgb))

    def getPixelRGB(self, n):
        return C(rgb=(
            (self._led_data[n] >> 16 & 0xff)/255,
            (self._led_data[n] >> 8  & 0xff)/255,
            (self._led_data[n]    & 0xff)/255)
            )

with open('config.json') as f:
    config = json.load(f)
print(config)

frame_time = 30 # ms

# Create NeoPixel object with appropriate configuration.
strip = MyPixelStrip(
    config["led_count"], # Number of LED pixels.
    config["pin"], # GPIO pin connected to the pixels (18 uses PWM!).
    config["frequency"], # LED signal frequency in hertz (usually 800khz)
    config["dma"], # DMA channel to use for generating signal (try 10)
    config["invert"], # True to invert the signal (when using NPN transistor level shift)
    config["brightness"], # Set to 0 for darkest and 255 for brightest
    config["channel"]) # set to '1' for GPIOs 13, 19, 41, 45 or 53
# Intialize the library (must be called once before other functions).
strip.begin()

@celery.task
def clear():
    for i in range(strip.numPixels()):
        strip.setPixelRGB(i, C('black'))
        strip.show()

@celery.task
def brighteness(value=0.5):
    value = int(max(0,min(value,1))*255)
    strip.setBrightness(value)
    strip.show()

@celery.task
def colorFade(duration_s=1):
    start = timer()
    initColors = []
    for i in range(strip.numPixels()):
        initColors.append(strip.getPixelRGB(i))
    while True:
        elasped = (timer() - start)
        if elasped >= duration_s:
            break
        ratio = max(0,(duration_s - elasped) / duration_s)
        for i in range(strip.numPixels()):
            initColor = initColors[i]
            color = C(rgb=tuple([e * ratio for e in initColor.rgb]))
            strip.setPixelRGB(i, color)
        strip.show()
        time.sleep(frame_time/1000.0)

@celery.task
def colorWipe(color, wait_ms=50, duration_s=1):
    """Wipe color across display a pixel at a time."""
    j=0
    start = timer()
    while (timer() - start) < duration_s:
        for i in range(strip.numPixels()):
            strip.setPixelRGB(i, C(color) if j % 2 else C('black'))
            strip.show()
            time.sleep(wait_ms/1000)
        j += 1

@celery.task
def colorRandom(wait_ms=10, duration_s=1):
    """Wipe color across display a pixel at a time."""
    start = timer()
    while (timer() - start) < duration_s:
        i = int(random.uniform(0, strip.numPixels()))
        strip.setPixelRGB(i, C(rgb = (random.random(),random.random(),random.random())))
        strip.show()
        time.sleep(random.uniform(0, 2*wait_ms/1000))

@celery.task
def colorFire(from_color='orange', to_color='red', wait_ms=20, duration_s=10):
    colors = list(C(from_color).range_to(C(to_color), 100))
    start = timer()
    while (timer() - start) < duration_s:
        i = int(random.uniform(0, strip.numPixels()))
        c = colors[int(random.uniform(0, len(colors)))]
        intensity = random.uniform(0, 1)
        color = C(rgb=tuple([e * intensity for e in c.rgb]))
        strip.setPixelRGB(i, color)
        strip.show()
        time.sleep(random.uniform(0, 2*wait_ms/1000))

@celery.task
def colorStar(color='white', wait_ms=100, duration_s=10):
    start = timer()
    clear()
    while (timer() - start) < duration_s:
        i = int(random.uniform(0, strip.numPixels()))
        intensity = random.uniform(0.5, 1)
        life = random.uniform(0.99, 0.999)
        speed = random.uniform(-0.1, 0.1)
        position = i
        c = C(rgb=tuple([e * intensity for e in C(color).rgb]))
        while c.rgb != (0,0,0):
            strip.setPixelRGB(i, C('black'))
            position = position + speed
            speed = speed * random.uniform(1, 1.01)
            i = int(position) % 12
            c = C(rgb=tuple([max(0, e * life - 0.01) for e in C(c).rgb]))
            strip.setPixelRGB(i, c)
            strip.show()
            time.sleep(random.uniform(0, wait_ms/1000))
        time.sleep(random.uniform(0, 100*wait_ms/1000))

################## FIX COLOR

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

@celery.task
def rainbow(wait_ms=20, duration_s=10):
    """Draw rainbow that fades across all pixels at once."""
    start = timer()
    while (timer() - start) < duration_s:
        for j in range(256):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((i+j) & 255))
            strip.show()
            time.sleep(wait_ms/1000)

@celery.task
def rainbowCycle(wait_ms=20, duration_s=10):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    start = timer()
    while (timer() - start) < duration_s:
        for j in range(256):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
            strip.show()
            time.sleep(wait_ms/1000)

@celery.task
def theaterChaseRainbow(wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

@celery.task
def theaterChase(color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

colorWipe('#010101')
clear()

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
    try:
        while True:
            colorFire()
            colorRandom()
            print ('Color wipe animations.')
            colorWipe(C(rgb=(1, 0, 0)))  # Red wipe
            colorWipe(C('blue'))  # Blue wipe
            colorWipe(C('lime'))  # Green wipe
            colorWipe(C(hue=0, saturation=1, luminance=0.5))
            colorWipe(C('gold'))
            colorWipe(C('orangered'))
            print ('Theater chase animations.')
            theaterChase(Color(127, 127, 127))  # White theater chase
            theaterChase(Color(127,   0,   0))  # Red theater chase
            theaterChase(Color(  0,   0, 127))  # Blue theater chase
            print ('Rainbow animations.')
            rainbow()
            rainbowCycle()
            theaterChaseRainbow()

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(Color(0,0,0), 10)
