FROM ubuntu:18.04

# INSTALL NECESSARY SOFTWARE
RUN apt update
RUN apt install -y apache2 nodejs npm curl mysql-server

# ADD USER
RUN adduser --disabled-password --gecos "" player
RUN echo 'player:d4AP?5RB7k5My68' | chpasswd
RUN ln -sf /dev/null /home/player/.bash_history

# CONFIGURE APACHE SERVER
COPY apache2_conf/000-default.conf /etc/apache2/sites-available
COPY apache2_conf/apache2.conf /etc/apache2

# COPY ENTRY SCRIPT
COPY start.sh /root/start.sh
RUN chmod 755 /root/start.sh

#COPY FLAG
COPY flag.txt /home/player
RUN chmod 755 /home/player/flag.txt

# SETUP WEBSITE AND SERVER
COPY server /home/player/server
COPY website /home/player/website
COPY scripts /home/player/scripts
RUN chmod -R 755 /home/player/website/
RUN chmod +x /home/player/scripts/* /home/player/server/database/setupDb.sh
WORKDIR /home/player/website

# SETUP DATABASE
RUN /home/player/server/database/setupDb.sh

# CLEAN UP
RUN rm /home/player/server/database/setupDb.sh

# RUN ENTRYPOINT
EXPOSE 80
CMD /root/start.sh