FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y socat software-properties-common gcc

COPY ./Impossible.c /impossible/
RUN gcc -o /impossible/Impossible /impossible/Impossible.c -lm
COPY ./entry.sh /impossible/
COPY ./flag.txt /impossible/

RUN groupadd ctf && \
    useradd -G ctf --home=/impossible player && \
    chown player:player /impossible/Impossible

RUN chmod 4755 /impossible/Impossible && \
    chmod 4755 /impossible/entry.sh

ENV LISTEN_PORT 7000
EXPOSE ${LISTEN_PORT}
ENTRYPOINT ["/impossible/entry.sh"]