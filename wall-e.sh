#!/bin/bash

cmd=${1}

case $cmd in
run)
    echo "🎨 Running"
    sudo python3 rpi_ws281x_hub/api.py --port 8000
    ;;
wheel)
    echo "🐍 Building wheel ..."
    python3 setup.py bdist_wheel
    ;;
clean)
    echo "🧨 Cleaning wheel ..."
    rm -r $(pwd)/__pycache__
    rm -r $(pwd)/dist
    rm -r $(pwd)/build
    rm -r $(pwd)/rpi_ws281x_hub.egg-info
    ;;  
deploy)
    echo "🚀 Deploying wheel ..."
    python3 -m twine upload dist/*
    ;;
*)
  echo "🪗 Nothing to do ..."
  ;;
esac

echo "💫 Done"