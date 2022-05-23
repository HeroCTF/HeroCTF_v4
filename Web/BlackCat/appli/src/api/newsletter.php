<?php
header("Content-Type:application/json");
if($_SERVER["REQUEST_METHOD"] === "POST")
{
    if(isset($_POST["email"]) && !empty($_POST["email"]))
    {
        if(strlen($_POST["email"]) <= 1000)
        {
            $db = new PDO("mysql:host=blackcatbdd;dbname=blackcat;charset=UTF8", "evilhackerz", "wjKNQJLSP4X3uPL522Q6");
            $query = "INSERT INTO newsletter(`id`,`send_date`,`email`) VALUES (0,'".date('Y-m-d')."','".$_POST["email"]."')";
            if($db->query($query) !== False) echo '{"ok":"You will receive the email for the exact location in 3 days. Thank you."}';
            else echo '{"error":"An error occured, please try again."}';
        }else echo '{"error":"Email must be at least 100 characters."}';
    }else echo '{"error":"Missing parameters."}';
}else echo '{"error":"Method not allowed."}';
