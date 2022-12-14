# Simulates Trusted Authority
from AESCipher import AESCipher
import sqlite3
from sqlite3 import Error
import hashlib
import sys

# This is kinda crappy fix, but structurarly secure and easy fix so class architecture doesn't need to be changed
TAModule = sys.modules[__name__]
TAModule.DOWORD = None
TAModule.DOKEYS = None


# Saves TA key
def addDOTA(aes):
    TAModule.DOKEYS = AESCipher("notNeeded", aes)


# This structure worksa as No.Files and No.Search
# Data is encrypted in transit
def addTaIndex(connection, cmds):
    for cmd in cmds:
        cmd = TAModule.DOKEYS.decrypt(cmd, "TA").split("X")
        try:
            query = """INSERT INTO
                sse_keywords (sse_keyword, sse_keyword_numfiles, sse_keyword_numsearch)
                VALUES ('{a}', {b}, {c});""".format(a=cmd[0], b=cmd[1], c=cmd[2])
            connection.cursor().execute(query)

        except Error as e:
            print(cmd[1], cmd[2])
            print(e)
            print()

    connection.commit()


# retrieve No.Files and No.Search for word
def getKWIndex(connection, key, word):
    # here user is autheticated with the key
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sse_keywords WHERE sse_keyword=?", (word,))
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("Word " + word + " isn't in the databases files")
            return 0

        print(rows)
        tmp = []
        for e in rows[0]:
            tmp.append(e)

        TAModule.DOWORD = tmp

        return tmp

    except Error as e:
        print(e)


# Update No.Search for word
def updateTAIndex(connection, word):
    try:
        query = """UPDATE sse_keywords SET sse_keyword_numsearch={a}
        WHERE sse_keyword='{b}'""".format(a=str(TAModule.DOWORD[2] + 1), b=word)
        connection.cursor().execute(query)

    except Error as e:
        print(e)

    connection.commit()


# Extra
def updateTAIndex2(connection, cmds):
    for cmd in cmds:
        cmd = TAModule.DOKEYS.decrypt(cmd, "TA").split("X")
        try:
            query = """UPDATE sse_keywords 
            SET sse_keyword_numfiles={a},
            sse_keyword_numsearch={b}
            WHERE sse_keyword='{c}'""".format(a=cmd[1], b=cmd[2], c=cmd[0])
            connection.cursor().execute(query)

        except Error as e:
            print(cmd[1], cmd[2])
            print(e)
            print()

    connection.commit()


# Empty TA SQL database, so empties No.Search and No.Files
def emptyDB():
    connection = None
    try:
        connection = sqlite3.connect("SQL\sm_app.sqlite")
        connection.cursor().execute("DELETE FROM sse_keywords;")

    except Error as e:
        print(f"The error '{e}' occurred")

    connection.commit()

    return connection


# Processes search, receives kwj and No.Files for word
def processSearch(kwj, NoFiles):
    wordHash = hashlib.sha256(TAModule.DOWORD[0].encode()).hexdigest()
    CSPkwj = wordHash + str(TAModule.DOWORD[2])
    DOkwj = TAModule.DOKEYS.decrypt(kwj, "TA")

    if DOkwj == CSPkwj:
        newkwj = TAModule.DOKEYS.encrypt(wordHash + str(int(TAModule.DOWORD[2]) + 1), "TA").decode()

        Lta = []
        for i in range(1, int(NoFiles)):  # MODIFIED
            addressThingy = hashlib.sha256((newkwj + ',' + str(i) + str(0)).encode()).hexdigest()
            Lta.append(addressThingy)

        return Lta

    else:
        print("Word encryption doesn't match, key is wrong or no authority")
        return 0



