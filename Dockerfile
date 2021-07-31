FROM python:3.9.6

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN pip3 install pipenv

COPY requirements.txt /code

RUN pipenv install -r requirements.txt

COPY . /code/