#!/bin/bash

PWD=$(pwd)

function build() {
    path=$1
    image_name=$2

    pushd "${PWD}/${path}"
    docker build . -t "$image_name"
    popd
}

# Image tag supports only lowercase letters
build "./Prog/SSHs" "sshs:latest"
build "./System/BlackOps" "blackops:latest"
build "./System/Starlink" "starlink:latest"
# build "./Web/whereBackdoor" "wherebackdoor:latest"
build "./Web/HeroVIP" "herovip:latest"
build "./System/undercover1" "undercover_1:latest"
build "./System/undercover2" "undercover_2:latest"
