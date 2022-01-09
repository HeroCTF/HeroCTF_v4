#! /bin/bash

while :
do
    su -c "exec socat TCP-LISTEN:7002,reuseaddr,fork EXEC:'/deadalus/chall.py,stderr'" - player;
done