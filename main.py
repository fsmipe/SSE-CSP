import DataOwner
import CSP
import TA
import time

DESTINATIONFOLDER = "CSPFiles"

dataOwners = []  # for now only one, but code can expand to multiple DO's


def main():
    CSP.initialize()

    while True:
        i = input("User command: ")
        i = i.split(" ")

        if i[0] == "emptyALL" and i.__len__() == 1:
            CSP.emptyDB()
            TA.emptyDB()
            CSP.deleteCSPFiles(DESTINATIONFOLDER)

        elif i[0] == "emptyCSP" and i.__len__() == 1:
            CSP.emptyDB()
            CSP.deleteCSPFiles(DESTINATIONFOLDER)

        elif i[0] == "emptyTA" and i.__len__() == 1:
            TA.emptyDB()


        # newDataOwner/existingDataOwner, this reads local files and creates DB
        elif i[0] == "addDO" and i.__len__() == 1:
            do = input("Give DataOwner 2 key seeds: ")
            start = time.time()
            do = do.split(" ")
            firstDO = DataOwner.DataOwner(do[0], do[1])
            TA.addDOTA(do[1])
            dataOwners.append(firstDO)

        elif i[0] == "addFolder" and i.__len__() == 1:
            start = time.time()
            dataOwners[0].InGenFolder("LocalFiles", DESTINATIONFOLDER)
            end = time.time()
            print("Initialization took: " + str(end - start) + " seconds")

        elif i[0] == "addFolderEX" and i.__len__() == 2:
            f = i[1]
            start = time.time()
            dataOwners[0].addFolder(f, DESTINATIONFOLDER)
            end = time.time()
            print("DB update took: " + str(end - start) + " seconds")


        elif i[0] == "search" and i.__len__() == 2:
            start = time.time()
            word = i[1]
            dataOwners[0].search(word, "tmp", DESTINATIONFOLDER)
            end = time.time()

            print("Search took: " + str(end - start) + " seconds")


        elif i[0] == "q" and i.__len__() == 1:
            break

        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
