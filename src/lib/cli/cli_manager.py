# Stdlib
import os
from pathlib import Path
from datetime import datetime
# Local
from lib.cli.menus.analytics.analytics_manager import AnalyticsManager
from lib.cli.menus.analytics.package_manager import PackageManager
from lib.cli.menus.analytics.truck_manager import TruckManager
from lib.cli.menus.file_population_manager import FilePopulationManager
from lib.cli.menus.main_menu_manager import MainMenuManager
from lib.cli.utils.convert_csv_to_json import convert_distance_table_to_json, convert_package_file_to_json
from lib.cli.utils.meta import clear_screen
from lib.delivery_system.delivery_system_package import DSPackage
from lib.delivery_system.delivery_system_truck import DSTruck


# Delegate the CLIManager with the composition Pattern
# - MenuManager handles the menu display and user choice handling
# - PopulationManager handles the file population menu
# - Analytics Manager composes analytics for the following
#	- Package Manager displays package information
# 	- Truck Manager displays truck information
class CLIManager:
    def __init__(self, first_run=True) -> None:
        """
        Initializes the CLIManager class, setting up the base directory, default file paths,
        and ensuring the necessary directories exist.
        """
        self.first_run = first_run
        self.base_dir = Path(__file__).resolve().parents[3]
        self.data_available = False  # Track availability of data for analytics
        self.distance_json_path = self.base_dir / "data" / "distance_table.json"
        self.package_json_path = self.base_dir / "data" / "package_file.json"
        
        # Setup directories and files
        self._setup_base_directory()
        self._ensure_directories_exist(['files', 'data'])
        self._convert_default_files_to_json()

        # Instantiate menu managers
        self.main_menu_manager = MainMenuManager(self)
        self.file_population_manager = FilePopulationManager(self)

        # Instantiate analytics-related managers if data is available
        if self.data_available:
            self.ds_package = DSPackage(self.package_json_path)
            self.ds_truck = DSTruck(self.distance_json_path)
            self.package_manager = PackageManager(self, self.ds_package)
            self.truck_manager = TruckManager(self, self.ds_truck)
            self.analytics_manager = AnalyticsManager(self, self.package_manager, self.truck_manager)

    def _setup_base_directory(self) -> None:
        """Sets up the base directory and default file paths."""
        self.base_dir: Path = Path(__file__).resolve().parents[3]
        self.default_distance_table_path: Path = self.base_dir / "files" / "WGUPS_Distance_Table.csv"
        self.default_package_file_path: Path = self.base_dir / "files" / "WGUPS_Package_File.csv"

    def _ensure_directories_exist(self, directory_names: list) -> None:
        """Ensures that necessary directories exist within the base directory."""
        for dir_name in directory_names:
            (self.base_dir / dir_name).mkdir(exist_ok=True)
            

    # Call this on startup, this way we can reliably 
    # have an automatic way of reading the data
    def _convert_default_files_to_json(self) -> None:
        """Converts default CSV files to JSON format."""
        # Check if JSON files exist to set data_available flag
        if self.distance_json_path.exists() and self.package_json_path.exists():
            self.data_available = True
            
        convert_distance_table_to_json(self.default_distance_table_path, self.distance_json_path)
        convert_package_file_to_json(self.default_package_file_path, self.package_json_path)
        
    def _display_header(self, menu_name=None) -> None:
        """Displays the CLI header dynamically based on the menu context."""
        if self.first_run:
            print("===== Welcome to the WGUPS Admin Console - Main Menu =====")
            self.first_run = False
        else:
            print(f"=========== WGUPS Admin Console - {menu_name} ===============")

    def _display_meta(self) -> None:
        """Displays meta information in the footer."""
        # Check for the existence of JSON files
        distance_exists = '[✓]' if os.path.exists(self.base_dir / "data" / "distance_table.json") else '[X]'
        package_exists = '[✓]' if os.path.exists(self.base_dir / "data" / "package_file.json") else '[X]'

        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"Distance Table {distance_exists}, Package File {package_exists} | Current Time: {current_time}\n")


    def run(self) -> None:
        """
        Runs the CLI application, allowing the user to navigate through menus and perform actions.
        This function delegates the showing of menus and handling of user input to the MenuManager.
        """
        while True:
            clear_screen()  # Clear the screen for a clean menu display each time
            self.main_menu_manager.show_menu_and_capture_choice()

            