#include "vm.h"
#include "stack.h"
#include "memory.h"
#include "telemetry.h"
#include "opcodes.h"
#include "errors.h"
#include "positiveTests.h"
#include <stdlib.h>

// Setup function. Just initializes memory, stack, and telemetry
void setupPositive(){
    memory_init();
    stack_init();
    telemetry_init();
}

// Teardown function
void teardownPositive(){
    // Nothing is needed for this as the setup function handles resetting (tearing down) everything that needs to be reset
}


// Test cases
// Test 1: push a value, store it, load it back, and verify it is correct
START_TEST(test_store_load_roundtrip){

    // Push 42, store it to address 0, then halt
    uint8_t program[] = {OP_PUSH, 42, OP_STORE, 0, OP_HALT};
    vm_run(program, sizeof(program));

    // Load the value from address 0 and verify it is 42
    uint8_t loaded;
    memory_load(0, &loaded);
    ck_assert_int_eq(loaded, 42);

}END_TEST

// Test 2: add two values and verify the result
START_TEST(test_add){

    // Push 5 and 3, add them, store the result to address 0, then halt
    uint8_t program[] = {OP_PUSH, 5, OP_PUSH, 3, OP_ADD, OP_STORE, 0, OP_HALT};
    vm_run(program, sizeof(program));

    // Load the result from address 0 and verify it is 8
    uint8_t loaded;
    memory_load(0, &loaded);
    ck_assert_int_eq(loaded, 8);

}END_TEST

// Test 3: subtract two values and verify the result
START_TEST(test_sub){

    // Push 5 and 3, subtract them, store the result to address 0, then halt
    uint8_t program[] = {OP_PUSH, 5, OP_PUSH, 3, OP_SUB, OP_STORE, 0, OP_HALT};
    vm_run(program, sizeof(program));

    // Load the result from address 0 and verify it is 2
    uint8_t loaded;
    memory_load(0, &loaded);
    ck_assert_int_eq(loaded, 2);

}END_TEST

// Test 4: multiply two values and verify the result
START_TEST(test_mul){

    // Push 4 and 3, multiply them, store the result to address 0, then halt
    uint8_t program[] = {OP_PUSH, 4, OP_PUSH, 3, OP_MUL, OP_STORE, 0, OP_HALT};
    vm_run(program, sizeof(program));

    // Load the result from address 0 and verify it is 12
    uint8_t loaded;
    memory_load(0, &loaded);
    ck_assert_int_eq(loaded, 12);

}END_TEST

// Test 5: divide two values and verify the result
START_TEST(test_div){

    // Push 6 and 2, divide them, store the result to address 0, then halt
    uint8_t program[] = {OP_PUSH, 6, OP_PUSH, 2, OP_DIV, OP_STORE, 0, OP_HALT};
    vm_run(program, sizeof(program));

    // Load the result from address 0 and verify it is 3
    uint8_t loaded;
    memory_load(0, &loaded);
    ck_assert_int_eq(loaded, 3);

}END_TEST

// Test 6: verify that jmp skips instructions correctly
START_TEST(test_jmp){

    // Push 5, jump over the second push, store 5 to address 0, then halt
    uint8_t program[] = {OP_PUSH, 5, OP_JMP, 6, OP_PUSH, 99, OP_STORE, 0, OP_HALT};
    vm_run(program, sizeof(program));

    // Load the value from address 0 and verify it is 5 (not 99)
    uint8_t loaded;
    memory_load(0, &loaded);
    ck_assert_int_eq(loaded, 5);

}END_TEST

// Test 7: verify that jmp_if_zero jumps when the top of the stack is zero
START_TEST(test_jmp_if_zero_taken){

    // Push 5, push 0, jump over the push 99 since top is zero, store 5 to address 0, then halt
    uint8_t program[] = {OP_PUSH, 5, OP_PUSH, 0, OP_JMP_IF_ZERO, 8, OP_PUSH, 99, OP_STORE, 0, OP_HALT};
    vm_run(program, sizeof(program));

    // Load the value from address 0 and verify it is 5 (not 99)
    uint8_t loaded;
    memory_load(0, &loaded);
    ck_assert_int_eq(loaded, 5);

}END_TEST

// Test 8: verify that jmp_if_zero does not jump when the top of the stack is non zero
START_TEST(test_jmp_if_zero_not_taken){

    // Push 5, push 1, do not jump since top is non zero, store 99 to address 0, then halt
    uint8_t program[] = {OP_PUSH, 5, OP_PUSH, 1, OP_JMP_IF_ZERO, 8, OP_PUSH, 99, OP_STORE, 0, OP_HALT};
    vm_run(program, sizeof(program));

    // Load the value from address 0 and verify it is 99
    uint8_t loaded;
    memory_load(0, &loaded);
    ck_assert_int_eq(loaded, 99);

}END_TEST

// Test 9: verify that pushing exactly 256 values (max stack size) succeeds
START_TEST(test_max_stack){

    // Make the program big enough for 256 push operations and a single halt
    uint8_t program[256 * 2 + 1];

    // Add the 256 pushes to the program
    int i;
    for (i = 0; i < 256 * 2; i += 2){
        program[i] = OP_PUSH;
        program[i + 1] = 0x01;
    }

    // Add a halt to the end
    program[i] = OP_HALT;

    // Ensure vm_run returns KERN_OK
    ck_assert_int_eq(vm_run(program, sizeof(program)), KERN_OK);

}END_TEST


// Create the test suite
Suite *positiveSuite(){

    // Define the suite and tc
    Suite *s = suite_create("Positive");
    TCase *tc = tcase_create("Main");

    // Register the setup and teardown functions to run before/after every test
    tcase_add_checked_fixture(tc, setupPositive, teardownPositive);

    // Add tests
    tcase_add_test(tc, test_store_load_roundtrip);
    tcase_add_test(tc, test_add);
    tcase_add_test(tc, test_sub);
    tcase_add_test(tc, test_mul);
    tcase_add_test(tc, test_div);
    tcase_add_test(tc, test_jmp);
    tcase_add_test(tc, test_jmp_if_zero_taken);
    tcase_add_test(tc, test_jmp_if_zero_not_taken);
    tcase_add_test(tc, test_max_stack);

    // Add the tc to the suite
    suite_add_tcase(s, tc);

    // Return the suite
    return s;

}