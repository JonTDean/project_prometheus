from lib.cli.utils.meta import clear_screen


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

        print("1. Package Analytics")
        print("2. Truck Analytics")

        print("b. Return to Main Menu")

        choice = input("Enter choice (1/2/b): ").lower()
        self.handle_analytics_choice(choice)
        
    def handle_analytics_choice(self, cli_manager, choice):
        # Logic to handle user choice
        if choice == "1":
            print("Package analytics placeholder.")
        elif choice == "2":
            print("Truck analytics placeholder.")
        elif choice == "b":
            # Invoke the main menu display method
            self.cli_manager.show_main_menu()
        else:
            print("Invalid choice. Please enter a valid option.")
            
            
#=======================================================================================================================
#! Add methods for displaying analytics for:
#* 	- trucks
#       - Tasks:
#*          - the total mileage traveled 
#               - by all trucks
#               - by a specific truck
#           - The city the truck is at by a certain time
#           - The packages on the truck at a certain time
#           - The status of the truck at a certain time
#* 	- package deliveries
#       - Tasks:
#           - the total number of packages delivered
#               - If a time is selected then total number of packages up to that time
#* 	        - View the delivery status of any package at any time
#*               - Delivery status must include the time.
#*               - The delivery status should report the package as at the hub, en route, or delivered.
