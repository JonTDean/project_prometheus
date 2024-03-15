import os

from lib.cli.utils.meta import UserBack, UserExit, exit_or_back_prompt, exit_process

def get_file_path(file_type: str) -> str:
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
        print("\nEnter 'exit' (e) to quit or 'back' (b) to return to the previous menu.")
        file_path = input(f"Please enter the fully qualified file path for the {file_type} (.csv): ")

        try:
            exit_or_back_prompt(file_path)
        except UserExit:
            exit_process()
        except UserBack:
            return None

        # Check if the provided file path exists and is a .csv file
        if os.path.exists(file_path) and file_path.endswith('.csv'):
            # Ask for confirmation to proceed
            confirm = input(f"Path entered: {file_path}\nProceed? (y/n): ").lower()
            if confirm == 'y':
                return file_path
            elif confirm == 'n':
                print("Operation cancelled. Please enter the file path again or choose 'back' to return.")
        else:
            print("Invalid file or format. Please ensure the file exists and is a '.csv' file.")
