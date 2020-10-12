from python:3.8.6

COPY    . /code/api
WORKDIR /code/api
RUN     apt-get update -y && apt-get install redis-server -y

CMD     service redis-server start && pip install -r requirements.txt && python app.py