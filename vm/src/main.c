#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

// Main function
int main(int argc, char *argv[]){
    
    // Check if a file name was passed
    if (argc < 2){
        fprintf(stderr, "Usage: kern <file.bin>\n");
        return 1;
    }
    
    // Try to open the file
    FILE *inFile = fopen(argv[1], "rb");

    // If not found, return -1
    if (inFile == NULL){
        fprintf(stderr, "Error: file %s not found/could not be opened\n", argv[1]);
        return 1;
    }

    // Find out how long the file is and rewind the pointer
    fseek(inFile, 0, SEEK_END);
    long size = ftell(inFile);
    rewind(inFile);

    // Unsigned int array of size size to store the flat sequence of bytes
    uint8_t *buffer = malloc(size);

    // Make sure it was allocated. If not, inform the user and close the file
    if (buffer == NULL){
        fprintf(stderr, "Error: could not allocate memory\n");
        fclose(inFile);
        return 1;
    }

    // Use size to read from the file size times
    fread(buffer, 1, size, inFile);

    // TODO: init memory, stack, telemetry
    // TODO: vm_run(buffer, size)
    // TODO: print telemtry

    // Free the buffer
    free(buffer);

    // Close the file
    fclose(inFile);

    // Return 0
    return 0;
}