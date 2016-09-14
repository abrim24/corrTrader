def calcCapm(b, r, erm):
    return (b * (erm - r)) + r


def getVals():
    try:
        b = input("Enter beta: ")
        erm = input("Enter risk-free rate: ")
        r = input("Enter expected of Market: ")
    except: badInput()
    if (not type(b) == float) or (not type(r) == float) or (not type(erm == float)): badInput()
    return [b, erm, r]


def badInput():
    print("Bad Input, Run Again!")
    exit


def main():
    vals = getVals()
    print("Expected return is: ", calcCapm(vals[0], vals[1], vals[2]))


if __name__ == "__main__": main()