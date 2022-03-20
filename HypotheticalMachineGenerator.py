import os, sys
from LexicGenerator import *

lexic()

category = ""
deviation = ""
operatorType = ""
commandType = ""
procedureType = ""

firstPosition = 0
lastPosition = 0
parameterCount = 0
deviationPosition = 0
positionDSVI = 0
procedureDSVI = 0
positionDSVF = 0
positionPUSHER = 0
counterDESM = 0

symbolTable = []
procedures = []
typeVerification = []
commandTypeVerification = []
parametersTypeVerification = []
proceduresList = []
variables = []
codeArea = []

isCommand = False
isParameter = False
isProcedure = False

scope = {"ID" : "", "firstPosition": 0}

syntacticLalgFile = open(os.path.join(os.path.dirname(sys.argv[0]), "GeneratedFiles/syntacticLalg.txt"), "r")
keys = syntacticLalgFile.read().split(" ")

def programa(key, position):
    global codeArea
    if key == "program":
        codeArea.append("INPP")
        key, position = nextSymbol(position)
        if isID(key):
            addProgramNameToSymbolTable(key)
            key, position = nextSymbol(position)
            key, position = corpo(key, position)
            if key == ".":
                codeArea.append("PARA")
            else:
                print("Error: invalid last key @programa")
                exit()
        else:
            print("Error: invalid ID @programa")
            exit()
    else:
        print("Error: invalid first @programa")
        exit()

def corpo(key, position):
    key, position = dc(key, position)
    if key == "begin":
        key, position = nextSymbol(position)
        key, position = comandos(key, position)
        if key == "end":
            key, position = nextSymbol(position)
            return (key, position)
        else:
            print("Error: invalid end key @corpo")
            exit()
    else:
        print("Error: invalid begin key @corpo")
        exit()

def dc(key, position):
    if key == "real" or key == "integer":
        key, position = dc_v(key, position)
        key, position = mais_dc(key, position)
        return (key, position)
    elif key == "procedure":
        key, position = dc_p(key, position)
        return (key, position)
    elif key == "begin":
        return (key, position)
    else:
        print("Error: invalid key @dc")
        exit()

def mais_dc(key, position):
    if key == ";":
        key, position = nextSymbol(position)
        key, position = dc(key, position)
        return (key, position)
    elif key == "begin":
        return (key, position)
    else:
        print("Error: invalid key @mais_dc")
        exit()

def dc_v(key, position):
    if key == "real" or key == "integer":
        global category
        category = "var"
        keyType = key
        key, position = nextSymbol(position)
        if key == ":":
            key, position = nextSymbol(position)
            key, position = variaveis(key, position)
            addTypeToSymbolTable(keyType)
            return (key, position)
        else:
            print("Error: invalid : key @dc_v")
            exit()     
    else:
        print("Error: invalid category @dc_v")
        exit()

def variaveis(key, position):
    if isID(key):
        global category, isCommand, codeArea, commandType, counterDESM, isProcedure, scope
        if (isCommand) and (not verifyVarExistence(key)):
            print("Error: variable does not exist @variaveis")
            exit()
        if isCommand:
            addToCommandTypeVerification(key)
            if commandType == "write":
                codeArea.append("CRVL %d" %(varPosition(key, scope)))
                codeArea.append("IMPR")
            elif commandType == "read":
                codeArea.append("LEIT")
                codeArea.append("ARMZ %d" %(varPosition(key, scope)))
            else:
                codeArea.append("ARMZ %d" %(varPosition(key, scope)))
        if not isCommand and category != "param":
            codeArea.append("ALME 1")
        if not isCommand and isProcedure:
            counterDESM += 1
        addVarToSymbolTable(key, category)
        key, position = nextSymbol(position)
        key, position = mais_var(key, position)
        return (key, position)
    else:
        print("Error: invalid key @variaveis")
        exit()

def mais_var(key, position):
    if key == ",":
        key, position = nextSymbol(position)
        key, position = variaveis(key, position)
        return (key, position)
    elif key == ";" or key == ")" or key == "begin":
        return (key, position)
    else:
        print("Error: invalid key @mais_var")
        exit()

