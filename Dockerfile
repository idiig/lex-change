FROM python:3.8-buster as builder

LABEL maintainer="avionplat@hotmail.com"

WORKDIR /opt/app

# Environment
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install --no-install-recommends -yq ssh git curl apt-utils && \
    apt-get install -yq gcc g++ && \
    apt-get install -y r-base

# Code
# RUN git clone -b main https://github.com/idiig/lex-change.git
RUN mkdir lex-change
COPY * /opt/app/lex-change

# Python dependencies
RUN pip install -r lex-change/requirements.lock

# Data
RUN wget -c https://github.com/yamagen/hachidaishu/raw/main/hachidai.db -P lex-change/data/hachidai.db
