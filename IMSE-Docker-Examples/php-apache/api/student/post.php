<?php 
  header("Access-Control-Allow-Origin: *");
  header("Content-Type: application/json; charset=UTF-8");
  header("Access-Control-Allow-Methods: OPTIONS,GET,POST,PUT,DELETE");
  header("Access-Control-Max-Age: 3600");
  header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");
  

  include_once '../config/DBConnection.php';
  include_once '../models/Student.php';

  $_db = new DBConnection();
  $db = $_db->connect();

  $student = new Student($db);

  $data = json_decode(file_get_contents("php://input"));

  if($data->first_name != ""){
    $student->_firstName = $data->first_name;
    $student->_lastName = $data->last_name;
    $student->_grade = $data->grade;

    if($student->createStudent()) {
        echo json_encode(
        array('message' => 'Student Created')
        );
    } else {
        echo json_encode(
        array('message' => 'Student Not Created')
        );
    }
  }
  