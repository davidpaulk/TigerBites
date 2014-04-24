CREATE TABLE users_item (
       id int NOT NULL PRIMARY KEY,
       isVegan bool NOT NULL,
       isVegetarian bool NOT NULL,
       isPork bool NOT NULL,
       hasNuts bool NOT NULL,
       type varchar(10) NOT NULL,
       name varchar(50) NOT NULL
)
;
CREATE TABLE users_netid_favorites (
       id int NOT NULL PRIMARY KEY,
       netid_id int NOT NULL,
       item_id int NOT NULL REFERENCES users_item (id),
       UNIQUE (netid_id, item_id)
)
;
CREATE TABLE users_netid (
       id int NOT NULL PRIMARY KEY,
       netid varchar(15) NOT NULL
)
;
