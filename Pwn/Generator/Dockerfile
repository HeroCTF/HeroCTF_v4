FROM ubuntu:21.10

RUN apt-get update 
RUN apt-get install -y socat
RUN groupadd ctf

RUN mkdir /Generator
COPY ./Generator /Generator/
COPY ./entry.sh /Generator/
COPY ./flag.txt /Generator/

RUN useradd -G ctf --home=/Generator player

RUN chown player:player /Generator/Generator

RUN chmod 4755 /Generator/Generator
RUN chmod 4755 /Generator/entry.sh
RUN chmod 4755 /Generator/flag.txt

USER player

EXPOSE ${LISTEN_PORT}

ENTRYPOINT ["/Generator/entry.sh"]
