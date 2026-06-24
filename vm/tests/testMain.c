#include "negativeTests.h"
#include "positiveTests.h"
#include <check.h>
#include <stdlib.h>

// Main runner
int main(){

    // Create a suite runner to run the suites
    // Create it with negativeSuite
    SRunner *sr = srunner_create(negativeSuite());

    // Add positiveSuite to it
    srunner_add_suite(sr, positiveSuite());

    // Run the suite runner
    srunner_run_all(sr, CK_NORMAL);

    // Get the number of failed tests
    int failed = srunner_ntests_failed(sr);

    // Free the runner
    srunner_free(sr);

    // Return 0 if no tests failed and 1 if any tests failed
    return failed == 0 ? 0 : 1;

}