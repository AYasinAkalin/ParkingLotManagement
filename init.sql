-- Database Initialization for Parking Lot Management System

-- Change-log
-- v0.1
-- -- Initial SQL commands were created.

DROP DATABASE IF EXISTS parkinglots;
CREATE DATABASE IF NOT EXISTS parkinglots;

USE parkinglots;

DROP TABLE IF EXISTS 	Firm,
						ParkingLots,
						Floors,
						RentalAreas,
						ChargeSpots,
						ParkingSpots,
						RentalAgreements,
						TenantContacts,
						ChargingInfo,
						ParkingInfo,
						Users,
						Permissions,
						UserPermissions,
						Members,
						WalletAccounts,
						Memberships,
						CreditCards,
						CardQuartets,
						MembershipDiscounts,
						MembershipRentals,
						Rentals,
						Discounts;

CREATE TABLE `Firm` (
  `FirmName` varchar(50),
  `EMail` varchar(50),
  `Telephone` varchar(15),
  `Street_1` varchar(80),
  `Street_2` varchar(80),
  `City` varchar(40),
  `Region` varchar(40), -- Change to ENUM
  `PostalCode` varchar(10),
  PRIMARY KEY (`FirmName`)
);

CREATE TABLE `ParkingLots` (
  `LotAlias` varchar(4),
  `LotName` varchar(50),
  `PriceMultiplier` float(3, 2),
  `Street_1` varchar(80),
  `Street_2` varchar(80),
  `City` varchar(40),
  `Region` varchar(40), -- Change to ENUM
  `PostalCode` varchar(10),
  PRIMARY KEY (`LotAlias`)
);

CREATE TABLE `Floors` (
  `FloorNumber` varchar(3),
  `LotAlias` varchar(4),
  PRIMARY KEY (`FloorNumber`),
  KEY `FK` (`LotAlias`)
);

-- Connected to Floors
CREATE TABLE `RentalAreas` (
  `RentalD` varchar(200),
  `FloorNumber` varchar(3),
  PRIMARY KEY (`RentalD`),
  KEY `PK, FK` (`FloorNumber`)
);

-- Connected to Floors
CREATE TABLE `ChargeSpots` (
  `CSpotID` varchar(200),
  `FloorNumber` varchar(3),
  PRIMARY KEY (`CSpotID`),
  KEY `FK` (`FloorNumber`)
);

-- Connected to Floors and MembershipRentals
CREATE TABLE `ParkingSpots` (
  `PSpotID` varchar(200),
  `FloorNumber` varchar(200),
  `MShipNum` varchar(200),
  PRIMARY KEY (`PSpotID`),
  KEY `FK` (`FloorNumber`, `MShipNum`)
);

-- Connected to RentalAreas
CREATE TABLE `RentalAgreements` (
  `RentalID` varchar(200),
  `RentID` varchar(200),
  `TenantID` varchar(200),
  `StartDate` date,
  `EndDate` date,
  `Rent` int,
  `Duration` int,
  PRIMARY KEY (`RentID`),
  KEY `PK, FK` (`RentalID`),
  KEY `FK` (`TenantID`)
);

-- Connected to RentalAgreements
CREATE TABLE `TenantContacts` (
  `TenantID` varchar(200),
  `Name` varchar(50),
  `Telephone` varchar(15),
  `EMail` varchar(50),
  PRIMARY KEY (`TenantID`)
);

-- Connected to ChargingSpots
CREATE TABLE `ChargingInfo` (
  `CSpotID` varchar(200),
  `StartedAt` datetime,
  `CPercentage` float(3, 2),
  `CPower` int,
  `ChargetAt` datetime,
  KEY `PK, FK` (`CSpotID`)
);

-- Connected to ParkingSpots
CREATE TABLE `ParkingInfo` (
  `PSpotID` varchar(200),
  `StartedAt` datetime,
  KEY `PK, FK` (`PSpotID`)
);

CREATE TABLE `Users` (
  `UserID` varchar(200),
  `UserName` varchar(50),
  `EMail` varchar(50),
  `Password` varchar(150),
  PRIMARY KEY (`UserID`)
);

CREATE TABLE `Permissions` (
  `PermissionKey` varchar(10),
  `Description` varchar(255),
  PRIMARY KEY (`PermissionKey`)
);

-- Bridge table between Users and Permissions
CREATE TABLE `UserPermissions` (
  `UserID` varchar(200),
  `PermissionKey` varchar(10),
  KEY `PK, FK` (`UserID`, `PermissionKey`)
);

CREATE TABLE `Members` (
  `MemberID` varchar(200),
  `UserID` varchar(200),
  `WalletID` varchar(200),
  `MShipNum` varchar(200),
  `MemberName` varchar(50),
  PRIMARY KEY (`MemberID`),
  KEY `FK` (`UserID`, `WalletID`, `MShipNum`)
);

CREATE TABLE `WalletAccounts` (
  `WalletID` varchar(200),
  `CardID` varchar(200),
  PRIMARY KEY (`WalletID`),
  KEY `FK` (`CardID`)
);

CREATE TABLE `Memberships` (
  `MShipNum` varchar(200),
  `PackageType` varchar(20),
  `StartDate` date,
  `Duration` int,
  `EndDate` date,
  `Price` int,
  PRIMARY KEY (`MShipNum`)
);

-- Connected to Wallet Accounts
CREATE TABLE `CreditCards` (
  `CardID` varchar(200),
  `HolderName` varchar(80),
  `Valid Until` tinyint,
  PRIMARY KEY (`CardID`)
);

-- Connected to CreditCards
CREATE TABLE `CardQuartets` (
  `CardID` varchar(200),
  `CardQ1` varchar(150),
  `CardQ2` varchar(150),
  `CardQ3` varchar(150),
  `CardQ4` varchar(4),
  KEY `PK, FK` (`CardID`)
);

-- Connected to Memberships
CREATE TABLE `MembershipDiscounts` (
  `MShipNum` varchar(200),
  `VehicleCount` tinyint,
  KEY `PK, FK` (`MShipNum`, `VehicleCount`)
);

-- Connected to Memberships
CREATE TABLE `MembershipRentals` (
  `MShipNum` varchar(200),
  `VehicleType` varchar(20),
  `PSpotID` varchar(200),
  `RentalTerm` varchar(10), -- Change to ENUM
  KEY `PK, FK` (`MShipNum`, `VehicleType`),
  KEY `FK` (`PSpotID`, `RentalTerm`)
);

-- Connected to MembershipRentals
CREATE TABLE `Rentals` (
  `VehicleType` varchar(20), -- Change to ENUM
  `RentalTerm` int, -- Change to ENUM
  `BaseFee` int,
  PRIMARY KEY (`VehicleType`, `RentalTerm`)
);

-- Connected to MembershipDiscounts
CREATE TABLE `Discounts` (
  `VehicleCount` tinyint, -- Change to ENUM
  `Discount` int,
  `Fee` int,
  PRIMARY KEY (`VehicleCount`)
);
