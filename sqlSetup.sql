/*
This procedure sets up the sql environment for use in the
sei app.. It creates a new user with the given credentials,
creates a database under those credentials and creates a table 
with the required fields 
*/
/*CREATE VIRTUAL PROCEDURE*/
BEGIN
	CREATE DATABASE seidb;
	CREATE USER 'seiuser'@'localhost' IDENTIFIED BY 'r1o2o3t4`';
	USE seidb;
	GRANT ALL ON seidb.* TO 'seiuser'@'localhost';
	CREATE TABLE sensorData(
		id INT NOT NULL AUTO_INCREMENT,
		sensorID TEXT NOT NULL,
		data TEXT NOT NULL,
		timestamp TEXT,
		PRIMARY KEY ( id );
);
END