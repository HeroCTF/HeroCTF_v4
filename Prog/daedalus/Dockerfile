FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y socat
RUN apt-get install -y python3.10

RUN mkdir /deadalus
COPY ./chall.py /deadalus/
COPY ./solve.py /deadalus/
COPY ./entry.sh /deadalus/
COPY ./flag.txt /deadalus/
COPY ./levels/ /deadalus/levels

RUN groupadd ctf
RUN useradd -G ctf --home=/deadalus player
RUN chown player:player /deadalus/chall.py

RUN chmod 4755 /deadalus/chall.py
RUN chmod 4755 /deadalus/entry.sh

EXPOSE 7002
ENTRYPOINT ["/deadalus/entry.sh"]