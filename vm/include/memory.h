#ifndef MEMORY_H
#define MEMORY_H

// Include stdint
#include <stdint.h>

// Define a constant for the ram size
#define RAM_SIZE 256

// Function headers
// memory_init
void memory_init();

// memory_store
int memory_store(uint8_t addr, uint8_t value);

// memory_load
int memory_load(uint8_t addr, uint8_t *out);

// memory_dump
void memory_dump();

// End definition
#endif