#!/bin/bash

PWD=$(pwd)

function build() {
    path=$1
    image_name=$2

    cd "${PWD}/${path}"
    sudo docker build . -t "$image_name"
}

# Image tag supports only lowercase letters
build "./Prog/SSHs" "sshs:latest"