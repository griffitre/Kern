import sys

# Opcode lookup table (TODO)
opcodes = {}

# Symbol table for labels (TODO)
symbols = {}

# Function to tokenize
def tokenize(source):
    pass #(TODO)

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
