<h1>Login</h1>
<? if (!empty($message)): ?>
<p><?=$message?></p>
<? endif ?>
<form action="<?=Request::route()?>" method="post">
	<label for="login-name">Name</label>
	<input type="name" id="login-name" name="login_name">
	<label for="login-password">Password</label>
	<input type="password" id="login-password" name="login_password">
	<input type="submit" value="Login">
</form>