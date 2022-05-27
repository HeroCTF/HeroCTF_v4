FROM ubuntu:latest

RUN apt-get update && apt install -y python3 python3-pip cron
RUN pip3 install mysql-connector-python

COPY ./mailer.py /root/mailer.py
COPY ./root /var/spool/cron/crontabs
RUN crontab /var/spool/cron/crontabs/root
CMD ["cron","-f"]
