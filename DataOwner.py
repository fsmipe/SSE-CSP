import CSP
from AESCipher import AESCipher
import os
from collections import Counter
from itertools import chain
import hashlib
import string
import TA


class DataOwner:
    # This operates as KeyGen function
    def __init__(self, aes, seed2):
        self.aes = AESCipher("a", "a")
        self.TAseed = seed2
        self.allMap = {}
        self.connection = CSP.initialize()
        self.wordDict = {}

    # InGen
    def InGen(self, sourceDir, desDir):

        for fname in os.listdir(sourceDir):
            self.AddFileInit(fname, sourceDir, desDir)

        print("Done with file encryption")
        print(str(self.wordDict.__len__()) + " unique keywords in files")

        sse_keywords_id = 0
        csp_keywords_id = 0

        sqlcmdscsp = []
        TAIndexSearchandFiles = []
        pushCounter = 0

        for key, value in self.wordDict.items():
            wordHash = hashlib.sha256(key.encode()).hexdigest()
            kwij = self.aes.encrypt(wordHash + str(value[2]), "TA").decode()

            csp_keywords_address = hashlib.sha256((kwij + ',' + str(value[1]) + str(0)).encode()).hexdigest()
            csp_keyvalue = self.aes.encrypt("-".join(value[0]) + "-" + str(value[1]), "DO").decode()

            # CAP AllMap, file sent to CSP is simulated with just a different folder
            sqlcmdscsp.append([csp_keywords_id, str(csp_keywords_address), str(csp_keyvalue)])

            # this is No.Files and No.Search
            tempTAIndex = "X".join([str(sse_keywords_id), key, str(value[1]), str(value[2])])
            try:
                TAIndexSearchandFiles.append(self.aes.encrypt(tempTAIndex, "TA").decode())
            except:
                print(key)
            else:
                if pushCounter == 200000:
                    print("DB push event")
                    TA.addTaIndex(self.connection, TAIndexSearchandFiles, self.TAseed)
                    CSP.addSSEDB(self.connection, sqlcmdscsp)
                    sqlcmdscsp = []
                    TAIndexSearchandFiles = []
                    pushCounter = 0

            csp_keywords_id += 1
            sse_keywords_id += 1
            pushCounter += 1

        TA.addTaIndex(self.connection, TAIndexSearchandFiles, self.TAseed)
        CSP.addSSEDB(self.connection, sqlcmdscsp)
        sqlcmdscsp = []
        TAIndexSearchandFiles = []

    def AddFileInit(self, fname, sourceDir, desDir):
        file1 = open(sourceDir + "/" + fname, "r")
        try:
            freadOG = file1.read()
        except:
            print(fname + " couldn't be red")
        else:
            fread = ' '.join(freadOG.splitlines())
            fread = ' '.join(fread.split())
            for reg in ['{', '}', '\n', '/', '-', '#', '!', ',', '.', '"', '(', ')', '*', '>', '<', '?', '\\', '_',
                        '[', '\'', ']', '=', '@', ';', '+', ':', '&', '´', '|', '`', '$', '¿', '»']:
                fread = fread.replace(reg, ' ')

            for word in fread.split(' '):
                word = word.lower()
                if 2 < word.__len__() < 50:  # and not word.isnumeric():
                    if word in self.wordDict:
                        if fname not in self.wordDict[word][0]:
                            self.wordDict[word][0].append(fname)
                            self.wordDict[word][1] += 1

                    else:
                        self.wordDict.update({word: [[fname], 1, 0]})

            # words.append(list(dict.fromkeys(fread.split(" "))))

            try:
                cipherTextt = self.aes.encrypt(freadOG, "DO").decode()
            except:
                print(fname + " Couldn't be encrypted")
            else:
                file2 = open(desDir + "/" + fname, "w")
                # print(fname + " " + str(len(fread)))
                file2.write(cipherTextt)
                file2.close()

    # HERE FILE DELETION

    def getKWIndex(self, word):
        # index in form of (0, 'the', 10, 0)
        index = TA.getKWIndex(self.connection, self.TAseed, word)

        wordHash = hashlib.sha256(index[1].encode()).hexdigest()
        kwj = self.aes.encrypt(wordHash + str(int(index[3])), "TA").decode()
        newkwj = self.aes.encrypt(wordHash + str(int(index[3]) + 1), "TA").decode()

        Lu = []
        for i in range(1, int(index[2])):
            addressThingy = hashlib.sha256((newkwj + ',' + str(i) + str(0)).encode()).hexdigest()
            Lu.append(addressThingy)

        # send kwj, no.files, LU to CSP
        qAddress = CSP.forwardCSPtoTA([kwj, int(index[2]), Lu])
        files = self.aes.decrypt(qAddress[0], "DO")
        files = files.split("-")
        print(files)



