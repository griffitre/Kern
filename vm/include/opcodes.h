#ifndef OPCODES_H
#define OPCODES_H

typedef enum {
    OP_PUSH       = 0x01,
    OP_POP        = 0x02,
    OP_ADD        = 0x03,
    OP_SUB        = 0x04,
    OP_MUL        = 0x05,
    OP_DIV        = 0x06,
    OP_STORE      = 0x07,
    OP_LOAD       = 0x08,
    OP_JMP        = 0x09,
    OP_JMP_IF_ZERO = 0x0A,
    OP_PRINT      = 0x0B,
    OP_HALT       = 0xFF
} Opcode;

#endif