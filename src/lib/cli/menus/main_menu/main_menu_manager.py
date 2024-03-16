# Local
from lib.cli.menus.analytics.analytics_manager import AnalyticsManager
from lib.cli.menus.file_population_menu.file_population_menu import show_file_population_menu
from lib.cli.utils.meta import clear_screen, exit_process

class MainMenuManager:
    def __init__(self, cli_manager):
        """
        Initializes the MainMenuManager with a CLIManager instance to access shared functionality.

        Parameters:
        - cli_manager: Instance of the CLIManager class providing access to the broader application context.
        """
        self.cli_manager = cli_manager

    def show_menu_and_capture_choice(self):
        """
        Displays the main menu, captures the user's choice, and handles the choice appropriately.
        """
        choice = self._show_main_menu()
        self.handle_user_choice(choice)

    def _show_main_menu(self) -> str:
        """
        Displays the main menu and returns the user's choice as a lowercase string.

        Returns:
            The user's choice as a lowercase string.
        """
        clear_screen()
        # Display menu header
        self.cli_manager._display_header("Main Menu")
        self.cli_manager._display_meta()

        # Display menu options
        self._display_menu()

        # Display footer with meta information and current time

        # Capture and return the user's choice
        return input("\nEnter choice (a/p/e): ").lower()

    def _display_menu(self):
        """
        Prints the main menu options to the console.
        """
        print("a. View Analytics")
        print("p. Populate (Custom or Original) delivery data and package data")
        print("e. Exit Application")

    def handle_user_choice(self, choice: str):
        """
        Processes the user's choice from the main menu and triggers the appropriate action.

        Parameters:
        - choice: The user's selected option as a string.
        """
        if choice == "v":
            # Delegate to show analytics menu
            AnalyticsManager.show_analytics_menu(self.cli_manager, self)
        elif choice == "p":
            # Delegate to process file population using the provided paths
            show_file_population_menu(self.cli_manager)
        elif choice == "e":
            # Trigger application exit
            exit_process()
        else:
            # Notify the user of an invalid choice and prompt again
            print("Invalid choice. Please enter a valid option.")
