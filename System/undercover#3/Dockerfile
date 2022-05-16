FROM ubuntu:16.04

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

# Install dependecies
RUN apt update && apt install openssh-server sudo openssh-client -y

# Setup users
RUN adduser --disabled-password --gecos "" user1
RUN echo 'user1:password123' | chpasswd
RUN ln -sf /dev/null /home/user1/.bash_history

RUN adduser --disabled-password --gecos "" user2
RUN echo 'user2:Yo8c489EcAcQT&pa' | chpasswd
RUN ln -sf /dev/null /home/user2/.bash_history

# Write flag
RUN echo "Hero{f4ke_fl4g}" > /root/flag.txt

# Copy starup file to container and run it
COPY start.sh /root/start.sh
RUN chmod +x /root/start.sh
EXPOSE 22
CMD ["/root/start.sh"]