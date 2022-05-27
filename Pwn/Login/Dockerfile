FROM ubuntu:21.10

RUN apt-get update && \
    apt-get install -y socat

COPY ./Login /login/
COPY ./entry.sh /login/
COPY ./flag.txt /login/

RUN groupadd ctf && \
    useradd -G ctf --home=/login player && \
    chown player:player /login/Login

RUN chmod 4755 /login/Login && \
    chmod 4755 /login/entry.sh && \
	chmod 4755 /login/

EXPOSE ${LISTEN_PORT}

ENTRYPOINT ["/login/entry.sh"]
