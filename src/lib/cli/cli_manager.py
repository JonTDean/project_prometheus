class CLIManager:
    def show_main_menu(self):
        print("\nWelcome to the WGUPS Package System")
        print("\n3. Exit")
        choice: str = str(input("Enter choice: "))
        
        return choice

    def run(self):
        while True:
            user_choice: str = self.show_main_menu()

            if user_choice == "1":
                break
            elif user_choice == "2":
                break
            elif user_choice == "3" or user_choice.lower() == "exit":
                print("Exiting Task Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a valid option.")
