import DataOwner
import CSP
import time

def main():
    CSP.deleteCSPFiles("CSPFiles")
    CSP.initialize()
    start = time.time()
    CSP.emptyDB()
    firstDO = DataOwner.DataOwner("exampleSeed1", "exampleSeed2")
    firstDO.InGen("LocalFiles", "CSPFiles")

    end = time.time()
    print("Task 1 process took: " + str(end - start) + " seconds")

    # CSP.emptyDB()

    # CSP.printDB(CSP.initialize())



if __name__ == "__main__":
    main()
