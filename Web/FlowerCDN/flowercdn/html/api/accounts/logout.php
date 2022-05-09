<?php
require_once("../functions/helpers.php");
addHint();
session_start();
session_destroy();
header("Location: /");