def dc_p(key, position):
    if key == "procedure":
        key, position = nextSymbol(position)
        if isID(key):
            global codeArea, procedureDSVI, isProcedure, proceduresList
            isProcedure = True
            codeArea.append("DSVI")
            procedureDSVI = len(codeArea)-1
            proceduresList.append({"ID": key, 'LinhaInicioCod': procedureDSVI+1})
            addProgramNameToSymbolTable(key)
            key, position = nextSymbol(position)
            key, position = parametros(key, position)
            key, position = corpo_p(key, position)
            return (key, position)
        else:
            print("Error: invalid variable @dc_p")
            exit() 
    else:
        print("Error: invalid key @dc_p")
        exit() 
    
def parametros(key, position):
    if key == "(":
        global category
        category = "param"
        key, position = nextSymbol(position)

        if key == "real" or key == "integer":
            keyType = key
            key, position = nextSymbol(position)
            key, position = lista_par(key, position, keyType)

        if key == ")":
            key, position = nextSymbol(position)
            return (key, position)
        else:
            print("Error: invalid ending key @parametros")
            exit() 
    elif key == "real" or key == "integer" or key == "begin":
        return (key, position)
    else:
        print("Error: invalid starting key @parametros")
        exit()

def lista_par(key, position, keyType):
    if key == ":":
        key, position = nextSymbol(position)
        key, position = variaveis(key, position)
        addTypeToSymbolTable(keyType)

        key, position = mais_par(key, position)
        return (key, position)
    else:
        print("Error: invalid key @lista_par")
        exit() 

def mais_par(key, position):
    if key == ";":
        key, position = nextSymbol(position)

        if key == "real" or key == "integer":
            keyType = key

        key, position = nextSymbol(position)
        key, position = lista_par(key, position, keyType)
        return (key, position)
    elif key == ")":
        return (key, position)
    else:
        print("Error: invalid key @mais_par")
        exit() 

def corpo_p(key, position):
    key, position = dc_loc(key, position)
    if key == "begin":
        key, position = nextSymbol(position)
        key, position = comandos(key, position)
        if key == "end":
            global codeArea, procedureDSVI, counterDESM, isProcedure
            codeArea.append("DESM %d" %(counterDESM))
            codeArea.append("RTPR")
            codeArea[procedureDSVI] = "DSVI %d" %(len(codeArea))
            counterDESM = 0
            isProcedure = False
            restartRange()
            key, position = nextSymbol(position)
            return (key, position)
        else:
            print("Error: invalid ending key @corpo_p")
            exit() 
    else:
        print("Error: invalid starting key @corpo_p")
        exit() 

def dc_loc(key, position):
    if key == "real" or key == "integer":
        key, position = dc_v(key, position)
        key, position = mais_dcloc(key, position)
        return (key, position)
    elif key == "begin":
        return (key, position)
    else:
        print("Error: invalid key @dc_loc")
        exit() 

def mais_dcloc(key, position):
    if key == ";":
        key, position = nextSymbol(position)
        key, position = dc_loc(key, position)
        return (key, position)
    elif key == "begin":
        return (key, position)
    else:
        print("Error: invalid key @mais_dcloc")
        exit() 

def lista_arg(key, position):
    if key == "(":
        key, position = nextSymbol(position)
        key, position = argumentos(key, position)
        if key == ")":
            key, position = nextSymbol(position)
            return (key, position)
        else:
            print("Error: invalid arguments ending key @lista_arg")
            exit() 
    elif key == "end" or key == ";" or key == "else" or key == "$":
        return (key, position)
    else:
        print("Error: invalid arguments starting key @lista_arg")
        exit() 

def argumentos(key, position):
    if isID(key):
        global isParameter, codeArea, scope
        if not verifyVarExistence(key):
            print("Error: variable not set @argumentos")
            exit()
        if isParameter:
            addParametersToSymbolTable(key)
            codeArea.append("PARAM %d" %(varPosition(key, scope)))
        if not isParameter:
            addKeyToSymbolTable(key)
        key, position = nextSymbol(position)
        key, position = mais_ident(key, position)
        return (key, position)
    else:
        print("Error: invalid key @argumentos")
        exit() 

