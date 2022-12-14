# This works as a static class, data hub if you will, for sending stuff to SQL server (local)
import sqlite3
from sqlite3 import Error
import os
import TA
import hashlib


def initialize():
    connection = None
    try:
        connection = sqlite3.connect("SQL\sm_app.sqlite")
        # print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    # connection.cursor().execute("CREATE TABLE sse_keywords(sse_keywords_id INT, sse_keyword VARCHAR(10), sse_keyword_numfiles INT, sse_keyword_numsearch INT);")
    # connection.cursor().execute("CREATE TABLE sse_csp_keywords(csp_keywords_id INT, csp_keywords_address VARCHAR(10), csp_keyvalue VARCHAR(10));")
    # connection.commit()

    return connection


def addSSEDB(connection, cmds):
    strings = []
    for cmd in cmds:
        try:
            query = """INSERT INTO
                sse_csp_keywords(csp_keywords_address, csp_keyvalue)
                VALUES ('{a}', '{b}');""".format(a=cmd[0], b=cmd[1])

            connection.cursor().execute(query)

        except Error as e:
            print(cmd[1], cmd[2])
            print(e)
            print()

    connection.commit()


def searchDB(connection, CSPaddress):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT csp_keyvalue FROM sse_csp_keywords WHERE csp_keywords_address=?", (CSPaddress,))
        rows = cursor.fetchall()

        tmp = []
        for address in rows:
            tmp.append(address)

        return tmp[0]

    except Error as e:
        print(e)


def emptyDB():
    connection = None
    try:
        connection = sqlite3.connect("SQL\sm_app.sqlite")

        connection.cursor().execute("DELETE FROM sse_csp_keywords;")
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def deleteCSPFiles(sourceDir):
    for fname in os.listdir(sourceDir):
        os.remove(sourceDir + "/" + fname)


def forwardCSPtoTA(kwj, NoFiles, Lu):
    LTA = TA.processSearch(kwj, NoFiles)

    if LTA == Lu:
        print("Address space is valid")
        queryAddress = hashlib.sha256((kwj + ',' + str(NoFiles) + str(0)).encode()).hexdigest()
        res = searchDB(initialize(), queryAddress)
        return res

    else:
        return 0;


def updateSSEDB(connection, oldAddress, newAddress):
    try:
        query = """UPDATE sse_csp_keywords SET csp_keywords_address='{a}'
        WHERE csp_keywords_address='{b}'""".format(a=newAddress, b=oldAddress)
        connection.cursor().execute(query)

    except Error as e:
        print(e)

    connection.commit()