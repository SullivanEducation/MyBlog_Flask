DROP TABLE users;
CREATE TABLE users (
    id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    email text,
    password text,
    username text
);