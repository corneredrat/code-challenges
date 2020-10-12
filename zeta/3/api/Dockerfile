from python:3.8.6

COPY    . /code/api
WORKDIR /code/api
RUN     apt-get update -y && apt-get install redis-server -y
RUN     pip install -r requirements.txt

CMD     service redis-server start && python app.py