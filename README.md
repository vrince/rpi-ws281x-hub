# RPi WS281x Python

This is the official Python distribution of the ws281x library: http://github.com/richardghirst/rpi_ws281x

# Installing

## From pip

Most users should simply run:

```bash
sudo pip3 install rpi_ws281x colour flask flask-cors celery redis 
```

## Sync to pi

```
./sync
```

run with same ssh

## Redis in docker

https://thisdavej.com/how-to-install-redis-on-a-raspberry-pi-using-docker/#option-1---create-redis-server-for-localhost-requests-only

```bash
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
sudo usermod -aG docker pi
newgrp docker
docker run --name redis -d -p 6379:6379 --restart unless-stopped arm32v7/redis --appendonly yes --maxmemory 512mb --tcp-backlog 128
```

## Development

Deploy code on the pi (auto synchronize in develoment : keep locel file deployed to the pi al long as the script is running).

```bash
./sync
```

### Run the `service`

```bash
ssh pi@<ip>
cd leds/
./run-service.sh
```

### Run worker `worker`

Worker need to be run as root ta access the hardware.

```bash
ssh pi@<ip>
cd leds/
sudo ./run-worker.sh
```