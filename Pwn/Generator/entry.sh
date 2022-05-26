#!/bin/bash

while :
do
	exec socat TCP-LISTEN:${LISTEN_PORT},reuseaddr,fork EXEC:'/Generator/Generator,stderr'
done

