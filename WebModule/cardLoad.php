<!DOCTYPE html>
<?php include "cardMenu.html"; ?>

<?php
$objectId = $_GET['objectId'];
//echo $objectId;

session_start();
$login = $_SESSION['inputLogin'];
$password = $_SESSION['inputPassword'];

if(isset($login, $password)){
	echo "start <br>";
	$conn = pg_connect("host=pg3.sweb.ru port=5432 dbname=avkuzbkru user=".$login." password=".$password);
	if (!$conn) {
		echo "Ошибка подключения к БД.\n";
		echo "Возможно, необходима <a href=\"authentificationForm.php\">авторизация</a>\n";
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
		$out = "<style>
		table, th, td {
		  border:1px solid black;
		}</style>
		<div id=\"source-html\">
		<h2>Карточка №".$objectId."</h2>
		<table style=\"width:100%\">
		<tr><td>Наименование объекта</td>
		<td>".$resRow[1]."</td></tr>
		<tr><td>Обиходные названия*</td>
		<td>".$resRow[2]."</td></tr>
		<tr><td>Место размещения объекта</td>	
		<td>".$resRow[3]."</td></tr>
		<tr><td>Время возникновения, открытия объекта</td>
		<td>".$resRow[4]."</td></tr>
		<tr><td>Краткая история объекта</td>
		<td>".$resRow[5]."</td></tr>
		<tr><td>Внешние признаки (особенности стиля, общая характеристика, сохранность)
		<td>".$resRow[6]."</td></tr>
		<tr><td>Данные об авторах объекта</td>
		<td>".$resRow[7]."</td></tr>
		<tr><td>Источники сведений об объекте</td>		
		<td>".$resRow[8]."</td></tr>
		<tr><td>Фотографии или видеоматериалы</td>
		<td><img src=\"data:image/png;base64,".$resRow[9]."\"/></td></tr>
		<tr><td>Дата составления карточки</td>
		<td>".$resRow[10]."</td></tr>
		</table>
		<p>* данная строка используется при необходимости</p>
		</div>";
		echo $out;
		
echo "<form id=\"actionForm\" action=\"\">
<p style=\"text-align: center;\">
<button name=\"objectId\" value=".$objectId." formmethod=\"GET\" formaction=\"cardAppendForm.php\">Редактировать</button>
<button formmethod=\"GET\" name=\"objectId\" value=".$objectId." formaction=\"cardDelete.php\">Удалить</button>
<button name=\"objectExport\" formmethod=\"GET\" onclick=\"exportHTML(); return false;\">Экспорт</button>
</p>
</form>";
		pg_close($conn);
	}
}
else {
	echo "Не заданы пароль и логин.\n";
	echo "Возможно, необходима <a href=\"authentificationForm.php\">авторизация</a>\n";
}
?>
<script>
    function exportHTML(){
       var header = "<html xmlns:o='urn:schemas-microsoft-com:office:office' "+
            "xmlns:w='urn:schemas-microsoft-com:office:word' "+
            "xmlns='http://www.w3.org/TR/REC-html40'>"+
            "<head><meta charset='utf-8'><title>Export HTML to Word Document with JavaScript</title></head><body>";
       var footer = "</body></html>";
       var sourceHTML = header+document.getElementById("source-html").innerHTML+footer;
       
       var source = 'data:application/vnd.ms-word;charset=utf-8,' + encodeURIComponent(sourceHTML);
       var fileDownload = document.createElement("a");
       document.body.appendChild(fileDownload);
       fileDownload.href = source;
       fileDownload.download = 'Карточка_№_<?=$objectId?>.doc';
       fileDownload.click();
       document.body.removeChild(fileDownload);
    }
</script> 
