FROM ubuntu:18.04

RUN apt-get update 
RUN apt-get install -y socat cron
RUN groupadd ctf

RUN mkdir /self
COPY ./sELF_control /self/
COPY ./entry.sh /self/
COPY ./EXECUTE_ME /self/
COPY ./flag.txt /self/
COPY ./clean.sh /self/

RUN useradd -G ctf --home=/self player

RUN chown player:player /self/sELF_control
RUN chown player:player /self/EXECUTE_ME
RUN chown player:player /self/flag.txt
RUN chown player:player /self/clean.sh

RUN chmod +x /self/clean.sh
RUN chmod 777 /self/
RUN chmod 4777 /self/sELF_control
RUN chmod 4777 /self/EXECUTE_ME
RUN chmod 4777 /self/entry.sh

RUN (crontab -l 2>/dev/null; echo "*/10 * * * * /self/clean.sh") | crontab -

EXPOSE 8000
ENTRYPOINT ["/self/entry.sh"]
