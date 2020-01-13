import os
from celery import Celery

from strip import *

celery = Celery('tasks',broker=os.getenv('REDIS_URL', 'redis://localhost'))

# decorate celery task "after the fact"
clear = celery.task(name='clear')(clear)
brighteness = celery.task(name='brighteness')(brighteness)
colorFade = celery.task(name='colorFade')(colorFade)
colorWipe = celery.task(name='colorWipe')(colorWipe)
colorRandom = celery.task(name='colorRandom')(colorRandom)
colorFire = celery.task(name='colorFire')(colorFire)
colorStar = celery.task(name='colorStar')(colorStar)
rainbow = celery.task(name='rainbow')(rainbow)
rainbowCycle = celery.task(name='rainbowCycle')(rainbowCycle)
theaterChaseRainbow = celery.task(name='theaterChaseRainbow')(theaterChaseRainbow)
theaterChase = celery.task(name='theaterChase')(theaterChase)
