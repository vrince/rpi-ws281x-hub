from flask import Flask, jsonify, request
app = Flask(__name__)

from celery import Celery
celery = Celery('tasks', broker='redis://localhost')

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

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
    result = celery.send_task('playground.{}'.format(task_name),(),arguments)
    return jsonify({
        'task': {
            'name': task_name,
            'id': str(result),
            'arguments': arguments
        },
        'ok': True
        })
