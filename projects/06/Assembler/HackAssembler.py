CompTable = {
    "0"     :"0101010",
    "1"     :"0111111",
    "-1"    :"0111010",
    "D"     :"0001100",
    "A"     :"0110000",
    "!D"    :"0001101",
    "-D"    :"0001111",
    "-A"    :"0110011",
    "D+1"   :"0011111",
    "A+1"   :"0110111",
    "D-1"   :"0001110",
    "A-1"   :"0110010",
    "D+A"   :"0000010",
    "D-A"   :"0010011",
    "A-D"   :"0000111",
    "D&A"   :"0000000",
    "D|A"   :"0010101",
    "M"     :"1110000",
    "!M"    :"1110001",
    "-M"    :"1110011",
    "M+1"   :"1110111",
    "M-1"   :"1110010",
    "D+M"   :"1000010",
    "D-M"   :"1010011",
    "M-D"   :"1000111",
    "D&M"   :"1000000",
    "D|M"   :"1010101"
}

DestTable = {
    "M"     :"001",
    "D"     :"010",
    "MD"    :"011",
    "A"     :"100",
    "AM"    :"101",
    "AD"    :"110",
    "AMD"   :"111"
}

JumpTable = {
    "JGT"   :"001",
    "JEQ"   :"010",
    "JGE"   :"011",
    "JLT"   :"100",
    "JNE"   :"101",
    "JLE"   :"110",
    "JMP"   :"111"
}

SymbolTable = {
    "SP"    :"0",
    "LCL"   :"1",
    "ARG"   :"2",
    "THIS"  :"3",
    "THAT"  :"4",
    "R0"    :"0",
    "R1"    :"1",
    "R2"    :"2",
    "R3"    :"3",
    "R4"    :"4",
    "R5"    :"5",
    "R6"    :"6",
    "R7"    :"7",
    "R8"    :"8",
    "R9"    :"9",
    "R10"   :"10",
    "R11"   :"11",
    "R12"   :"12",
    "R13"   :"13",
    "R14"   :"14",
    "R15"   :"15",
    "SCREEN":"16384",
    "KBD"   :"24576"
}

variableSymbol_Value = 16

def isWhitespace(line):
    i=0
    while(i<len(line) and line[i]==' '):
        i=i+1
    # Blank line
    if i==len(line):
        return True
    # Comment
    elif line[i]=='/' and line[i+1]=='/':
        return True
    #EOL
    elif line[i]=='\n':
        return True

    else:
        return False

def decimalToBinary(n):
    return bin(n).replace("0b", "")

# Convert the supplied decimal string into n bit binary A instruction
def code_nbit_AInstr(decStrVal, n):
    value_int = int(decStrVal)
    value_bin = str(decimalToBinary(value_int))
    print("In Binary - ", value_bin)
    instruction = ""
    for i in range(n-len(value_bin)):
        instruction+='0'
    for i in range(len(value_bin)):
        instruction+=value_bin[i]
    print("Resulting Code - ", instruction)
    return instruction

def parse_AInstruction(line, index):
    global variableSymbol_Value
    A_value_str = ''
    tableVal = ''
    i=index
    while(i<len(line) and line[i]!='\n' and line[i]!=' '):
        A_value_str+=line[i]
        i+=1
    print(" A instruction value = ", A_value_str)
    
    
    if(A_value_str.isnumeric()):
        result = code_nbit_AInstr(A_value_str, 16) # We need 16 bit value
    else:
        # @Symbol
        # Check if symbol already present in symbol table   
        # If not, it's a variable - add it to the table
        try:
            tableVal = SymbolTable[A_value_str]
        except KeyError:
            tableVal = variableSymbol_Value
            SymbolTable[A_value_str] = tableVal
            variableSymbol_Value+=1
            print("Adding variable: ", A_value_str, " : ", tableVal)
        
        result = code_nbit_AInstr(tableVal, 16)
    return result

def destPresent(line, index):
    for i in range(index, len(line)):
        if(line[i]=="="):
            return True
    return False

def jumpPresent(line, index):
    for i in range(index, len(line)-1):
        if(line[i]==';' and line[i+1]!='\n'):
            return True
    return False

