CREATE TABLE Client(
	id INT IDENTITY(1,1) PRIMARY KEY,
	username VARCHAR(20),
	is_deleted BIT
)

CREATE TABLE ClientSecret(
	id INT IDENTITY(1,1) PRIMARY KEY,
	client_id INT FOREIGN KEY REFERENCES  Client(id) ON DELETE CASCADE,
	password_hash VARCHAR(64),
	password_salt VARCHAR(10),
	user_private VARBINARY(530),
	user_public VARBINARY(130)
)

CREATE TABLE ClientPersonalData(
	id INT IDENTITY(1,1) PRIMARY KEY,
	client_id INT FOREIGN KEY REFERENCES Client(id) ON DELETE CASCADE,
	user_first_name VARCHAR(15),
	user_last_name VARCHAR(20)
)

CREATE TABLE ClientLocation(
	id INT IDENTITY(1,1) PRIMARY KEY,
	client_id INT FOREIGN KEY REFERENCES Client(id) ON DELETE CASCADE,
	country VARCHAR(20),
	city VARCHAR(20),
	addr VARCHAR(20),
	ind INT
)

CREATE TABLE ClientContact(
	id INT IDENTITY(1,1) PRIMARY KEY,
	client_id INT FOREIGN KEY REFERENCES Client(id) ON DELETE CASCADE,
	email VARCHAR(20),
	phone VARCHAR(15),
	telegram VARCHAR(20)
)

CREATE TABLE Camera(
	id INT IDENTITY(1,1) PRIMARY KEY,
	client_id INT FOREIGN KEY REFERENCES Client(id) ON DELETE CASCADE,
	device_name VARCHAR(10),
	is_deleted BIT
)