FROM python:3.11-slim-buster

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

ENV TZ=America/Sao_Paulo

RUN apt-get update \
    && apt-get -y install curl gcc cron vim tzdata python3-dev default-libmysqlclient-dev build-essential pkg-config

RUN curl -fsSL https://get.docker.com | sh

# sync timezone
RUN echo $TZ > /etc/timezone \
    && ln -fsn /usr/share/zoneinfo/$TZ /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /doguipy
COPY . /doguipy
WORKDIR /doguipy

EXPOSE 8088

CMD ["python", "main.py"]