CREATE DATABASE /*!32312 IF NOT EXISTS*/`ireserve` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `ireserve`;

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `UserID` INT PRIMARY KEY, 
  `FirstName` VARCHAR(255) NOT NULL,
  `LastName` VARCHAR(255) NOT NULL, 
  `Email` VARCHAR(255) NOT NULL, 
  `HashedPassword` VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS `building`;

CREATE TABLE `building` (
  `BuildingID` INT PRIMARY KEY,
  `Address` VARCHAR(255) NOT NULL,
  `BuildingName` VARCHAR(255) NOT NULL,
  `Region` VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS `room`;

CREATE TABLE `room` (
  `RoomID` INT PRIMARY KEY,
  `BuildingID` INT,
  `FloorNumber` INT,
  `RoomNumber` INT,
  `RoomCapacity` INT,
  `RoomType` VARCHAR(50) NOT NULL,
  `Popularity` REAL,
  FOREIGN KEY (`BuildingID`) REFERENCES `building` (`BuildingID`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `group`;

CREATE TABLE `group`(
  `GroupID` INT PRIMARY KEY,
  `GroupName` VARCHAR(100) NOT NULL
);

DROP TABLE IF EXISTS `groupassignment`;

CREATE TABLE `groupassignment`(
  `AssignmentID` INT PRIMARY KEY,
  `UserID` INT,
  `GroupID` INT,
  FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE,
  FOREIGN KEY (`GroupID`) REFERENCES `group` (`GroupID`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `reservation`;

CREATE TABLE `reservation` (
  `ReservationID` INT PRIMARY KEY,
  `RoomID` INT,
  `UserID` INT,
  `GroupID` INT,
  `StartTime` VARCHAR(100) NOT NULL,
  `EndTime` VARCHAR(100) NOT NULL,
  FOREIGN KEY (`RoomID`) REFERENCES `room` (`RoomID`) ON DELETE CASCADE,
  FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE,
  FOREIGN KEY (`GroupID`) REFERENCES `group` (`GroupID`) ON DELETE CASCADE
);