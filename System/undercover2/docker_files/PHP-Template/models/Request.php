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


class Request
{
	/**
	 * path
	 */
	private static $routes = false;
	
	
	/**
	 * Path and file
	 *
	 * @param integer $n (Optional) Return specific route.
	 * @return string|false
	 */
	public static function route($n=false)
	{
		if (self::$routes === false)
		{
			self::$routes = self::getRoutesOfPath($_SERVER['REQUEST_URI']);
		}

		// return full URL
		if ($n === false)
		{
			return '/' . implode('/', self::$routes);
		}
		
		// last or nth element
		else {
			$n = $n == -1 ? count(self::$routes) - 1 : $n;
			return array_key_exists($n, self::$routes) ? self::$routes[$n] : false;
		}
	}
	
	
	/**
	 * Returns routes from path
	 */
	private static function getRoutesOfPath($path) {
		return explode('/', preg_replace('/^\/|\/$/', '', preg_replace("/\.json.*$/", '', $path)));
	}
	
	
	/**
	 * HTTP redirect
	 *
	 * @param string $location
	 */
	public static function redirect($location)
	{
		header("Location: {$location}");
		exit();
	}
}
?>