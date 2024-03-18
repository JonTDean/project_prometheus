# file: tests/base_test.py
import sys
from pathlib import Path
import unittest

# Allows modules from 'lib' to be imported directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

class BaseTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self._test_success = None 

    def tearDown(self):
        super().tearDown()
        if self._test_success is True:
            print(f"{self.id()}: Success")
        elif self._test_success is False:
            print(f"{self.id()}: Failure or error occurred")
        else:
            print(f"{self.id()}: Test outcome not captured")

    def run(self, result=None):
        super().run(result)
        if result.wasSuccessful():
            self.test_passed = True
        else:
            self.test_passed = False
