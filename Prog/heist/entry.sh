#! /bin/bash

while :
do
    su -c "exec socat TCP-LISTEN:7001,reuseaddr,fork EXEC:'/heist/chall.py,stderr'" - player;
done