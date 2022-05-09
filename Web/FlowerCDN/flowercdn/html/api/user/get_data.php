<?php
error_reporting(E_ALL ^ E_WARNING); 
session_start();
require_once("../functions/helpers.php");
addHint();
header("Content-Type: application/json");
if($_SERVER["REQUEST_METHOD"] === "GET")
{
    if(!isset($_SESSION["name"])) echo('{"err":"Access denied"}');
    else{
        if(!isset($_GET["size"]) || !is_numeric($_GET["size"])) $size = 10;
        else $size = htmlspecialchars($_GET["size"]);
        require_once("../functions/connect_db.php");
        $db = connect();
        $sth = $db->prepare("SELECT id FROM users WHERE alias = :a");
        $sth->bindValue(":a",htmlspecialchars($_SESSION["name"]));
        $sth->execute();
        $res = $sth->fetchAll();
        if(sizeof($res) > 0)
        {
            $sth_storage = $db->prepare("SELECT id,link_to_img FROM cdn WHERE associateUser = :au LIMIT :size");
            $sth_storage->bindValue(":au",$res[0][0]);
            $sth_storage->bindValue(":size",$size,PDO::PARAM_INT);
            $sth_storage->execute();
            $res_storage = $sth_storage->fetchAll();
            $res_storage['host'] = $_SERVER["HTTP_HOST"];
            echo(json_encode($res_storage));
        }else echo('{"err":"Access denied"}');
    }
}else echo('{"err":"Method not allowed"}');