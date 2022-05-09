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
            $sth_already_exist = $db->prepare("SELECT * FROM users WHERE alias = :a");
            $sth_already_exist->bindValue(":a",htmlspecialchars($_POST["alias"]));
            $sth_already_exist->execute();
            $res = $sth_already_exist->fetchAll();
            if(sizeof($res) == 0)
            {
                $sth_insert_user = $db->prepare("INSERT INTO users VALUES (0,:a,:p)");
                $sth_insert_user->bindValue(":a",htmlspecialchars($_POST["alias"]));
                $sth_insert_user->bindValue(":p",md5($_POST["password"]));
                $sth_insert_user->execute();
                echo('{"ok":"User created"}');
            }else echo('{"err":"Alias already taken"}');
        }else echo('{"err":"Alias must be at least 100 characters"}');
    }else echo('{"err":"Missing parameters"}');
}else echo('{"err":"Method not allowed"}');