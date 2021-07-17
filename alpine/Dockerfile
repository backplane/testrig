FROM python:3.9-alpine
LABEL maintainer="Backplane BV <info@backplane.be>"

WORKDIR /testrig

COPY requirements.txt /
RUN set -x \
  && python -m venv venv \
  && source venv/bin/activate \
  && pip install -r /requirements.txt
