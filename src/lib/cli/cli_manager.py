# Stdlib
import os
from pathlib import Path
from datetime import datetime
# Local
from lib.cli.menu_manager import MenuManager
from lib.cli.utils.convert_csv_to_json import convert_distance_table_to_json, convert_package_file_to_json
from lib.cli.utils.meta import clear_screen


# Delegate the CLIManager with the composition Pattern
# - MenuManager handles the menu display and user choice handling
# - Analytics Manager composes analytics for the following
#	- Package Manager displays package information
# 	- Truck Manager displays truck information
# 	- Distance Manager displays distance information
# 	- Delivery Manager displays delivery information
# 	- Route Manager displays route information
class CLIManager:
    def __init__(self, first_run=True) -> None:
        """
        Initializes the CLIManager class, setting up the base directory, default file paths,
        and ensuring the necessary directories exist.
        """
        self.first_run = first_run
        self.menu_manager = MenuManager(self)  # Instantiate MenuManager with a reference to this CLIManager instance
        self._setup_base_directory()
        self._ensure_directories_exist(['files', 'data'])
        self._convert_default_files_to_json()

    def _setup_base_directory(self) -> None:
        """Sets up the base directory and default file paths."""
        self.base_dir: Path = Path(__file__).resolve().parents[3]
        self.default_distance_table_path: Path = self.base_dir / "files" / "WGUPS_Distance_Table.csv"
        self.default_package_file_path: Path = self.base_dir / "files" / "WGUPS_Package_File.csv"

    def _ensure_directories_exist(self, directory_names: list) -> None:
        """Ensures that necessary directories exist within the base directory."""
        for dir_name in directory_names:
            (self.base_dir / dir_name).mkdir(exist_ok=True)

    def _convert_default_files_to_json(self) -> None:
        """Converts default CSV files to JSON format."""
        convert_distance_table_to_json(self.default_distance_table_path, self.base_dir / "data" / "distance_table.json")
        convert_package_file_to_json(self.default_package_file_path, self.base_dir / "data" / "package_file.json")
        
    def _display_header(self, menu_name=None) -> None:
        """Displays the CLI header dynamically based on the menu context."""
        if self.first_run:
            print("===== Welcome to the WGUPS Admin Console - Main Menu =====")
            self.first_run = False
        else:
            print(f"=========== WGUPS Admin Console - {menu_name} ===============")

    def _display_footer(self) -> None:
        """Displays meta information in the footer."""
        # Check for the existence of JSON files
        distance_exists = '[✓]' if os.path.exists(self.base_dir / "data" / "distance_table.json") else '[X]'
        package_exists = '[✓]' if os.path.exists(self.base_dir / "data" / "package_file.json") else '[X]'

        print(f"\nMeta Information: Distance Table {distance_exists}, Package File {package_exists}")
        # Get current time
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"Current Time: {current_time}")


    def run(self) -> None:
        """
        Runs the CLI application, allowing the user to navigate through menus and perform actions.
        This function delegates the showing of menus and handling of user input to the MenuManager.
        """
        while True:
            clear_screen()
            choice = self.menu_manager.show_main_menu()  # Delegate to MenuManager
            self.menu_manager.handle_user_choice(choice)  # Delegate choice handling to MenuManager
            