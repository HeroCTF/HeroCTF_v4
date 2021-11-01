#!/bin/bash

for i in $(find . -name challenge.yml -type f)
do
    echo "--------[ $i ]--------"
    ctf challenge install $i
    ctf challenge sync $i
done
