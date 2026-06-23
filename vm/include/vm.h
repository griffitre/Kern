#ifndef VM_H
#define VM_H

#include <stdint.h>

int vm_run(uint8_t *bytecode, long size);

#endif