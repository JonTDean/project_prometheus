def show_main_menu() -> str:
    """
    Displays the main menu of the CLI and captures the user's choice.

    Returns:
        The user's choice as a lowercase string.
    """
    print("Welcome to the WGUPS Package System - Main Menu\n")
    print("p. Populate delivery data and package data")
    print("e. Exit")
    return input("Enter choice: ").lower()