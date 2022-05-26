#!/bin/bash

while :
do
	exec socat TCP-LISTEN:${LISTEN_PORT},reuseaddr,fork EXEC:'/aargh/aargh,stderr'
done

