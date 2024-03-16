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

class UserExit(Exception):
    pass

class UserBack(Exception):
    pass

def exit_or_back_prompt(user_choice: str) -> None:
    """
    Checks if the user input is an exit or back command and raises exceptions accordingly.

    Parameters:
        user_choice (str): The user's input choice.

    Raises:
        UserExit: If the user chooses to exit.
        UserBack: If the user chooses to go back to the previous menu.
    """
    if user_choice.lower() in ['exit', 'e']:
        raise UserExit
    elif user_choice.lower() in ['back', 'b']:
        raise UserBack
