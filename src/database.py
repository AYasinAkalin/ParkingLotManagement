import sqlite3
def init(file):
    c = open(file)
    c.close()


def open(file):
    conn = sqlite3.connect(file)
    return conn
    



