# Stdlib
from pathlib import Path
from typing import Optional
# Local
from lib.cli.menus.file_population_menu import process_file_population
from lib.cli.menus.main_menu import show_main_menu
from lib.cli.utils.meta import clear_screen, exit_process


        
class CLIManager:
    def __init__(self) -> None:
        """
        Initializes the CLIManager class, setting up the base directory, default file paths,
        and ensuring the necessary directories exist.
        """
        # Navigate up from current file location to the project root
        self.base_dir: Path = Path(__file__).resolve().parents[3]
        self.default_distance_table_path: Path = self.base_dir / "files" / "WGUPS_Distance_Table.csv"
        self.default_package_file_path: Path = self.base_dir / "files" / "WGUPS_Package_File.csv"
        
        # Ensure the 'data' and 'files' directories exist
        (self.base_dir / "data").mkdir(exist_ok=True)
        (self.base_dir / "files").mkdir(exist_ok=True)


    def handle_user_choice(self, choice: str) -> None:
        """
        Handles the user's choice from the main menu.

        Parameters:
            choice (str): The user's choice as a lowercase string.
        """
        if choice in ["p", "populate"]:
            process_file_population(self.base_dir, self.default_distance_table_path, self.default_package_file_path)
        elif choice in ["e", "exit"]:
            exit_process()
        else:
            print("Invalid choice. Please enter a valid option.")

            
    def run(self) -> None:
        """
        Runs the CLI application, allowing the user to navigate through menus and perform actions.
        """
        while True:
            choice = show_main_menu()
            clear_screen()
            self.handle_user_choice(choice)