#!/bin/bash
#https://stackoverflow.com/questions/12264238/restart-process-on-file-change-in-linux
while true; do
  sudo pkill -f "celery -A worker worker"
  sudo celery -A worker worker --concurrency=1 --loglevel=info -n rpi-ws281x@pi &
  inotifywait worker.py
  sleep 1
done