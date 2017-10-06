<?php
$server_name = "localhost";
$db_username = "root";
$db_password = "";
$db_name = "raf_anketa5";

$conn = new mysqli($server_name, $db_username, $db_password, $db_name);
if ($conn->connect_error) {
    die("connection failed: " . $conn->connect_error);
}
$conn->set_charset("utf8")

?>
