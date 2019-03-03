#!/bin/bash
export FLASK_APP=$(pwd)/service.py
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

function service() {
    while true; do
        pkill -f "flask run --host=0.0.0.0 --port=5000"
        flask run --host=0.0.0.0 --port=5000 &> service.log
        sleep 15
    done
}

function worker() {
    while true; do
      sudo pkill -f "celery -A worker worker"
      sudo celery -A worker worker --concurrency=1 --loglevel=info -n rpi-ws281x@pi &> worker.log
      sleep 15
    done
}

function start() {
    worker &
    service &
}

function stop() {
    pkill -f "flask run --host=0.0.0.0 --port=5000"
    sudo pkill -f "celery -A worker worker"
    pkill -f "/bin/bash ./run.sh"
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    *)
        echo $"Usage: $0 {start|stop|restart}"
        exit 1
esac