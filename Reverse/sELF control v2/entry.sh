#!/bin/bash

/self/clean.sh&
while :
do
	su -c "exec socat TCP-LISTEN:8000,reuseaddr,fork EXEC:'/self/sELF_control,stderr'" - player;
done
