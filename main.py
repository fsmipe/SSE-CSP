import DataOwner
import CSP

def main():
    firstDO = DataOwner.DataOwner("exampleSeed1", "exampleSeed2")
    firstDO.InGen("LocalFiles", "CSPFiles")

    CSP.printDB(CSP.initialize())


if __name__ == "__main__":
    main()