FROM ubuntu:18.04

RUN apt-get update 
RUN apt-get install -y socat
RUN groupadd ctf

RUN mkdir /aargh
COPY ./aargh /aargh/
COPY ./entry.sh /aargh/

RUN useradd -G ctf --home=/aargh player

RUN chown player:player /aargh/aargh

RUN chmod 4755 /aargh/aargh
RUN chmod 4755 /aargh/entry.sh

USER player

ENV LISTEN_PORT 1337
EXPOSE 1337

ENTRYPOINT ["/aargh/entry.sh"]
