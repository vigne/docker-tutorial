<?php

include_once "../config/DBConnection.php";
class Student 
{
    private $db;
    private $table = 'student';
    private $_id;
    public $_firstName;
    public $_lastName;
    public $_grade;

    public function __construct($db) {
        $this->db = $db;
    }

    public function createStudent() {
        $query = 'INSERT INTO ' . $this->table . ' SET first_name = :first_name, last_name = :last_name, grade = :grade';

        $stmt = $this->db->prepare($query);

        $this->_firstName = htmlspecialchars(strip_tags($this->_firstName));
        $this->_lastName = htmlspecialchars(strip_tags($this->_lastName));
        $this->_grade = htmlspecialchars(strip_tags($this->_grade));

        $stmt->bindParam(':first_name', $this->_firstName);
        $stmt->bindParam(':last_name', $this->_lastName);
        $stmt->bindParam(':grade', $this->_grade);

        if($stmt->execute()) {
          return true;
    }
    printf("Error: %s.\n", $stmt->error);

    return false;
  }
   
    public function getAllStudent() {
    	try {
    		$sql = "SELECT * FROM student";
		    $stmt = $this->db->prepare($sql);

		    $stmt->execute();
            return $stmt;
		} catch (Exception $e) {
		    die("There's an error in the query!");
		}
    }
}
?>	