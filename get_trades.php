<?php
header("Content-Type: application/json");

$mysqli = new mysqli("localhost", "root", "password", "crypto_transaction");

if ($mysqli->connect_error) {
   
    echo json_encode(["error" => "Database connection failed: " . $mysqli->connect_error]);
    exit();
}

$query = "SELECT user_id, type AS action, coin AS pair, amount, price, created_at FROM transactions ORDER BY created_at DESC LIMIT 10";

if ($result = $mysqli->query($query)) {
    $transactions = [];
    while ($row = $result->fetch_assoc()) {
        $transactions[] = $row;
    }

    echo json_encode($transactions);
    $result->free();
} else {
    echo json_encode(["error" => "Query failed: " . $mysqli->error]);
}

$mysqli->close();
?>
