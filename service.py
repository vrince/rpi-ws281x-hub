import json
import os
from time import sleep
import datetime
from dateutil import parser as date_parser
from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
from multiprocessing import Pool

from tasks import tasks

app = Flask(__name__,
            static_url_path='',
            static_folder='rpi-ws281x-vue/dist')
CORS(app)


payload = list()
error = None
pool = Pool(processes=1)


@app.route('/')
def root():
    return redirect(url_for('static', filename='index.html'))


@app.route('/payload')
def get_payload():
    global payload
    if len(payload) == 0:
        return jsonify({
            'payload': [],
            'ok': True
        })

    task = payload[0]['task']
    delta = None
    progress = None

    try:
        at = date_parser.parse(task['at'])
        delta = (datetime.datetime.now() - at).total_seconds()
        duration = task['arguments']['duration_s']
        progress = 1 - (duration - delta) / duration
    except Exception:
        pass

    return jsonify({
        'payload': payload,
        'delta': delta,
        'progress': progress,
        'ok': True
    })


@app.route('/error')
def get_error():
    global payload
    return jsonify({
        'error': error,
        'ok': True
    })


@app.route('/config')
def config():
    with open('config.json') as f:
        config = json.load(f)
    return jsonify({
        'config': config,
        'ok': True
    })


def process_callback(x):
    global payload
    task = payload.pop()
    print('process_callback', task, x)


def error_process_callback(x):
    global payload, error
    task = payload.pop()
    error = {'message': str(x),
             'at': datetime.datetime.now().isoformat()}
    print('error_process_callback', task, x)


@app.route('/task/<task_name>')
def task(task_name):

    arguments = {}
    for key in request.args:
        try:
            arguments[key] = float(request.args[key])
        except ValueError:
            arguments[key] = request.args[key]

    try:
        f_task = tasks[task_name]
    except KeyError:
        return jsonify({
            'error': f'task not found, name : {task_name}',
            'ok': False}), 404

    global payload, pool, error

    if len(payload) >= 0:
        print('pool running --> terminate')
        payload = list()
        pool.terminate()
        pool.join()
        pool = Pool(processes=1)

    task_content = {
        'name': task_name,
        'arguments': arguments,
        'at': datetime.datetime.now().isoformat()}

    payload.append({'task': task_content})

    error = None
    pool.apply_async(func=f_task,
                     kwds=arguments,
                     callback=process_callback,
                     error_callback=error_process_callback)

    # hack to get trivial error like missing args and stuff sync-ish
    sleep(0.01)
    if error:
        return jsonify({
            'task': task_content,
            'error': error,
            'ok': False}), 500

    return jsonify({
        'task': task_content,
        'ok': True
    })
