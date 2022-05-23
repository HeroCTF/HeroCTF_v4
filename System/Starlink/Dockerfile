FROM ubuntu:18.04

# Install dependecies
RUN apt update && apt install openssh-server openssh-client vim python3 python3-pip sudo wget unzip -y

# Setup users
RUN adduser --disabled-password --gecos "" user1
RUN echo 'user1:password123' | chpasswd
RUN ln -sf /dev/null /home/user1/.bash_history

RUN adduser --disabled-password --gecos "" user2
RUN echo 'user2:ke@5D!LF?LAALYH3' | chpasswd
RUN ln -sf /dev/null /home/user2/.bash_history

# Setup ssh keys
USER user2
RUN ssh-keygen -b 4096 -t rsa -f ~/.ssh/id_rsa -q -N ""
RUN cp /home/user2/.ssh/id_rsa.pub /home/user2/.ssh/authorized_keys
USER root
RUN ssh-keygen -b 4096 -t rsa -f ~/.ssh/id_rsa -q -N ""
RUN cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys

# Setup vulns
RUN groupadd zip
RUN usermod -aG zip user1
RUN usermod -aG zip user2
RUN usermod -aG user1 user2
RUN mkdir /home/zip
RUN chown root:zip /home/zip
RUN chmod 775 /home/zip
RUN chmod 777 /tmp
RUN chmod 750 /home/user2
COPY clone1.py /home/user1/clone1.py
COPY clone2.py /home/user2/clone2.py
RUN echo "user1 ALL=(user2) NOPASSWD:/home/user1/clone1.py" >> /etc/sudoers
RUN echo "user2 ALL=(root) NOPASSWD:/home/user2/clone2.py" >> /etc/sudoers

# Write flag
RUN echo "Hero{SymL1nk5_4r3_tr1cky}" > /root/flag.txt

# Copy starup file to container and run it
COPY start.sh /root/start.sh
RUN chmod +x /root/start.sh
EXPOSE 22
CMD ["/root/start.sh"]