<!DOCTYPE html>
<html>
<head>
<title>Математика в археологии</title>
<meta http-equiv="Content-Type" content="text/html" charset="utf8"/>
<meta content="nofollow"/>
</head>
<body>

<?php include "cardMenu.html"; ?>

<form id="cardLoadForm" action="cardLoad.php" method="GET">
<p><strong>КАРТОЧКА ЭКСКУРСИОННОГО ОБЪЕКТА №</strong>
<input name="objectId" type="text" value="1" /></p>
<p style="text-align: center;"><input name="objectSubmit" type="submit" value="Поиск карточки"/></p>
</form>
<p id="log"></p>
<?php include "baseLoad.php"; ?>
<script>
function logSubmit(event) {
  log.textContent = `Form Submitted! Timestamp: ${event.timeStamp}`;
  //event.preventDefault();
}

const form = document.getElementById("cardLoadForm");
const log = document.getElementById("log");
form.addEventListener("submit", logSubmit);

var image = new Image();
image.src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO        9TXL0Y4OHwAAAABJRU5ErkJggg==';
document.body.appendChild(image);
</script>
</body>
</html>
