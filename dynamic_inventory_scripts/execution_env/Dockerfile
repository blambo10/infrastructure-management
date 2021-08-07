#[BL] source https://medium.com/bitcraft/dockerizing-a-python-3-flask-app-line-by-line-400aef1ded3a
FROM python:3.7-alpine
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev libxml2-dev libxslt-dev libressl-dev python3-dev rust cargo
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
