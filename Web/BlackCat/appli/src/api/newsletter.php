<?php
header("Content-Type:application/json");
if($_SERVER["REQUEST_METHOD"] === "POST")
{
    if(isset($_POST["email"]) && !empty($_POST["email"]))
    {
        if(strlen($_POST["email"]) <= 1000)
        {
            $db = new PDO("mysql:host=blackcatbdd;dbname=blackcat;charset=UTF8", "evilhackerz", "wjKNQJLSP4X3uPL522Q6");
            $secret = bin2hex(openssl_random_pseudo_bytes(10));
            $query = "INSERT INTO newsletter(`send_date`,`email`,`secret`) VALUES ('".date('Y-m-d')."','".$_POST["email"]."','".$secret."')";
            if($db->query($query) !== False) echo '{"ok":"Check at /api/check.php with your email as get parameter and this secret: '.$secret.' as get parameter too, to check if you\'ve been accepted.<br>Example: https://blackcat.web.heroctf.fr/api/check.php?email=worty@blackcat.fr&secret=a32ecb08749ffeaf4e78"}';
            else echo '{"error":"An error occured, try again"}';
        }else echo '{"error":"Email must be at least 1000 characters."}';
    }else echo '{"error":"Missing parameters."}';
}else echo '{"error":"Method not allowed."}';
