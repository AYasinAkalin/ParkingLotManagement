import sqlite3
import config as cfg


def init(file, clean=True):
    c = open(file)
    if clean:
        delete_tables(c)
    # create Firm table
    Firm_sql = "CREATE TABLE Firm(\
        'FirmAlias' TEXT NOT NULL UNIQUE,\
        'FirmNAME' TEXT  NOT NULL,\
        'EMail' TEXT UNIQUE,\
        'Telephone' TEXT UNIQUE,\
        'Street_1' TEXT UNIQUE,\
        'Street_2' TEXT UNIQUE,\
        'City' TEXT UNIQUE,\
        'Region' TEXT UNIQUE,\
        'PostalCode' TEXT UNIQUE,\
        PRIMARY KEY ('FirmAlias'))"
    execute(Firm_sql, c)

    # create ParkingLots
    ParkingLots_sql = "Create Table ParkingLots(\
        'LotAlias' TEXT NOT NULL UNIQUE,\
        'FirmAlias' TEXT UNIQUE,\
        'LotName' TEXT NOT NULL UNIQUE,\
        'PriceMultiplier' TEXT NOT NULL UNIQUE,\
        'Street_1' TEXT UNIQUE,\
        'Street_2' TEXT UNIQUE,\
        'City' TEXT UNIQUE,\
        'Region' TEXT UNIQUE,\
        'PostalCode' TEXT UNIQUE,\
        PRIMARY KEY ('LotAlias'),\
        CONSTRAINT FK_TO_FIRM\
            FOREIGN KEY (FirmAlias)\
            REFERENCES Firm(FirmAlias))"
    execute(ParkingLots_sql, c)

    # create table Floors
    Floors_sql = "CREATE TABLE Floors(\
        'FloorNumber'   TEXT NOT NULL,\
        'LotAlias'      TEXT\
            UNIQUE\
            REFERENCES ParkingLots(LotAlias),\
        PRIMARY KEY('FloorNumber', 'LotAlias')\
        )"

    execute(Floors_sql, c)

    # create table RentalAreas
    Rental_Areas_sql = "CREATE TABLE RentalAreas(\
       'RentalID' TEXT UNIQUE,\
       'FloorNumber'   TEXT NOT NULL\
        REFERENCES Floors(Floornumber),\
        'LotAlias' TEXT UNIQUE\
        REFERENCES Floors(LotAlias),\
        PRIMARY KEY(FloorNumber, LotAlias, RentalID))"
    execute(Rental_Areas_sql, c)

    # create table ChargeSpots
    Charge_spots_sql = "CREATE TABLE ChargeSpots(\
       'CSpotID' TEXT NOT NULL,\
       'LotAlias' TEXT UNIQUE\
         REFERENCES Floors(LotAlias),\
        'Floornumber' TEXT UNIQUE\
         REFERENCES Floors(Floornumber),\
        PRIMARY KEY('CSpotID','LotAlias'))"
    execute(Charge_spots_sql, c)

    # create table ParkingSpots
    Parking_Spots_sql = "CREATE TABLE ParkingSpots(\
        'PSpotID' TEXT NOT NULL PRIMARY KEY,\
        'LotAlias' TEXT UNIQUE\
         REFERENCES Chargespots(LotAlias),\
         'FloorNumber'   TEXT NOT NULL\
        REFERENCES Floors(Floornumber))"
    execute(Parking_Spots_sql, c)

    # create table ReservedSpots
    Reserved_Spots_sql = "CREATE TABLE ReservedSpots(\
        'PSpotID' TEXT NOT NULL\
         REFERENCES ParkingSpots(PSpotID),\
         'MShipNum'  TEXT NOT NULL\
        REFERENCES MembershipRentals(MshipNum),\
        PRIMARY KEY('PSpotID','MShipNum'))"
    execute(Reserved_Spots_sql, c)

    # create table RentalAgreements
    Rental_Agreement_sql = "CREATE TABLE RentalAgreement(\
         'RentalID' TEXT NOT NULL\
         REFERENCES RentalAreas(RentalID),\
         'LotAlias'  TEXT UNIQUE\
        REFERENCES RentalAreas(LotAlias),\
        'TenandID'  TEXT UNIQUE\
        REFERENCES RentalAreas(TenandID),\
        'StartDate' TEXT NOT NULL,\
        'EndDate'   TEXT NOT NULL,\
         'ftent' TEXT NOT NULL,\
        'Duration' INTEGER NOT NULL,\
         'Description' TEXT NOT NULL,\
         PRIMARY KEY(RentalID ,'LotAlias','TenandID'))"

    execute(Rental_Agreement_sql, c)

    # create table TenantContacts
    Tenant_Contacts_sql = "CREATE TABLE TenantContacts(\
          'TenantID' TEXT NOT NULL PRIMARY KEY,\
           'Name'    TEXT NOT NULL,\
            'Telephone' TEXT NOT NULL,\
            'EMail'  TEXT NOT NULL)"
    execute(Tenant_Contacts_sql, c)

    # create table ChargingInfo
    Charging_info_sql = "CREATE TABLE ChargingInfo(\
                  'CSpotID' TEXT NOT NULL PRIMARY KEY\
                    REFERENCES ChargeSpots(CSpotID),\
                    'StartedAt'    TEXT NOT NULL,\
                    'CPercentage' TEXT NOT NULL,\
                    'CPower' TEXT NOT NULL,\
                    'ChargeAt'  TEXT NOT NULL)"
    execute(Charging_info_sql, c)

    # create table ParkingInfo
    Parking_info_sql = "CREATE TABLE Parkinginfo(\
                    'PSpotID' TEXT NOT NULL PRIMARY KEY\
                    REFERENCES ParkingSpots(PSpotID),\
                    'StartedAt' TEXT NOT NULL)"
    execute(Parking_info_sql, c)

    users_sql = "CREATE TABLE Users\
        (\
            'UserID'    TEXT\
                PRIMARY KEY\
                    ASC\
                    ON CONFLICT REPLACE\
                UNIQUE\
                    ON CONFLICT REPLACE\
                NOT NULL,\
            'UserName'  TEXT\
                UNIQUE\
                    ON CONFLICT REPLACE\
                NOT NULL,\
            'EMail'     TEXT\
                UNIQUE\
                    ON CONFLICT ABORT\
        )"
    execute(users_sql, c)
    users_creditentials_sql = "CREATE TABLE UsersCreditentials\
        (\
            'UserID'        TEXT\
                PRIMARY KEY\
                REFERENCES Users(UserID)\
                NOT NULL,\
            'Password'  TEXT\
                NOT NULL,\
            'Salt'      TEXT\
                UNIQUE\
                    ON CONFLICT ABORT\
                DEFAULT (\
                    'S-' || lower(hex(randomblob(4))) ||\
                    '-' || lower(hex(randomblob(4)))\
                    )\
                NOT NULL\
        )"
    execute(users_creditentials_sql, c)
    permissions_sql = "CREATE TABLE Permissions\
        (\
            'PermissionKey' TEXT\
                PRIMARY KEY,\
            'Description'   TEXT\
        )"
    execute(permissions_sql, c)
    user_permissions_sql = "CREATE TABLE UserPermissions\
        (\
            'UserID'        TEXT\
                PRIMARY KEY\
                    ASC\
                    ON CONFLICT REPLACE\
                REFERENCES Users(UserID)\
                NOT NULL,\
            'PermissionKey' TEXT\
                REFERENCES Permissions(PermissionKey)\
                NOT NULL\
        )"
    execute(user_permissions_sql, c)
    members_sql = "CREATE TABLE Members\
        (\
            'MemberID'      TEXT\
                PRIMARY KEY\
                    ASC\
                    ON CONFLICT ROLLBACK\
                UNIQUE\
                NOT NULL,\
            'UserID'        TEXT\
                REFERENCES Users(UserID)\
                NOT NULL,\
            'MemberName'    TEXT\
                NOT NULL\
        )"
    execute(members_sql, c)
    wallet_accounts_sql = "CREATE TABLE WalletAccounts\
        (\
            'WalletID'      TEXT\
                PRIMARY KEY\
                    ASC\
                    ON CONFLICT ROLLBACK\
                UNIQUE\
                    ON CONFLICT ROLLBACK\
                NOT NULL,\
            'MemberID'      TEXT\
                REFERENCES Members(MemberID)\
                UNIQUE\
                NOT NULL\
        )"
    execute(wallet_accounts_sql, c)
    credit_cards_sql = "CREATE TABLE CreditCards\
        (\
            'CardID'        TEXT\
                PRIMARY KEY\
                    ON CONFLICT ROLLBACK\
                UNIQUE\
                    ON CONFLICT ROLLBACK\
                NOT NULL,\
            'WalletID'      TEXT\
                REFERENCES WalletAccounts(WalletID),\
            'HolderName'    TEXT\
                NOT NULL,\
            'ValidUntil'    TEXT\
                NOT NULL\
        )"
    execute(credit_cards_sql, c)
    card_quartets_sql = "CREATE TABLE CardQuartets\
        (\
            'CardID'        TEXT\
                PRIMARY KEY\
                    ASC\
                    ON CONFLICT REPLACE\
                REFERENCES CreditCards(CardID)\
                NOT NULL,\
            'CardQ1'        TEXT\
                NOT NULL,\
            'CardQ2'        TEXT\
                NOT NULL,\
            'CardQ3'        TEXT\
                NOT NULL,\
            'CardQ4'        TEXT\
                NOT NULL\
        )"  # Save 1st, 2nd, 3rd quartets encrypted, leave 4th as it is
    execute(card_quartets_sql, c)
    memberships_sql = "CREATE TABLE Memberships\
        (\
            'MShipNum'      TEXT\
                PRIMARY KEY\
                    ASC\
                    ON CONFLICT ROLLBACK\
                UNIQUE\
                NOT NULL,\
            'MemberID'      TEXT\
                REFERENCES Members(MemberID)\
                NOT NULL,\
            'Type'          TEXT,\
            'StartDate'     TEXT,\
            'EndDate'       TEXT,\
            'Duration'      INTEGER,\
            'Price'         REAL\
        )"
    execute(memberships_sql, c)
    membership_rentals_sql = "CREATE TABLE MembershipRentals\
        (\
            'MShipNum'      TEXT\
                PRIMARY KEY\
                    ON CONFLICT ROLLBACK\
                REFERENCES Memberships(MShipNum)\
                NOT NULL,\
            'RentalType'    INTEGER\
                REFERENCES Rentals(RentalType)\
        )"
    execute(membership_rentals_sql, c)
    rentals_sql = "CREATE TABLE Rentals\
        (\
            'RentalType'    INTEGER\
                PRIMARY KEY\
                    ASC\
                    ON CONFLICT REPLACE\
                    AUTOINCREMENT\
                UNIQUE\
                    ON CONFLICT REPLACE\
                NOT NULL,\
            'VehicleType'   TEXT\
                CHECK(VehicleType = 'Car' or VehicleType = 'Motorcycle')\
                NOT NULL,\
            'RentalTerm'    TEXT\
                CHECK(RentalTerm = 'Monthly' or RentalTerm = 'Annual')\
                NOT NULL,\
            'BaseFee'       INTEGER\
                NOT NULL\
        )"
    execute(rentals_sql, c)
    membership_discounts_sql = "CREATE TABLE MembershipDiscounts\
        (\
            'MemberID'      TEXT\
                PRIMARY KEY\
                REFERENCES Memberships(MemberID)\
                UNIQUE\
                NOT NULL,\
            'VehicleCount'  INTEGER\
                CHECK(1 or 2 or 3)\
                REFERENCES Discounts(VehicleCount)\
        )"
    execute(membership_discounts_sql, c)
    discounts_sql = "CREATE TABLE Discounts\
        (\
            'VehicleCount'  INTEGER\
                PRIMARY KEY\
                    ASC\
                    ON CONFLICT REPLACE\
                UNIQUE\
                    ON CONFLICT REPLACE\
                CHECK(1 or 2 or 3)\
                NOT NULL,\
            'Discounts'     REAL\
                NOT NULL\
        )"
    execute(discounts_sql, c)
    parking_prices_sql = "CREATE TABLE ParkingPrices\
        (\
            'VehicleType'   TEXT\
                PRIMARY KEY\
                    ON CONFLICT REPLACE\
                UNIQUE\
                    ON CONFLICT REPLACE\
                CHECK(VehicleType = 'Car' or VehicleType = 'Motorcycle')\
                NOT NULL,\
            'StartingFee'   REAL\
                NOT NULL,\
            'ExtraFee'      REAL\
                NOT NULL\
        )"
    execute(parking_prices_sql, c)
    charging_prices_sql = "CREATE TABLE ChargingPrices\
        (\
            'VehicleType'   TEXT\
                PRIMARY KEY\
                    ON CONFLICT REPLACE\
                UNIQUE\
                    ON CONFLICT REPLACE\
                CHECK(VehicleType = 'Car' or VehicleType = 'Motorcycle')\
                NOT NULL,\
            'ChargingFeeT1' REAL\
                NOT NULL,\
            'ChargingFeeT2' REAL\
                NOT NULL,\
            'IdleFee'       REAL\
                NOT NULL\
        )"
    execute(charging_prices_sql, c)
    charger_tier_profiles_sql = "CREATE TABLE ChargerTiers\
        (\
            'ProfileNumber'     INTEGER\
                PRIMARY KEY\
                    ASC\
                    ON CONFLICT REPLACE\
                    AUTOINCREMENT\
                UNIQUE\
                    ON CONFLICT REPLACE,\
            'Tier'              INTEGER\
                UNIQUE\
                    ON CONFLICT REPLACE\
                CHECK(1 or 2)\
                NOT NULL,\
            'VehicleType'       TEXT\
                CHECK(VehicleType = 'Car' or VehicleType = 'Motorcycle')\
                NOT NULL,\
            'LowerBound'        REAL\
                NOT NULL,\
            'UpperBound'        REAL\
                NOT NULL\
        )"
    execute(charger_tier_profiles_sql, c)
    fill_tables(conn=c, demo=cfg.DEMO)
    c.close()


