# Local
from lib.cli.utils.meta import clear_screen


class PackageManager:
    def __init__(self, cli_manager, ds_package):
        self.cli_manager = cli_manager
        self.ds_package = ds_package

    def show_package_menu(self):
        clear_screen()
        self.cli_manager._display_header("Package Management Menu")
        
        print("\n1. View Package Details")
        print("2. View All Packages")
        print("m. Back to Main Menu")
        
        choice = input("\nEnter your choice: ").lower()
        self._handle_package_analytics_choice(choice)
    
    def _handle_package_analytics_choice(self, choice: str):
        while True:
            if choice == "1":
                package_id = input("Enter Package ID: ")
                self.view_package_details(package_id)
                break
            elif choice == "2":
                self.view_all_packages()
                break
            elif choice == 'm':
                self.cli_manager.main_menu_manager.show_menu_and_capture_choice()
            else:
                print("Invalid choice. Please try again.")
                input("\nEnter your choice: ")

    def view_package_details(self, package_id):
        package = self.ds_package.get_package_details(package_id)
        if package:
            print(f"Details for package {package_id}: {package}")
        else:
            print("Package not found.")

    def view_all_packages(self):
        # Assuming DSPackage or HashTable class has a method to iterate all packages
        for package_id in self.ds_package.packages.keys():
            package = self.ds_package.get_package_details(package_id)
            print(f"Package {package_id}: {package}")
