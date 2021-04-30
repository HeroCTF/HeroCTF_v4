FROM alpine:3.13.1 

WORKDIR /usr/src
RUN apk add --no-cache python3 python3-dev py3-pip socat gcc g++ make libffi-dev openssl-dev
RUN python3 -m pip install --no-cache-dir pycrypto

COPY ./challenge.py /usr/src/challenge.py
COPY ./entry.sh /usr/src/entry.sh

RUN adduser --disabled-password --no-create-home heroctf
RUN chown heroctf:heroctf /usr/src/challenge.py
RUN chown heroctf:heroctf /usr/src/entry.sh
RUN chmod 540 /usr/src/challenge.py
RUN chmod 540 /usr/src/entry.sh

USER heroctf

ENTRYPOINT ["/usr/src/entry.sh"]
