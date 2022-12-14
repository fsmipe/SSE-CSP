# This works as a static class, data hub if you will, for sending stuff to SQL server (local)
# This file simulates CSP!
import sqlite3
from sqlite3 import Error
import os
import TA
import hashlib


# DB connection established
def initialize():
    connection = None
    try:
        connection = sqlite3.connect("SQL\sm_app.sqlite")
    except Error as e:
        print(f"The error '{e}' occurred")

    # connection.cursor().execute("CREATE TABLE sse_keywords(sse_keyword VARCHAR(10), sse_keyword_numfiles INT, sse_keyword_numsearch INT);")
    # connection.cursor().execute("CREATE TABLE sse_csp_keywords(ccsp_keywords_address VARCHAR(10), csp_keyvalue VARCHAR(10));")
    # connection.commit()

    return connection


# add multiple address and value pairs to CSP 
def addSSEDB(connection, cmds):
    for cmd in cmds:
        try:
            query = """INSERT INTO
                sse_csp_keywords(csp_keywords_address, csp_keyvalue)
                VALUES ('{a}', '{b}');""".format(a=cmd[0], b=cmd[1])

            connection.cursor().execute(query)

        except Error as e:
            print(e)

    connection.commit()


# search from database keywords value
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


# clears CSP SQL data
def emptyDB():
    connection = None
    try:
        connection = sqlite3.connect("SQL\sm_app.sqlite")

        connection.cursor().execute("DELETE FROM sse_csp_keywords;")
        connection.commit()

    except Error as e:
        print(e)


# removes all encrypted files from CSP
def deleteCSPFiles(sourceDir):
    for fname in os.listdir(sourceDir):
        os.remove(sourceDir + "/" + fname)


# Forwards kwj and NoFiles to TA, compares LTA and LU address saces and returns address's keyvalue
def forwardCSPtoTA(kwj, NoFiles, Lu):
    LTA = TA.processSearch(kwj, NoFiles)

    if LTA == Lu:
        print("Address space is valid")
        queryAddress = hashlib.sha256((kwj + ',' + str(NoFiles) + str(0)).encode()).hexdigest()
        res = searchDB(initialize(), queryAddress)
        return res

    else:
        return 0


# after search updates to new address
def updateSSEDB(connection, oldAddress, newAddress):
    try:
        query = """UPDATE sse_csp_keywords SET csp_keywords_address='{a}'
        WHERE csp_keywords_address='{b}'""".format(a=newAddress, b=oldAddress)
        connection.cursor().execute(query)

    except Error as e:
        print(e)

    connection.commit()


# after file deletion/insertion after first database run, updates correct values
def updateSSEDB2(connection, cmds):
    for cmd in cmds:
        try:
            query = """UPDATE sse_csp_keywords
            SET csp_keywords_address='{a}',
            csp_keyvalue='{b}'
            WHERE csp_keywords_address='{c}'""".format(a=cmd[1], b=cmd[2], c=cmd[0])
            connection.cursor().execute(query)

        except Error as e:
            print(e)

    connection.commit()