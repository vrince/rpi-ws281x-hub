from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS

app = Flask(__name__,
            static_url_path='', 
            static_folder='rpi-ws281x-vue/dist')
CORS(app)

from celery import Celery
celery = Celery('tasks', broker='redis://localhost')

@app.route('/')
def root():
    return redirect(url_for('static', filename='index.html'))

@app.route('/queue')
def init():
    inspect = celery.control.inspect()
    return jsonify({
        'scheduled': inspect.scheduled(), 
        'active': inspect.active(), 
        'reserved': inspect.reserved(), 
        'ok': True
        })

@app.route('/task/<task_name>')
def task(task_name):
    arguments = {}
    for key in request.args:
        try: 
            arguments[key] = float(request.args[key])
        except ValueError: 
            arguments[key] = request.args[key]
    print(arguments)
    result = celery.send_task('playground.{}'.format(task_name),(),arguments)
    return jsonify({
        'task': {
            'name': task_name,
            'id': str(result),
            'arguments': arguments
        },
        'ok': True
        })
