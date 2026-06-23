#include "stack.h"

// Define a constant for stack size. Didn't define it in stack.h as nothing outside of this file needs to know the max stack size
#define STACK_SIZE 256

// Create the stack and the stack pointer. -1 stack pointer means the stack is empty
static int stack[256];
static int sp = -1;

// Definition of stack_init
void stack_init(){

    // Just set the stack pointer to -1 to reset the stack
    sp = -1;

}

// Definition of stack_push
int stack_push(int value){

    // First, check for overflow, return -1 if so
    if (sp >= STACK_SIZE - 1){
        return -1;
    }

    // Otherwise, increment the pointer and write the value
    sp++;
    stack[sp] = value;

    // Last, return 0
    return 0;

}

// Definition of stack_pop
int stack_pop(int *out){

    // First, check for underflow, return -1 if so
    if (sp < 0){
        return -1;
    }

    // Next, ensure that out is not null. If it isn't, pass the value pointed to by the stack pointer to it
    if (out != NULL){
        *out = stack[sp];
    }

    // Decrease the pointer
    sp--;

    // Last, return 0
    return 0;

}

// Definition of stack_depth
int stack_depth(){

    // Simply return sp + 1
    return sp + 1;

}