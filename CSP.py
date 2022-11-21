# This works as a static class, data hub if you will, for sending stuff to SQL server (local)
import sqlite3
from sqlite3 import Error

def initialize():
    connection = None
    try:
        connection = sqlite3.connect("SQL\sm_app.sqlite")
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def test(connection):
    mycursor = connection.cursor()


    try:
        mycursor.execute("""CREATE TABLE sse_keywords(sse_keywords_id INT, sse_keyword VARCHAR(10), sse_keyword_numfiles INT,  sse_keyword_numsearch INT);""")
        connection.commit()
        print("Query executed successfully")
        mycursor.execute("""CREATE TABLE sse_csp_keywords(csp_keywords_id INT, csp_keywords_address VARCHAR(10),csp_keyvalue VARCHAR(10) );""")
        connection.commit()
        print("Query executed successfully")

    except Error as e:
        print(e)


