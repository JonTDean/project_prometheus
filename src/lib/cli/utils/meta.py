# Stdlib
import os
import sys  # Import sys for sys.exit()
from datetime import datetime
import time

def clear_screen():
    """
    Clears the console screen.

    This function checks the operating system and executes the appropriate command
    to clear the console screen. It uses 'cls' for Windows (nt) and 'clear' for Unix/Linux.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    
def exit_process():
    """
    Prints a goodbye message and terminates the program using sys.exit().
    """
    print("Exiting WGUPS Package System. Goodbye!")
    sys.exit()