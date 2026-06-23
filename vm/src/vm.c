#include "vm.h"
#include "stack.h"
#include "memory.h"
#include "telemetry.h"
#include "opcodes.h"

// Main run function
int vm_run(uint8_t *bytecode, long size){

    // Set pc to 0
    int pc = 0;

    // Unsigned 8 bit int to store opcode
    uint8_t opcode;

    // Run indefinitely
    while (1){

        // Do a bounds check on pc immediately. If it is out of bounds (only possible if no bytecode was given), return 1
        if (pc >= size){
            return 1;
        }

        // Fetch the opcode and increment the pc
        opcode = bytecode[pc];
        pc++;

        // Decode and execute
        switch (opcode){

            case 1:

            case 2:

            case 3:

            // etc etc etc...

        }

        // Update telemetry
        // Tick

    }

}