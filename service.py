import json
import os
from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
from strip import *
from tasks import tasks
from multiprocessing import Process


app = Flask(__name__,
            static_url_path='',
            static_folder='rpi-ws281x-vue/dist')
CORS(app)


payload = list()


@app.route('/')
def root():
    return redirect(url_for('static', filename='index.html'))


@app.route('/current')
def current():
    return jsonify({
        'payload': payload,
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


process = None


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
            'ok': False
        }), 404

    global process
    if isinstance(process, Process):
        process.terminate()
        process.join()
    process = Process(target=f_task, kwargs=arguments, daemon=True)
    process.start()

    # check if started in an ugly way
    process.join(0.1)
    if process.exitcode is not None:
        return jsonify({
            'task': {
                'name': task_name,
                'process_name': str(process.name),
                'arguments': arguments
            },
            'ok': process.exitcode is 0
        }), 200 if process.exitcode is 0 else 500

    return jsonify({
        'task': {
            'name': task_name,
            'process_name': str(process.name),
            'arguments': arguments
        },
        'ok': True
    })
