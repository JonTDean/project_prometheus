# Local
from lib.cli.utils.meta import clear_screen, exit_process

#! Add methods for displaying analytics for:
#* 	- package deliveries
#       - Tasks:
#           - the total number of packages delivered
#               - If a time is selected then total number of packages up to that time
#* 	        - View the delivery status of any package at any time
#*               - Delivery status must include the time.
#*               - The delivery status should report the package as at the hub, en route, or delivered.
#* 	- trucks
#       - Tasks:
#*          - the total mileage traveled 
#               - by all trucks
#               - by a specific truck
#           - The city the truck is at by a certain time
#           - The packages on the truck at a certain time
#           - The status of the truck at a certain time
class AnalyticsManager:
    def __init__(self, cli_manager, package_manager, truck_manager):
        self.cli_manager = cli_manager
        self.package_manager = package_manager
        self.truck_manager = truck_manager
        
    def show_analytics_menu(self):
        """
        Displays the analytics menu and handles the user's choice for viewing different analytics.

        Parameters:
        - cli_manager: Instance of CLIManager class for UI operations.
        - menu_manager: Instance of MenuManager class for handling choices.
        """
        clear_screen()
        self.cli_manager._display_header("Analytics Menu")

        print("\n1. Package Analytics")
        print("2. Truck Analytics")

        print("m. Return to Main Menu")
        print("e. Exit Application")

        choice = input("\nEnter choice (1/2/m/e): ").lower()
        self._handle_analytics_choice(choice)
        
    def _handle_analytics_choice(self, choice):
        while True:
            if choice == "1":
                self.cli_manager.package_manager.show_package_menu()
                break
            elif choice == "2":
                self.cli_manager.truck_manager.show_truck_menu()
                break
            elif choice == "m":
                self.cli_manager.main_menu_manager.show_menu_and_capture_choice()
                break
            elif choice == "e":
                exit_process()
            else:
                print("Invalid choice. Please enter 1, 2, m, or e.")
                choice = input("\nEnter choice (1/2/m/e): ").lower()