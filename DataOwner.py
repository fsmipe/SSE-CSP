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
            try:
                fread = file1.read()
            except:
                print(fname + " couldn't be red")
            else:
                fread = ' '.join(fread.splitlines())
                fread = ' '.join(fread.split())
                for reg in ['\n', '/', '-', '!', ',', '.', '"', '(', ')', '*', '>', '<', '?', '\\', '_', '[', ']', '=', '@', ';', '+']:
                    fread = fread.replace(reg, ' ')
                words.append(list(dict.fromkeys(fread.split(" "))))

                for key in words:
                    if key.__len__() <= 2:
                        words.remove(key)
                    if key.__contains__("\\"):
                        return

                try:
                    cipherTextt = self.aes.encrypt(fread).decode()
                except:
                    print(fname + " Couldn't be encrypted")
                else:
                    file2 = open(desDir + "/" + fname, "w")
                    # print(fname + " " + str(len(fread)))
                    file2.write(cipherTextt)
                    file2.close()

        sse_keywords_id = 0
        csp_keywords_id = 0
        fileIndex = 0

        flatten_list = Counter(list(chain.from_iterable(words)))
        sqlcmdscsp = []
        sqlcmdssse = []

        for fw in words:
            for w in fw:
                sse_keyword_numfiles = flatten_list[w]
                sse_keyword_numsearch = 0
                sse_keyword = hashlib.sha256(w.encode()).hexdigest()
                kw = hashlib.sha256((sse_keyword + str(sse_keyword_numsearch)).encode()).hexdigest()

                csp_keywords_address = hashlib.sha256((kw + str(sse_keyword_numfiles)).encode()).hexdigest()
                csp_keyvalue = self.aes.encrypt(plainTextFiles[fileIndex] + str(sse_keyword_numsearch)).decode()
                # sqlcmdscsp.append([csp_keywords_id, csp_keywords_address, csp_keyvalue])
                # sqlcmdssse.append([sse_keywords_id, sse_keyword, sse_keyword_numfiles, sse_keyword_numsearch])

                # print([csp_keywords_id, str(csp_keywords_address), str(csp_keyvalue)])

                sqlcmdscsp.append([csp_keywords_id, str(csp_keywords_address), str(csp_keyvalue)])
                sqlcmdssse.append([sse_keywords_id, str(sse_keyword), sse_keyword_numfiles, sse_keyword_numsearch])

                csp_keywords_id += 1
                sse_keywords_id += 1
            fileIndex += 1

        # CSP.addMultiToDB(self.connection, sqlcmds)
        CSP.addSSECSPDB(self.connection, sqlcmdssse)
        CSP.addSSEDB(self.connection, sqlcmdscsp)



        for i in plainTextFiles:
            if os.path.exists(sourceDir + "/" + i):
                # os.remove(d + "/" + i)
                continue


    def AddFile(self):
        return



