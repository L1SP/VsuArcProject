<?php

require 'designFile.php';

session_start();

$inputLogin = $_POST['username'];
$inputPassword = $_POST['password'];

$conn = pg_connect("host=pg3.sweb.ru port=5432 dbname=avkuzbkru user=".$inputLogin." password=".$inputPassword);
if (!$conn) {
	echo "connection error occurred.\n";
	$_SESSION['inputError'] = 'Неправильный логин/пароль.';
	header('Location: authentificationForm.php');
	exit;
}
else {
	echo "Подключение к БД успешно.\n";
	$_SESSION['inputLogin'] = $inputLogin;
	$_SESSION['inputPassword'] = $inputPassword;
	unset($_session['inputerror']);
	header('Location:cardLoadForm.php');
	die();
	pg_close();
}


//if($inputLogin == $login && $inputPassword == $password){
//	unset($_session['inputerror']);
//	header('Location:cardMenu.html');
//	die();
//}
//else{
//	$_SESSION['inputError'] = 'Неправильный логин/пароль.';
//	 header('Location: authentificationForm.php');
//	 exit();
//}


?>
