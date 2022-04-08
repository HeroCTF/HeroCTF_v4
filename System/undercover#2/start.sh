#! /bin/bash
apachectl start
mkdir /var/run/sshd
/usr/sbin/sshd -D