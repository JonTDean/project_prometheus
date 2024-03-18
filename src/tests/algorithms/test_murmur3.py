# Local
from src.tests.BaseTest import BaseTest
from src.lib.dsa.algorithms.hashing.murmur_3 import Murmur3_32

class TestMurmur3_32(BaseTest):
    """
    Test suite for the Murmur3_32 algorithm.
    """

    def test_hash_string(self):
        """
        Test hashing of a string.
        """
        key = "test string hashing"
        seed = 42 
        expected_hash = 2295284957
        result = Murmur3_32.hash(key, seed=seed, debug=True)
        self.assertEqual(result, expected_hash, "Hashing string did not produce expected hash value.")

    def test_hash_integer(self):
        """
        Test hashing of an integer.
        """
        key = 123456789
        seed = 42
        expected_hash = 2435864455 
        result = Murmur3_32.hash(key, seed=seed, debug=True)
        self.assertEqual(result, expected_hash, "Hashing integer did not produce expected hash value.")

    def test_hash_bytes(self):
        """
        Test hashing of a byte sequence.
        """
        key = b'\x01\x02\x03\x04\x05'
        seed = 42
        expected_hash = 1057704281
        result = Murmur3_32.hash(key, seed=seed, debug=True)
        self.assertEqual(result, expected_hash, "Hashing bytes did not produce expected hash value.")

    def test_hash_with_seed(self):
        """
        Test hashing with a non-zero seed.
        """
        key = "seeded hash"
        seed = 42
        expected_hash = 1797170608
        result = Murmur3_32.hash(key, seed, debug=True)
        self.assertEqual(result, expected_hash, "Hashing with seed did not produce expected hash value.")
        
    def test_hash_with_zero_seed(self):
        """
        Test hashing with a non-zero seed.
        """
        key = "seedless hash"
        seed = 0
        expected_hash = 1002887161
        result = Murmur3_32.hash(key, seed, debug=True)
        self.assertEqual(result, expected_hash, "Hashing with seed did not produce expected hash value.")

    def test_hash_consistency(self):
        """
        Test that hashing the same value multiple times produces consistent results.
        """
        key = "apple berry"
        seed = 42
        result1 = Murmur3_32.hash(key, seed, debug=True)
        result2 = Murmur3_32.hash(key, seed, debug=True)
        self.assertEqual(result1, result2, "Hashing the same value did not produce consistent results.")
