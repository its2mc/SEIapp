
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
SHOW DATABASES;
