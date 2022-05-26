FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

# Install dependecies
RUN apt update && apt install openssh-server sudo apache2 curl openssh-client php libapache2-mod-php vim -y

# Setup users
RUN adduser --disabled-password --gecos "" dev
RUN echo 'dev:z85r@dhMCJJHN#sh' | chpasswd
RUN ln -sf /dev/null /home/dev/.bash_history
RUN echo "dev ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN adduser --disabled-password --gecos "" user1
RUN echo 'user1:password123' | chpasswd
RUN ln -sf /dev/null /home/user1/.bash_history
USER user1
RUN ssh-keygen -q -t rsa -N '' -f /home/user1/.ssh/id_rsa
USER root

# Setup php server
RUN a2enmod mpm_prefork && sudo a2enmod php*
COPY docker_files/envvars /etc/apache2/envvars
RUN rm -rf /var/www/html
COPY docker_files/PHP-Template /var/www/html
RUN chmod 777 /var/www/html

# Copy flag
COPY flag.txt /root/flag.txt

# Copy startup file to container and run it
COPY start.sh /root/start.sh
RUN chmod +x /root/start.sh
EXPOSE 22
CMD ["/root/start.sh"]