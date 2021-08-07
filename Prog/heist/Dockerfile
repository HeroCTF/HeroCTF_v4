FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y socat
RUN apt-get install -y python3

RUN mkdir /heist
COPY ./chall.py /heist/
COPY ./entry.sh /heist/
COPY ./flag.txt /heist/

RUN groupadd ctf
RUN useradd -G ctf --home=/heist player
RUN chown player:player /heist/chall.py

RUN chmod 4755 /heist/chall.py
RUN chmod 4755 /heist/entry.sh

EXPOSE 7001
ENTRYPOINT ["/heist/entry.sh"]