<?php
session_start();
require_once("../functions/connect_db.php");
require_once("../functions/helpers.php");
addHint();
header("Content-Type: application/json");
if($_SERVER["REQUEST_METHOD"] === "POST")
{
    if(isset($_POST["alias"]) && isset($_POST["password"]) && !empty($_POST["alias"]) && !empty($_POST["password"]))
    {
        if(strlen($_POST["alias"]) < 100)
        {
            $db = connect();
            $sth = $db->prepare("SELECT password FROM users WHERE alias = :a");
            $sth->bindValue(":a",htmlspecialchars($_POST["alias"]));
            $sth->execute();
            $res = $sth->fetchAll();
            if(sizeof($res) > 0)
            {
                if($res[0][0] === md5($_POST["password"]))
                {
                    $_SESSION["name"] = htmlspecialchars($_POST["alias"]);
                    echo '{"ok":"User connected"}';
                }else echo('{"err":"Invalid credentials"}');
            }else echo('{"err":"Invalid credentials"}');
        }else echo('{"err":"Alias must be at least 100 characters"}');
    }else echo('{"err":"Missing parameters"}');
}else echo('{"err":"Method not allowed"}');