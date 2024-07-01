<h1 class="mb-5">Вход</h1>

<?php require 'designFile.php'; ?>


<form method="post" action="authentification.php">
<div class="container">
        <label for="username" class="form-label">Логин</label>
        <input type="text" class="form-control" id="username" name="username" required><br>


        <label for="password" class="form-label">Пароль</label>
        <input type="password" class="form-control" id="password" name="password" required><br>

        <button type="submit" class="btn btn-primary">Login</button>
        </div>	
        
        <a class="btn btn-outline-primary" href="index.php">Register</a>
</form>


<?php
session_start();
		if(isset($_SESSION['inputError'])){
			echo $_SESSION['inputError'];
			unset($_SESSION['inputError']);
		}
	?>
