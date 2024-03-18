# Stdlib
import json
import unittest
# Local
from src.lib.dsa.data_structures.muxmux_hash_table import MuxMuxHashTable
from src.tests.BaseTest import BaseTest
from src.utils.load_package_from_json import load_packages_from_json


class TestMuxMuxHashTable(BaseTest):
    """
    Test suite for the MuxMuxHashTable data structure.
    """

    @classmethod
    def setUpClass(cls):
        """
        Load JSON data once before all tests.
        """
        # Adjust the path to match your actual file location
        cls.packages = load_packages_from_json("/home/jon/programming/WGU/c950/data/package_file.json")

    def test_hash_table_with_json_data(self):
        """
        Test inserting and retrieving data from the MuxMuxHashTable using JSON data.
        """
        hash_table = MuxMuxHashTable(min_size=10, debug=True)

        # Insert each package into the hash table using its "id" as the key
        for package in self.packages:
            package_id = int(package["id"])  # Convert the ID to an integer for consistency
            hash_table.insert(package_id, package)

        # Retrieve each package from the hash table and assert that the retrieved data matches the original data
        for package in self.packages:
            package_id = int(package["id"])
            retrieved_data = hash_table.lookup(package_id)
            
            self.assertEqual(retrieved_data, package, f"Data mismatch for package ID {package_id}")
