#!/bin/bash

#send pi_id_rsa to the pi
# cat ~/.ssh/pi_id_rsa.pub | ssh pi@192.168.2.109 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >>  ~/.ssh/authorized_keys"

SOURCE=$(pwd)
DESTINATION=pi@192.168.2.109:/home/pi/leds/

while inotifywait -r -e modify,create,delete ${SOURCE}; do
    rsync -avz --exclude '.*' -e ssh  ${SOURCE}/ ${DESTINATION}
done