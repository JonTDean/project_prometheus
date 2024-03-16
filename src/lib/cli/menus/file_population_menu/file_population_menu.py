# Stdlib
from pathlib import Path
from typing import Tuple, Optional
from typing import TYPE_CHECKING
# Local
from lib.cli.utils.convert_csv_to_json import convert_distance_table_to_json, convert_package_file_to_json
from lib.cli.menus.main_menu.get_file_path import get_file_path
from lib.cli.utils.meta import UserBack, UserExit, clear_screen, exit_process

# To prevent circular dependency issues
if TYPE_CHECKING:
    from lib.cli.cli_manager import CLIManager
    
def show_file_population_menu(cli_manager: 'CLIManager', default_distance_table_path: Path, default_package_file_path: Path) -> Tuple[Optional[Path], Optional[Path]]:
    """
    Displays the file population menu, allowing the user to choose between using default files or providing paths.
    Additionally offers options to exit the process or return to the previous menu.

    Parameters:
        cli_manager: The instance of the CLIManager class for accessing shared functionality.
        default_distance_table_path (Path): The default path for the distance table CSV file.
        default_package_file_path (Path): The default path for the package file CSV file.

    Returns:
        Tuple[Optional[Path], Optional[Path]]: The paths for the distance table and package file, or None for each if the user chooses to go back or exit.
    """
    while True:
        clear_screen()
        cli_manager._display_header("File Population Menu")
        print("1. Use the current csv files (Default)")
        print("2. Please provide the fully qualified file paths of the csv files to be converted")
        print("Enter 'back' (b) to return to the main menu or 'exit' (e) to quit.")
        choice = input("Enter choice (1/2): ").upper()

        if choice == "1":
            cli_manager._display_footer()
            return default_distance_table_path, default_package_file_path
        elif choice == "2":
            try:
                distance_table_path = get_file_path("Distance Table")
                if distance_table_path is None:  # User chose 'back' in get_file_path
                    cli_manager._display_footer()
                    continue
                package_file_path = get_file_path("Package File")
                if package_file_path is None:  # User chose 'back' in get_file_path
                    cli_manager._display_footer()
                    continue
                cli_manager._display_footer()
                return distance_table_path, package_file_path
            except UserExit:
                exit_process()  # Assuming this gracefully exits the application
            except UserBack:
                cli_manager._display_footer()
                return None, None  # Return to the main menu
        elif choice in ["BACK", "B"]:
            cli_manager._display_footer()
            return None, None  # User chooses to go back to the main menu directly
        elif choice in ["EXIT", "E"]:
            exit_process()  # Assuming this gracefully exits the application
        else:
            print("Invalid choice. Please select '1', '2', 'back', or 'exit'.")
            cli_manager._display_footer()
        
def process_file_population(cli_manager: 'CLIManager') -> None:
    """
    Processes file population based on user choice, converting CSV files to JSON.

    Parameters:
    - cli_manager: The instance of CLIManager to access shared properties.
    """
    # Prompt the user for the file paths
    distance_table_path_str, package_file_path_str = show_file_population_menu(
        cli_manager,
        cli_manager.default_distance_table_path,
        cli_manager.default_package_file_path
    )

    # Convert string paths to Path objects, if paths were provided
    distance_table_path = Path(distance_table_path_str) if distance_table_path_str else None
    package_file_path = Path(package_file_path_str) if package_file_path_str else None

    # Specify the target folder for the JSON files
    target_folder = cli_manager.base_dir / "data"

    # Ensure target folder exists, create if necessary
    if not target_folder.exists():
        target_folder.mkdir(parents=True, exist_ok=True)
        print(f"Created folder: {target_folder}")

    if distance_table_path and package_file_path:
        # Proceed only if the user-provided paths are valid
        if distance_table_path.exists() and package_file_path.exists():
            # Specify the full path for the JSON files
            json_distance_table_path = target_folder / "distance_table.json"
            json_package_file_path = target_folder / "package_file.json"

            # Track whether files are being created or overwritten
            distance_action = "Overwritten" if json_distance_table_path.exists() else "Created"
            package_action = "Overwritten" if json_package_file_path.exists() else "Created"

            # Convert CSV files to JSON
            convert_distance_table_to_json(distance_table_path, json_distance_table_path)
            convert_package_file_to_json(package_file_path, json_package_file_path)

            # Inform the user of the actions taken
            print(f"{distance_action} file: {json_distance_table_path}")
            print(f"{package_action} file: {json_package_file_path}")
            print(f"Files processed successfully and saved to: {target_folder}")
        else:
            # Handle case where provided paths do not point to existing files
            print("One or both of the provided file paths do not exist. Please check and try again.")
    else:
        # Handle case where user returns to the menu without providing paths
        print("Returning to the main menu...")