def getJumpIndex(line, index):
    for i in range(index, len(line)-1):
        if (line[i]==';' and line[i+1] != '\n'):
            return i+1
    return -1   # Should never return this

def getCompIndex(line, index):
    for i in range(index, len(line)):
        if(line[i]=="="):
            return i+1
    return index


def parseCompField(line, index):
    i = getCompIndex(line, index)
    comp=''
    while(i<len(line) and line[i]!=';' and line[i]!='\n' and line[i]!='/'):
        if line[i]!=' ':
            comp+=line[i]
        i+=1

    print("Comp field: ", comp)
    print("Comp Field Code", CompTable[comp])
    return CompTable[comp]

def parseDestField(line, index):
    dest=''
    i=index
    while(line[i]!='='):
        if(line[i]!=' '):
            dest+=line[i]
        i+=1
    print("Dest Field: ", dest)
    print("Dest Field Code: ", DestTable[dest])
    return DestTable[dest]

def parseJumpField(line, index):
    i=getJumpIndex(line, index)
    assert(i!=-1)
    jump = ''
    while(i<len(line) and line[i]!='\n' and line[i]!='/'):
        if(line[i]!=' '):
            jump+=line[i]
        i+=1
    print("Jump Field: ", jump)
    print("Jump Field Code: ", JumpTable[jump])
    return JumpTable[jump]


def parse_CInstruction(line, index):
    result = "111"
    result = result + parseCompField(line, index) 
    
    if destPresent(line, index) == True:
        result += parseDestField(line, index) 
    else:
        # No dest field
        result+="000"
    
    if jumpPresent(line, index) != False:
        result+=parseJumpField(line, index)
    else:
        result+="000"
    
    print("Resulting C instruction Code - ", result)
    return result
    



def parseLine(line):
    i=0
    result = ''
    while(line[i] == ' '):
        i+=1
    # A instruction
    if(line[i]=="@"):
        result = parse_AInstruction(line, i+1)
    
    else:
        # C Instruction
        result = parse_CInstruction(line, i)
    return result

# Opens source file, removes empty lines and returns list of lines
def processFile(fileName):
    srcFile = open(fileName, "r+")
    srcFileLineList = srcFile.readlines()
    fileLineList_nowhitespaces = []
    srcFile.close()
    
    for line in srcFileLineList:
        # Remove whitespaces and comments
        if(isWhitespace(line) == False):
            fileLineList_nowhitespaces.append(line)
    
    for line in fileLineList_nowhitespaces:
        print(line)
    return fileLineList_nowhitespaces

def getDestFileName(srcFileName):
    destFile = ''
    for i in range(len(srcFileName)-3):
        destFile+=srcFileName[i]
    destFile+="hack"
    print("Output File Name: ", destFile)
    return destFile

# Does input line have label declaration
def isLabel(line):
    i=0
    while(line[i]==' '):
        i+=1
    if line[i]=='(':
        return True
    return False

# Inserts the label declaration into the symbol table
def insertLabel(line, lineNumber):
    i=0
    label = ''
    while(line[i]!='('):
        i+=1
    i+=1
    while(line[i]!=')'):
        label+=line[i]
        i+=1
    
    SymbolTable[label] = lineNumber
    print("inserted ", label, " : ", SymbolTable[label], " into symbol table")

## First pass of the assembler
# Search for and add label symbols to the symbol table
def firstPass(fileLines):
    numSymbols=0
    
    for i in range(len(fileLines)):
        if(isLabel(fileLines[i])==True):
            insertLabel(fileLines[i], i-numSymbols)
            numSymbols+=1

## Input - source code file
## Generates binary code and writes .hack file
def assemble(srcFileName):
    fileLines = processFile(srcFileName)
    destFileName = getDestFileName(srcFileName)

    destFileObj = open(destFileName, "w+")
    
    ## Add label symbols to symbol table
    firstPass(fileLines)

    for line in fileLines:
        if(isLabel(line) == False):
            result = parseLine(line)
            destFileObj.write(result+'\n')
    destFileObj.close()

# fileLines = processFile("../add/Add.asm")
# fileName = "../max/Max.asm"
fileName = "../rect/Rect.asm"
# fileName = "../pong/Pong.asm"
assemble(fileName)
#parseLine(fileLines[10])

