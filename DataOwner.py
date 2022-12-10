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
        # words = []
        wordDict = {}
        plainTextFiles = []

        for fname in os.listdir(sourceDir):
            plainTextFiles.append(fname)
            file1 = open(sourceDir + "/" + fname, "r")
            try:
                freadOG = file1.read()
            except:
                print(fname + " couldn't be red")
            else:
                fread = ' '.join(freadOG.splitlines())
                fread = ' '.join(fread.split())
                for reg in ['{', '}', '\n', '/', '-', '#', '!', ',', '.', '"', '(', ')', '*', '>', '<', '?', '\\', '_',
                            '[', '\'', ']', '=', '@', ';', '+', ':', '&']:
                    fread = fread.replace(reg, ' ')

                for word in fread.split(' '):
                    word = word.lower()
                    if word.__len__() > 3 and word.__len__() < 50 and not word.isnumeric():
                        if word in wordDict:
                            if fname not in wordDict[word][0]:
                                wordDict[word][0].append(fname)
                                wordDict[word][1] += 1
                        else:
                            wordDict.update({word: [[fname], 1]})

                # words.append(list(dict.fromkeys(fread.split(" "))))

                try:
                    cipherTextt = self.aes.encrypt(freadOG).decode()
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
        print("Done with file encryption")

        # flatten_list = Counter(list(chain.from_iterable(words)))
        # print(str(len(words)))

        sqlcmdscsp = []
        sqlcmdssse = []
        pushCounter = 0

        for key, value in wordDict.items():
            # print(key)
            sse_keyword_numfiles = value[1]
            sse_keyword = hashlib.sha256(key.encode()).hexdigest()
            kw = hashlib.sha256((sse_keyword + str(0)).encode()).hexdigest()

            csp_keywords_address = hashlib.sha256((kw + str(sse_keyword_numfiles)).encode()).hexdigest()
            csp_keyvalue = self.aes.encrypt("-".join(value[0]) + str(0)).decode()

            sqlcmdscsp.append([csp_keywords_id, str(csp_keywords_address), str(csp_keyvalue)])
            sqlcmdssse.append([sse_keywords_id, key, sse_keyword_numfiles, 0])
            if pushCounter == 200000:
                print("DB push event")
                CSP.addSSECSPDB(self.connection, sqlcmdssse)
                CSP.addSSEDB(self.connection, sqlcmdscsp)
                sqlcmdscsp = []
                sqlcmdssse = []
                pushCounter = 0

            csp_keywords_id += 1
            sse_keywords_id += 1
            pushCounter += 1

        CSP.addSSECSPDB(self.connection, sqlcmdssse)
        CSP.addSSEDB(self.connection, sqlcmdscsp)
        sqlcmdscsp = []
        sqlcmdssse = []

        for i in plainTextFiles:
            if os.path.exists(sourceDir + "/" + i):
                # os.remove(d + "/" + i)
                continue

    def AddFile(self):
        return



