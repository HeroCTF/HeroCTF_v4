FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /deadalus/

RUN apt-get update && \
    apt-get install -y socat software-properties-common

RUN add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get install -y python3.10

COPY ./chall.py /deadalus/
COPY ./solve.py /deadalus/
COPY ./entry.sh /deadalus/
COPY ./flag.txt /deadalus/
COPY ./levels/ /deadalus/levels

RUN groupadd ctf && \
    useradd -G ctf --home=/deadalus player && \
    chown player:player /deadalus/chall.py

RUN chmod 4755 /deadalus/chall.py && \
    chmod 4755 /deadalus/entry.sh

EXPOSE 7000
ENTRYPOINT ["/deadalus/entry.sh"]