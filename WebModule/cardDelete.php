<!DOCTYPE html>
<?php include "cardMenu.html"; ?>

<?php
$objectId = $_GET['objectId'];

session_start();
$login = $_SESSION['inputLogin'];
$password = $_SESSION['inputPassword'];

if(isset($login, $password)){
	echo "start <br>";
	echo $objectId;
	$conn = pg_connect("host=pg3.sweb.ru port=5432 dbname=avkuzbkru user=".$login." password=".$password);
	if (!$conn) {
		echo "connection error occurred.\n";
		exit;
	}
	$statement = "DELETE FROM card_legacy WHERE \"Номер карточки\"=".$objectId.";";
	$result = pg_query($conn, $statement);
	if (!$result) {
		echo "query error occurred.\n";
		exit;
	}
	else{
		echo "delete success <br>";
		header("Location: cardLoadForm.php");
	}
	}
else {
	echo "Не заданы пароль и логин.\n";
	echo "Возможно, необходима <a href=\"authentificationForm.php\">авторизация</a>\n";
}
?>
