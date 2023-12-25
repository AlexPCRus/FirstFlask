#Source
FROM python:3.12-slim as base
LABEL maintainer="AlexPC (alexmed2000@mail.ru)"

# Updates
ARG BUILD_DEPS="curl"
RUN apt-get update && apt-get install -y $BUILD_DEPS

# Python settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Ports
EXPOSE 5000

# Requirements
WORKDIR /first_flask
COPY requirements.txt .
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Source code
COPY static static
COPY templates templates
COPY main.py main.py

# Run
ENV FLASK_APP=/first_flask/main.py
CMD ["flask", "run", "--host", "0.0.0.0"]
