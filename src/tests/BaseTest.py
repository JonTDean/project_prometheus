# file: tests/base_test.py
import sys
from pathlib import Path
import unittest

# Allows modules from 'lib' to be imported directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.test_passed = False

    def tearDown(self):
        if self.test_passed:
            print(f"{self.id()}: Success")

    def run(self, result=None):
        super().run(result)
        if result.wasSuccessful():
            self.test_passed = True
        else:
            self.test_passed = False
