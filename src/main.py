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

def run_tests():
    """Runs all the tests found in the 'tests' directory."""
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(project_root / 'tests'), pattern='test_*.py')
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CLI tool for WGUPS package delivery system.')
    parser.add_argument('-test', action='store_true', help='Run all tests in the tests folder')
    args = parser.parse_args()

    if args.test:
        run_tests()
    else:
        cli_manager = CLIManager()
        cli_manager.run()
