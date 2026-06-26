import curses
from curses.textpad import Textbox, rectangle
import subprocess
import sys
import os

# Function to allow hitting enter to submit text
def enterSubmit(key):
    # If enter is hit, return 7, which is control + g, which is curses default submit key
    if key == curses.KEY_ENTER or key in [10, 13]:
        return 7
    return key

# Main
def main(stdscr):

    # Clear screen
    stdscr.clear()

    # Get terminal dimensions
    height, width = stdscr.getmaxyx()

    # Check minimum terminal dimensions (TODO)

    # Draw title in the center
    title = "KERN"
    stdscr.addstr(0, width // 2 - len(title) // 2, title)

    # Draw input box
    rectangle(stdscr, 3, 2, 5, width - 2)

    # Create input window inside the box
    inputWin = curses.newwin(1, width - 6, 4, 4)

    # Draw prompt
    prompt = "Enter .krn file path:"
    stdscr.addstr(2, 2, prompt)

    # Draw hint
    hint = "Press Enter to run"
    stdscr.addstr(6, 2, hint)

    # Refresh screen
    stdscr.refresh()

    # Get input
    box = Textbox(inputWin)
    box.edit(enterSubmit)
    filePath = box.gather().strip()

    # Run the assembler
    assemblerResult = subprocess.run(["python3", "assembler/src/assembler.py", filePath], capture_output=True, text=True)

    # Check if the assembler failed or if it succeeded
    # Failed, show the error screen
    if assemblerResult.returncode != 0:
        # Fail/error screen (TODO)
        pass

    # Succeeeded, run the vm
    else:
        
        # Derive the .bin path from the .krn path
        binPath = filePath.replace(".krn", ".bin")

        # Run the VM with the binPath
        vmResult = subprocess.run(["./vm/bin/kern", binPath], capture_output=True, text=True)

        # Split stdout into the PRINT instruction output and the telemetry output
        parts = vmResult.stdout.split("----TELEMETRY----\n")

        # Get the print output and strip leading/trailing whitespace
        printOutput = parts[0].strip()

        # Get the telemetry output and strip leading/trailing whitespace, as long as it didnt crash (which it shouldn't, im just including this for safety reasons)
        if len(parts) > 1:
            telemetryOutput = parts[1].strip()
        # If it did crash, inform the user by setting telemetryOutput to "VM CRASHED"
        else:
            telemetryOutput = "VM CRASHED BEFORE TELEMETRY COULD BE PRINTED"
        pass


    # Wait for keypress before exiting the program
    stdscr.getch()

# If name = main, run the curses wrapper
if __name__ == "__main__":
    curses.wrapper(main)