CREATE TABLE newsletter(
	send_date DATE NOT NULL,
	email VARCHAR(500) NOT NULL,
	secret VARCHAR(50) NOT NULL,
	PRIMARY KEY(`email`)
);
