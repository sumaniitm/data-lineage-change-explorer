FROM ubuntu:18.04
FROM python:3

LABEL maintainer="Suman Gangopadhyay <ganguly.04@gmail.com>"

COPY ./requirements.txt /data-lineage-change-explorer/requirements.txt

WORKDIR /data-lineage-change-explorer

RUN pip3 install -r requirements.txt

COPY . /data-lineage-change-explorer

CMD [ "python3", "app.py" ]