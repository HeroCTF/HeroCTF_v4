
FROM ubuntu:21.10

RUN apt update && apt install openssh-server gcc g++ python3 sudo -y

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
