import os
from pathlib import Path
from typing import Optional, TYPE_CHECKING, Tuple
from lib.cli.utils.convert_csv_to_json import convert_distance_table_to_json, convert_package_file_to_json
from lib.cli.utils.meta import clear_screen, exit_process

if TYPE_CHECKING:
    from lib.cli.cli_manager import CLIManager

def prompt_file_population_choice(cli_manager: 'CLIManager') -> Optional[str]:
    """
    Prompts the user for the file population choice and returns the selected option.

    Parameters:
        cli_manager: The instance of CLIManager for accessing shared functionality.

    Returns:
        The user's choice as a string or None if the user chooses to go back or exit.
    """
    clear_screen()
    cli_manager._display_header("File Population Menu")
    cli_manager._display_meta()
    print("\n1. Use the current csv files (Default)")
    print("2. Provide the fully qualified file paths of the csv files to be converted")
    print("m. Return to main menu")
    print("e. Exit Application")
    choice = input("\nEnter choice (1/2/m/e): ").lower()

    return choice

def handle_file_population_choice(choice: str, cli_manager: 'CLIManager') -> Optional[Tuple[Path, Path]]:
    """
    Handles the file population choice made by the user.

    Parameters:
        choice: The user's choice as a string.
        cli_manager: The instance of CLIManager for accessing shared functionality.

    Returns:
        A tuple containing the paths for the distance table and package file, or None if going back or exiting.
    """
    if choice == "1":
        # Use the default files
        return cli_manager.default_distance_table_path, cli_manager.default_package_file_path, False
    elif choice == "2":
        # This simply indicates that the user wants to provide paths, action is not taken here
        return None, None, True  # Indicating that we should proceed but with custom paths
    else:
        # Return None, None, False for other choices indicating no action should be taken here
        return None, None, False

def show_file_population_menu(cli_manager: 'CLIManager') -> None:
    """
    Initiates the file population process based on the user's choice.

    Parameters:
        cli_manager: The instance of CLIManager for accessing shared functionality.
    """
    choice = prompt_file_population_choice(cli_manager)
    
    if choice == "exit" or choice == "e":
        exit_process()
        return
    elif choice == "main" or choice == "m":
        cli_manager.main_menu_manager.show_menu_and_capture_choice()
        return

    if choice == "2":  # If the user chooses to provide custom paths
        distance_table_path = get_file_path("Distance Table", cli_manager)
        if distance_table_path == 'back':
            show_file_population_menu(cli_manager)  # Rerun this menu
            return
        elif distance_table_path == 'main':
            cli_manager.main_menu_manager.show_menu_and_capture_choice()
            return
        package_file_path = get_file_path("Package File", cli_manager)
        if package_file_path == 'back':
            show_file_population_menu(cli_manager)  # Rerun this menu
            return
        elif package_file_path == 'main':
            cli_manager.main_menu_manager.show_menu_and_capture_choice()
            return
        if distance_table_path and package_file_path:
            convert_and_save_files(cli_manager, Path(distance_table_path), Path(package_file_path))
            print("Files processed successfully.")
    elif choice == "1":
        cli_manager._convert_default_files_to_json()
        print("Default files processed successfully.")
    else:
        print("Invalid choice. Returning to the file population menu...")
        show_file_population_menu(cli_manager)
        
def convert_and_save_files(cli_manager: 'CLIManager', distance_table_path: Path, package_file_path: Path) -> None:
    """
    Converts the provided CSV files to JSON and saves them to the specified locations.

    Parameters:
        cli_manager: The instance of CLIManager for accessing shared functionality.
        distance_table_path: Path to the distance table CSV file.
        package_file_path: Path to the package file CSV file.
    """
    # Define JSON file paths
    json_distance_table_path = cli_manager.base_dir / "data" / "distance_table.json"
    json_package_file_path = cli_manager.base_dir / "data" / "package_file.json"

    # Convert CSV to JSON
    convert_distance_table_to_json(distance_table_path, json_distance_table_path)
    convert_package_file_to_json(package_file_path, json_package_file_path)

    print(f"Files processed successfully and saved to: {cli_manager.base_dir / 'data'}")

def get_file_path(file_type: str, cli_manager: 'CLIManager') -> str:
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
            
            
            