def mais_ident(key, position):
    if key == ";" or key == ",":
        key, position = nextSymbol(position)
        key, position = argumentos(key, position)
        return (key, position)
    elif key == ")":
        global codeArea, positionPUSHER, procedureType, proceduresList
        codeArea.append("CHPR %d" %(startProcedures(procedureType)))
        codeArea[positionPUSHER] = "PUSHER %d" %(len(codeArea))
        verifyParametersType()
        return (key, position)
    else:
        print("Error: invalid key @mais_ident")
        exit()

def comandos(key, position):
    key, position = comando(key, position)
    key, position = mais_comandos(key, position)
    return (key, position)

def mais_comandos(key, position):
    if key == ";":
        key, position = nextSymbol(position)
        key, position = comandos(key, position)
        return (key, position)
    elif key == "end" or key == "else" or key == "$":
        return (key, position)
    else:
        print("Error: invalid key @mais_comandos")
        exit() 

def comando(key, position):
    global isCommand, commandTypeVerification, codeArea, deviation, commandType, deviationPosition, positionDSVF, positionDSVI
    if key == "read" or key == "write":
        commandType = key
        key, position = nextSymbol(position)
        if key == "(":
            key, position = nextSymbol(position)
            isCommand = True
            key, position = variaveis(key, position)
            verifyCommandType()
            isCommand = False
            if key == ")":
                key, position = nextSymbol(position)
                return (key, position)
            else:
                print("Error: invalid command ending key @comando")
                exit() 
        else:
            print("Error: invalid command starting key @comando")
            exit()
    elif key == "if":
        deviation = key
        deviationPosition = len(codeArea)
        key, position = nextSymbol(position)
        key, position = condicao(key, position)
        if key == "then":
            codeArea.append("DSVF ")
            positionDSVF = len(codeArea)-1
            key, position = nextSymbol(position)
            key, position = comandos(key, position)
            key, position = pfalsa(key, position)
            if key == "$":
                codeArea[positionDSVI] = ("DSVI %d" %(len(codeArea)))
                deviation = ""
                key, position = nextSymbol(position)
                return (key, position)
            else:
                print("Error: invalid ending key on 'if' @comando")
                exit() 
        else:
            print("Error: invalid starting key on 'if' @comando")
            exit() 
    elif key == "while":
        deviation = key
        deviationPosition = len(codeArea)
        key, position = nextSymbol(position)
        key, position = condicao(key, position)
        if key == "do":
            codeArea.append("DSVF ")
            positionDSVF = len(codeArea)-1
            key, position = nextSymbol(position)
            key, position = comandos(key, position)
            if key == "$":
                codeArea.append("DSVI %d" %(deviationPosition))
                codeArea[positionDSVF] = "DSVF %d" %(len(codeArea))
                deviation = ""
                key, position = nextSymbol(position)
                return (key, position)
            else:
                print("Error: invalid ending key on 'while' @comando")
                exit() 
        else:
            print("Error: invalid starting key on 'while' @comando")
            exit()
    elif isID(key):
        global isParameter, procedureType, positionPUSHER
        if (not verifyVarExistence(key)) and (not verifyProgramNameExistence(key)):
            print("Error: invalid ID @comando")
            exit()
        if (verifyProgramNameExistence(key)) and (not verifyVarExistence(key)):
            procedureType = key
            isParameter = True
            codeArea.append("PUSHER")
            positionPUSHER = (len(codeArea)-1)
        if not isParameter:
            addKeyToSymbolTable(key)
        key, position = nextSymbol(position)
        key, position = restoIdent(key, position)
        return (key, position)
    else:
        print("Error: invalid key @comando")
        exit() 

def restoIdent(key, position):
    if key == ":=":
        key, position = nextSymbol(position)
        key, position = expressao(key, position)
        return (key, position)
    elif key == "(" or key == "end" or key == ";" or key == "else" or key == "$":
        key, position = lista_arg(key, position)
        return (key, position)
    else:
        print("Error: invalid key @restoIdent")
        exit() 

def condicao(key, position):
    key, position = expressao(key, position)
    key, position = relacao(key, position)
    key, position = expressao(key, position)
    return (key, position)

