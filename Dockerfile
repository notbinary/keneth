FROM python:alpine

ARG SERVICE_ACCOUNT_KEY

RUN apk add --no-cache build-base

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ARG VES_API_KEY

ENV VES_API_KEY=$VES_API_KEY
ENV SERVICE_ACCOUNT_KEY=$SERVICE_ACCOUNT_KEY
ENTRYPOINT flask run --host=0.0.0.0
