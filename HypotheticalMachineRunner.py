import os, sys
from HypotheticalMachineGenerator import *

command = ""
value = ""

i = 0
s = -1
readingsCount = 0

D = []
C = []
varAddress = []

def CRCT(k):
    global D, s
    s += 1
    D.append(0)
    D[s] = k

def CRVL(n):
    global D, s, varAddress
    s += 1
    D.append(D[varAddress[n]])

def SOMA():
    global D, s
    D[s-1] = D[s-1] + D[s]
    s -= 1
    D.pop()

def SUBT():
    global D, s
    D[s-1] = D[s-1] - D[s]
    s -= 1
    D.pop()

def MULT():
    global D, s
    D[s-1] = D[s-1] * D[s]
    s -= 1
    D.pop()

def DIVI():
    global D, s
    if D[s] == 0:
        print("Unable to divide by 0")
        exit()
    D[s-1] = D[s-1] / D[s]
    s -= 1
    D.pop()

def INVE():
    global D, s
    D[s] = - D[s]

def CPME():
    global D, s
    if D[s-1] < D[s]:
        D[s-1] = 1
    else:
        D[s-1] = 0
    s -= 1
    D.pop()

def CPMA():
    global D, s
    if D[s-1] > D[s]:
        D[s-1] = 1
    else:
        D[s-1] = 0
    s -= 1
    D.pop()

def CPIG():
    global D, s
    if D[s-1] == D[s]:
        D[s-1] = 1
    else:
        D[s-1] = 0
    s -= 1
    D.pop()

def CDES():
    global D, s
    if D[s-1] != D[s]:
        D[s-1] = 1
    else:
        D[s-1] = 0
    s -= 1
    D.pop()

def CPMI():
    global D, s
    if D[s-1] <= D[s]:
        D[s-1] = 1
    else:
        D[s-1] = 0
    s -= 1
    D.pop()

def CMAI():
    global D, s
    if D[s-1] >= D[s]:
        D[s-1] = 1
    else:
        D[s-1] = 0
    s -= 1
    D.pop()

def ARMZ(n):
    global D, s, varAddress
    D[varAddress[n]] = D[s]
    s -= 1
    D.pop()

def DSVI(p):
    global i
    i = p - 1

def DSVF(p):
    global i, s, D
    if D[s] == 0:
        i = p - 1
    s -= 1
    D.pop()

def LEIT():
    global s, D, readingsCount
    s += 1
    readingsCount += 1

    D.append(input("Digite o valor de entrada " + str(readingsCount) + ": "))

    if isInteger(D[s]):
        D[s] = int(D[s])
    else:
        D[s] = float(D[s])

def IMPR():
    global s, D
    print(D[s])
    s -= 1
    D.pop()

def ALME(m):
    global s, D, varAddress
    s = s + m
    D.append(0)
    varAddress.append(s)

def INPP():
    global s
    s = -1

def PARA():
    exit()

def PARAM(n):
    global s, D, varAddress
    s += 1
    D.append(0)
    D[s] = D[varAddress[n]]
    varAddress.append(s)

def PUSHER(e):
    global s, D
    s += 1
    D.append(0)
    D[s] = e

def CHPR(p):
    global i
    i = p - 1

def DESM(m):
    global s, D, varAddress
    s = s - m
    for j in range(m):
        D.pop()
        varAddress.pop()

def RTPR():
    global i, s, D
    i = D[s]
    i = i - 1
    s -= 1
    D.pop()

def runHypMachine():
    global i

    generateHypMachine()

    hypotheticalMachineCodeFile = open(os.path.join(os.path.dirname(sys.argv[0]), 'GeneratedFiles/hypotheticalMachineCode.txt'), "r")
    hypotheticalMachineCodeFile = hypotheticalMachineCodeFile.readlines()

    for j in range(len(hypotheticalMachineCodeFile)):
        instruction = hypotheticalMachineCodeFile[j].replace("\n","")
        instruction = instruction.split(" ")
        C.append(instruction)

    while i < len(C):

        command = C[i][0]
        if len(C[i]) != 1:
            command = C[i][0]
            if (isInteger(C[i][1])):
                value = int(C[i][1])
            else:
                value = float(C[i][1])

        if command == "CRCT":
            CRCT(value)
        elif command == "CRVL":
            CRVL(value)
        elif command == "SOMA":
            SOMA()
        elif command == "SUBT":
            SUBT()
        elif command == "MULT":
            MULT()
        elif command == "DIVI":
            DIVI()
        elif command == "INVE":
            INVE()
        elif command == "CPME":
            CPME()
        elif command == "CPMA":
            CPMA()
        elif command == "CPIG":
            CPIG()
        elif command == "CDES":
            CDES()
        elif command == "CPMI":
            CPMI()
        elif command == "CMAI":
            CMAI()
        elif command == "ARMZ":
            ARMZ(value)
        elif command == "DSVI":
            DSVI(value)
        elif command == "DSVF":
            DSVF(value)
        elif command == "LEIT":
            LEIT()
        elif command == "IMPR":
            IMPR()
        elif command == "ALME":
            ALME(value)
        elif command == "INPP":
            INPP()
        elif command == "PARA":
            PARA()
        elif command == "PARAM":
            PARAM(value)
        elif command == "PUSHER":
            PUSHER(value)
        elif command == "CHPR":
            CHPR(value)
        elif command == "DESM":
            DESM(value)
        elif command == "RTPR":
            RTPR()
        else:
            print("Error: unknown instruction")
            exit()

        i += 1