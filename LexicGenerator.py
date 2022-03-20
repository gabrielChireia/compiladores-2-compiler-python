import os, sys

def lexic():
    fileToRun = open(os.path.join(os.path.dirname(sys.argv[0]), "AVAFiles/correto.lalg-v2.txt"), "r")
    
    keys = []
    linesList = []
    isComment = False

    for line in fileToRun:
        linesList.append(len(keys) + 1)
        line = line.rstrip()
        i = 0
        fileSize = len(line)

        while i < fileSize:
            if isComment:
                j = i
                while (j < fileSize):
                    if (line[j] == "*" and line[j+1] == "/"):
                        isComment = False
                        break
                    elif (line[j] == "}"):
                        isComment = False
                        break
                    elif j + 1 == fileSize:
                        isComment = True
                        break
                    else:
                        j = j + 1
                if isComment:
                    i = j + 1
                else:    
                    i = j + 2
            elif ((line[i] >= "a" and line[i] <= "z") or (line[i] >= "A" and line[i] <= "Z")):
                j = i + 1
                k = line[i]
                while (j < fileSize):
                    if ((line[j] >= "a" and line[j] <= "z") or (line[j] >= "A" and line[j] <= "Z") or (line[j] >= "0" and line[j] <= "9")):
                        k = k + line[j]
                        j = j + 1
                    else:
                        break
                keys.append(" " + k)
                i = j
            elif (line[i] >= "0" and line[i] <= "9"):
                j = i + 1
                k = line[i]
                isFloat = False
                while (j < fileSize):
                    if (line[j] >= "0" and line[j] <= "9"):
                        k = k + line[j]
                        j = j + 1
                    elif (line[j] == "." and isFloat == False):
                        k = k + line[j]
                        j = j + 1
                        isFloat = True
                    else:
                        break
                keys.append(" " + k)
                i = j
            elif line[i] == ":" and line[i+1] == "=":
                keys.append(" :=")
                i = i + 2
            elif line[i] == "<" and line[i+1] == ">":
                keys.append(" <>")
                i = i + 2
            elif line[i] == ">" and line[i+1] == "=":
                keys.append(" >=")
                i = i + 2
            elif line[i] == "<" and line[i+1] == "=":
                keys.append(" <=")
                i = i + 2
            elif line[i] == "/" and line[i+1] == "*":
                j = i + 2
                if j + 1 >= fileSize:
                    isComment = True
                    break
                while (j < fileSize):
                    if (line[j] == "*" and line[j+1] == "/"):
                        break
                    elif j + 1 >= fileSize:
                        isComment = True
                        break
                    else:
                        j = j + 1
                if isComment:
                    i = j + 1
                else:    
                    i = j + 2
            elif line[i] == "{":
                j = i + 1
                if j + 1 >= fileSize:
                    isComment = True
                    break
                while (j < fileSize):
                    if (line[j] == "}"):
                        break
                    elif j + 1 >= fileSize:
                        isComment = True
                        break
                    else:
                        j = j + 1
                i = j + 1
            elif line[i] == "i" and line[i+1] == "n" and line[i+2] == "t" and line[i+3] == "e" \
                    and line[i+4] == "g" and line[i+5] == "e" and line[i+6] == "r":
                keys.append(" integer")
                i = i + 7
            elif line[i] == "r" and line[i+1] == "e" and line[i+2] == "a" and line[i+3] == "l":
                keys.append(" real")
                i = i + 4
            elif line[i] == "," or line[i] == ";" or line[i] == "+" or line[i] == ":" or line[i] == "(" or line[i] == ")" or line[i] == "*" or line[i] == "/" or line[i] == "-" or line[i] == ">" or line[i] == "<" or line[i] == "$" or line[i] == ".":
                keys.append(" " + line[i])
                i = i + 1
            elif line[i] == "i" and line[i+1] == "f":
                keys.append(" if")
                i = i + 2
            elif line[i] == "t" and line[i+1] == "h" and line[i+2] == "e" and line[i+3] == "n":
                keys.append(" then")
                i = i + 4
            elif line[i] == "w" and line[i+1] == "h" and line[i+2] == "i" and line[i+3] == "l" and line[i+4] == "e":
                keys.append(" while")
                i = i + 5
            elif line[i] == "d" and line[i+1] == "o":
                keys.append(" do")
                i = i + 2
            elif line[i] == "w" and line[i+1] == "r" and line[i+2] == "i" and line[i+3] == "t" and line[i+4] == "e":
                keys.append(" write")
                i = i + 5
            elif line[i] == "r" and line[i+1] == "e" and line[i+2] == "a" and line[i+3] == "d":
                keys.append(" read")
                i = i + 4
            elif line[i] == "e" and line[i+1] == "l" and line[i+2] == "s" and line[i+3] == "e":
                keys.append(" else")
                i = i + 4
            elif line[i] == "b" and line[i+1] == "e" and line[i+2] == "g" and line[i+3] == "i" and line[i+4] == "n":
                keys.append(" begin")
                i = i + 5
            elif line[i] == "e" and line[i+1] == "n" and line[i+2] == "d":
                keys.append(" end")
                i = i + 4
            elif line[i] == " ":
                i = i + 1
                continue
            else:
                print("Error: character " + line[i] + " not defined. Remove invalid tab identation.")
                exit()

    keys[0] = keys[0].replace(" ", "")

    syntacticLalgFile = open(os.path.join(os.path.dirname(sys.argv[0]), 'GeneratedFiles/syntacticLalg.txt'), "w")
    syntacticLalgFile.writelines(keys)
    syntacticLalgFile.close()

    fileToRun.close()