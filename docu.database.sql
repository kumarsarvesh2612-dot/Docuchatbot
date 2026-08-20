CREATE DATABASE document;
USE document;
CREATE TABLE USERS(
id int auto_increment primary key,
name varchar(100) not null,
email varchar(150)unique not null,
password varchar(125) not null
);