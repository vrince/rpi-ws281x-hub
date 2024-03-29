import argparse
from strip import *

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    #parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    print('Ctrl-C quit')
    try:
        while True:
            #print ('rainbowCycle')
            #rainbowCycle(wait_ms=33,duration_s=300)

            print ('Fire')
            #colorFire(from_color='#0033cc', to_color='#cc3300', duration_s=30)
            colorFire(from_color='#9900ff', to_color='#ff3399', duration_s=30)
            #colorFire(from_color='#9933ff', to_color='#6600cc', duration_s=30)
            
            #print ('Random')
            #colorRandom(duration_s=1)
            #print ('Color')
            #colorWipe('blue', duration_s=1)  # Blue wipe
            #colorWipe('lime', duration_s=1)  # Green wipe
            #print ('Star')
            #colorStar(wait_ms=5, duration_s=1)
            #print ('Theater chase')
            #theaterChase('lime', wait_ms=200, duration_s=1)
            #theaterChase('yellow', wait_ms=20, duration_s=1)
            #print ('Rainbow')
            #rainbow(wait_ms=20, duration_s=120)
            #rainbowCycle(wait_ms=20, duration_s=1)
            #theaterChaseRainbow(wait_ms=20, duration_s=1)

    except KeyboardInterrupt:
        colorFade()
        clear()