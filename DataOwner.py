# Simulates DataOwner/User, can be multiple classes
import CSP
from AESCipher import AESCipher
import os
import hashlib
import TA


class DataOwner:
    # This operates as KeyGen function
    def __init__(self, seed1, seed2):
        self.aes = AESCipher(seed1, seed2)
        self.TAseed = seed2
        self.connection = CSP.initialize()
        # this is local No.Fiels and No.Search
        self.wordDict = {}

    # InGen
    def InGenFolder(self, sourceDir, desDir):

        for fname in os.listdir(sourceDir):
            self.AddFileInGenFolder(fname, sourceDir, desDir)

        print("Done with file encryption")
        print(str(self.wordDict.__len__()) + " unique keywords in files")

        sqlcmdscsp = []
        TAIndexSearchandFiles = []
        pushCounter = 0

        for key, value in self.wordDict.items():
            wordHash = hashlib.sha256(key.encode()).hexdigest()
            kwij = self.aes.encrypt(wordHash + str(value[2]), "TA").decode()

            csp_keywords_address = hashlib.sha256((kwij + ',' + str(value[1]) + str(0)).encode()).hexdigest()
            csp_keyvalue = self.aes.encrypt("-".join(value[0]) + "-" + str(value[1]), "DO", True).decode()

            # CAP AllMap, file sent to CSP is simulated with just a different folder
            sqlcmdscsp.append([str(csp_keywords_address), str(csp_keyvalue)])

            # this is No.Files and No.Search
            tempTAIndex = "X".join([key, str(value[1]), str(value[2])])
            try:
                TAIndexSearchandFiles.append(self.aes.encrypt(tempTAIndex, "TA", True).decode())
            except:
                print(key)
            else:
                if pushCounter == 200000:
                    print("DB push event")
                    TA.addTaIndex(self.connection, TAIndexSearchandFiles)
                    CSP.addSSEDB(self.connection, sqlcmdscsp)
                    sqlcmdscsp = []
                    TAIndexSearchandFiles = []
                    pushCounter = 0

            pushCounter += 1

        TA.addTaIndex(self.connection, TAIndexSearchandFiles)
        CSP.addSSEDB(self.connection, sqlcmdscsp)
        sqlcmdscsp = []
        TAIndexSearchandFiles = []

    def AddFileInGenFolder(self, fname, sourceDir, desDir):
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

            try:
                cipherTextt = self.aes.encrypt(freadOG, "DO", True).decode()
            except:
                print(fname + " Couldn't be encrypted")
            else:
                file2 = open(desDir + "/" + fname, "w")
                file2.write(cipherTextt)
                file2.close()
                # os.remove(sourceDir + "/" + fname)

    def addFile(self, fname, sourceDir, desDir):
        return

    def search(self, word, desDir, sourceDir):
        # index in form of ('the', 10, 0)
        word = word.lower()
        index = TA.getKWIndex(self.connection, self.TAseed, word)

        if index == 0:
            return

        TA.updateTAIndex(self.connection, word)

        wordHash = hashlib.sha256(index[0].encode()).hexdigest()
        kwj = self.aes.encrypt(wordHash + str(int(index[2])), "TA").decode()
        newkwj = self.aes.encrypt(wordHash + str(int(index[2]) + 1), "TA").decode()

        Lu = []
        for i in range(1, int(index[1])):
            addressThingy = hashlib.sha256((newkwj + ',' + str(i) + str(0)).encode()).hexdigest()
            Lu.append(addressThingy)

        # send kwj, no.files, LU to CSP
        qAddress = CSP.forwardCSPtoTA(kwj, int(index[1]), Lu)
        if qAddress != 0:
            files = self.aes.decrypt(qAddress[0], "DO")
            files = files.split("-")
            files = files[:-1]
            print(files)
            i = input("Dow you want to decrypt these files?: (y/n)")

            oldAddress = hashlib.sha256((kwj + ',' + str(index[1]) + str(0)).encode()).hexdigest()
            newAddress = hashlib.sha256((newkwj + ',' + str(index[1]) + str(0)).encode()).hexdigest()

            CSP.updateSSEDB(self.connection, oldAddress, newAddress)

            if i == "y":
                for fname in files:
                    try:
                        file1 = open(sourceDir + "/" + fname, "r")
                        freadOG = file1.read()
                        cipherTextt = self.aes.decrypt(freadOG, "DO")
                    except:
                        print(fname + " Couldn't be decrypted")
                    else:
                        file2 = open(desDir + "/" + fname, "w")
                        file2.write(cipherTextt)
                        file2.close()






