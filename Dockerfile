FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt update \
    && apt add postgresql-dev gcc python3-dev musl-dev

COPY ./req.txt /app/requirements.txt

#RUN #apt-get update && apt-get install -y postgis

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD python manage.py runserver 0.0.0.0:8000
