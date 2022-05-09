<?php
session_start();
require_once("../functions/helpers.php");
addHint();
header("Content-Type: application/json");
if($_SERVER["REQUEST_METHOD"] === "POST")
{
    if(!isset($_SESSION["name"])) echo('{"err":"Access denied"}');
    else{
        require_once("../functions/connect_db.php");
        $db = connect();
        $sth = $db->prepare("SELECT id FROM users WHERE alias = :a");
        $sth->bindValue(":a",htmlspecialchars($_SESSION["name"]));
        $sth->execute();
        $res = $sth->fetchAll();
        if(sizeof($res) > 0)
        {
            $authorized_filetype = ["image/jpeg","image/jpg","image/png"];
            if(isset($_POST["url"]))
            {
                $url = $_POST["url"];
                if(filter_var($url, FILTER_VALIDATE_URL))
                {
                    $parsed_url = parse_url($url);
                    if(isset($parsed_url['scheme']) && ($parsed_url['scheme'] === "http" || $parsed_url['scheme'] === "https"))
                    {
                        
                        $img = file_get_contents($url, false, stream_context_create(['http' => ['ignore_errors' => true]]));
                        if($img){
                            $status_code = explode(" ",$http_response_header[0])[1];
                            $file_info = new finfo(FILEINFO_MIME_TYPE);
                            $mime_type = $file_info->buffer($img);
                            if(in_array($mime_type,$authorized_filetype))
                            {
                                $img_name = generateRandomString(15);
                                if($mime_type == "image/png") $ext = "png";
                                else $ext = "jpg";
                                $path_for_users = "/assets/users/".$ext."/";
                                $real_path = "/var/www/html".$path_for_users;
                                $filename = $real_path.$img_name.".".$ext;
                                file_put_contents($filename, $img);
                                $sth_new_image = $db->prepare("INSERT INTO cdn VALUES (0, :lti, :au)");
                                $sth_new_image->bindValue(":lti",$path_for_users.$img_name.".".$ext);
                                $sth_new_image->bindValue(":au",$res[0][0]);
                                $sth_new_image->execute();
                                echo('{"ok":"Image uploaded","reach":true}');
                            }else echo ('{"err":"Unauthorized file type","reach":true}');
                        }else echo('{"err":"Impossible to download image, please try again or provide another URL","reach":false}');
                    }else echo ('{"err":"Invalid url provided."}');
                }else echo ('{"err":"Invalid url provided."}');
            }else if(isset($_FILES["file"]) && $_FILES["file"]["error"] === UPLOAD_ERR_OK)
            {
                $fileType = $_FILES['file']['type'];
                $fileSize = $_FILES['file']['size'];
                $fileTmpPath = $_FILES['file']['tmp_name'];
                if(getimagesize($fileTmpPath))
                {
                    if($fileSize <= 400000)
                    {
                        if(in_array($fileType, $authorized_filetype))
                        {
                            $img_name = generateRandomString(15);
                            if($fileType == "image/png") $ext = "png";
                            else $ext = "jpg";
                            $path_for_users = "/assets/users/".$ext."/";
                            $real_path = "/var/www/html".$path_for_users;
                            $filename = $real_path.$img_name.".".$ext;
                            if(move_uploaded_file($fileTmpPath, $filename)){
                                $sth_new_image = $db->prepare("INSERT INTO cdn VALUES (0, :lti, :au)");
                                $sth_new_image->bindValue(":lti",$path_for_users.$img_name.".".$ext);
                                $sth_new_image->bindValue(":au",$res[0][0]);
                                $sth_new_image->execute();
                                echo('{"ok":"Image uploaded"}');
                            }else echo ('{"err":"An error occured, please try again"}');
                        }else echo('{"err":"Forbidden file provided, only jpg, jpeg and png are accepted."}');
                    }else echo('{"err":"File too large, upload are limited to 4Mo for free users"}');
                }else echo('{"err":"Forbidden file provided, only jpg, jpeg and png are accepted."}');
            }else echo('{"err":"Missing parameters"}');
        }else echo('{"err":"Access denied"}');
    }
}else echo('{"err":"Method not allowed"}');