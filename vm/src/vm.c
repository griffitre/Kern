#include "vm.h"
#include "stack.h"
#include "memory.h"
#include "telemetry.h"
#include "opcodes.h"
#include <stdio.h>

// Main run function
int vm_run(uint8_t *bytecode, long size){

    // Set pc to 0
    int pc = 0;

    // Unsigned 8 bit int to store opcode
    uint8_t opcode;

    // Values to push/store values to/from the stack
    int value1;
    int value2;

    // Unsigned 8 bit int to passed parameters in the bytecode, and another to store a loaded value
    uint8_t passedParameter;
    uint8_t loadedValue;

    // Run indefinitely
    while (1){

        // Do a bounds check on pc immediately. If it is out of bounds (only possible if no bytecode was given), return 1
        if (pc >= size){
            return 1;
        }

        // Fetch the opcode and increment the pc
        opcode = bytecode[pc];
        pc++;

        // Decode and execute.
        // All of the if/return things are just for if an operation fails, such as a stack pop or push failing, or an invalid operation, like dividing by 0
        switch (opcode){

            // Push operation
            case OP_PUSH:
                // Get the passed value (that is currently at the pc)
                passedParameter = bytecode[pc];
                
                // Increment pc
                pc++;

                // Push the value
                if (stack_push((int)passedParameter) < 0){
                    return 1;
                }

                // Break
                break;


            // Pop operation
            case OP_POP:
                // Just pop the top of the stack
                if (stack_pop(NULL) < 0){
                    return 1;
                }

                // Break
                break;


            // Add operation
            case OP_ADD:
                // Get the two values from the top of the stack
                if (stack_pop(&value1) < 0 || stack_pop(&value2) < 0){
                    return 1;
                }

                // Push the sum of the values
                if (stack_push(value1 + value2) < 0){
                    return 1;
                }

                // Break
                break;

            
            // Sub operation
            case OP_SUB:
                // Get the two values from the top of the stack
                if (stack_pop(&value1) < 0 || stack_pop(&value2) < 0){
                    return 1;
                }
                
                // Push the difference between them (by doing value2 - value1)
                if (stack_push(value2 - value1) < 0){
                    return 1;
                }

                // Break
                break;

            
            // Mul operation
            case OP_MUL:
                // Get the two values from the top of the stack
                if (stack_pop(&value1) < 0 || stack_pop(&value2) < 0){
                    return 1;
                }

                // Push their product
                if (stack_push(value1 * value2) < 0){
                    return 1;
                }

                // Break
                break;


            // Div operation
            case OP_DIV:
                // Get the two values from the top of the stack
                if (stack_pop(&value1) < 0 || stack_pop(&value2) < 0){
                    return 1;
                }

                // Check if the first value is zero and return 1 if it is
                if (value1 == 0){
                    return 1;
                }

                // Push their quotient
                if (stack_push(value2 / value1) < 0){
                    return 1;
                }

                // Break
                break;


            // Store operation
            case OP_STORE:
                // Get the value from the top of the stack
                if (stack_pop(&value1) < 0){
                    return 1;
                }

                // Get the passed address (that is currently at the pc)
                passedParameter = bytecode[pc];

                // Increment pc
                pc++;

                // Store the value to the address
                if (memory_store((int)passedParameter, (uint8_t)value1) < 0){
                    return 1;
                }

                // Break
                break;


            // Load operation
            case OP_LOAD:
                // Get the address passed (that is currently at the pc)
                passedParameter = bytecode[pc];

                // Increment pc
                pc++;

                // Load the value from the address
                if (memory_load((int)passedParameter, &loadedValue) < 0){
                    return 1;
                }

                // Push the value onto the stack
                if (stack_push((int)loadedValue) < 0){
                    return 1;
                }

                // Break
                break;

            
            // Jmp operation
            case OP_JMP:
                // Get the address passed (that is currently at the pc)
                passedParameter = bytecode[pc];

                // Increment the pc
                pc++;

                // Set the pc to the value passed
                pc = (int)passedParameter;

                // Break
                break;


            // Jmp if zero operation
            case OP_JMP_IF_ZERO:
                // Pop the top of the stack
                if (stack_pop(&value1) < 0){
                    return 1;
                }

                // Get the address passed (that is currently at the pc)
                passedParameter = bytecode[pc];

                // Increment the pc
                pc++;

                // Set the pc to the passed address if value1 = 0
                if (value1 == 0){
                    pc = (int)passedParameter;
                }

                // Break
                break;

            
            // Print operation
            case OP_PRINT:
                // Pop the top of the stack
                if (stack_pop(&value1) < 0){
                    return 1;
                }

                // Print it to stdout
                fprintf(stdout, "%d ", value1);

                // Break
                break;

            
            // Halt operation
            case OP_HALT:
                // Simply return 0
                return 0;

            
            // Default for invalid opcode. Return 1
            default:
                return 1;

        }

        // Update telemetry
        telemetry_tick();

    }

}