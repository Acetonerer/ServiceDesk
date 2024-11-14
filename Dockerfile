FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/

RUN pip install -r /code/requirements.txt


