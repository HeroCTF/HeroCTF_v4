USE user_db;

CREATE TABLE IF NOT EXISTS USERS (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    password VARCHAR(255)
);

INSERT INTO USERS VALUES (1, "user1", "dummyPass1");
INSERT INTO USERS VALUES (2, "user2", "dummyPass2");