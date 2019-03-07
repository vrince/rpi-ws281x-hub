# RPi WS281x Hub

This project is meant to manage `ws281x` leds on the RPi. It's compose of 3 parts, a web app (`vuejs`), a web services (`python flask`) that dispatch a sequence of led tasks to a worker (`celery worker`). Celery queue is serve by redis (`docker arm32v7/redis`). All that running on the rpi, microservice style using containerized application. 

## Application

![](media/rpi-ws281x-vue.gif)

You can set task duration and speed of ~6 led effects.

## Architecture

```mermaid
graph LR
    0((user)) -- finger --> 1
    subgraph vrince/rpi-ws281x-service
    1(App.vue) == http ==> 2(service.py)
    end
    subgraph vrince/rpi-ws281x-worker
    2 == redis ==> 3(worker.py)
    3 == rpi-ws281x ==> 4(gpio)
    end
    4 -- wire --> 5((leds))
```

Uhhgg github ? no mermaid ? --> [diagram](https://mermaidjs.github.io/mermaid-live-editor/#/view/eyJjb2RlIjoiZ3JhcGggTFJcbiAgICAwKCh1c2VyKSkgLS0gZmluZ2VyIC0tPiAxXG4gICAgc3ViZ3JhcGggdnJpbmNlL3JwaS13czI4MXgtc2VydmljZVxuICAgIDEoQXBwLnZ1ZSkgPT0gaHR0cCA9PT4gMihzZXJ2aWNlLnB5KVxuICAgIGVuZFxuICAgIHN1YmdyYXBoIHZyaW5jZS9ycGktd3MyODF4LXdvcmtlclxuICAgIDIgPT0gcmVkaXMgPT0-IDMod29ya2VyLnB5KVxuICAgIDMgPT0gcnBpLXdzMjgxeCA9PT4gNChncGlvKVxuICAgIGVuZFxuICAgIDQgLS0gd2lyZSAtLT4gNSgobGVkcykpXG4iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9fQ)

This is tested on the RPi3 with a adafruits neopixels.

All of it is overkill for what is does.

## Installing

On the pi run the following commands, **no need to clone the code**.

### Docker & docker-compose

```bash
ssh pi@<pi-ip>
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
sudo usermod -aG docker pi
newgrp docker
sudo pip3 install docker-compose
```

### The stack

Get and enjoy the docker / docker-compose power.

```bash
wget https://raw.githubusercontent.com/vrince/rpi-ws281x-hub/master/docker-compose.yml
docker-compose up -d
```

:tada: you shoul be able to open `http://<pi-ip>:5000` and send leds commands.

To see logs while running.

```bash
docker-compose logs -f
```

To stop the thing.

```bash
docker-compose stop
```

## Developing

## Sync to pi

This will continously push the code to the pi as you change it on your computer.

```
git clone https://github.com/vrince/rpi-ws281x-hub.git
cat ~/.ssh/pi_id_rsa.pub | ssh pi@<pi-ip> "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >>  ~/.ssh/authorized_keys"
./sync <pi-ip>
```

All the following (execpt the `vueapp`) is appening on th pi so ssh to it.

```bash
ssh pi@<pi-ip>
```

### Dependencies

```bash
sudo pip3 install rpi_ws281x colour flask flask-cors celery redis 
```

### Redis in docker

https://thisdavej.com/how-to-install-redis-on-a-raspberry-pi-using-docker/#option-1---create-redis-server-for-localhost-requests-only

```bash
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
sudo usermod -aG docker pi
newgrp docker
docker run --name redis -d -p 6379:6379 --restart unless-stopped arm32v7/redis --appendonly yes --maxmemory 512mb --tcp-backlog 128
```

### Run the `service`

Flask service that serve generic celery task dispatcher on port `5000` **and** the static build of the vue app. **This script auto reload the service when `service.py` change**.

```bash
ssh pi@<pi-ip>
cd rpi-ws281x-hub
./run-service.sh
```

Open `http://<pi-ip>:5000/queue` to see the current worker queue.

### Run worker `worker`

Worker need to be run as root ta access the hardware. **This script auto reload the celery worker when `worker.py` change or crash**.

```bash
ssh pi@<ip>
cd rpi-ws281x-hub
sudo ./run-worker.sh
```

### Run the `vueapp`

#### Run locally

**!! this is on your computer not on the pi !!**

```bash
cd rpi-ws281x-vue
VUE_APP_BASE_URL="http://<pi-ip>:5000" yarn serve
```

open http://localhost:8080

#### Deploy the `vueapp` on the pi

Make sure the `sync.sh` script is running, the build result will be generated locaaly then sync to the `pi` then serve by the flask app.

```bash
yarn build
```

### Docker build

For those a litle familiar with docker you'll be able to build docker images simply.

## Credits

### RPi-ws281x-python ([source](https://github.com/rpi-ws281x/rpi-ws281x-python))

At the very beging it was a fork of RPi-ws281x-python, I basically hack the `SK6812_strandtest.py` file to make the `worker.py` credit goes to [Gadgetoid](https://github.com/Gadgetoid) !

### Redis on docker ([source](https://thisdavej.com/how-to-install-redis-on-a-raspberry-pi-using-docker/#option-1---create-redis-server-for-localhost-requests-only))