def open(file):
    conn = sqlite3.connect(file)
    return conn


def execute(sql, conn):
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


def delete_tables(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Firm")
    cursor.execute("DROP TABLE IF EXISTS ParkingLots")
    cursor.execute("DROP TABLE IF EXISTS Floors")
    cursor.execute("DROP TABLE IF EXISTS RentalAreas")
    cursor.execute("DROP TABLE IF EXISTS ChargeSpots")
    cursor.execute("DROP TABLE IF EXISTS ParkingSpots")
    cursor.execute("DROP TABLE IF EXISTS ReservedSpots")
    cursor.execute("DROP TABLE IF EXISTS RentalAgreement")
    cursor.execute("DROP TABLE IF EXISTS TenantContacts")
    cursor.execute("DROP TABLE IF EXISTS ChargingInfo")
    cursor.execute("DROP TABLE IF EXISTS Parkinginfo")
    cursor.execute("DROP TABLE IF EXISTS Users")
    cursor.execute("DROP TABLE IF EXISTS UsersCreditentials")
    cursor.execute("DROP TABLE IF EXISTS Permissions")
    cursor.execute("DROP TABLE IF EXISTS UserPermissions")
    cursor.execute("DROP TABLE IF EXISTS Members")
    cursor.execute("DROP TABLE IF EXISTS WalletAccounts")
    cursor.execute("DROP TABLE IF EXISTS CreditCards")
    cursor.execute("DROP TABLE IF EXISTS CardQuartets")
    cursor.execute("DROP TABLE IF EXISTS Memberships")
    cursor.execute("DROP TABLE IF EXISTS MembershipRentals")
    cursor.execute("DROP TABLE IF EXISTS Rentals")
    cursor.execute("DROP TABLE IF EXISTS MembershipDiscounts")
    cursor.execute("DROP TABLE IF EXISTS Discounts")
    cursor.execute("DROP TABLE IF EXISTS ChargingPrices")
    cursor.execute("DROP TABLE IF EXISTS ParkingPrices")
    cursor.execute("DROP TABLE IF EXISTS ChargerTiers")
    conn.commit()


def fill_tables(conn, demo=True, verbose=False):
    queries = (
        "INSERT INTO Discounts VALUES (1, 0.10)",
        "INSERT INTO Discounts VALUES (2, 0.15)",
        "INSERT INTO Discounts VALUES (3, 0.20)",
        "INSERT INTO Rentals VALUES (1, 'Car', 'Monthly', 80)",
        "INSERT INTO Rentals VALUES (2, 'Car', 'Annual', 800)",
        "INSERT INTO Rentals VALUES (3, 'Motorcycle', 'Monthly', 30)",
        "INSERT INTO Rentals VALUES (4, 'Motorcycle', 'Annual', 300)",
        "INSERT INTO ChargingPrices VALUES('Car', 0.07, 0.05, 0.30)",
        "INSERT INTO ChargingPrices VALUES('Motorcycle', 0.05, 0.04, 0.15)",
        "INSERT INTO ParkingPrices VALUES('Car', 2, 1)",
        "INSERT INTO ParkingPrices VALUES('Motorcycle', 0.80, 0.30)",
        "INSERT INTO ChargerTiers VALUES(1, 1, 'Car', 60, 999)",
        "INSERT INTO ChargerTiers VALUES(2, 1, 'Motorcycle', 12, 999)",
        "INSERT INTO ChargerTiers VALUES(3, 2, 'Car', 60, 60)",
        "INSERT INTO ChargerTiers VALUES(4, 2, 'Motorcycle', 0, 12)",
        "INSERT INTO Permissions\
            VALUES(0, '(00000) No permissions')",
        "INSERT INTO Permissions\
            VALUES(1, '(00001) Only member permissions')",
        "INSERT INTO Permissions\
            VALUES(2, '(00010) Only tenant permission')",
        "INSERT INTO Permissions\
            VALUES(3, '(00011) Tenant+Member permissions')",
        "INSERT INTO Permissions\
            VALUES(4, '(00100) Only Manager permissions')",
        "INSERT INTO Permissions\
            VALUES(5, '(00101) Manager+Member')",
        "INSERT INTO Permissions\
            VALUES(6, '(00110) Manager+Tenant')",
        "INSERT INTO Permissions\
            VALUES(7, '(00111) Manager+Tenant+Member')",
        "INSERT INTO Permissions\
            VALUES(8, '(01000) Only Admin permissions')",
        "INSERT INTO Permissions\
            VALUES(9, '(01001) Admin+Member')",
        "INSERT INTO Permissions \
            VALUES(10, '(01010) Admin+Tenant')",
        "INSERT INTO Permissions \
            VALUES(11, '(01011) Admin+Tenant+Member')",
        "INSERT INTO Permissions \
            VALUES(12, '(01100) Admin+Manager')",
        "INSERT INTO Permissions \
            VALUES(13, '(01101) Admin+Manager+Member')",
        "INSERT INTO Permissions \
            VALUES(14, '(01110) Admin+Manager+Tenant')",
        "INSERT INTO Permissions \
            VALUES(15, '(01111) Admin+Manager+Tenant+Member')",
        "INSERT INTO Permissions \
            VALUES(16, '(10000) Only Developer permissions')",
        "INSERT INTO Permissions \
            VALUES(17, '(10001) Developer+Member')",
        "INSERT INTO Permissions \
            VALUES(18, '(10010) Developer+Tenant')",
        "INSERT INTO Permissions \
            VALUES(19, '(10011) Developer+Tenant+Member')",
        "INSERT INTO Permissions \
            VALUES(20, '(10100) Developer+Manager')",
        "INSERT INTO Permissions \
            VALUES(21, '(10101) Developer+Manager+Member')",
        "INSERT INTO Permissions \
            VALUES(22, '(10110) Developer+Manager+Tenant')",
        "INSERT INTO Permissions \
            VALUES(23, '(10111) Developer+Manager+Tenant+Member')",
        "INSERT INTO Permissions \
            VALUES(24, '(11000) Developer+Admin')",
        "INSERT INTO Permissions \
            VALUES(25, '(11001) Developer+Admin+Member')",
        "INSERT INTO Permissions \
            VALUES(26, '(11010) Developer+Admin+Tenant')",
        "INSERT INTO Permissions \
            VALUES(27, '(11011) Developer+Admin+Tenant+Member')",
        "INSERT INTO Permissions \
            VALUES(28, '(11100) Developer+Admin+Manager')",
        "INSERT INTO Permissions \
            VALUES(29, '(11101) Developer+Admin+Manager+Member')",
        "INSERT INTO Permissions \
            VALUES(30, '(11110) Developer+Admin+Manager+Tenant')",
        "INSERT INTO Permissions \
            VALUES(31, '(11111) SUPERUSER=Dev.+Admin+Manager+Tenant+Member')")
    for query in queries:
        execute(query, conn)
    
    if cfg.DEMO:
        demo_queries = (
            "INSERT INTO Firm(FirmAlias, FirmNAME, EMail,Telephone,Street_1,Street_2,City,Region,PostalCode)\
                VALUES('sa',\
                    'sabancı',\
                    'tsuruta@att.net',\
                    '0539471',\
                    '8591 South Mountainview Road Montclair',\
                    'NJ 07042',\
                    'antalya',\
                    'muratpaşa',\
                    '07042')",
        
        
            "INSERT INTO ParkingLots(LotAlias,FirmAlias,LotName,PriceMultiplier,Street_1,Street_2,City,Region,PostalCode)\
                VALUES('ltals',\
                    'Frmls',\
                    'LtNm',\
                    'PrcMltplr',\
                    'Strt1',\
                    'Strt2',\
                    'Cty',\
                    'Rgn',\
                    'PstCd')",
                


            "INSERT INTO Floors(FloorNumber,LotAlias)\
                VALUES('flrnmb',\
                       'ltals')",
            "INSERT INTO Floors(FloorNumber,LotAlias)\
                VALUES('flrnmb',\
                       'ltals')",
            "INSERT INTO Floors(FloorNumber,LotAlias)\
                VALUES('flrnmb',\
                       'ltals')",

          
            "INSERT INTO RentalAreas(RentalID,FloorNumber,LotAlias)\
                VALUES('R00101',\
                    'Flr_8',\
                    'ltals')",
            

         
         
          "INSERT INTO ChargeSpots(CSpotID,LotAlias,Floornumber)\
          VALUES('C01111',\
                    'Ltals',\
                    'Flr_8')",
               
          

           
           "INSERT INTO ParkingSpots(PSpotID,LotAlias,FloorNumber)\
            VALUES('PSPD',\
                   'Ltals',\
                   'flr_8')",
           

            
        
          "INSERT INTO ReservedSpots(PSpotID,MShipNum)\
           VALUES('P01100',\
                  'mshpnm')",
           
          
          
          
          
          "INSERT INTO RentalAgreement(RentalID,LotAlias,TenandID,StartDate,EndDate,ftent,Duration,Description)\
           VALUES('R00101',\
                    'ltals',\
                    'T010101',\
                    'strdt',\
                    'endt',\
                    'ftnt',\
                    'drtn',\
                    'dscrptn')",

            "INSERT INTO TenantContacts(TenantID,Name,Telephone,EMail)\
                VALUES('T010101',\
                    'nm',\
                    'Telephone',\
                    'parkmanager@gmail.com')",
              

           "INSERT INTO ChargingInfo(CSpotID,StartedAt,CPercentage,CPower,ChargeAt)\
            VALUES('C01111',\
                   'strdt',\
                   'cprctg',\
                   'cpwr',\
                   'chrgt')",
            


        
            "INSERT INTO ParkingInfo(PSpotID,StartedAt)\
             VALUES('P01100',\
                    'strdt')",

            "INSERT INTO Users(UserID,UserName,EMail)\
                VALUES('S0001',\
                       'manager',\
                       'parkmanager@gmail.com')",
           
           
            "INSERT INTO UsersCreditentials(UserID,Password)\
                VALUES('0001',\
                       '01000')",

            
           "INSERT INTO Members(MemberID,UserID,MemberName)\
            VALUES('M00011',\
                   'S0001',\
                   'mmbrnm')",

            
             "INSERT INTO WalletAccounts(WalletID,MemberID)\
             VALUES('W00101',\
                    'M00011')",

            
             "INSERT INTO CreditCards(CardID,WalletID,HolderName,ValidUntil)\
             VALUES('C01111',\
                    'W00101',\
                    'hldrnm',\
                    'vldntl')",



             "INSERT INTO CardQuartets(CardID,CardQ1,CardQ2,CardQ3,CardQ4)\
              VALUES('C01111',\
                     'HASHEDxNASDKFCHEJSSMASJVIDIdDM+vs',\
                     'HASHEDxNASDKFCHEJSSMASJVIDIasdaSD',\
                     'HASHEDxNASDKFCHEJSSMASJV23zI5DIDn',\
                     '2345')",


          "INSERT INTO Memberships(MShipNum,MemberID,Type,StartDate,EndDate,Duration,Price)\
             VALUES('mshpnm',\
                    'M0001',\
                    'typ',\
                    'strdt',\
                    'endt',\
                    'drtn',\
                    'prc')",

          
          "INSERT INTO Discounts(VehicleCount,Discounts)\
            VALUES('vhclcnt',\
                   'dscnts')",
                


         "INSERT INTO ParkingPrices(VehicleType,StartingFee,ExtraFee)\
           VALUES('vhctyp',\
                  'strngf',\
                  'extrf')",


        "INSERT INTO ChargingPrices(VehicleType,ChargingFeeT1,ChargingFeeT2,IdleFee)\
           VALUES('vhctyp',\
                   'chrgf1',\
                   'chrgf2',\
                   'ıdlfe')",
         
         
         "INSERT INTO ChargerTiers(ProfileNumber,Tier,VehicleType,LowerBound,UpperBound)\
          VALUES('prflnmbr',\
                 'tie',\
                 'vhctyp',\
                'lwrbnd',\
                'uprboud')"






       )
    
        for query in demo_queries:
            execute(query, conn)

        