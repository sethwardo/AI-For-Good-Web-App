DROP DATABASE IF EXISTS insta_db;
CREATE DATABASE insta_db;
USE insta_db;

DROP TABLE IF EXISTS insta_db.article;

CREATE TABLE insta_db.article (
	id INT NOT NULL,
	title VARCHAR(255) NULL,
	author VARCHAR(255) NULL,
	keywords VARCHAR(255) NULL,
	publish_date VARCHAR(255) NULL,
	articleLink VARCHAR(255) NULL,
	graph LONGTEXT NULL,
	PRIMARY KEY (id)
);


   