# Student ID: 011035744

# Stdlib
import sys
from pathlib import Path
import argparse
import unittest
project_root = Path(__file__).parent.resolve()
sys.path.append(str(project_root))
# Local
from lib.cli.cli_manager import CLIManager


class CustomTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        # You can modify this message to include whatever information you find useful.
        self.stream.writeln(f"SUCCESS: {test._testMethodName} - {test.shortDescription()}\n")

class CustomTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, resultclass=CustomTestResult, **kwargs)

def run_tests(test_dirs=None):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    if test_dirs:
        for dir in test_dirs:
            dir_path = project_root / 'tests' / dir
            discovered = loader.discover(start_dir=str(dir_path), pattern='test_*.py')
            suite.addTests(discovered)
    else:
        suite = loader.discover(start_dir=str(project_root / 'tests'), pattern='test_*.py')

    # Use CustomTestRunner instead of the default runner.
    runner = CustomTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CLI tool for WGUPS package delivery system.')
    parser.add_argument('-test', action='store_true', help='Run all tests in the tests folder')
    parser.add_argument('-dirs', nargs='*', help='Specify directories within the tests folder to run tests from')

    args = parser.parse_args()

    if args.test:
        run_tests(args.dirs)
    else:
        cli_manager = CLIManager()
        cli_manager.run()