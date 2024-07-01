<!DOCTYPE html>
<html>
<head>
<title>Математика в археологии</title>
<meta http-equiv="Content-Type" content="text/html" charset="utf8"/>
<meta content="nofollow"/>
</head>
<body>

<?php include "cardMenu.html"; ?>

<?php 
$objectId = $_GET['objectId'];
session_start();
$login = $_SESSION['inputLogin'];
$password = $_SESSION['inputPassword'];

if (isset($objectId)) {
    echo "Редактирование карточки № ".$objectId."</br>";
    //тут надо грузить в форму поля из БД
    $conn = pg_connect("host=pg3.sweb.ru port=5432 dbname=avkuzbkru user=".$login." password=".$password);
    if (!$conn) {
	echo "connection error occurred.\n";
	exit;
	}
	$statement = "SELECT * FROM card_legacy WHERE \"Номер карточки\"=".$objectId.";";
	$result = pg_query($conn, $statement);
	if (!$result) {
		echo "query error occurred.\n";
		exit;
	}
	else{
		echo "load success <br>";
		$resRow = pg_fetch_row($result); 
		pg_close($conn);
		$objectName = $resRow[1];
		$objectCommonName = $resRow[2];
		$objectPlace = $resRow[3];
		$objectCreationTime = $resRow[4];
		$objectShortStory = $resRow[5];
		$objectFeatures = $resRow[6];
		$objectAuthorsData = $resRow[7];
		$objectInformationSource = $resRow[8];
		$objectMedia = $resRow[9];
		$objectCardDateS = $resRow[10];
		
		preg_match("/^[0-9\.]+/", $objectCardDateS, $objectCardDateM);
		$objectCardDateN = date_create_immutable($objectCardDateM[0]);
		$objectCardDate = $objectCardDateN->format('Y-m-d');
		$cardFormEdit = $objectId;
		pg_close($conn);
	}
}
else {
	echo "Добавление новой карточки";
	$objectName = "Предмет кремневый";
	$objectCommonName = "";
	$objectPlace = "Археологический музей ВГУ";
	$objectCreationTime = "Эпоха камня (верхний палеолит)";
	$objectShortStory = "Найден в 2005 г. при раскопках в музее-заповеднике &laquo;Костёнки&raquo;";
	$objectFeatures = "Камень (светло-серый валунный кремень), Ретушь. Без видимых повреждений.";
	$objectAuthorsData = "Нет данных";
	$objectInformationSource = "Археологические раскопки";
	$objectMedia = "";
	$objectCardDate = "";
	$cardFormEdit = 0;
}
?>

<form id="inputForm" enctype="multipart/form-data" action="cardWrite.php" method="POST">
<p><strong>КАРТОЧКА ЭКСКУРСИОННОГО ОБЪЕКТА</strong></p>
<p>
<label for="objectName">Наименование объекта</label>
<input name="objectName" id="objectName" type="text" value="<?= $objectName ?>" required />
</p>
<p>
<label for="objectCommonName">Обиходные названия*</label>
<input name="objectCommonName" id="objectCommonName" type="text" value="<?= $objectCommonName ?>" /></p>
<p>
<label for="objectPlace">Место размещения объекта</label>
<input name="objectPlace" id="objectPlace" type="text" value="<?= $objectPlace ?>" />
</p>
<p>
<label for="objectCreationTime">Время возникновения, открытия объекта</label>
<input name="objectCreationTime" id="objectCreationTime" type="text" value="<?= $objectCreationTime ?>" />
</p>
<p>
<label for="objectShortStory">Краткая история объекта</label>
<textarea name="objectShortStory" id="objectShortStory" style="width: 50%;" required ><?= $objectShortStory ?> </textarea></p>
<p>
<label for="objectFeatures">Внешние признаки (особенности стиля, общая характеристика, сохранность)</label>
<textarea name="objectFeatures" id="objectFeatures" style="width: 50%;" required ><?= $objectFeatures ?></textarea></p>
<p>
<label for="objectAuthorsData">Данные об авторах объекта</label>
<input name="objectAuthorsData" id="objectAuthorsData" type="text" value="<?= $objectAuthorsData ?>" style="width: 50%;"/></p>
<p>Источники сведений об объекте <input name="objectInformationSource" type="text" value="<?= $objectInformationSource ?>" style="width: 50%;"/></p>
<p>
<label for="objectMedia">Фотографии или видеоматериалы</label>
<input name="objectMedia" id="objectMedia" type="file" value="" multiple/></p>
<p>
<label for="objectMedia">Дата составления карточки</label>
<input name="objectCardDate" type="date" value="<?= $objectCardDate ?>" required /></p>
<input type="hidden" name="formEditAction" value="<?=$cardFormEdit?>">
<p style="text-align: center;">
<input name="objectSubmit" type="submit" value="Записать карточку" onclick="checkDate()"/></p>
</form>
<p>* данная строка используется при необходимости</p>
</body>
</html>
