#!/bin/bash
IP=$1
echo "make sure you sent you pub key to the pi before with"
echo ""
echo "cat ~/.ssh/pi_id_rsa.pub | ssh pi@${IP} \"mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >>  ~/.ssh/authorized_keys\""
echo ""
SOURCE=$(pwd)
DESTINATION=pi@${IP}:/home/pi/rpi-ws281x-hub
while inotifywait -r -e modify,create,delete ${SOURCE}; do
    rsync -avz --exclude '.*' -e ssh  ${SOURCE}/ ${DESTINATION}
done