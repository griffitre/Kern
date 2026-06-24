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

# Symbol table for labels (TODO)
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
    pass #(TODO)

# Function to emit bytes (opcode/operands)
def second_pass(tokens):
    pass #(TODO)

# Function to convert the list of emitted bytes to a .bin file for the VM
def write_bin(bytecode, outputPath):
    pass #(TODO)

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
