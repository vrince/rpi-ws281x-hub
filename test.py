import argparse
from strip import *

######################3

Rouge = Couleur(rouge=1)
Vert = Couleur(vert=1)
Bleu = Couleur(bleu=1)
Jaune = Couleur(rouge=1, vert=1)
Gris = Couleur(rouge=0.5, vert=0.5, bleu=0.5)

VertBleu = melange(Vert, Bleu)


def allumerUnParCoin():
    lumieres.allumerLed(0, Jaune)
    lumieres.allumerLed(12, VertBleu)
    lumieres.allumerLed(24, Bleu)
    lumieres.allumerLed(36, Vert)
    lumieres.afficher()


def essayerLesCouleurs():
    lumieres.allumerLed(0, Couleur(rouge=1))
    lumieres.allumerLed(12, Couleur(vert=1))
    lumieres.allumerLed(24, Couleur(bleu=1))
    lumieres.allumerLed(36, Couleur(rouge=0.25, vert=0.5, bleu=0.75))
    lumieres.afficher()


def attendre(secondes=1):
    time.sleep(secondes)


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    #parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    print('Ctrl-C quit')
    try:
        while True:
            #allumerUnParCoin()
            #attendre(secondes=1)
            #essayerLesCouleurs()
            #attendre(secondes=1)
            #rainbowCycle(wait_ms=33,duration_s=300)

            #print ('Fire')
            #colorFire(from_color='#0033cc', to_color='#cc3300', duration_s=30)
            #colorFire(from_color='#9900ff', to_color='#ff3399', duration_s=30)
            colorFire(from_color='#9933ff', to_color='#6600cc', duration_s=30)
            
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