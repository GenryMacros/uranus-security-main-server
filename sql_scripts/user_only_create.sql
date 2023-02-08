CREATE TABLE Clients(
	id INT IDENTITY(1,1) PRIMARY KEY,
	username VARCHAR(20),
	email VARCHAR(20),
	is_deleted BIT
)

CREATE TABLE ClientsSecrets(
	id INT IDENTITY(1,1) PRIMARY KEY,
	client_id INT FOREIGN KEY REFERENCES  Clients(id) ON DELETE CASCADE,
	password_hash VARCHAR(64),
	password_salt VARCHAR(10),
	user_private VARCHAR(1680),
	user_public VARCHAR(450)
)


CREATE TABLE ClientsLocations(
	id INT IDENTITY(1,1) PRIMARY KEY,
	client_id INT FOREIGN KEY REFERENCES Clients(id) ON DELETE CASCADE,
	country VARCHAR(20),
	city VARCHAR(20),
	addr VARCHAR(20),
	ind INT
)

CREATE TABLE ClientsAdditionalContacts(
	id INT IDENTITY(1,1) PRIMARY KEY,
	client_id INT FOREIGN KEY REFERENCES Clients(id) ON DELETE CASCADE,
	phone VARCHAR(15),
	telegram VARCHAR(20)
)

CREATE TABLE ClientsServersData(
    id INT IDENTITY(1,1) PRIMARY KEY,
    client_id INT FOREIGN KEY REFERENCES Clients(id) ON DELETE CASCADE,
    server_ip VARCHAR(10) DEFAULT '',
    server_port VARCHAR(5) DEFAULT ''
)

CREATE TABLE Cameras(
	id INT IDENTITY(1,1) PRIMARY KEY,
	client_id INT FOREIGN KEY REFERENCES Clients(id) ON DELETE CASCADE,
	device_name VARCHAR(10),
	is_deleted BIT
)
