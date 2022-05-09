<?php

function generateRandomString($length) {
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $charactersLength = strlen($characters);
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[rand(0, $charactersLength - 1)];
    }
    return $randomString;
}

function getip()
{
    //yeah I know, it's... awful
    return shell_exec("ip a | tr -d '\n' | awk '{print $71}' | cut -d'/' -f1");
}

function addHint(){
    header("X-Internal-Ip: ".getip());
}