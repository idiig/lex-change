FROM python:3.8-buster as builder

MAINTAINER Xudong Chen <avionplat@hotmail.com>

WORKDIR /opt/app
COPY requirements.lock /opt/app

# Environment
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install --no-install-recommends -yq ssh git curl apt-utils && \
    apt-get install -yq gcc g++ && \
    apt-get install -y r-base

# Data
RUN mkdir data &&\
    wget -c https://github.com/yamagen/hachidaishu/raw/main/hachidai.db -P data

# Python dependencies
RUN pip install -r requirements.lock
