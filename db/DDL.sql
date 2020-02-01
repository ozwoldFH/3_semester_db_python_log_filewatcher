-- this file will delete existing table and create new ones

CREATE DATABASE IF NOT EXISTS db_logs CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE db_logs;

DROP TABLE IF EXISTS T_OnSuccess;
DROP TABLE IF EXISTS T_OnError;


CREATE TABLE IF NOT EXISTS T_OnSuccess(
	id INT AUTO_INCREMENT PRIMARY KEY,
	log_datetime DATETIME,
	insert_datetime DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	pc_name VARCHAR(255),
	name VARCHAR(255) NOT NULL,
	a VARCHAR(255),
	b VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS T_OnError(
	id INT AUTO_INCREMENT PRIMARY KEY,
	log_datetime DATETIME,
	insert_datetime DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	message VARCHAR(255) NOT NULL
);

-- add inital data
INSERT INTO T_OnSuccess (log_datetime, pc_name, name, a, b)
	VALUES(NOW(), 'init_db', 'init_db', '-', '-');

-- add inital data
INSERT INTO T_OnError (log_datetime, message)
	VALUES(NOW(), 'init_db');