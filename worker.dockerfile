FROM arm32v7/python:3.6-slim
RUN apt update && apt install -y make gcc
RUN pip3 install rpi_ws281x colour celery redis
ADD ./worker.py /opt/worker.py
ADD ./config.json /opt/config.json
WORKDIR /opt
CMD [ "celery", "-A", "worker", "worker", "--concurrency=1", "--loglevel=info", "-n", "rpi-ws281x@pi"]
