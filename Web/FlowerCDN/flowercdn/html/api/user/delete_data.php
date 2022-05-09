<?php
session_start();
require_once("../functions/helpers.php");
addHint();
header("Content-Type: application/json");
if($_SERVER["REQUEST_METHOD"] === "POST")
{
    if(!isset($_SESSION["name"])) echo('{"err":"Access denied"}');
    else{
        if(isset($_POST["id"]) && is_numeric($_POST["id"]))
        {
            require_once("../functions/connect_db.php");
            $db = connect();
            $sth = $db->prepare("SELECT id FROM users WHERE alias = :a");
            $sth->bindValue(":a",htmlspecialchars($_SESSION["name"]));
            $sth->execute();
            $res = $sth->fetchAll();
            if(sizeof($res) > 0)
            {
                $sth_images = $db->prepare("SELECT id,link_to_img FROM cdn WHERE associateUser = :au");
                $sth_images->bindValue(":au",$res[0][0]);
                $sth_images->execute();
                $all_images = $sth_images->fetchAll();
                $found = False;
                $link = "";
                foreach($all_images as $image)
                {
                    if($image[0] == $_POST["id"])
                    {
                        $link = $image[1];
                        $found = True;
                        break;
                    }
                }
                if($found)
                {
                    unlink("/var/www/html".$link);
                    $sth_delete = $db->prepare("DELETE FROM cdn WHERE id = :id");
                    $sth_delete->bindValue(":id",htmlspecialchars($_POST["id"]));
                    $sth_delete->execute();
                    echo('{"ok":"Image deleted"}');
                }else echo('{"err":"Wrong id provided or this image doesn\'t belong to you."}');
            }else echo('{"err":"Access denied"}');
        }else echo('{"err":"Missing parameter or id is not an integer."}');
    }
}else echo('{"err":"Method not allowed"}');