from AESCipher import AESCipher
import os
from collections import Counter
from itertools import chain
import hashlib

class DataOwner:
    # This operates as KeyGen function
    def __init__(self, seed1, seed2):
        self.aes = AESCipher(seed1, seed2)
        self.allMap = {}


    # InGen
    def InGen(self, sourceDir, desDir):
        words = []
        plainTextFiles = []

        for fname in os.listdir(sourceDir):
            plainTextFiles.append(fname)
            file1 = open(sourceDir + "/" + fname, "r")
            fread = file1.read()
            words.append(list(dict.fromkeys(fread.split(" "))))

            file2 = open(desDir + "/" + fname, "w")
            file2.write(self.aes.encrypt(fread).decode())
            file2.close()


        sse_keywords_id = 0
        csp_keywords_id = 0
        fileIndex = 0

        flatten_list = Counter(list(chain.from_iterable(words)))
        sqlcmdscsp = []
        sqlcmdssse = []
        sqlcmds = []

        for fw in words:
            for w in fw:
                sse_keyword_numfiles = flatten_list[w]
                sse_keyword_numsearch = 0
                sse_keyword = hashlib.sha256(w.encode()).digest()
                kw = hashlib.sha256((sse_keyword + str(sse_keyword_numsearch).encode())).digest()

                csp_keywords_address = hashlib.sha256((kw + str(sse_keyword_numfiles).encode())).digest()
                csp_keyvalue = self.aes.encrypt(plainTextFiles[fileIndex] + str(sse_keyword_numsearch))
                sqlcmdscsp.append([csp_keywords_id, csp_keywords_address, csp_keyvalue])
                sqlcmdssse.append([sse_keywords_id, sse_keyword, sse_keyword_numfiles, sse_keyword_numsearch])

                # these would be pushed to data base, but didn't have time to do it (tables at bottom)
                # but here i just have local database, which is just vectors :3
                sqlcmds.append(
                    "\"\"\"INSERT into sse_csp_keywords values(" + str(csp_keywords_id) + ", \'" + str(
                        csp_keywords_address) +
                    "\', \'" + str(csp_keyvalue) + "\');\"\"\""
                )
                sqlcmds.append(
                    "\"\"\"INSERT into sse_keywords values(" + str(sse_keywords_id) + ", \'" + str(sse_keyword) +
                    "\', " + str(sse_keyword_numfiles) + ", " + str(sse_keyword_numsearch) + ");\"\"\""
                )

                # this would be pushed to database

                csp_keywords_id += 1
                sse_keywords_id += 1
            fileIndex += 1




        for i in plainTextFiles:
            if os.path.exists(sourceDir + "/" + i):
                # os.remove(d + "/" + i)
                continue


    def AddFile(self):
        return



