# syntax=docker/dockerfile:1
FROM ubuntu:18.04
FROM python:3.8-slim-buster

LABEL maintainer="Suman Gangopadhyay <ganguly.04@gmail.com>"

WORKDIR /data-lineage-change-explorer

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "app.py" ]