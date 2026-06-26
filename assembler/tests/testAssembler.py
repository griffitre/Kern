import unittest
import sys

# Import assembler functions
sys.path.append("assembler/src")
from assembler import tokenize, first_pass, second_pass, opcodes, symbols

# Tokenizer test class
class TestTokenizer(unittest.TestCase):

    # Test 1: ensure basic input is correct
    def test_basic(self):
        input = "PUSH 5\nHALT"
        tokenized = tokenize(input)
        self.assertEqual(tokenized, [["PUSH", "5"], ["HALT"]])

    # Test 2: Ensure leading/trailing whitespace is stripped
    def test_whitespace(self):
        input = "PUSH 5 \n HALT"
        tokenized = tokenize(input)
        self.assertEqual(tokenized, [["PUSH", "5"], ["HALT"]])

    # Test 3: ensure comments are stripped
    def test_comments(self):
        input = "PUSH 5 ; push 5 to stack \n HALT"
        tokenized = tokenize(input)
        self.assertEqual(tokenized, [["PUSH", "5"], ["HALT"]])

    # Test 4: ensure blank lines are skipped
    def test_blank(self):
        input = "PUSH 5 \n \n HALT"
        tokenized = tokenize(input)
        self.assertEqual(tokenized, [["PUSH", "5"], ["HALT"]])

    # Test 5: ensure lowercase gets uppercased
    def test_upper(self):
        input = "push 5 \n halt"
        tokenized = tokenize(input)
        self.assertEqual(tokenized, [["PUSH", "5"], ["HALT"]])

    # Test 6: ensure labels are tokenized correctly
    def test_labels(self):
        input = "loop: \n HALT"
        tokenized = tokenize(input)
        self.assertEqual(tokenized, [["LOOP:"], ["HALT"]])


# FirstPass test class
class TestFirstPass(unittest.TestCase):

    # Setup method to clear the symbols dictionary before running each time
    def setUp(self):
        symbols.clear()

    # Test 1: ensure labels are identified and added to symbols with correct byte address
    def test_basic(self):
        input = [["END:"], ["HALT"]]
        first_pass(input)
        self.assertEqual(symbols["END"], 0x00)

    # Test 2: ensure labels after a 2-byte instruction have the correct byte address
    def test_two_bytes(self):
        input = [["PUSH", "5"], ["END:"], ["HALT"]]
        first_pass(input)
        self.assertEqual(symbols["END"], 0x02)
    
    # Test 3: ensure a program with multiple labels have them all resolved correctly
    def test_multiple(self):
        input = [["LOOP:"], ["PUSH", "5"], ["PRINT"], ["END:"], ["HALT"]]
        first_pass(input)
        self.assertEqual(symbols["LOOP"], 0x00)
        self.assertEqual(symbols["END"], 0x03)


# SecondPass test class
class TestSecondPass(unittest.TestCase):

    # Setup method to clear the symbols dictionary before running each time
    def setUp(self):
        symbols.clear()

    # Test 1: ensure valid instructions emit valid bytes
    def test_basic(self):
        input = [["PUSH", "5"], ["PRINT"], ["HALT"]]
        output = second_pass(input)
        self.assertEqual(output, [0x01, 0x05, 0x0B, 0xFF])

    # Test 2: ensure label references resolve to correct addresses in bytecode 
    def test_label(self):
        input = [["PUSH", "5"], ["PRINT"], ["JMP", "END"], ["END:"], ["HALT"]]
        first_pass(input)
        output = second_pass(input)
        self.assertEqual(output, [0x01, 0x05, 0x0B, 0x09, 0x05, 0xFF])

    # Test 3: ensure unknown opcode triggers sys.exit(1)
    def test_exit(self):
        input = [["PUSH", "5"], ["INVALIDCODE"], ["HALT"]]
        with self.assertRaises(SystemExit):
            second_pass(input)
    
    # Test 4: ensure missing operand triggers sys.exit(1)
    def test_missing(self):
        input = [["PUSH"], ["HALT"]]
        with self.assertRaises(SystemExit):
            second_pass(input)

    # Test 5: ensure operand larger than 255 triggers sys.exit(1)
    def test_large(self):
        input = [["PUSH", "256"], ["HALT"]]
        with self.assertRaises(SystemExit):
            second_pass(input)

    # Test 6: ensure unknown label triggers sys.exit(1)
    def test_unknown(self):
        input = [["PUSH", "5"], ["JMP", "UNKNOWN"], ["HALT"]]
        with self.assertRaises(SystemExit):
            second_pass(input)


# If name = main, run unittest classes (unittest.main)
if __name__ == "__main__":
    unittest.main()
