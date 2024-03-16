# MenuManager.py
# Local
from lib.cli.menus.file_population_menu.file_population_menu import process_file_population
from lib.cli.menus.main_menu.main_menu import show_main_menu
from lib.cli.menus.package_menu.package_menu import PackageMenu
from lib.cli.utils.meta import clear_screen, exit_process

class MenuManager:
    def __init__(self, cli_manager):
        """
        Initializes the MenuManager with a CLIManager instance to access shared functionality.
  
        Parameters:
        - cli_manager: Instance of the CLIManager class.
        """
        self.package_menu = PackageMenu(self.cli_manager.package_manager)

    def show_main_menu(self) -> str:
        """
        Displays the main menu and captures the user's choice.
        """
        # Display header and menu options
        self.cli_manager._display_header("Main Menu")
        
        print("Welcome to the WGUPS Admin Console - Main Menu\n")
        print("p. Populate delivery data and package data")
        print("e. Exit")
        
        # Display footer with meta information and current time
        self.cli_manager._display_footer()
        
        # Return the user's choice
        return input("Enter choice: ").lower()

    def handle_user_choice(self, choice: str) -> None:
        """
        Processes the user's choice from the main menu.

        Parameters:
        - choice: The user's selected option as a string.
        """
        if choice == "p":
            # Process file population using the provided paths
            process_file_population(self.cli_manager)  # Updated to pass cli_manager
        elif choice == "e":
            # Exit the application
            exit_process()
        else:
            # Handle invalid choices
            print("Invalid choice. Please enter a valid option.")