def relacao(key, position):
    if key == "=" or key == "<>" or key == ">=" or key == "<=" or key == ">" or key == "<":
        global operatorType
        operatorType = key
        key, position = nextSymbol(position)
        return (key, position)
    else:
        print("Error: invalid key @relacao")
        exit() 

def expressao(key, position):
    key, position = termo(key, position)
    key, position = outros_termos(key, position)
    return (key, position) 

def termo(key, position):
    key, position = op_un(key, position)
    key, position = fator(key, position)
    key, position = mais_fatores(key, position)
    return (key, position)

def op_un(key, position):
    if key == "-":
        global operatorType
        operatorType = "INVE"
        key, position = nextSymbol(position)
        return (key, position)
    elif isID(key) or key == "(" or isInteger(key) or isReal(key):
        return (key, position)
    else:
        print("Error: invalid key @op_un")
        exit()

def fator(key, position):
    global codeArea, operatorType, scope
    if isID(key) or isInteger(key) or isReal(key):
        if (isID(key)) and (not verifyVarExistence(key)):
            print("Error: invalid ID @fator")
            exit()
        if isInteger(key) or isReal(key):
            codeArea.append("CRCT " + key)
            addNumberToSymbolTable(key)
        if isID(key):
            codeArea.append("CRVL %d" %(varPosition(key, scope)))
        if operatorType != "":
            addOperator()
        addKeyToSymbolTable(key)
        key, position = nextSymbol(position)
        return (key, position)
    elif key == "(":
        key, position = nextSymbol(position)
        key, position = expressao(key, position)
        if key == ")":
            key, position = nextSymbol(position)
            return (key, position)
        else:
            print("Error: invalid ending key @fator")
            exit() 
    else:
        print("Error: invalid key @fator")
        exit() 

def outros_termos(key, position):
    if isID(key) or key == "(" or key == "+" or key == "-" or isInteger(key) or isReal(key):
        key, position = op_ad(key, position)
        key, position = termo(key, position)
        key, position = outros_termos(key, position)
        return (key, position)
    elif key == "end" or key == ";" or key == key == ")" or key == "else" or key == "do" or key == "$" or key == "then" or key == "=" or key == "<>" or key == ">=" or key == "<=" or key == ">" or key == "<":
        global typeVerification, codeArea, variables, operatorType, scope
        if len(typeVerification) != 0:
            if not verifyKeyType(typeVerification):
                exit()
            if (len(variables) == 1) or ((len(variables) > 1) and (not isOperator(key))):
                codeArea.append("ARMZ %d" %(varPosition(variables[0], scope)))
                variables = []
                typeVerification = []
        return (key, position)
    else:
        print("Error: invalid key @outros_termos")
        exit()

def op_ad(key, position):
    if key == "+" or key == "-":
        global operatorType
        operatorType = key
        key, position = nextSymbol(position)
        return (key, position)
    else:
        print("Error: invalid key @op_ad")
        exit()

def mais_fatores(key, position):
    if key == "*" or key == "/":
        key, position = op_mul(key, position)
        key, position = fator(key, position)
        key, position = mais_fatores(key, position)
        return (key, position)
    elif key == "end" or key == ";" or key == ")" or key == "else" or key == "do" or key == "$" or key == "then" or key == "=" or key == "<>" or key == ">=" or key == "<=" or key == ">" or key == "<" or key == "+" or key == "-":
        global typeVerification, codeArea, variables, operatorType, deviation, scope
        if len(typeVerification) != 0:
            if not verifyKeyType(typeVerification):
                exit()
            if (len(variables) == 1) or ((len(variables) > 1) and (not isOperator(key))):
                if deviation == "":
                    codeArea.append("ARMZ %d" %(varPosition(variables[0], scope)))
                variables = []
                typeVerification = []
            elif (len(variables) > 1) and (isOperator(key)):
                operatorType = key
        return (key, position)
    else:
        print("Error: invalid key @mais_fatores")
        exit() 

def op_mul(key, position):
    if key == "*" or key == "/":
        global operatorType
        operatorType = key
        key, position = nextSymbol(position)
        return (key, position)
    else:
        print("Error: invalid key @op_mul")
        exit()

