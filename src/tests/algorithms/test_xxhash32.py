# Stdlib
import unittest
# Local
from lib.dsa.algorithms.xxHash import XXHash_32

class TestXXHash32(unittest.TestCase):
    """
    Test suite for the XXHash_32 algorithm.
    """

    def setUp(self):
        """
        Initialize test conditions.
        """
        self.test_passed = False

    def tearDown(self):
        """
        If the test doesn't raise an exception, it is considered successful.
        """
        if self.test_passed:
            print(f"{self.id()}: Success")

    def run(self, result=None):
        """
        Overrides the default run behavior to update test_passed based on the test result.
        """
        super().run(result)
        if result.wasSuccessful():
            self.test_passed = True
        else:
            self.test_passed = False


    def test_hash_string(self):
        """
        Test hashing of a string.
        """
        key = "test string hashing"
        expected_hash = 3795567459
        result = XXHash_32.hash(key)
        self.assertEqual(result, expected_hash, "Hashing string did not produce expected hash value.")

    def test_hash_integer(self):
        """
        Test hashing of an integer.
        """
        key = 123456789
        expected_hash = 2421873597  
        result = XXHash_32.hash(key)
        self.assertEqual(result, expected_hash, "Hashing integer did not produce expected hash value.")

    def test_hash_bytes(self):
        """
        Test hashing of a byte sequence.
        """
        key = b'\x01\x02\x03\x04\x05'
        expected_hash = 258619656 
        result = XXHash_32.hash(key)
        self.assertEqual(result, expected_hash, "Hashing bytes did not produce expected hash value.")

    def test_hash_with_seed(self):
        """
        Test hashing with a non-zero seed.
        """
        key = "seeded hash"
        seed = 42
        expected_hash =  3904641812
        result = XXHash_32.hash(key, seed)
        self.assertEqual(result, expected_hash, "Hashing with seed did not produce expected hash value.")
        
    def test_hash_with_zero_seed(self):
        """
        Test hashing with a non-zero seed.
        """
        key = "seedless hash"
        seed = 0
        expected_hash = 3242396756
        result = XXHash_32.hash(key, seed)
        self.assertEqual(result, expected_hash, "Hashing with seed did not produce expected hash value.")

    def test_hash_consistency(self):
        """
        Test that hashing the same value multiple times produces consistent results.
        """
        key = "apple berry"
        result1 = XXHash_32.hash(key)
        result2 = XXHash_32.hash(key)
        self.assertEqual(result1, result2, "Hashing the same value did not produce consistent results.")
