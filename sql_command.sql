CREATE TABLE Visitors(
    visitor_name VARCHAR(50),
    visitor_password VARCHAR(50),
    ip_address VARCHAR(50),
    visitor_address VARCHAR(50),
    phone_number VARCHAR(50),
    email VARCHAR(50),
    infect_status VARCHAR(50)
);
CREATE TABLE Places(
    place_name VARCHAR(50),
    place_password VARCHAR(50),
    place_address VARCHAR(50),
    qr_code_string VARCHAR(50)
);
CREATE TABLE Hospitals(
    hospital_name VARCHAR(50),
    hospital_password VARCHAR(50)
);
CREATE TABLE Agents(
    agent_name VARCHAR(50),
    agent_password VARCHAR(50)
);
CREATE TABLE VisitorToPlaces(
    visitor_name VARCHAR(50),
    place_name VARCHAR(50),
    enter_time DATETIME,
    exit_time DATETIME
);