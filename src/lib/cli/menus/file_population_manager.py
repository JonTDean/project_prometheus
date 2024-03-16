import os
from pathlib import Path
from typing import Optional, Tuple
from lib.cli.utils.convert_csv_to_json import convert_distance_table_to_json, convert_package_file_to_json
from lib.cli.utils.meta import clear_screen, exit_process

class FilePopulationManager:
    def __init__(self, cli_manager):
        self.cli_manager = cli_manager

    def prompt_file_population_choice(self) -> Optional[str]:
        """
        Prompts the user for the file population choice and returns the selected option.

        Returns:
            The user's choice as a string or None if the user chooses to go back or exit.
        """
        clear_screen()
        self.cli_manager._display_header("File Population Menu")
        self.cli_manager._display_meta()
        print("1. Use the current csv files (Default)")
        print("2. Provide the fully qualified file paths of the csv files to be converted")
        print("m. Return to main menu")
        print("e. Exit Application")
        choice = input("\nEnter choice (1/2/m/e): ").lower()
        return choice

    def handle_file_population_choice(self, choice: str) -> Optional[Tuple[Path, Path, bool]]:
        """
        Handles the file population choice made by the user.

        Parameters:
            choice: The user's choice as a string.

        Returns:
            A tuple containing the paths for the distance table and package file, or None if going back or exiting.
        """
        if choice == "1":
            return self.cli_manager.default_distance_table_path, self.cli_manager.default_package_file_path, False
        elif choice == "2":
            return None, None, True
        else:
            return None, None, False

    def show_file_population_menu(self):
        """
        Initiates the file population process based on the user's choice.
        """
        choice = self.prompt_file_population_choice()
        
        if choice == "exit" or choice == "e":
            exit_process()
            return
        elif choice == "main" or choice == "m":
            self.cli_manager.main_menu_manager.show_menu_and_capture_choice()
            return

        distance_table_path, package_file_path, proceed_with_conversion = self.handle_file_population_choice(choice)
        
        if proceed_with_conversion and choice == "2":
            distance_table_path = self.get_file_path("Distance Table")
            if distance_table_path == 'back':
                self.show_file_population_menu()
                return
            elif distance_table_path == 'main':
                self.cli_manager.main_menu_manager.show_menu_and_capture_choice()
                return
            package_file_path = self.get_file_path("Package File")
            if package_file_path == 'back':
                self.show_file_population_menu()
                return
            elif package_file_path == 'main':
                self.cli_manager.main_menu_manager.show_menu_and_capture_choice()
                return
            if distance_table_path and package_file_path:
                self.convert_and_save_files(Path(distance_table_path), Path(package_file_path))
                print("Files processed successfully.")
        elif choice == "1":
            self.cli_manager._convert_default_files_to_json()
            print("Default files processed successfully.")
        else:
            print("Invalid choice. Returning to the file population menu...")
            self.show_file_population_menu()

    def convert_and_save_files(self, distance_table_path: Path, package_file_path: Path):
        """
        Converts the provided CSV files to JSON and saves them to the specified locations.

        Parameters:
            distance_table_path: Path to the distance table CSV file.
            package_file_path: Path to the package file CSV file.
        """
        json_distance_table_path = self.cli_manager.base_dir / "data" / "distance_table.json"
        json_package_file_path = self.cli_manager.base_dir / "data" / "package_file.json"
        convert_distance_table_to_json(distance_table_path, json_distance_table_path)
        convert_package_file_to_json(package_file_path, json_package_file_path)
        print(f"Files processed successfully and saved to: {self.cli_manager.base_dir / 'data'}")

    def get_file_path(self, file_type: str) -> str:
        """
        Prompts the user to enter a fully qualified file path for a specified file type.
        
        Parameters:
            file_type (str): A string representing the type of file for which the path is being requested.
                            This is used to customize the prompt message.
        
        Returns:
            str: The fully qualified path to the file provided by the user. Returns None if the user chooses
                to go back or exit.
        
        The function allows the user to:
        - Enter a path to a file of the specified type (.csv).
        - Type 'exit' or 'e' to quit the application.
        - Type 'back' or 'b' to return to the previous menu without providing a file path.
        
        If the provided file path does not exist or does not end with '.csv', the user is prompted again.
        """
        while True:
            print("\nEnter 'exit' (e) to quit, 'back' (b) for file population menu, or 'main' (m) to return to the main menu.")
            file_path = input(f"Please enter the fully qualified file path for the {file_type} (.csv): ")

            if file_path.lower() in ['exit', 'e']:
                exit_process()
            elif file_path.lower() in ['back', 'b']:
                return 'back'
            elif file_path.lower() in ['main', 'm']:
                return 'main'

            if os.path.exists(file_path) and file_path.endswith('.csv'):
                confirm = input(f"Path entered: {file_path}\nProceed? (y/n): ").lower()
                if confirm == 'y':
                    return file_path
                # If user says 'n', it will just loop for another input
            else:
                print("Invalid file or format. Please ensure the file exists and is a '.csv' file.")
