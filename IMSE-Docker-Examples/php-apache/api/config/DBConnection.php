<?php
class DBConnection {
    private $host = "sql";
    private $db_name = "imse_sql_db";
    private $username = "user";
    private $password = "password";
    private $_con;
 
    public function __construct() {
        $this->_con = null;
        
        try {
        	$this->_con = new PDO('mysql:host=' . $this->host . ';dbname=' . $this->db_name, $this->username, $this->password);    
        	$this->_con->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	    } catch(PDOException $e) {
			echo "Connection failed: " . $e->getMessage();
		}
    }
    
    public function connect() {
        return $this->_con;
    }
}