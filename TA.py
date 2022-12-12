from AESCipher import AESCipher
import sqlite3
from sqlite3 import Error
import hashlib
import sys

TAModule = sys.modules[__name__]
TAModule.DOWORD = None
TAModule.DOKEYS = None


def addDOTA(aes):
    TAModule.DOKEYS = aes


def getDOTA():
    return


def addTaIndex(connection, cmds):
    for cmd in cmds:
        cmd = TAModule.DOKEYS.decrypt(cmd, "TA").split("X")
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

    connection.commit()


# word could be encrypted+decrypted but i don't see the benefit, not specified
def getKWIndex(connection, key, word):
    # here DO is identified with the key
    try:
        cursor = connection.cursor()
        # query = """SELECT * FROM sse_keywords WHERE sse_keyword = {a}""".format(word)
        cursor.execute("SELECT * FROM sse_keywords WHERE sse_keyword=?", (word,))
        rows = cursor.fetchall()

        tmp = []
        for e in rows[0]:
            tmp.append(e)

        TAModule.DOWORD = tmp
        return tmp

    except Error as e:
        print(e)


def updateTAIndex(connection, key, word):
    return


def emptyDB():
    connection = None
    try:
        connection = sqlite3.connect("SQL\sm_app.sqlite")
        # print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    connection.cursor().execute("DELETE FROM sse_keywords;")

    connection.commit()

    return connection


def processSearch(CSPdata):
    # TODO: fix the zero
    wordHash = hashlib.sha256(TAModule.DOWORD[1].encode()).hexdigest()
    CSPkwj = wordHash + str(TAModule.DOWORD[3])
    DOkwj = TAModule.DOKEYS.decrypt(CSPdata[0], "TA")

    if DOkwj == CSPkwj:
        print("all is bueno")
        kwj = TAModule.DOKEYS.encrypt(wordHash + str(int(TAModule.DOWORD[3])), "TA").decode()
        newkwj = TAModule.DOKEYS.encrypt(wordHash + str(int(TAModule.DOWORD[3]) + 1), "TA").decode()

        Lta = []
        for i in range(1, int(TAModule.DOWORD[2])):
            addressThingy = hashlib.sha256((newkwj + ',' + str(i) + str(0)).encode()).hexdigest()
            Lta.append(addressThingy)

        return Lta

    else:
        print("fucked")
        return 0



