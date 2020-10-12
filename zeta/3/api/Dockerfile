from python:3.8.6

COPY    . /code/api
WORKDIR /code/api
RUN     apt-get update -y && apt-get install redis-cli -y

CMD     service redis-server start && pip install -r requirements.txt && python app.py