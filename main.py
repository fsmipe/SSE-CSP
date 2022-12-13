import DataOwner
import CSP
import TA
import time
from AESCipher import AESCipher

dataOwners = []  # for now only one, but code can expand to multiple DO's


def main():
    # CSP.deleteCSPFiles("CSPFiles")
    CSP.initialize()
    # start = time.time()
    # CSP.emptyDB()
    # firstDO = DataOwner.DataOwner("exampleSeed1", "exampleSeed2")
    # firstDO.InGen("LocalFiles", "CSPFiles")

    # end = time.time()
    # print("Task 1 process took: " + str(end - start) + " seconds")

    while True:
        i = input("User command: ")
        i = i.split(" ")

        if i[0] == "emptyALL" and i.__len__() == 1:
            CSP.emptyDB()
            TA.emptyDB()
            CSP.deleteCSPFiles("CSPFiles")

        elif i[0] == "emptyCSPFiles" and i.__len__() == 1:
            CSP.deleteCSPFiles("CSPFiles")

        elif i[0] == "emptyDB" and i.__len__() == 1:
            TA.emptyDB()
            CSP.emptyDB()

        elif i[0] == "nDO" and i.__len__() == 1:
            do = input("Give DataOwner 2 key seeds: ")

            start = time.time()
            do = do.split(" ")
            firstDO = DataOwner.DataOwner(do[0], do[1])
            TA.addDOTA(do[0])
            firstDO.InGen("LocalFiles", "CSPFiles")
            end = time.time()

            print("Initialization took: " + str(end - start) + " seconds")
            dataOwners.append(firstDO)

        elif i[0] == "eDO" and i.__len__() == 1:
            do = input("Give DataOwner 2 key seeds: ")
            do = do.split(" ")
            firstDO = DataOwner.DataOwner(do[0], do[1])
            TA.addDOTA(do[1])
            dataOwners.append(firstDO)

        elif i[0] == "nF" and i.__len__() == 3:
            do = i[2]
            file = i[1]
            continue

        elif i[0] == "search" and i.__len__() == 2:
            start = time.time()
            word = i[1]
            dataOwners[0].getKWIndex(word)
            end = time.time()

            print("Search took: " + str(end - start) + " seconds")


        elif i[0] == "q" and i.__len__() == 1:
            break

        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
