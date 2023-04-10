CREATE DATABASE Uranus_Security
GO
USE Uranus_Security;
GO

CREATE TABLE Clients(
	id INT PRIMARY KEY IDENTITY(1,1),
	username VARCHAR(20),
	email VARCHAR(20),
	is_deleted BIT,
	is_confirmed BIT,
    signup_date VARCHAR(11)
)

CREATE TABLE ClientsSecrets(
	id INT IDENTITY(1,1) PRIMARY KEY,
	client_id INT FOREIGN KEY REFERENCES Clients(id) ON DELETE CASCADE,
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

CREATE TABLE ClientsConfirmations(
    id INT IDENTITY(1,1) PRIMARY KEY,
    client_id INT FOREIGN KEY REFERENCES Clients(id) ON DELETE CASCADE,
    confirmation_code VARCHAR(5),
    expiration_date VARCHAR(11)
)

CREATE TABLE Invasion(
	id INT IDENTITY(1,1) PRIMARY KEY,
	camera_id INT FOREIGN KEY REFERENCES Cameras(id) ON DELETE CASCADE,
	video_path VARCHAR(50),
	created VARCHAR(11),
	is_deleted BIT
)

CREATE TABLE Intruder(
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(10),
)

CREATE TABLE InvasionIntruders(
    invasion_id INT FOREIGN KEY REFERENCES Invasion(id) ON DELETE CASCADE,
    intruder_id INT FOREIGN KEY REFERENCES Intruder(id) ON DELETE CASCADE
)
