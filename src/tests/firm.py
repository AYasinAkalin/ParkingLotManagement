# firm.py
import unittest
import config
import sqlite3


def insert(value_dictionary, db=config.FILE_DATABASE):
    conn = sqlite3.connect(str(db))
    cursor = conn.cursor()
    query = "INSERT INTO Firm VALUES (\
            '{FirmAlias}',\
            '{FirmName}',\
            '{URL}',\
            '{EMail}',\
            '{Telephone}',\
            '{Street_1}',\
            '{Street_2}',\
            '{City}',\
            '{Region}',\
            '{PostalCode}')".format(**value_dictionary)
    cursor.execute(query)
    # conn.commit()  # Disabled to not write extra code to revert INSERTion
    result = True
    conn.close()
    return result


def insertMany(rows, db=config.FILE_DATABASE):
    conn = sqlite3.connect(str(db))
    cursor = conn.cursor()
    for i, value_dictionary in enumerate(rows):
        query = "INSERT INTO Firm VALUES (\
                '{FirmAlias}',\
                '{FirmName}',\
                '{URL}',\
                '{EMail}',\
                '{Telephone}',\
                '{Street_1}',\
                '{Street_2}',\
                '{City}',\
                '{Region}',\
                '{PostalCode}')".format(**value_dictionary)
        cursor.execute(query)
    result = True
    conn.close()
    return result


class MyTest(unittest.TestCase):
    firm = {
            'FirmAlias': 'tfa1',
            'FirmName': 'TestName',
            'URL': 'test.com',
            'EMail': 'mail@test.com',
            'Telephone': '+1 500 400 90',
            'Street_1': '1 Test Street Mars City',
            'Street_2': 'Testing Hotel',
            'City': 'Mars City',
            'Region': 'Big Region',
            'PostalCode': '1000'
        }
    firm2 = {
            'FirmAlias': 'tfa2',
            'FirmName': 'Firm2Name',
            'URL': 'test2.com',
            'EMail': 'mail@test2.com',
            'Telephone': '+2 345 6 789',
            'Street_1': '2 Red Avenue',
            'Street_2': 'Testers Inn',
            'City': 'Palo Alto',
            'Region': 'San Fransisco',
            'PostalCode': '1000'
        }

    def test_correct_single_row(self):
        self.assertTrue(insert(self.firm))

    def test_firm_blank_insertion(self):
        firm1 = {key: '' for key in self.firm.keys()}
        with self.assertRaises(sqlite3.IntegrityError):
            insert(firm1)

    def test_faulty_single_row(self):
        firm1 = self.firm.copy()
        firm1['FirmAlias'] = 'LongAliasWithLength>5'
        with self.assertRaises(sqlite3.IntegrityError):
            insert(firm1)

    def test_firm_postal(self):
        firm2 = self.firm.copy()
        firm2['PostalCode'] = '123456789'  # Max allowed postal code len. is 8
        with self.assertRaises(sqlite3.IntegrityError):
            insert(firm2)

    def test_firm_email(self):
        firm3 = self.firm.copy()
        firm3['EMail'] = 'notAnActualEMailAddress'
        with self.assertRaises(sqlite3.IntegrityError):
            insert(firm3)

        firm3['EMail'] = '@noUserNameGivenToMail.com'
        with self.assertRaises(sqlite3.IntegrityError):
            insert(firm3)

        firm3['EMail'] = 'noDomainIsEntered@'
        with self.assertRaises(sqlite3.IntegrityError):
            insert(firm3)

        firm3['EMail'] = 'IncorrectDomain@.com'
        with self.assertRaises(sqlite3.IntegrityError):
            insert(firm3)

    def test_firm_website(self):
        firm4 = self.firm.copy()
        firm4['URL'] = 'notAWebSite'
        with self.assertRaises(sqlite3.IntegrityError):
            insert(firm4)

        firm4['URL'] = 'AlsoNotAWebSite.'
        with self.assertRaises(sqlite3.IntegrityError):
            insert(firm4)

        firm4['URL'] = '.com'
        with self.assertRaises(sqlite3.IntegrityError):
            insert(firm4)

    def test_correct_many_rows(self):
        firms = (self.firm, self.firm2)
        self.assertTrue(insertMany(firms))

    def test_faulty_many_rows(self):
        firms = (self.firm, self.firm)
        with self.assertRaises(sqlite3.IntegrityError):
            insertMany(firms)

        firm1 = self.firm.copy()
        firm2 = self.firm2.copy()
        firm2['FirmAlias'] = firm1['FirmAlias']
        firms = (firm1, firm2)
        with self.assertRaises(sqlite3.IntegrityError):
            insertMany(firms)


# Following check is suggested by Official Python Documentation
# https://docs.python.org/3/library/unittest.html#unittest.main
if __name__ == '__main__':
    unittest.main()
