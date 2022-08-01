import sqlite3 as sl 
from sqlite3 import OperationalError

connection = sl.connect('index.db', check_same_thread=False)

def createTable():
    with connection:
        try:
            connection.execute("""
                CREATE TABLE WORD_INDEX (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    word TEXT,
                    filename TEXT,
                    occurence INTEGER
                );
            """)
        
        except OperationalError:
            print("Table already exists")

def addToDB(w, f, o):
    with connection:
        sql = f"INSERT INTO WORD_INDEX (word, filename, occurence) values('{w}', '{f}', {o})"
        connection.execute(sql)

def queryDB(sqlQuery):
    with connection:
        return connection.execute(sqlQuery)

def fetchWordOccurence(word):
    with connection:
        data = connection.execute(f"SELECT * FROM WORD_INDEX WHERE word = '{word}'")
        c = 0
        res = []
        for row in data:
            c += 1
            res.append([row[1] , row[2] , str(row[3])])
        if(c < 1):
            res.append("Word does'nt exist in any document")
    return res

def createIndex():
    with connection:
        connection.execute("""
            CREATE INDEX wi on WORD_INDEX (word)
        """)
