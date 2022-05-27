<?php
date_default_timezone_set('Europe/Berlin');
mb_internal_encoding('UTF-8');


$config = array(
	// add data in this scheme
	"key" => "value",
	
	// Simple file based login
	// Best practice: Make a baseRoute. Create a directory with the same name in /views.
	// Place in the created directory all views and additional files. They will automatically
	// be streamed if prefixed with "stream", e.g. /stream/login/sample.js. The password
	// must always be a SHA1 string, see PHP string function sha1() or create temporary a
	// new view sha1.php with the content: <?=sha("my password")
	//
	// baseRoute: All routes with this base will be secured.
	// users: Array with array having the keys "name" and "password", e.g. array("name" => "", "password" => "")
	"login" => array(
		"baseRoute" => "login",
		"users" => array(
			array("name" => "admin", "password" => "d033e22ae348aeb5660fc2140aec35850c4da997") // default password: admin
		)
	)
);
?>