def pfalsa(key, position):
    if key == "else":
        global codeArea, positionDSVI, positionDSVF
        codeArea.append("DSVI")
        positionDSVI = len(codeArea)-1
        codeArea[positionDSVF] = ("DSVF %d" %(len(codeArea)))
        key, position = nextSymbol(position)
        key, position = comandos(key, position)
        return (key, position)
    elif key == "$":
        return (key, position)
    else:
        print("Error: invalid key @pfalsa")
        exit()

def nextSymbol(position):
    if position < len(keys)-1:
        return (keys[position + 1], position + 1)
    else:
        return ("#", position)

def isID(key):
    if key == "var" or key == "integer" or key == "real" or key == "if" or key == "then" or key == "do" or key == "(" or key == ")" or key == "*" or key == "/" or key == "+" or key == "-" or key == "<>" or key == ">=" or key == "<=" or key == ">" or key == "<" or key == "=" or key == "$" or key == "while" or key == "write" or key == "real" or key == ";" or key == "else" or key == "begin" or key == "end" or key == ":" or key == ",":
        return False
    elif (key[0] >= "a" and key[0] <= "z") or (key[0] >= "A" and key[0] <= "Z"):
        return True
    else:
        return False

def isInteger(key):
    try: 
        int(key)
        return True
    except ValueError:
        return False

def isReal(key):
    try: 
        float(key)
        return True
    except ValueError:
        return False

def addProgramNameToSymbolTable(key):
    global firstPosition, lastPosition, symbolTable, scope, procedures
    
    procedureData = []

    if verifyProgramNameExistence(key):
        print("Error: unable to add name key")
        exit()

    procedureData.append(key)

    content = {"ID": key, "Key": "ID", "Category": "Name", "Type": "", "Value": ""}
    scope = {"ID": key, "firstPosition": lastPosition}
    lastPosition += 1
    firstPosition = lastPosition
    symbolTable.append(content)
    procedures.append(procedureData)

def verifyProgramNameExistence(key):
    global procedures

    for i in range(1, len(procedures)):
        if procedures[i][0] == key:
            return True
    return False

def addVarToSymbolTable(key, category):
    global lastPosition, symbolTable, isCommand, scope

    if isCommand:
        return

    if verifyVarExistence(key):
        print("Error: unable to add var key")
        exit()

    lastPosition += 1
    content = {"ID": key, "Key": "ID", "Category": category, "Type": "NULL", "Value": ""}
    symbolTable.append(content)

def verifyVarExistence(key):
    global symbolTable, scope

    for i in range(scope["firstPosition"], len(symbolTable)):
        if symbolTable[i]["ID"] == key:
            return True
    return False

def varPosition(key, scope):
    global symbolTable
    rangeFirstPosition = scope["firstPosition"]

    pos = -1
    for i in range(1, len(symbolTable)):
        pos += 1
        if (symbolTable[i]["ID"] == key) and (i >= rangeFirstPosition):
            return pos
        if (symbolTable[i]["Category"] == "Name"):
            pos -= 1

def addNumberToSymbolTable(key):
    global lastPosition, symbolTable

    if verifyNumberExistence(key):
        return

    type = ""
    if isReal(key) and isInteger(key):
        type = "integer"
    elif not isInteger(key):
        type = "real"

    lastPosition += 1
    content = {"ID": key, "Key": "Number", "Category": "", "Type": type, "Value": key}
    symbolTable.append(content)

def verifyNumberExistence(key):
    global symbolTable, scope

    for i in range(scope["firstPosition"], len(symbolTable)):
        if i != scope["firstPosition"]:
            if symbolTable[i]["ID"] == key:
                if isInteger(key) and isReal(key):
                    return True
    return False

def addParameters(key):
    global procedures
    aux = []

    aux.extend(procedures[len(procedures)-1])
    if len(aux) == 1:
        aux.append(1)
    else:
        aux[1] = len(aux) - 1
    aux.append(key)
    procedures.pop()
    procedures.append(aux)

    return

def addTypeToSymbolTable(type):
    global firstPosition, lastPosition, symbolTable

    for i in range(firstPosition, lastPosition):
        symbolTable[i]["Type"] = type
        if symbolTable[i]["Category"] == "param":
            addParameters(type)

    firstPosition = lastPosition
    
