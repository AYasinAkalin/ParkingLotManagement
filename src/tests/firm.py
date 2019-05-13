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

    def test_correct_single_row(self):
        self.assertTrue(insert(self.firm))


# Following check is suggested by Official Python Documentation
# https://docs.python.org/3/library/unittest.html#unittest.main
if __name__ == '__main__':
    unittest.main()
