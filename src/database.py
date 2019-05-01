import sqlite3
def init(file):
    c = open(file)

    # Create Boat table
    boat_sql = "CREATE TABLE `boats` (\
    `bid` INTEGER NOT NULL,\
    `bname` TEXT NOT NULL,\
    `color` TEXT NOT NULL DEFAULT 'white',\
    PRIMARY KEY (`bid`));"
    
    #execute(boat_sql, c)

    #c.close()
    #create Firm table
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

    #c.close()
    
      #create ParkingLots
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
      
    #c.close()
      #create taable Floors 
    Floors_sql = "CREATE TABLE Floors(\
        'FloorNumber'   TEXT NOT NULL,\
        'LotAlias'      TEXT\
            UNIQUE\
            REFERENCES ParkingLots(LotAlias),\
        PRIMARY KEY('FloorNumber', 'LotAlias')\
        )"

    execute(Floors_sql,c)

     #create table RentalAreas
    Rental_Areas_sql = "CREATE TABLE RentalAreas(\
       'RentalID' TEXT UNIQUE,\
       'FloorNumber'   TEXT NOT NULL\
        REFERENCES Floors(Floornumber),\
        'LotAlias' TEXT UNIQUE\
        REFERENCES Floors(LotAlias),\
        PRIMARY KEY(FloorNumber, LotAlias, RentalID))"
       
    execute(Rental_Areas_sql,c)
   

       #create table ChargeSpots
    Charge_spots_sql = "CREATE TABLE ChargeSpots(\
       'CSpotID' TEXT NOT NULL,\
       'LotAlias' TEXT UNIQUE\
         REFERENCES Floors(LotAlias),\
        'Floornumber' TEXT UNIQUE\
         REFERENCES Floors(Floornumber),\
        PRIMARY KEY('CSpotID','LotAlias'))"

    execute(Charge_spots_sql,c)
           
        #create table ParkingSpots
    Parking_Spots_sql = "CREATE TABLE ParkingSpots(\
        'PSpotID' TEXT NOT NULL PRIMARY KEY,\
        'LotAlias' TEXT UNIQUE\
         REFERENCES Chargespots(LotAlias),\
         'FloorNumber'   TEXT NOT NULL\
        REFERENCES Floors(Floornumber))"
      

    execute(Parking_Spots_sql,c)


         #create table ReservedSpots
    Reserved_Spots_sql = "CREATE TABLE ReservedSpots(\
        'PSpotID' TEXT NOT NULL\
         REFERENCES ParkingSpots(PSpotID),\
         'MShipNum'  TEXT NOT NULL\
        REFERENCES MembershipRentals(MshipNum),\
        PRIMARY KEY('PSpotID','MShipNum'))"
    
    execute(Reserved_Spots_sql,c)


          
          #create table Rentalagreements
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

    execute(Rental_Agreement_sql,c)

           

         #create table TenantContacts
    Tenant_Contacts_sql = "CREATE TABLE TenantContacts(\
          'TenantID' TEXT NOT NULL PRIMARY KEY,\
           'Name'    TEXT NOT NULL,\
            'Telephone' TEXT NOT NULL,\
            'EMail'  TEXT NOT NULL)"
           
    execute(Tenant_Contacts_sql,c)


        #create table Charginginfo
    Charging_info_sql = "CREATE TABLE Charginginfo(\
                  'CSpotID' TEXT NOT NULL PRIMARY KEY\
                    REFERENCES ChargeSpots(CSpotID),\
                    'StartedAt'    TEXT NOT NULL,\
                    'CPercentage' TEXT NOT NULL,\
                    'Cpower' TEXT NOT NULL,\
                    'ChargeAt'  TEXT NOT NULL)"
                    
    execute(Charging_info_sql,c)


                     
         #create table Parkinginfo
    Parking_info_sql = "CREATE TABLE Parkinginfo(\
                    'PSpotID' TEXT NOT NULL PRIMARY KEY\
                    REFERENCES ParkingSpots(PSpotID),\
                    'StartedAt' TEXT NOT NULL)"

    execute(Parking_info_sql,c)

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
                    ON CONFLICT ABORT,\
            'Password'  TEXT\
        )"
    execute(users_sql, c)
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
    c.close()


def open(file):
    conn = sqlite3.connect(file)
    return conn
    


def execute(sql,conn):
   cursor = conn.cursor()
   cursor.execute(sql) 
   conn.commit()

