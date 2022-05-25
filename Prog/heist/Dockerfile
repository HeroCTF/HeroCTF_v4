FROM ubuntu:20.04

WORKDIR /heist/

RUN apt-get update && \
    apt-get install -y socat python3

COPY ./chall.py /heist/
COPY ./entry.sh /heist/
COPY ./flag.txt /heist/

RUN groupadd ctf && \
    useradd -G ctf --home=/heist player && \
    chown player:player /heist/chall.py

RUN chmod 4755 /heist/chall.py && \
    chmod 4755 /heist/entry.sh

ENV TERM xterm

EXPOSE ${LISTEN_PORT}
ENTRYPOINT ["/heist/entry.sh"]