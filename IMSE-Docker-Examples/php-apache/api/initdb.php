<?php
    header('Access-Control-Allow-Origin: *');
    header('Content-Type: application/json');

    include_once 'config/DBConnection.php';

    $_db = new DBConnection();
    $_con = $_db->connect();

    $sql = "CREATE TABLE student (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    grade int(11) NOT NULL
    )";

    $_con->exec($sql);

    $sql = "INSERT INTO student (first_name, last_name, grade) VALUES
    ('Max', 'Mustermann', 2),
    ('Martin', 'Bogenbauer', 1),
    ('Henry', 'Split', 4),
    ('Anton', 'Quincy', 3),
    ('Kevin', 'Miller', 1);";

    $_con->exec($sql);
    echo json_encode(
        array('message' => 'Student Tables Created')
    );

    $_con = null;