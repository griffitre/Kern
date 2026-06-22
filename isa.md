# Kern ISA Specifications

## Overview
Kern uses a stack-based architecture. In simple terms, all operations either read or write to a single data stack, sometimes they do both. <br>
Each instruction is either 1 byte (meaning no operand), or two bytes (meaning there is an operand). All values are unsigned 8 bit integers (0-255). <br>
This concept is further demonstrated below in this fun little table I made:
| Format | Size | Description |
|---|---|---|
| `[opcode]` | 1 byte | Instruction with no operand |
| `[opcode][operand]` | 2 bytes | Instruction with one 1-byte operand |

## Binary Format
Each `.bin` file is a flat sequence of bytes. The VM will load the entire file into an instruction buffer, and execute everything starting from byte zero.

## Opcode Table
| Mnemonic | Opcode | Operand | Pops | Pushes | Description |
|---|---|---|---|---|---|
| PUSH | 0x01 | value | - | value | Pushes operand onto the stack |
| POP | 0x02 | - | top | - | Pops and discards the top of the stack |
| ADD | 0x03 | - | a, b | a + b | Pops two values, pushes a + b |
| SUB | 0x04 | - | a, b | b - a | Pops two values (a then b), pushes b - a |
| MUL | 0x05 | - | a, b | a * b | Pops two values, pushes a * b |
| DIV | 0x06 | - | a, b | b / a | Pops two values (a then b), pushes b / a |
| STORE | 0x07 | addr | value | - | Pops top of stack and writes it to memory address |
| LOAD | 0x08 | addr | - | value | Reads from memory address and pushes value onto stack |
| JMP | 0x09 | addr | - | - | Sets program counter to addr |
| JMP_IF_ZERO | 0x0A | addr | top | - | Pops top of stack, sets program counter if value is 0 |
| PRINT | 0x0B | - | top | - | Pops top of stack and prints it to stdout |
| HALT | 0xFF | - | - | - | Stops execution |

## Fault Conditions
The VM will intercept and halt safely on any of the following errors/problems:
- Stack Overflow: An operation tries to PUSH, when a PUSH would exceed maximum stack depth
- Stack Underflow: An operation tries to POP from an empty stack
- Memory Out of Bounds: STORE or LOAD targets a memory address outside of the allocated RAM block
- Invalid Opcode: A byte does not match any defined opcode
- Program Counter Out of Bounds: JMP or JMP_IF_ZERO targets an address outside of the instruction buffer
- Divide By Zero: DIV is called with 0 on top of the stack

## Output
On termination, whether complete or fault, the VM will print:
- The exit code (default is 0, meaning clean, with non-zero meaning fault type)
- Total number of cycles executed
- Final stack depth
- Execution runtime
- Hex dump of virtual RAM