#!/bin/bash

if ! test -f ".ctf/config"; then
    ctf init
fi

for i in $(find . -name challenge.yml -type f 2>/dev/null)
do
    echo "--------[ $i ]--------"
    ctf challenge install "$i"
    # ctf challenge sync "$i"
done
