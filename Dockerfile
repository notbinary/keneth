FROM python:alpine

RUN apk add --no-cache build-base

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

USER 1000
ENTRYPOINT flask run --host=0.0.0.0
