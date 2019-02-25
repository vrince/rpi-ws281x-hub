#!/bin/bash
export FLASK_APP=$(pwd)/service.py
export FLASK_ENV=development
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
pkill -f "flask run --host=0.0.0.0 --port=5000"
flask run --host=0.0.0.0 --port=5000