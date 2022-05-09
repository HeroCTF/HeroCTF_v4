<?php
require_once("api/functions/helpers.php");
addHint();
session_start();
include("templates/header.html");
if(!isset($_SESSION["name"])) include("templates/notlogged/index.html");
else include("templates/logged/index.html");