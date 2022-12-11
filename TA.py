from AESCipher import AESCipher
import sqlite3
from sqlite3 import Error

DOkeys = {}

def addDOTA(keyseed):
    DOkeys.update({keyseed: AESCipher("notNeeded", keyseed)})


def addTaIndex(connection, cmds, seed):
    aes = DOkeys[seed]

    errors = 0
    for cmd in cmds:
        cmd = aes.decrypt(cmd, "TA").split("X")
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