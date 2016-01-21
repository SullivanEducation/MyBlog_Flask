CREATE TABLE article (
    title tinytext,
    body text,
    timestamp datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    modified_at datetime NOT NULL
);

CREATE TABLE comment (
    body text,
    nickname tinytext,
    articleid int,
    timestamp datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE users (
    id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    email text,
    password text,
    username text
);