#ifndef STACK_H
#define STACK_H

// Function headers
// stack_init
void stack_init();

// stack_push
int stack_push(int value);

// stack_pop
int stack_pop(int *out);

// stack_depth
int stack_depth();

// stack_get
int stack_get(int index);

// End definition
#endif