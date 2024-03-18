# Adjust the import paths according to your project structure
from src.lib.cli.utils.meta import clear_screen, exit_process

class PackageManager:
    def __init__(self, cli_manager, ds_package):
        self.cli_manager = cli_manager
        self.ds_package = ds_package

    def show_package_menu(self):
        while True:
            clear_screen()
            self.cli_manager._display_header("Package Management Menu")
            
            print("\n1. View Package Details")
            print("2. View All Packages")
            print("m. Back to Main Menu")
            print("e. Exit Application")
            
            
            choice = input("\nEnter your choice: ").lower()
            if choice in ['1', '2', 'm', 'e']:
                self._handle_package_analytics_choice(choice)
            else:
                print("Invalid choice. Please try again.")
    
    def _handle_package_analytics_choice(self, choice: str):
        if choice == "1":
            package_id = input("Enter Package ID: ")
            self.view_package_details(package_id)
        elif choice == "2":
            self.view_all_packages()
        elif choice == 'm':
            self.cli_manager.main_menu_manager.show_menu_and_capture_choice()
        elif choice == "exit" or choice == "e":
            exit_process()
            
    def view_package_details(self, package_id):
        try:
            package_id = int(package_id)  # Ensure the package_id is an integer
            package = self.ds_package.get_package_details(package_id)
            if package:
                print(f"\nDetails for package {package_id}: {package}")
            else:
                print("\nPackage not found.")
        except ValueError:
            print("\nInvalid package ID. Please enter a numeric ID.")
        input("\nPress Enter to continue...")  # Pause before returning to the menu

    def view_all_packages(self):
        self.ds_package.view_all_packages()
        input("\nPress Enter to continue...")  # Pause before returning to the menu