#! /bin/bash
apachectl -D FOREGROUND &
mkdir /var/run/sshd
/usr/sbin/sshd -D