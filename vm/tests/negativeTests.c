#include "vm.h"
#include "stack.h"
#include "memory.h"
#include "telemetry.h"
#include "opcodes.h"
#include "errors.h"
#include <check.h>
#include <stdlib.h>

// Setup function. Just initializes memory, stack, and telemetry
void setup(){
    memory_init();
    stack_init();
    telemetry_init();
}

// Teardown function
void teardown(){
    // Nothing is needed for this as the setup function handles resetting (tearing down) everything that needs to be reset
}


// Test cases
// Test 1: halt (yea just a halt operation thats it)
START_TEST(test_halt){

    // Make a program with just halt
    uint8_t program[] = {OP_HALT};

    // Ensure vm_run returns KERN_OK
    ck_assert_int_eq(vm_run(program, 1), KERN_OK);

}END_TEST

// Test 2: stack overflow
START_TEST(test_stackoverflow){

    // Make the program big enough for 257 push operations and a single halt operation
    uint8_t program[257 * 2 + 1];

    // Create an int i to store the index of the end of the push operations
    int i;

    // Add the 257 pushes to the program
    for (i = 0; i < 257 * 2; i += 2){
        program[i] = OP_PUSH;
        program[i + 1] = 0x01;
    }

    // Add a halt to the end
    program[i] = OP_HALT;

    // Ensure vm_run returns KERN_ERR_STACKOVERFLOW
    ck_assert_int_eq(vm_run(program, sizeof(program)), KERN_ERR_STACKOVERFLOW);

}END_TEST

// Test 3: stack underflow
START_TEST(test_stackunderflow){

    // Make a program that just pops immediately then halts
    uint8_t program[] = {OP_POP, OP_HALT};

    // Ensure vm_run returns KERN_ERR_STACKUNDERFLOW
    ck_assert_int_eq(vm_run(program, 2), KERN_ERR_STACKUNDERFLOW);

}END_TEST

// Test 4: memory out of bounds when running memory_store
START_TEST(test_oob_memory_store){

    // Try to store to a memory address thats out of bounds and ensure that memory_store returns -1
    ck_assert_int_eq(memory_store(256, 1), -1);

}END_TEST

// Test 5: memory out of bounds when running memory_load
START_TEST(test_oob_memory_load){

    // uint8_t to store the loaded value to (required to compile)
    uint8_t loadedValue;

    // Try to load from a memory address thats out of bounds and ensure that memory_load returns -1
    ck_assert_int_eq(memory_load(256, &loadedValue), -1);

}END_TEST

// Test 6: program counter out of bounds from jmp operation
START_TEST(test_oob_pc_jump){

    // Make a program that tries to jump to a value larger than the size of the program
    uint8_t program[] = {OP_JMP, 4, OP_HALT};

    // Ensure vm_run returns KERN_ERR_OOB_PC
    ck_assert_int_eq(vm_run(program, 3), KERN_ERR_OOB_PC);

}END_TEST

// Test 7: program counter out of bounds from jmp_if_zero operation
START_TEST(test_oob_pc_jump_zero){

    // Make a program that tries to jump to a value larger than the size of the program
    uint8_t program[] = {OP_PUSH, 0, OP_JMP_IF_ZERO, 6, OP_HALT};

    // Ensure vm_run returns KERN_ERR_OOB_PC
    ck_assert_int_eq(vm_run(program, 5), KERN_ERR_OOB_PC);

}END_TEST

// Test 8: invalid opcode
START_TEST(test_invalid_opcode){

    // Make a program with invalid opcode (the 0x20)
    uint8_t program[] = {OP_PUSH, 2, 0x20, OP_HALT};

    // Ensure vm_run returns KERN_ERR_INVALID_OPCODE
    ck_assert_int_eq(vm_run(program, 4), KERN_ERR_INVALID_OPCODE);

}END_TEST

// Test 9: divide by 0
START_TEST(test_div_zero){

    // Make a program that divides by 0
    uint8_t program[] = {OP_PUSH, 2, OP_PUSH, 0, OP_DIV, OP_HALT};

    // Ensure vm_run returns KERN_ERR_DIV_ZERO
    ck_assert_int_eq(vm_run(program, 6), KERN_ERR_DIV_ZERO);

}END_TEST


// Create the test suite
Suite *vmSuite(){

    // Define the suite and tc
    Suite *s = suite_create("VM");
    TCase *tc = tcase_create("Main");

    // Register the setup and teardown functions to run before/after every test
    tcase_add_checked_fixture(tc, setup, teardown);

    // Add tests
    tcase_add_test(tc, test_halt);
    tcase_add_test(tc, test_stackoverflow);
    tcase_add_test(tc, test_stackunderflow);
    tcase_add_test(tc, test_oob_memory_store);
    tcase_add_test(tc, test_oob_memory_load);
    tcase_add_test(tc, test_oob_pc_jump);
    tcase_add_test(tc, test_oob_pc_jump_zero);
    tcase_add_test(tc, test_invalid_opcode);
    tcase_add_test(tc, test_div_zero);

    // Add the tc to the suite
    suite_add_tcase(s, tc);

    // Return the suite
    return s;

}