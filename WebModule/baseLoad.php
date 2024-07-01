<?php
session_start();
$login = $_SESSION['inputLogin'];
$password = $_SESSION['inputPassword'];

if(isset($login, $password)){
	echo "start <br/>";
	$conn = pg_connect("host=pg3.sweb.ru port=5432 dbname=avkuzbkru user=".$login." password=".$password);
	if (!$conn) {
		echo "Ошибка подключения к БД.\n";
		echo "Возможно, необходима <a href=\"authentificationForm.php\">авторизация</a>\n";
		exit;
	}

	else{
		echo "Загрузка карточек из БД успешна<br>";
		echo "<h2>Список имеющихся карточек </h2>";
		$statementIndices = "SELECT \"Номер карточки\" FROM card_legacy ORDER BY \"Номер карточки\";";
		$resIndices = pg_query($conn, $statementIndices);
	if (!$resIndices) {
		echo "query error occurred.\n";
		exit;
	}
		while ($index = pg_fetch_row($resIndices)) {
  			echo "<a href=\"cardLoad.php?objectId=".$index[0]."\">Карточка № ".$index[0]."</a>";
  			echo "<br />\n";
		}
		//echo "<p>Предыдущая карточка Следующая карточка</p>";
		//print_r($resIndices);
		pg_close($conn);
	}
}
else {
	echo "Не заданы пароль и логин.\n";
	echo "Возможно, необходима <a href=\"authentificationForm.php\">авторизация</a>\n";
}
?>
