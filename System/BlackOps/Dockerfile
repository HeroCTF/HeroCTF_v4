FROM ubuntu:20.04

# Install dependecies
RUN apt-get update && \
    apt-get install -y openssh-server sudo openssh-client gcc psmisc nodejs patchelf vim

# Setup users
RUN adduser --disabled-password --gecos "" user1 && \
    echo 'user1:password123' | chpasswd && \
    ln -sf /dev/null /home/user1/.bash_history

# Setup Vulns
COPY servers /home/user1/servers
COPY *.c /tmp/
RUN gcc -s -c /tmp/genprocs.c -fpic -o /tmp/genprocs.o
RUN gcc -s -shared -o /tmp/libgenprocs.so /tmp/genprocs.o
RUN gcc -s -c /tmp/kc.c -o /tmp/kc.o
RUN gcc -s -o /tmp/kc /tmp/kc.o -L/tmp -lgenprocs
RUN gcc -s /tmp/main.c -o /tmp/restart_servers
RUN rm /tmp/*.c /tmp/*.o
RUN mkdir /home/user1/servers/utils/
RUN mv /tmp/restart_servers /home/user1/servers/utils/restart_servers
RUN cp /bin/rm /home/user1/servers/rm
RUN chmod +s /home/user1/servers/utils/restart_servers /home/user1/servers/rm
RUN mv /tmp/kc /bin/
RUN mv /tmp/libgenprocs.so /home/user1/servers/libs/libgenprocs.so
RUN echo "/home/user1/servers/libs/\n/home/user1/" > /etc/ld.so.conf.d/servers.conf
RUN chmod +x /home/user1/servers/src/*
RUN /home/user1/servers/utils/restart_servers

# Write flag
RUN echo "Hero{h1j4cked_l1k3_1n_Bl4ck_0ps}" > /root/flag.txt

# Copy starup file to container and run it
COPY start.sh /root/start.sh
RUN chmod +x /root/start.sh
EXPOSE 22
CMD ["/root/start.sh"]