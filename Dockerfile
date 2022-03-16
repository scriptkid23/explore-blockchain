FROM ubuntu:latest

RUN apt-get update 
RUN apt-get install -y software-properties-common
RUN apt-get install -y python3-pip
COPY . /blockchain