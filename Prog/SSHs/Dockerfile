
FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y openssh-server gcc g++ python3 sudo

# Copy setup file and run it
COPY flag.txt /root
COPY setupDocker.py /root
RUN python3 /root/setupDocker.py

# Restrict external ssh access to user1 only
RUN echo "\nPermitRootLogin no\n\nPasswordAuthentication no\n\nMatch User user1\n\tPasswordAuthentication yes\n\nMatch Address 127.0.0.1\n\tPasswordAuthentication yes" >> /etc/ssh/sshd_config

# Run ssh server
EXPOSE 22
RUN mkdir -p /run/sshd
CMD ["/usr/sbin/sshd", "-D"]
