# Student ID: 011035744

# Stdlib
import sys
from pathlib import Path
import argparse
## Fix for relative imports
project_root = Path(__file__).parent.resolve()
sys.path.append(str(project_root))

# Local
from utils.custom_tester import run_tests
from lib.cli.cli_manager import CLIManager

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CLI tool for WGUPS package delivery system.')
    parser.add_argument('-test', action='store_true', help='Run all tests in the tests folder')
    parser.add_argument('-dirs', nargs='*', help='Specify directories within the tests folder to run tests from')

    args = parser.parse_args()

    if args.test:
        # Corrected to pass project_root
        run_tests(project_root, args.dirs)
    else:
        cli_manager = CLIManager()
        cli_manager.run()