<?php
if($_SERVER["REQUEST_METHOD"] === "GET")
{
    $send_date = strtotime("2022-06-01");
    if(isset($_GET["email"]) && isset($_GET["secret"]) && !empty($_GET["email"]) && !empty($_GET["secret"]))
    {
        $db = new PDO("mysql:host=blackcatbdd;dbname=blackcat;charset=UTF8", "evilhackerz", "wjKNQJLSP4X3uPL522Q6");
        $sth = $db->prepare("SELECT secret,send_date FROM newsletter WHERE email = :e");
        $sth->bindValue(":e",htmlspecialchars($_GET["email"]));
        $sth->execute();
        $res = $sth->fetchAll();
        if(sizeof($res) > 0)
        {
            if($res[0][0] === $_GET["secret"])
            {
                if(strtotime($res[0][1]) > $send_date) echo "We are glad that you participate at this very hidden conference !<br>Conferences will take place at 'blackcatjnhhyaiolppiqnbsvvxgcifuelkzpalsm.onion'<br>Be sure to proof that you receive this email with this sentence : Hero{y0u_b34t_bl4ckc4t_0rg4n1z3rs!!}<br>BlackCat.";
                else{
                    header("Content-Type:application/json");
                    echo '{"err":"You have not been verified yet."}';
                }
            }else{
                header("Content-Type:application/json");
                echo '{"err":"Wrong secret"}';
            }
        }else{
            header("Content-Type:application/json");
            echo '{"err":"Wrong email"}';
        }
    }else{ 
        header("Content-Type:application/json");
        echo '{"err":"Missing parameters"}';
    }
}else{
    header("Content-Type:application/json");
    echo '{"err":"Method not allowed"}';
}