def addParametersToSymbolTable(key):
    global symbolTable, parameterCount, parametersTypeVerification

    parameterCount += 1
    for i in range(1, len(symbolTable)):
        if symbolTable[i]["ID"] == key:
            parametersTypeVerification.append(symbolTable[i]["Type"])

def verifyParametersType():
    global procedures, parameterCount, isParameter, procedureType, parametersTypeVerification

    for i in range(len(procedures)):
        if procedures[i][0] == procedureType: 
            if procedures[i][1] != parameterCount:
                print("Error: parameters and procedures values does not match")
                exit()
            proceduresCopy = []
            proceduresCopy.extend(procedures[i])
            for j in range(2, len(proceduresCopy)):
                if proceduresCopy[j] != parametersTypeVerification[j-2]:
                    print("Error: parameters and procedures names does not match")
                    exit()

    isParameter = False
    parameterCount = 0
    procedureType = ""
    parametersTypeVerification = []

def addKeyToSymbolTable(key):
    global typeVerification, symbolTable, scope, variables
    
    variables.append(key)
    if isID(key):
        for i in range(scope["firstPosition"]+1, len(symbolTable)):
            if symbolTable[i]["ID"] == key:
                typeVerification.append(symbolTable[i]["Type"])
                break
    elif isReal(key) and isInteger(key):
        typeVerification.append("integer")
    elif not isInteger(key):
        typeVerification.append("real")

def verifyKeyType(typeVerification):
    global variables
    type = typeVerification[0]

    if type == "real":
        return True
    else:
        for i in typeVerification:
            if i != type:
                print("Error: types does not match")
                return False
        return True

def addToCommandTypeVerification(key):
    global commandTypeVerification, symbolTable, scope

    if isID(key):
        for i in range(scope["firstPosition"]+1, len(symbolTable)):
            if symbolTable[i]["ID"] == key:
                commandTypeVerification.append(symbolTable[i]["Type"])
                break
    elif isReal(key) and isInteger(key):
        commandTypeVerification.append("integer")
    elif not isInteger(key):
        commandTypeVerification.append("real")

def verifyCommandType():
    global commandTypeVerification
    type = commandTypeVerification[0]
    for i in commandTypeVerification:
        if i != type:
            print("Error: commands does not match")
            exit()
    commandTypeVerification = []
    return True

def restartRange():
    global scope, firstPosition, lastPosition, symbolTable

    for i in range(scope["firstPosition"], len(symbolTable)):
        symbolTable.pop()
    firstPosition = scope["firstPosition"]
    lastPosition = firstPosition
    scope = {"ID": symbolTable[0]["ID"], "firstPosition": 0}

def addOperator():
    global operatorType, codeArea

    if operatorType == "+":
        codeArea.append("SOMA")
    elif operatorType == "-":
        codeArea.append("SUBT")
    elif operatorType == "*":
        codeArea.append("MULT")
    elif operatorType == "/":
        codeArea.append("DIVI")
    elif operatorType == "<":
        codeArea.append("CPME")
    elif operatorType == ">":
        codeArea.append("CPMA")
    elif operatorType == "=":
        codeArea.append("CPIG")
    elif operatorType == "<>":
        codeArea.append("CDES")
    elif operatorType == "<=":
        codeArea.append("CPMI")
    elif operatorType == ">=":
        codeArea.append("CMAI")
    elif operatorType == "INVE":
        codeArea.append("INVE")

    operatorType = ""

def isOperator(key):
    if key == "*" or key == "/" or key == "+" or key == "-" or key == "<>" or key == ">=" or key == "<=" or key == ">" or key == "<" or key == "=":
        return True
    else:
        return False

def startProcedures(key):
    global proceduresList

    for i in range(len(proceduresList)):
        if proceduresList[i]["ID"] == key:
            return proceduresList[i]['LinhaInicioCod']

def generateHypMachine():
    programa(keys[0], 0)

    hypotheticalMachineCodeFile = open(os.path.join(os.path.dirname(sys.argv[0]), 'GeneratedFiles/hypotheticalMachineCode.txt'), "w")
    for i in range(len(codeArea)):
        hypotheticalMachineCodeFile.write(codeArea[i] + "\n")
    hypotheticalMachineCodeFile.close()

syntacticLalgFile.close()