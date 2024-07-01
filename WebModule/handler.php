<?php
$input = $_REQUEST['a1'] ?? '';
if(strcasecmp($input,'CSVToDb') == 0){
	echo "start <br>";
	$conn = pg_connect("host = pg3.sweb.ru port = 5432 dbname = avkuzbkru user = avkuzbkru password=Klizma000");
	if (!$conn) {
		echo "connection error occurred.\n";
		exit;
	}
$statement = "COPY card_legacy2 ( object_name,usage_name,placement,period,history,appearance,author,data_source,resources,card_creation_date)

	FROM 'result.csv'
	DELIMITER ','
	CSV HEADER;";
//$statement = "SELECT * FROM card_legacy;";
	$result = pg_query($conn, $statement);
		if (!$result) {
			echo pg_last_error();
			echo "query error occurred.\n";
			exit;
		}

}
?>