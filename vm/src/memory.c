#include "memory.h"
#include <string.h>
#include <stdio.h>

// Define the ram array
static uint8_t ram[256];

// Definition of memory_init
void memory_init(){

    // Simply use memset to zero out the ram array
    memset(ram, 0, RAM_SIZE);

}

// Definition of memory_store
int memory_store(int addr, uint8_t value){

    // Do a bounds check first, return -1 if out of bounds
    if (addr >= RAM_SIZE){
        return -1;
    }

    // Then, write to the address
    ram[addr] = value;

    // Lastly, return 0
    return 0;

}

// Definition of memory_load
int memory_load(int addr, uint8_t *out){

    // Do a bounds check first, return -1 if out of bounds
    if (addr >= RAM_SIZE){
        return -1;
    }

    // Then, load the value from the address into the out pointer
    *out = ram[addr];

    return 0;

}

// Definition of memory_dump
void memory_dump(){

    // Just loop through the ram array and print every byte in hex format, adding a newline every 16 bytes
    for (int i = 0; i < RAM_SIZE; i++){

        // Print the row address at the start of each row
        if (i % 16 == 0){
            printf("0x%02X: ", i);
        }

        // Print a byte
        printf("%02X ", ram[i]);

        // Check if a newline should be printed (which it should be every 16 bytes)
        if ((i + 1) % 16 == 0){
            printf("\n");
        }
        
    }

}