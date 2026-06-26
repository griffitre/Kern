#include "telemetry.h"
#include "memory.h"
#include "stack.h"
#include <time.h>
#include <stdio.h>

// Int to store the number of cycles
static int cycles;

// Clock to store the start time
static clock_t startTime;

// Int to store the final pc value
static int finalPc;

// Definition of telemetry_init
void telemetry_init(){

    // Set cycles to 0
    cycles = 0;

    startTime = clock();

}

// Definition of telemetry_tick
void telemetry_tick(){

    // Just increase the cycles by 1
    cycles++;

}

// Definition of telemetry_print
void telemetry_print(){

    // Get the end time
    clock_t endTime = clock();

    // Calculate the difference
    clock_t elapsedTime = endTime - startTime;

    // Convert it to a double
    double elapsedConverted = (double)elapsedTime / CLOCKS_PER_SEC;

    // Inform the user that what is being printed is the telemetry
    printf("\n----TELEMETRY----\n");

    // Print the number of cycles
    printf("Number of cycles: %d\n", cycles);

    // Print the elapsed time
    printf("Elapsed time: %.4f seconds\n", elapsedConverted);

    // Call stack_depth to get the stack depth and print it
    int sDepth = stack_depth();
    printf("Stack depth: %d\n", sDepth);

    // Print the contents of the stack, if applicable
    printf("Stack contents: ");
    if (sDepth == 0){
        printf("[(Empty)]\n");
    }
    else{
        printf("[");
        for (int i = 0; i < sDepth; i++){
            printf("%d", stack_get(i));
            if (i < sDepth - 1){
                printf(", ");
            }
        }
        printf("]\n");
    }

    // Print the final pc value
    printf("Final program counter value: %d\n", finalPc);

    // Call memory_dump to dump the ram, then print a new line right after
    memory_dump();
    printf("\n");

}

// Definition of telemetry_store_pc
void telemetry_store_pc(int pc){
    
    // Just set the finalPc int
    finalPc = pc;

}