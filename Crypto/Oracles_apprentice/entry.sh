#! /bin/bash

while :
do
    su -c "exec socat TCP-LISTEN:9001,reuseaddr,fork EXEC:'/app/chall.py,stderr'" - user;
done
