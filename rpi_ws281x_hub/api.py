from typing import Optional, Callable
from threading import Thread
from timeit import default_timer as timer
import time
import logging

from os import path

import uvicorn
import click

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

# config_dir = user_config_dir('rpi-thermo-chick')
module_dir = path.dirname(__file__)

app = FastAPI()
vue_app = open( module_dir + '/index.html', 'r').read()

logger = logging.getLogger("gunicorn.error")

# state
thread = None
stop_thread = False

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


def event_loop(timeout : float = -1, tick: float = 1):
    print("event_loop")
    start = timer()
    while True:
        print("tick")
        if timeout > 0 and timer() - start > timeout:
            print("timeout")
            break
        if stop_thread:
            break
        time.sleep(tick)


def thread_wrapper(function: Callable, args: dict = {}, callback: Callable = None):
    print("thread_wrapper")
    function(**args)
    if callback is not None:
        callback()

def on_thread_close():
    print("on_thread_close")
    global thread, stop_thread
    thread = None
    stop_thread = False

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/app', response_class=HTMLResponse)
def read_vue_app():
    return open(module_dir + '/index.html', 'r').read()
    #return vue_app

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

@app.get("/status")
def start():
    global thread
    return {"running": (thread is not None)}

@app.get("/start")
def start(timeout: float = -1, tick: float = 1, effect: str = ""):
    global thread
    if not thread:
        thread = Thread(
            target=thread_wrapper, 
            args=(event_loop, {"timeout": timeout, "tick": tick}, on_thread_close))
        thread.start()
        return {"starting": True}
    else:
        return {"starting": False}

@app.get("/stop")
def stop():
    global thread, stop_thread
    if thread and not stop_thread:
        stop_thread = True
    return {"stopping": stop_thread}

#####################################

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
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