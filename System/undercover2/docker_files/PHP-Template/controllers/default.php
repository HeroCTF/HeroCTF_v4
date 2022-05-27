<?php
// login
if (self::loginRequiredURL()) {
	if (true === ($message = self::login())) {
		// logout
		if (Request::route(0) == "logout") {
			self::logout();
			Request::redirect("/");
		}
		
		// streaming of files
		elseif (Request::route(0) == "files") {
			if (!self::streamFile(Request::route())) {
				self::defaultView("fileNotFound");
			}
		}
		
		// views
		else {
			if (false !== ($baseRoute = self::loginBaseRoute())) {
				$view = self::loginBaseRoute() . "/" . (Request::route(1) ? Request::route(1) : "home");
				if (file_exists("views/" . $view . ".php")) {
					self::view($view, array(
						"user_name" => $_SESSION["user_name"]
					));
					exit();
				}
			}

			self::defaultView("viewNotFound");
		}
	}
	else {
		self::view("login", array(
			"message" => $message
		));
		exit();
	}
}


// view loading
$view = self::fileForBaseRouteInDirectory("views");
self::view($view, array());
?>