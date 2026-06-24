# Define variables
CC = gcc
CFLAGS = -Wall -Wextra -I vm/include

# Ensure required directories exist
$(shell mkdir -p vm/obj vm/bin)

# Command to build the kern executable
build: vm/obj/main.o vm/obj/vm.o vm/obj/memory.o vm/obj/stack.o vm/obj/telemetry.o
	$(CC) $(CFLAGS) vm/obj/main.o vm/obj/vm.o vm/obj/memory.o vm/obj/stack.o vm/obj/telemetry.o -o vm/bin/kern

# Command to build the test file
test: vm/obj/vm.o vm/obj/memory.o vm/obj/stack.o vm/obj/telemetry.o vm/obj/negativeTests.o vm/obj/positiveTests.o vm/obj/testMain.o
	$(CC) $(CFLAGS) vm/obj/vm.o vm/obj/memory.o vm/obj/stack.o vm/obj/telemetry.o vm/obj/negativeTests.o vm/obj/positiveTests.o vm/obj/testMain.o -o vm/bin/tests -lcheck -lm -lsubunit -lrt -lpthread

# Commands to build each object file
vm/obj/main.o: vm/src/main.c
	$(CC) $(CFLAGS) vm/src/main.c -c -o vm/obj/main.o

vm/obj/vm.o: vm/src/vm.c
	$(CC) $(CFLAGS) vm/src/vm.c -c -o vm/obj/vm.o

vm/obj/memory.o: vm/src/memory.c
	$(CC) $(CFLAGS) vm/src/memory.c -c -o vm/obj/memory.o

vm/obj/stack.o: vm/src/stack.c
	$(CC) $(CFLAGS) vm/src/stack.c -c -o vm/obj/stack.o

vm/obj/telemetry.o: vm/src/telemetry.c
	$(CC) $(CFLAGS) vm/src/telemetry.c -c -o vm/obj/telemetry.o

vm/obj/negativeTests.o: vm/tests/negativeTests.c
	$(CC) $(CFLAGS) vm/tests/negativeTests.c -c -o vm/obj/negativeTests.o

vm/obj/positiveTests.o: vm/tests/positiveTests.c
	$(CC) $(CFLAGS) vm/tests/positiveTests.c -c -o vm/obj/positiveTests.o

vm/obj/testMain.o: vm/tests/testMain.c
	$(CC) $(CFLAGS) vm/tests/testMain.c -c -o vm/obj/testMain.o

# Command to remove all object files and executables
clean:
	rm -f vm/obj/* vm/bin/*