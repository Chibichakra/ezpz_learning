FROM python:3.8-slim-buster

RUN apt update
RUN apt install -y python3-dev default-libmysqlclient-dev build-essential python-mysqldb

WORKDIR /app

COPY ./app/requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY /app /app

CMD [ "python3", "server.py"]