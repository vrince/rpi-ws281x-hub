# RPi WS281x Hub

Control your raspberry pi `ws281x` leds from your network, using a local api / web application.

Backend: `python` / `fast-api` | Frontend: `vuejs` / `vuetify`

[![PyPI version](https://badge.fury.io/py/rpi-ws281x-hub.svg)](https://badge.fury.io/py/rpi-ws281x-hub) ![](https://badgen.net/badge/license/MIT/blue) [![](https://badgen.net/badge/code/github/black?icon=github)](https://github.com/vrince/rpi-ws281x-hub)


## Application


## Installation

On the pi run the following pip commands (as root cause the service will need priviledges to access PWM channels).

```bash
sudo pip3 install rpi_ws281x_hub
```

Once installed make sure that the `config.json` file match your hardware setup, important part being `num` (number of pixels), `pin` (hardware pin used to control the led) and finally `channel` (depending on the pin).

Know working `pin|channel` pairs are: `12|0`, `18|0` or `13|1` see [rpi_ws281x](https://github.com/jgarff/rpi_ws281x) for more information.

Finally fire the thing with:

```bash
sudo rpi-ws281x-hub
```

And open `http://<your-pi-ip>:8000` in a web browser.

## Development

Clone this repository:

```bash
git clone https://github.com/vrince/rpi-ws281x-hub.git
cd rpi-ws281x-hub
```

Install dependencies and install package in dev mode:

```bash
sudo python3 setup.py develop
```

Run locally:

```bash
# using script
sudo rpi-ws281x-hub
# or directly using the api.py main
sudo python3 rpi_ws281x_hub/api.py --port 8000
```

Web application can be reach at `http://<your-pi-ip>:8000/app`

### Add a new led `task`



## Credits

https://github.com/jgarff/rpi_ws281x

All images used are from `flaticon.com` make sure to visite their site :
https://www.flaticon.com/search?author_id=1&style_id=15&type=standard&word=color