import DataOwner
import CSP

def main():
    firstDO = DataOwner.DataOwner("exampleSeed1", "exampleSeed2")
    c = CSP.initialize()
    CSP.test(c)


if __name__ == "__main__":
    main()