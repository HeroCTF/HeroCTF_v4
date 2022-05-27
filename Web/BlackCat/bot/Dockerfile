FROM ubuntu:latest

RUN apt-get update && apt install -y python3 python3-pip
RUN pip3 install mysql-connector-python

COPY ./mailer.py /root/mailer.py

CMD ["python3","/root/mailer.py"]
