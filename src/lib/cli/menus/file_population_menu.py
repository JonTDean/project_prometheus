# Stdlib
from pathlib import Path
from typing import Tuple, Optional
# Local
from lib.cli.utils.convert_csv_to_json import convert_distance_table_to_json, convert_package_file_to_json
from lib.cli.utils.get_file_path import get_file_path
from lib.cli.utils.meta import UserBack, UserExit, clear_screen, exit_process

def show_file_population_menu(default_distance_table_path: Path, default_package_file_path: Path) -> Tuple[Optional[Path], Optional[Path]]:
    """
    Displays the file population menu, allowing the user to choose between using default files or providing paths.
    Additionally offers options to exit the process or return to the previous menu.

    Parameters:
        default_distance_table_path (Path): The default path for the distance table CSV file.
        default_package_file_path (Path): The default path for the package file CSV file.

    Returns:
        Tuple[Optional[Path], Optional[Path]]: The paths for the distance table and package file, or None for each if the user chooses to go back or exit.
    """
    while True:
        clear_screen()
        print("WGUPS Package System - File Population Menu\n")
        print("1. Use the current csv files (Default)")
        print("2. Please provide the fully qualified file paths of the csv files to be converted")
        print("Enter 'back' (b) to return to the main menu or 'exit' (e) to quit.")
        choice = input("Enter choice (1/2): ").upper()

        if choice == "1":
            return default_distance_table_path, default_package_file_path
        elif choice == "2":
            try:
                distance_table_path = get_file_path("Distance Table")
                if distance_table_path is None:  # User chose 'back' in get_file_path
                    continue
                package_file_path = get_file_path("Package File")
                if package_file_path is None:  # User chose 'back' in get_file_path
                    continue
                return distance_table_path, package_file_path
            except UserExit:
                exit_process()  # Assuming this gracefully exits the application
            except UserBack:
                return None, None  # Return to the main menu
        elif choice in ["BACK", "B"]:
            return None, None  # User chooses to go back to the main menu directly
        elif choice in ["EXIT", "E"]:
            exit_process()  # Assuming this gracefully exits the application
        else:
            print("Invalid choice. Please select '1', '2', 'back', or 'exit'.")
        
def process_file_population(base_dir: Path, default_distance_table_path: Path, default_package_file_path: Path) -> None:
    """
    Processes file population based on user choice, converting CSV files to JSON.
    """
    distance_table_path, package_file_path = show_file_population_menu(default_distance_table_path, default_package_file_path)
    
    if distance_table_path and package_file_path:
        clear_screen()
        convert_distance_table_to_json(distance_table_path, base_dir / "data" / "distance_table.json")
        convert_package_file_to_json(package_file_path, base_dir / "data" / "package_file.json")
        print(f"Files processed successfully.")
        clear_screen()
    else:
        print("Returning to main menu...")