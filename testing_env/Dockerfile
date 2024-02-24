FROM alpine:latest

RUN apk add --no-cache python3
RUN apk add --no-cache gcc
RUN apk add --no-cache g++
RUN apk add --no-cache su-exec
RUN apk add --no-cache bash

WORKDIR /usr/test_env

COPY testing_pipeline.py .
