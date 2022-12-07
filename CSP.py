# This works as a static class, data hub if you will, for sending stuff to SQL server (local)
import sqlite3
from sqlite3 import Error
import os

def initialize():
    connection = None
    try:
        connection = sqlite3.connect("SQL\sm_app.sqlite")
        # print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")


    # connection.cursor().execute("CREATE TABLE sse_keywords(sse_keywords_id INT, sse_keyword VARCHAR(10), sse_keyword_numfiles INT, sse_keyword_numsearch INT);")
    # connection.cursor().execute("CREATE TABLE sse_csp_keywords(csp_keywords_id INT, csp_keywords_address VARCHAR(10), csp_keyvalue VARCHAR(10));")
    # connection.cursor().execute("DELETE FROM sse_keywords;")
    # connection.cursor().execute("DELETE FROM sse_csp_keywords;")

    connection.commit()

    # connection.cursor().execute("INSERT INTO sse_keywords (sse_keywords_id, sse_keyword, sse_keyword_numfiles, sse_keyword_numsearch) VALUES (2, 'fdsfs', 'fsfsdf', 'sfsdf'), (4, 'fdfsd', 'sdfsdf', 'sfsdf');")
    connection.commit()

    return connection

def addToDB(connection, command):
    mycursor = connection.cursor()

    try:
        mycursor.execute(command)
        connection.commit()
        # print("Query executed successfully")

    except Error as e:
        print(e)

def addSSECSPDB(connection, cmds):
    strings = []
    errors = 0
    for cmd in cmds:
        # print("(" + str(cmd[0]) + ", " + str(cmd[1])[2:-1] + ", " + str(cmd[2]) + ", " + str(cmd[3]) + ")")
        # sqlcmd = "(" + str(cmd[0]) + ", " + str(cmd[1])[2:-1] + ", " + str(cmd[2]) + ", " + str(cmd[3]) + ")"
        try:
            query = """INSERT INTO
                sse_keywords (sse_keywords_id, sse_keyword, sse_keyword_numfiles, sse_keyword_numsearch)
                VALUES ({a}, '{b}', {c}, {d});""".format(a=cmd[0], b=cmd[1], c=cmd[2], d=cmd[3])


            connection.cursor().execute(query)

        except Error as e:
            errors += 1
            print(cmd[1], cmd[2])
            print(e)
            print()

    print(errors)
    connection.commit()

def addSSEDB(connection, cmds):
    strings = []
    errors = 0
    for cmd in cmds:
        # print("(" + str(cmd[0]) + ", " + str(cmd[1])[2:-1] + ", " + str(cmd[2]) + ", " + str(cmd[3]) + ")")
        # sqlcmd = "(" + str(cmd[0]) + ", " + str(cmd[1])[2:-1] + ", " + str(cmd[2]) + ", " + str(cmd[3]) + ")"
        try:
            query = """INSERT INTO
                sse_csp_keywords(csp_keywords_id, csp_keywords_address, csp_keyvalue)
                VALUES ({a}, '{b}', '{c}');""".format(a=cmd[0], b=cmd[1], c=cmd[2])


            connection.cursor().execute(query)

        except Error as e:
            errors += 1
            print(cmd[1], cmd[2])
            print(e)
            print()

    print(errors)
    connection.commit()

def addMultiToDB(connection, commands):
    mycursor = connection.cursor()

    try:
        for i in commands:
            mycursor.execute(i)
        # print("Query executed successfully")
        connection.commit()

    except Error as e:
        print(e)

    mycursor.execute("SELECT * FROM sse_keywords")

    data = mycursor.fetchall()

    for i in data:
        print(i)


def searchDB(connection, kw):
    mycursor = connection.cursor()
    return "something"

def printDB(connection):
    mycursor = connection.cursor()

    mycursor.execute("SELECT * FROM sse_keywords")

    data = mycursor.fetchall()

    for i in data:
        print(i)


def emptyDB():
    connection = None
    try:
        connection = sqlite3.connect("SQL\sm_app.sqlite")
        # print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    connection.cursor().execute("DELETE FROM sse_keywords;")
    connection.cursor().execute("DELETE FROM sse_csp_keywords;")

    connection.commit()

    return connection

def deleteCSPFiles(sourceDir):
    for fname in os.listdir(sourceDir):
        os.remove(sourceDir + "/" + fname)
