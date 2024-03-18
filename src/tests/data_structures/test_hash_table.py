# Stdlib
import json
import unittest
# Local
from lib.dsa.data_structures.muxmux_hash_table import MuxMuxHashTable
from utils.load_package_from_json import load_packages_from_json

def test_hash_table_with_json_data(json_file_path):
    packages = load_packages_from_json(json_file_path)  # Load the JSON data into a list of dictionaries

    hash_table = MuxMuxHashTable(min_size=10)  # Adjust min_size as per your requirements

    # Insert each package into the hash table using its "id" as the key
    for package in packages:
        package_id = int(package["id"])  # Convert the ID to an integer for consistency
        hash_table.insert(package_id, package)
        print(f"Inserted package ID {package_id} into the hash table.")

    # Retrieve each package from the hash table and assert that the retrieved data matches the original data
    for package in packages:
        package_id = int(package["id"])
        retrieved_data = hash_table.lookup(package_id)
        
        # Assert that the data retrieved from the hash table matches the original package data
        assert retrieved_data == package, f"Data mismatch for package ID {package_id}"
        print(f"\nVerified package ID {package_id} retrieved correctly from the hash table.")
        print(f"Address: {package['address']} | City: {package['city']} | State: {package['state']} | Zip: {package['zip']} | Deadline: {package['deadline']} | Weight: {package['weight']} |\nNotes: {package['notes']}")

# Adjust the path to match your actual file location
test_hash_table_with_json_data("/home/jon/programming/WGU/c950/data/package_file.json")
