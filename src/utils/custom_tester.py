# Stdlib
import unittest


class CustomTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        # You can modify this message to include whatever information you find useful.
        self.stream.writeln(f"SUCCESS: {test._testMethodName} - {test.shortDescription()}\n")

class CustomTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, resultclass=CustomTestResult, **kwargs)


def run_tests(project_root, test_paths=None):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    tests_root = project_root / 'tests'

    if test_paths:
        for path in test_paths:
            full_path = tests_root / path

            # Check if the path is a directory; if so, discover all tests within it.
            if full_path.is_dir():
                discovered = loader.discover(start_dir=str(full_path), pattern='test_*.py')
                suite.addTests(discovered)
            # Check if the path is a file; if so, load the specific test file.
            elif full_path.is_file():
                if full_path.suffix == '.py':
                    # We need to convert the file path to a module path for loader.loadTestsFromName.
                    module_path = full_path.relative_to(project_root).with_suffix('')
                    dotted_path = str(module_path).replace('/', '.').replace('\\', '.')
                    discovered = loader.loadTestsFromName(dotted_path)
                    suite.addTests(discovered)
            else:
                print(f"Warning: {path} is not a valid directory or Python test file.")
    else:
        # Discover and run all tests if no specific paths are provided.
        suite = loader.discover(start_dir=str(tests_root), pattern='test_*.py')

    # Use CustomTestRunner instead of the default runner.
    runner = CustomTestRunner(verbosity=2)
    runner.run(suite)