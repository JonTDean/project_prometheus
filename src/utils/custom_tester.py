# Stdlib
import unittest

class CustomTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.writeln(f"SUCCESS: {test._testMethodName} - {test.shortDescription()}\n")

class CustomTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, resultclass=CustomTestResult, **kwargs)

def run_tests(project_root, test_paths=None, test_funcs=None):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    tests_root = project_root / 'tests'

    if test_paths:
        for path in test_paths:
            full_path = tests_root / path

            if full_path.is_dir():
                discovered = loader.discover(start_dir=str(full_path), pattern='test_*.py')
                suite.addTests(discovered)
            elif full_path.is_file() and full_path.suffix == '.py':
                if test_funcs:  # If specific functions are targeted within the file
                    for func in test_funcs:
                        module_path = full_path.relative_to(project_root).with_suffix('')
                        dotted_path = str(module_path).replace('/', '.').replace('\\', '.') + '.' + func
                        print(f"Attempting to load: {dotted_path}")  # Debug print
                        try:
                            discovered = loader.loadTestsFromName(dotted_path)
                            suite.addTests(discovered)
                        except Exception as e:
                            print(f"Warning: Could not load test '{func}' from '{path}'. Error: {e}")
                else:
                    module_path = full_path.relative_to(project_root).with_suffix('')
                    dotted_path = str(module_path).replace('/', '.').replace('\\', '.')
                    discovered = loader.loadTestsFromName(dotted_path)
                    suite.addTests(discovered)
            else:
                print(f"Warning: {path} is not a valid directory or Python test file.")
    else:
        suite = loader.discover(start_dir=str(tests_root), pattern='test_*.py')

    runner = CustomTestRunner(verbosity=2)
    runner.run(suite)