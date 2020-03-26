<?php
  header('Access-Control-Allow-Origin: *');
  header('Content-Type: application/json');

  include_once '../config/DBConnection.php';
  include_once '../models/Student.php';

  $_db = new DBConnection();
  $db = $_db->connect();

  $student = new Student($db);

  $result = $student->getAllStudent();
  $num = $result->rowCount();

  if($num > 0) {
    $students_arr = array();

    while($row = $result->fetch(PDO::FETCH_ASSOC)) {
      extract($row);

      $student_item = array(
        'id' => $id,
        'first_name' => $first_name,
        'last_name' => $last_name,
        'grade' => $grade
      );

      array_push($students_arr, $student_item);
    }

    echo json_encode($students_arr);

  } else {
    echo json_encode(
      array('message' => 'No Students Found')
    );
  }