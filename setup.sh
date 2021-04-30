#!/usr/bin/env bash

categories=( Blockchain Crypto Forensics Misc OSINT Pwn Reverse Steganography System Web )

for category in "${categories[@]}"
do
    mkdir $category
    touch $category/.gitkeep
done

echo "Done !"
