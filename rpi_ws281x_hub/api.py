from typing import Optional, Callable, Any, List
from threading import Thread
from timeit import default_timer as timer
import time
import logging
import json
from os import path
import asyncio
import uvicorn
import click
from appdirs import user_config_dir

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

from rpi_ws281x_hub.strip import ColorPixelStrip, ColorPixelStripConfig
from rpi_ws281x_hub.tasks import *

config_dir = user_config_dir('rpi-ws281x-hub')
config_file = path.join(config_dir, 'config.json')
module_dir = path.dirname(__file__)

app = FastAPI()
app.mount('/images', StaticFiles(directory=module_dir + '/../images'), name='images')

vue_app = open( module_dir + '/index.html', 'r').read()

logger = logging.getLogger('gunicorn.error')

# strip --> initialize the library (must be called once before other functions).
print(f'config file: {config_file}')
if path.exists(config_file):
    default_config = ColorPixelStripConfig()
    with open(config_file, 'w') as f:
        f.write(default_config.json())
    print(f'default config create: {config_file}, edit then restart')
    exit(1)
try:
    config = ColorPixelStripConfig.parse_file('config.json')
    strip = ColorPixelStrip(config)
    strip.begin()
    print(f'strip: {config.dict()}')
except Exception as e:
    print('cannot instanciate strip (check config.json)')
    print(e)
    exit(1)

# state
class State(BaseModel):
    stop_thread: bool = False
    timeout: float = 0
    period: float = 0
    tick: float = 0
    duration: float = 0
    position: float = 0
    ratio: float = 0
    progress: float = 0
    colors: List[str] = []
    task: str = None

state = State()
thread = None
factory = TaskFactory(strip)

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    def client_count(self):
        return len(self.active_connections)

manager = ConnectionManager()

# functions

def status():
    return {
        'running': (thread is not None),
        'clients': manager.client_count(),
        'state': state.dict()
    }

def event_loop(timeout : float, period: float, tick: float, effect: str, **kwargs):
    global state
    start = timer()
    state.timeout = timeout
    task = factory.get(effect, **kwargs)
    if task is not None:
        while True:
            state.duration = timer() - start
            state.position = state.duration / period
            state.ratio = state.position % 1
            state.progress = state.duration / state.timeout
            state.colors = task(state.ratio)
            if timeout > 0 and timer() - start > timeout:
                logger.info("timeout")
                break
            if state.stop_thread:
                break
            time.sleep(tick)


def thread_wrapper(function: Callable, args: dict = {}, callback: Callable = None):
    function(**args)
    if callback is not None:
        callback()

def start_thread(**kwargs):
    global thread
    if not thread:
        thread = Thread(
            target=thread_wrapper, 
            args=(event_loop, kwargs, on_thread_close),
            daemon=True)
        thread.start()

def on_thread_close():
    global thread, state
    thread = None
    state.stop_thread = False
    state.duration = 0
    state.position = 0
    state.ratio = 0
    state.progress = 0
    state.colors = []
    state.task = None
    strip.clear()

# Routes

@app.get("/")
def read_root():
    return status()

@app.get('/app', response_class=HTMLResponse)
def read_vue_app():
    return open(module_dir + '/index.html', 'r').read()
    #return vue_app

@app.get('/variables.scss')
def read_vue_app():
    data = open(module_dir + '/variables.scss', 'r').read()
    return Response(content=data, media_type="text/css")

@app.get('/config')
def read_vue_app():
    data = open(module_dir + '/../config.json', 'r').read()
    return Response(content=data, media_type="application/json")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        last_status = {}
        while True:
            await asyncio.sleep(0.1)
            current_status = status()
            if current_status != last_status:
                last_status = current_status
                await websocket.send_text(json.dumps(current_status))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)

@app.get("/start/{effect}")
def get_start(effect: TaskName,
              timeout: float = -1, period: float = 60, tick: float = 1,
              color: Optional[List[str]] = Query(None)):

    kwargs = {}

    if color is not None:
        kwargs['colors'] = [ f'#{c}' for c in color]

    global thread
    if thread:
        stop()
        thread.join()

    state.task = effect
    start_thread(effect=effect, timeout=timeout, period=period, tick=tick, **kwargs)
    return {"starting": True}


@app.get("/stop")
def stop():
    global thread, state
    if thread and not state.stop_thread:
        state.stop_thread = True
    return {"stopping": state.stop_thread}

#####################################

@click.command()
@click.option('--host', default='0.0.0.0', help='Host (default 0.0.0.0) [env RPI_WS281_HUB_HOST]')
@click.option('--port', default=8000,   help='Port (default 8000) [env RPI_WS281_HUB_PORT]')
def cli(host, port):
    """
    rpi-ws281x-hub
    """
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    cli(auto_envvar_prefix='RPI_WS281_HUB')