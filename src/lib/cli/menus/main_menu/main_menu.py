from typing import TYPE_CHECKING

# To prevent circular dependency issues
if TYPE_CHECKING:
    from lib.cli.cli_manager import CLIManager

def show_main_menu(cli_manager: 'CLIManager') -> str:
    """
    Displays the main menu of the CLI and captures the user's choice.

    Returns:
        The user's choice as a lowercase string.
    """
    cli_manager._display_header()
    
    print("Welcome to the WGUPS Admin Console - Main Menu\n")
    
    print("\np. Populate delivery data and package data")
    print("e. Exit")
    
    cli_manager._display_footer()
    
    return input("Enter choice: ").lower()