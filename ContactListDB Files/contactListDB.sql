-- If the database "COMPANY" already exists, then delete it.
DROP DATABASE IF EXISTS CONTACTLISTDB;
-- Create the Database "COMPANY"
CREATE DATABASE CONTACTLISTDB;

-- Set the currently active database to be "CONTACTLISTDB"
USE CONTACTLISTDB;

CREATE TABLE CONTACT (
     Contact_id INT NOT NULL AUTO_INCREMENT,
     Fname VARCHAR(45) NOT NULL,
     Mname VARCHAR(45),
     Lname VARCHAR(45) NOT NULL,
     PRIMARY KEY (Contact_id)
);

CREATE TABLE ADDRESS (
    Address_id INT NOT NULL AUTO_INCREMENT,
    Contact_id INT not null,
    Address_type VARCHAR(30),
    Address VARCHAR(45),
    City VARCHAR(45),
    State VARCHAR(45),
    Zip VARCHAR(45),
    PRIMARY KEY (Address_id),
    FOREIGN KEY (Contact_id) 
        REFERENCES CONTACT(Contact_id)
);

CREATE TABLE PHONE (
    Phone_id INT NOT NULL AUTO_INCREMENT,
    Contact_id INT not null,
    Phone_type VARCHAR(30),
    Area_code VARCHAR(45),
    Number VARCHAR(45),
    PRIMARY KEY (Phone_id),
    FOREIGN KEY (Contact_id) 
        REFERENCES CONTACT(Contact_id)
);

CREATE TABLE DATE (
    Date_id INT NOT NULL AUTO_INCREMENT,
    Contact_id INT not null,
    Date_type VARCHAR(30),
    Date DATETIME,
    PRIMARY KEY (Date_id),
    FOREIGN KEY (Contact_id) 
        REFERENCES CONTACT(Contact_id)
);