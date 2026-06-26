import curses
from curses.textpad import Textbox, rectangle
import subprocess
import sys
import os

# Dictionary mapping error codes to human readable text
errorMessages = {
    0: "OK",
    1: "Stack Overflow",
    2: "Stack Underflow", 
    3: "Memory Out of Bounds",
    4: "Program Counter Out of Bounds",
    5: "Invalid Opcode",
    6: "Divide by Zero"
}

# Function to allow hitting enter to submit text
def enterSubmit(key):
    # If enter is hit, return 7, which is control + g, which is curses default submit key
    if key == curses.KEY_ENTER or key in [10, 13]:
        return 7
    return key

# Helper function to clear the screen and draw the results
def show_results(stdscr, filePath, printOutput, telemetryOutput, returnCode):

    # Parse the telemetry
    cycles, elapsed, stackDepth, stackContents, pc, ramDump = parse_telemetry(telemetryOutput)

    # Set up the exit code string to display using the passed return code and the error messages dictionary
    exitCodeStr = f"Exit code: {returnCode} ({errorMessages.get(returnCode, 'Unknown Error')})"

    # Get terminal dimensions
    height, width = stdscr.getmaxyx()

    # Set the max window width
    width = min(width, 120)

    # Check terminal dimensions
    while True:
        curses.resizeterm(height, width)
        height, width = stdscr.getmaxyx()
        width = min(width, 120)
        if height >= 20 and width >= 120:
            break
        stdscr.clear()
        stdscr.addstr(0, 0, f"Terminal too small ({width}x{height}). Please resize to at least 120 columns by 20 rows.")
        stdscr.refresh()
        curses.napms(500)

    # Clear the screen
    stdscr.clear()
    stdscr.refresh()

    # Wrap the stack contents (if needed)
    wrappedStack = wrap_text(stackContents, width, width // 2 + 2)

    # Create the pad
    padHeight = 500
    pad = curses.newpad(padHeight, width)

    # Draw the status line at the top. If completed, inform the user, if failed, also inform the user (unsurprisingly)
    if returnCode == 0:
        status = "[SUCCESS] Execution completed successfully"
    else:
        status = "[FAILED] Execution failed"
    pad.addstr(0, 0, status)

    # Draw the centered title
    title = f"-----OVERVIEW OF EXECUTION OF {filePath}-----"
    pad.addstr(2, width // 2 - len(title) // 2, title)

    # Draw section headers
    machineHeader = "----MACHINE REPORT----"
    stackHeader = "----STACK OVERVIEW----"
    pad.addstr(4, width // 4 - len(machineHeader) // 2, machineHeader)
    pad.addstr(4, width // 2 + width // 4 - len(stackHeader) // 2, stackHeader)

    # Calculate how many rows each panel needs
    # 4 rows minimum for the machine report (4 content + 1 whitespace)
    leftRows = 5
    # Rows for the stack header (1 content, 1 dynamically sized content, 1 whitespace)
    rightRows = len(wrappedStack) + 2

    # Choose the larger number between the two
    panelHeight = max(leftRows, rightRows)

    # Draw a vertical divider ONLY as tall as needed
    for i in range(4, 4 + panelHeight):
        pad.addstr(i, width // 2, "|")

    # Draw machine report fields
    pad.addstr(5, 2, cycles)
    pad.addstr(6, 2, elapsed)
    pad.addstr(7, 2, pc)
    pad.addstr(8, 2, exitCodeStr)

    # Draw stack overview fields
    pad.addstr(5, width // 2 + 2, stackDepth)
    for i, line in enumerate(wrappedStack):
        pad.addstr(6 + i, width // 2 + 2, line)

    # Start machine output right after the panel
    machineOutputHeader = "----MACHINE OUTPUT----"
    machineOutputStart = 4 + panelHeight + 1
    pad.addstr(machineOutputStart, width // 2 - len(machineOutputHeader) // 2, machineOutputHeader)
    printLines = printOutput.split("\n")
    for i, line in enumerate(printLines):
        pad.addstr(machineOutputStart + 1 + i, 2, line)

    # Ram dump starts after machine output
    ramHeader = "----RAM DUMP----"
    ramStart = machineOutputStart + 2 + len(printLines)
    pad.addstr(ramStart, width // 2 - len(ramHeader) // 2, ramHeader)
    for i, line in enumerate(ramDump):
        pad.addstr(ramStart + 1 + i, 2, line)

    # Draw a hint on stdscrn so the user knows how to scroll and stuff
    stdscr.addstr(height - 1, 0, "Arrow keys to scroll | Q to exit")

    # Refresh the screen
    stdscr.refresh()

    # Scroll loop
    scrollPos = 0
    while True:
        pad.refresh(scrollPos, 0, 0, 0, height - 2, width - 1)

        # Get the user's input key
        key = stdscr.getch()

        # If up key, scroll up
        if key == curses.KEY_UP and scrollPos > 0:
            scrollPos -= 1
        
        # If down key, scroll down
        elif key == curses.KEY_DOWN and scrollPos < padHeight - height:
            scrollPos += 1
        
        # If q, quit
        elif key == ord('q'):
            break

# Helper function to clear the screen and draw the error results
def show_assembly_error(stdscr, filePath, errorMessage):

    # Get terminal dimensions
    height, width = stdscr.getmaxyx()

    # Set the max window width
    width = min(width, 120)

    # Check terminal dimensions
    while True:
        curses.resizeterm(height, width)
        height, width = stdscr.getmaxyx()
        width = min(width, 120)
        if height >= 20 and width >= 120:
            break
        stdscr.clear()
        stdscr.addstr(0, 0, f"Terminal too small ({width}x{height}). Please resize to at least 120 columns by 40 rows.")
        stdscr.refresh()
        curses.napms(500)
    
    # Clear the screen
    stdscr.clear()
    
    # Draw status line
    stdscr.addstr(0, 0, "[ERROR] Assembly failed")

    # Draw centered title
    title = f"-----ASSEMBLY ERROR: {filePath}-----"
    stdscr.addstr(2, width // 2 - len(title) // 2, title)

    # Draw error message
    stdscr.addstr(4, 2, errorMessage)

    # Draw hint
    stdscr.addstr(6, 2, "Press enter to exit")

    # Refresh screen and wait for the next keypress
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key in [10, 13, curses.KEY_ENTER]:
            break

# Helper function to parse the telemetry output
def parse_telemetry(telemetryOutput):

    # Split the lines
    lines = telemetryOutput.split("\n")

    # Declare the stats
    cycles = ""
    elapsed = ""
    stackDepth = ""
    stackContents = ""
    pc = ""
    ramDump = []

    # Go through the split lines and assign each stat their respective value
    for line in lines:
        if line.startswith("Number of cycles:"):
            cycles = line
        elif line.startswith("Elapsed time:"):
            elapsed = line
        elif line.startswith("Stack depth:"):
            stackDepth = line
        elif line.startswith("Stack contents:"):
            stackContents = line
        elif line.startswith("Final program counter value:"):
            pc = line
        elif line.startswith("0x"):
            ramDump.append(line)
    
    # Return all the stats
    return cycles, elapsed, stackDepth, stackContents, pc, ramDump

# Helper function to wrap text
def wrap_text(text, maxWidth, startCol):
    
    # Split the words
    words = text.split(", ")
    
    # Define line list
    lines = []

    # Define the current line as well
    currentLine = ""

    # Main text-wrapping loop
    for word in words:

        # If the size of the word that would be added to the line makes the line size go over the width, add currentLine to lines and start a new currentLine
        if len(currentLine) + len(word) + 2 > maxWidth - startCol:
            lines.append(currentLine)
            currentLine = word

        # Otherwise
        else:

            # If currentLine is not empty, add a comma and add the next word
            if currentLine:
                currentLine += ", " + word
            
            # If it is empty, start a new currentLine
            else:
                currentLine = word

    # If currentLine is not empty, add it to lines    
    if currentLine:
        lines.append(currentLine)
    
    # Return lines
    return lines

# Main
def main(stdscr):

    # Wrap all code in a try so when the window is resized, it doesnt crash
    try:
        # Clear screen
        stdscr.clear()

        #Get terminal dimensions
        height, width = stdscr.getmaxyx()

        # Set the max window width
        width = min(width, 120)

        # Check terminal dimensions
        while True:
            curses.resizeterm(height, width)
            height, width = stdscr.getmaxyx()
            width = min(width, 120)
            if height >= 20 and width >= 120:
                break
            stdscr.clear()
            stdscr.addstr(0, 0, f"Terminal too small ({width}x{height}). Please resize to at least 120 columns by 40 rows.")
            stdscr.refresh()
            curses.napms(500)

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
            show_assembly_error(stdscr, filePath, assemblerResult.stdout)

        # Succeeeded, run the vm
        else:
            
            # Derive the .bin path from the .krn path
            binPath = filePath.replace(".krn", ".bin")

            # Run the VM with the binPath
            vmResult = subprocess.run(["./vm/bin/kern", binPath], capture_output=True, text=True)

            # Split stdout into the PRINT instruction output and the telemetry output
            parts = vmResult.stdout.split("----TELEMETRY----\n")

            # Get the print output and strip leading/trailing whitespace (if there was any)
            if parts[0].strip() != "":
                printOutput = parts[0].strip()
            else:
                printOutput = "(No output)"

            # Get the telemetry output and strip leading/trailing whitespace, as long as it didnt crash (which it shouldn't, im just including this for safety reasons)
            if len(parts) > 1:
                telemetryOutput = parts[1].strip()

            # If it did crash, inform the user by setting telemetryOutput to "VM CRASHED"
            else:
                telemetryOutput = "VM CRASHED BEFORE TELEMETRY COULD BE PRINTED"
            
            # Run the show_results function with the respective return code
            show_results(stdscr, filePath, printOutput, telemetryOutput, vmResult.returncode)
    
    except curses.error:
        stdscr.clear()
        stdscr.addstr(0, 0, "Terminal resized too small. Please restart.")
        stdscr.refresh()
        while True:
            key = stdscr.getch()
            if key in [10, 13, curses.KEY_ENTER]:
                break

# If name = main, run the curses wrapper
if __name__ == "__main__":
    curses.wrapper(main)
