#include "telemetry.h"
#include "memory.h"
#include "stack.h"
#include <time.h>
#include <stdio.h>

// Int to store the number of cycles
static int cycles;

// Clock to store the start time
static clock_t startTime;

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

    // Print the number of cycles
    printf("Number of cycles: %d\n", cycles);

    // Print the elapsed time
    printf("Elapsed time: %.4f seconds\n", elapsedConverted);

    // Call stack_depth to get the stack depth and print it
    int sDepth = stack_depth();
    printf("Stack depth: %d\n", sDepth);

    // Call memory_dump to dump the ram, then print a new line right after
    memory_dump();
    printf("\n");

}