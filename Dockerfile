# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /remove_background_app

COPY requirements requirements
RUN pip3 install -r requirements

COPY . .

CMD ["/remove_background_app/start_flask_web"]
