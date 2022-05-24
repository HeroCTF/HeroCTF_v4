FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y socat python3 python3-pip
RUN python3 -m pip install pycryptodome

RUN mkdir /app
COPY . /app

RUN useradd --home=/app user
RUN chown user:user /app/chall.py

RUN chmod 4755 /app/chall.py
RUN chmod 4755 /app/entry.sh

EXPOSE 9000
ENTRYPOINT ["/app/entry.sh"]
