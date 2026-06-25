import sys

# Opcode lookup table
opcodes = {
    "PUSH": 0x01,
    "POP": 0x02,
    "ADD": 0x03,
    "SUB": 0x04,
    "MUL": 0x05,
    "DIV": 0x06,
    "STORE": 0x07,
    "LOAD": 0x08,
    "JMP": 0x09,
    "JMP_IF_ZERO": 0x0A,
    "PRINT": 0x0B,
    "HALT": 0xFF
}

# A set that keeps track of which opcodes have operands. Used for first pass calculating the location of labels for jump operations
operand_opcodes = {"PUSH", "STORE", "LOAD", "JMP", "JMP_IF_ZERO"}

# Symbol table for labels
symbols = {}

# Function to tokenize
def tokenize(source):

    # Split the source by newlines
    lines = source.split("\n")

    # Create a list to store the tokenized command lists and a list to construct the tokenized command lists that will be sent to returnList
    returnList = []
    loopList = []

    # Loop through the lines list
    for line in lines:

        # Strip comments
        line = line.split(";")[0]
        
        # Strip leading and trailing whitespace
        line = line.strip()

        # Ensure that there is actually content on said line. If not, skip over the rest of this loop
        if not line:
            continue

        # Make the string all uppercase to remove case-sensitivity
        line = line.upper()
        
        # Split the stripped line using split and store to loopList
        loopList = line.split()

        # Add loop list to returnList
        returnList.append(loopList)

    # Return returnList
    return returnList

# Function to find labels
def first_pass(tokens):
    
    # Int to store total byte count
    byteSum = 0

    # Loop through the passed tokens list
    for token in tokens:

        # If the token is a label (i.e. has a : in it), add it to the dict with current bytesum value
        if token[0].endswith(":"):

            # Strip the colon
            labelName = token[0][:-1]

            # Store to symbols
            symbols[labelName] = byteSum

            # Skip over the remaining loop
            continue
        
        # Check if the token is in the opcodes with an operand, and increase byteSum accordingly
        if token[0] in operand_opcodes:
            byteSum += 2
        else:
            byteSum += 1

# Function to emit bytes (converted opcode/operands)
def second_pass(tokens):
    
    # Create a list to store the converted opcode
    returnList = []

    # Go through the passed tokens array and convert everything that can/should be converted
    for token in tokens:

        # Check if the token is a label, skip over it if so
        if token[0].endswith(":"):
            continue

        # Check if opcode is unrecognized
        if (token[0] not in opcodes):
            print("Unrecognized opcode: " + token[0])
            sys.exit(1)

        # Checks involving opcodes that need operands
        if token[0] in operand_opcodes:

            # Check if an operand is not given
            if len(token) == 1:
                print("Operand not given for opcode: " + token[0])
                sys.exit(1)

            # Check if an operand is greater than 255
            if token[1].isdigit() and int(token[1]) > 255:
                print("Operand value should not be greater than 255")
                sys.exit(1)

        # Convert the bytes
        # For opcode with no operand, just convert it to the bytes and add it to returnList
        if len(token) == 1:
            returnList.append(opcodes[token[0]])

        # For opcode that needs an operand, convert it and then convert the operand (convert the operand if needed, like if its a label)
        elif len(token) == 2:

            # Check if the operand is a label. If it is, convert it and add the operand and the converted value to returnList
            if token[1] in symbols:
                returnList.append(opcodes[token[0]])
                returnList.append(symbols[token[1]])

            # Otherwise, just add the converted opcode and the value
            else:
                returnList.append(opcodes[token[0]])
                returnList.append(int(token[1]))

        # Otherwise, inform that they cant have more than 1 opcode and 1 operand per line
        else:
            print("No more than 1 opcode and 1 operand per line")
            sys.exit(1)

    # Return the list
    return returnList

# Function to convert the list of emitted bytes to a .bin file for the VM
def write_bin(bytecode, outputPath):
    with open(outputPath, "wb") as outFile:
        outFile.write(bytes(bytecode))

def main():

    # Ensure that a file was passed. If not, exit
    if len(sys.argv) < 2:
        print("Usage: python3 assembler.py <file.krn>")
        sys.exit(1)

    # Get the passed file name
    passedName = sys.argv[1]

    # Ensure a .krn file was passed. If not, exit
    if not passedName.endswith(".krn"):
        sys.exit(1)
    
    # Open + read the file
    with open(passedName, "r") as inFile:
        fileContent = inFile.read()

    # TODO: tokenize

    # TODO: first pass

    # TODO: second pass

    # TODO: write bin

    
# If name = main, run main
if __name__ == "__main__":
    main()
