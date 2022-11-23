import CSP
from AESCipher import AESCipher
import os
from collections import Counter
from itertools import chain
import hashlib
import string

class DataOwner:
    # This operates as KeyGen function
    def __init__(self, seed1, seed2):
        self.aes = AESCipher(seed1, seed2)
        self.allMap = {}
        self.connection = CSP.initialize()


    # InGen
    def InGen(self, sourceDir, desDir):
        words = []
        plainTextFiles = []

        for fname in os.listdir(sourceDir):
            plainTextFiles.append(fname)
            file1 = open(sourceDir + "/" + fname, "r")
            fread = file1.read()
            fread = ' '.join(fread.splitlines())
            fread = ' '.join(fread.split())
            for reg in ['\n', '/', '-', '!', ',', '.', '"', '(', ')', '*', '>', '<', '?', '\\', '_', '[', ']']:
                fread = fread.replace(reg, ' ')
            words.append(list(dict.fromkeys(fread.split(" "))))

            # file2 = open(desDir + "/" + fname, "w")
            # print(fname)
            # file2.write(self.aes.encrypt(fread).decode())
            # file2.close()


        sse_keywords_id = 0
        csp_keywords_id = 0
        fileIndex = 0

        flatten_list = Counter(list(chain.from_iterable(words)))
        sqlcmdscsp = []
        sqlcmdssse = []

        print(flatten_list)

        for fw in words:
            for w in fw:
                sse_keyword_numfiles = flatten_list[w]
                sse_keyword_numsearch = 0
                sse_keyword = hashlib.sha256(w.encode()).digest()
                kw = hashlib.sha256((sse_keyword + str(sse_keyword_numsearch).encode())).digest()

                csp_keywords_address = hashlib.sha256((kw + str(sse_keyword_numfiles).encode())).digest()
                csp_keyvalue = self.aes.encrypt(plainTextFiles[fileIndex] + str(sse_keyword_numsearch))
                # sqlcmdscsp.append([csp_keywords_id, csp_keywords_address, csp_keyvalue])
                # sqlcmdssse.append([sse_keywords_id, sse_keyword, sse_keyword_numfiles, sse_keyword_numsearch])

                sqlcmdscsp.append([csp_keywords_id, str(csp_keywords_address), str(csp_keyvalue)])
                sqlcmdssse.append([sse_keywords_id, str(sse_keyword), str(sse_keyword_numfiles), str(sse_keyword_numsearch)])

                csp_keywords_id += 1
                sse_keywords_id += 1
            fileIndex += 1

        # CSP.addMultiToDB(self.connection, sqlcmds)
        CSP.addSSEDB(self.connection, sqlcmdssse)


        for i in plainTextFiles:
            if os.path.exists(sourceDir + "/" + i):
                # os.remove(d + "/" + i)
                continue


    def AddFile(self):
        return



