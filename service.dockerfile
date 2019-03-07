FROM arm32v7/python:3.6-slim
RUN pip3 install flask flask-cors celery redis
ADD ./rpi-ws281x-vue/dist /opt/rpi-ws281x-vue/dist
ADD ./service.py /opt/service.py
ADD ./config.json /opt/config.json
WORKDIR /opt
EXPOSE 5000
ENV FLASK_APP=/opt/service.py
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
CMD [ "flask", "run", "--host=0.0.0.0", "--port=5000" ]
