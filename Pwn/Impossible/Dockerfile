FROM ubuntu:21.10

RUN apt-get update && \
    apt-get install -y socat

COPY ./Impossible /impossible/
COPY ./entry.sh /impossible/
COPY ./flag.txt /impossible/

RUN groupadd ctf && \
    useradd -G ctf --home=/impossible player && \
    chown player:player /impossible/Impossible

RUN chmod 4755 /impossible/Impossible && \
    chmod 4755 /impossible/entry.sh && \
	chmod 4755 /impossible/

EXPOSE ${LISTEN_PORT}

ENTRYPOINT ["/impossible/entry.sh"]
