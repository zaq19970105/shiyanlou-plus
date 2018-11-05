DROP TABLE IF EXISTS category;
CREATE TABLE category(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(80) NOT NULL,
    PRIMARY KEY ( id )
);

DROP TABLE IF EXISTS file;
CREATE TABLE file(
    id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(80) NOT NULL,
    created_time DATE,
    category_id INT,
    content TEXT,
    PRIMARY KEY ( id ),
    foreign key(category_id) references category(id)
);

