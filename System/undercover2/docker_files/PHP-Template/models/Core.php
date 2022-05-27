<?php
/**
 * Copyright (c) 2016 B. L.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 */


class Core {
	
	/**
	 * Autoloading PHP classes
	 */
	public static function autoload($name) {
		require "models/" . $name . ".php";
	}
	
	
	/**
	 * File by route
	 */
	public static function fileForBaseRouteInDirectory($dir) {
		$file_name = "default";
		$base_route = Request::route(0);
		
		if ($base_route == false)
			$base_route = "home";

		if ($base_route && preg_match("/^[\w\-]+$/", $base_route) && file_exists("{$dir}/{$base_route}.php"))
			$file_name = $base_route;
		
		return $file_name;
	}
	
	
	/**
	 * Controller
	 */
	public static function controller() {
		
		$controller = self::fileForBaseRouteInDirectory("controllers");
		
		require "controllers/{$controller}.php";
		exit();
	}
	
	
	/**
	 * View
	 */
	public static function view($name, $data=array(), $inView="master") {
		foreach ($data as $viewKey => $viewValue) {
			$$viewKey = $viewValue;
		}
		
		// do not show view files with full html tree in master view
		if (false !== strpos(file_get_contents("views/{$name}.php"), "<!DOCTYPE html>"))
			$inView = false;
		
		if ($inView) {
			$subView = $name;
			$name = $inView;
		}
		
		require "views/{$name}.php";
	}
	
	
	/**
	 * Load default view
	 */
	public static function defaultView($message = "") {
		self::view("default", array(
			"message" => $message
		));
		exit();
	}
	
	
	// ------------------------------------------------------------------------------
	
	
	/**
	 * Simple authentication feature
	 */
	private static function loginBaseRoute() {
		global $config;
		return isset($config, $config["login"]) && !empty($config["login"]["baseRoute"]) ? $config["login"]["baseRoute"] : false;
	}
	
	private static function loginRequiredURL() {
		
		global $config;
		
		if (isset($config, $config["login"]) && !empty($config["login"]["baseRoute"]) && in_array(Request::route(0), array("logout", "files", $config["login"]["baseRoute"])))
			return true;
		
		return false;
	}
	
	
	/**
	 * Simple authentication feature
	 */
	private static function loggedIn() {
		return isset($_SESSION["timeout"]) && $_SESSION["timeout"] > time() - 7200;
	}
	
	private static function login() {
		global $config;
		$baseRoute = Request::route(0);
		session_name("sid");
		$login_msg_id = false;
		
		// only start a session if the session cookie is provided
		if (isset($_COOKIE["sid"])) {
			session_start();
			// pass content for logged in users
			if (self::loggedIn()) {
				$_SESSION["timeout"] = time();
				return true;
			}
		}

		// try login
		if (isset($_POST["login_name"], $_POST["login_password"], $config["login"]["users"]) && is_array($config["login"]["users"])) {
			foreach ($config["login"]["users"] as $user) {
				if (array_key_exists("name", $user) && array_key_exists("password", $user) && $user["name"] == $_POST["login_name"] && $user["password"] == sha1($_POST["login_password"])) {
					session_start();
					$_SESSION["timeout"] = time();
					$_SESSION["user_name"] = $user["name"];
					return true;
				}
			}
			
			return "incorrect";
		}
		
		// otherwise present login and login if user name and password is passed
		self::logout();
		return false;
	}
	
	
	private static function logout() {
		if (session_status() == PHP_SESSION_ACTIVE)
			session_destroy();
		setcookie('sid', null, -1, '/');
		unset($_COOKIE["sid"]);
	}
	
	
	/**
	 * Stream file
	 * URL: /<baseRoute>/file/...
	 * Supported file extensions: css, js, png, jpg, gif
	 */
	public static function streamFile($file) {
		$mimes = array(
			"jpg" => "image/jpg",
			"png" => "image/png",
			"gif" => "image/gif",
			"css" => "text/css",
			"js" => "text/javascript"
		);

		// only allow files matching /views/<baseRoute>/...
		if (preg_match("/^\/files\/" . str_replace("-", "\-", self::loginBaseRoute()) . "\/[\w\/]+\.(" . implode("|", array_keys($mimes)) . ")$/", $file, $matches)) {
			$file = substr($file, 1);
			if (file_exists($file)) {
				header("Content-type: " . $mimes[$matches[1]] . ";charset=utf-8");
				die(file_get_contents($file));
			}
		}
		
		// streaming failed
		return false;
	}
}
?>