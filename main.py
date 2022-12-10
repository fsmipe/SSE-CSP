import DataOwner
import CSP
import TA
import time

def main():
    #CSP.deleteCSPFiles("CSPFiles")
    CSP.initialize()
    #start = time.time()
    #CSP.emptyDB()
    #firstDO = DataOwner.DataOwner("exampleSeed1", "exampleSeed2")
    #firstDO.InGen("LocalFiles", "CSPFiles")

    #end = time.time()
    #print("Task 1 process took: " + str(end - start) + " seconds")

    while True:
        i = input("User command: ")
        i = i.split(" ")

        if i[0] == "emptyCSP" and i.__len__() == 1:
            CSP.emptyDB()
            CSP.deleteCSPFiles("CSPFiles")
        elif i[0] == "nDO" and i.__len__() == 1:
            do = input("Give DataOwner 2 key seeds: ")
            do = do.split(" ")
            firstDO = DataOwner.DataOwner(do[0], do[1])
            TA.addDOTA(do[1])
            start = time.time()
            firstDO.InGen("LocalFiles", "CSPFiles")
            end = time.time()
            print("Initialization took: " + str(end - start) + " seconds")

        elif i[0] == "nF" and i.__len__() == 3:
            do = i[2]
            file = i[1]
            continue

        elif i[0] == "search" and i.__len__() == 2:
            word = i[1]

        elif i[0] == "q" and i.__len__() == 1:
            break

        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
