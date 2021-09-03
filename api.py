from typing import Optional, Callable
from threading import Thread
from timeit import default_timer as timer
import time
import logging

from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()
logger = logging.getLogger("gunicorn.error")
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