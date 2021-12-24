from typing import Optional, Callable, Any
from threading import Thread
from timeit import default_timer as timer
import time
import logging
import json

from os import path

import asyncio
import uvicorn
import click

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

# config_dir = user_config_dir('rpi-thermo-chick')
module_dir = path.dirname(__file__)

app = FastAPI()
vue_app = open( module_dir + '/index.html', 'r').read()

logger = logging.getLogger("gunicorn.error")

# state
class State(BaseModel):
    stop_thread: bool = False
    timeout: float = 0
    period: float = 0
    tick: float = 0
    duration: float = 0
    position: float = 0
    ratio: float = 0

state = State()
thread = None

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

manager = ConnectionManager()

# functions

def status():
    return {
        'running': (thread is not None),
        'state': state.dict()
    }

def event_loop(timeout : float, period: float, tick: float):
    print("event_loop")
    global state
    start = timer()
    while True:
        state.duration = timer() - start
        state.position = state.duration / period
        state.ratio = state.position % 1
        print(f"tick duration({state.duration}) position({state.position}) ratio({state.ratio})")
        asyncio.run(manager.broadcast(json.dumps(status())))
        if timeout > 0 and timer() - start > timeout:
            print("timeout")
            break
        if state.stop_thread:
            state.duration = 0
            state.position = 0
            state.ratio = 0
            break
        time.sleep(tick)


def thread_wrapper(function: Callable, args: dict = {}, callback: Callable = None):
    print("thread_wrapper")
    function(**args)
    if callback is not None:
        callback()

def start_thread(timeout: float = -1, period: float = 60, tick: float = 1, effect: str = ""):
    global thread
    if not thread:
        thread = Thread(
            target=thread_wrapper, 
            args=(event_loop, {"timeout": timeout, "period": period, "tick": tick}, on_thread_close),
            daemon=True)
        thread.start()
        asyncio.run(manager.broadcast(json.dumps(status())))

def on_thread_close():
    print("on_thread_close")
    global thread, state
    thread = None
    state.stop_thread = False
    asyncio.run(manager.broadcast(json.dumps(status())))

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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            #await websocket.send_text(f"message text was: {data}")
            await manager.broadcast(f"message text was: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/start")
def get_start(timeout: float = -1, period: float = 60, tick: float = 1, effect: str = ""):
    if not thread:
        start_thread(timeout, period, tick, effect)
        return {"starting": True}
    else:
        return {"starting": False}

@app.get("/stop")
def stop():
    global thread, state
    if thread and not state.stop_thread:
        state.stop_thread = True
    return {"stopping": state.stop_thread}

#####################################

@app.get("/items/{item_id}")
def get_read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


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