# Stdlib
import json
# Local
from lib.dsa.data_structures.murmur_atkins_hash_table import MurMurAtkinsHashTable
from utils.load_package_from_json import load_packages_from_json

def test_hash_table_with_json_data(file_path):
    packages = load_packages_from_json("/home/jon/programming/WGU/c950/data/package_file.json")
    hash_table = MurMurAtkinsHashTable(min_size=10, max_load_factor=0.7, min_load_factor=0.2)

    # Dynamically identify and insert each package into the hash table
    for package in packages:
        # Assuming the first key in each dictionary is the package ID
        package_id_key = next(iter(package))
        package_id = package[package_id_key]
        
        # Assuming the rest of the dictionary contains the package data
        # and you want to store this entire dictionary as the value
        package_data = {k: v for k, v in package.items() if k != package_id_key}

        hash_table.insert(package_id, package_data)

    # Optionally, print all keys and their values to verify insertion
    for key in hash_table.keys():
        value = hash_table.lookup(key)
        print(f"Key: {key}, Value: {value}")
    
    # Verify insertion by attempting to retrieve each package
    retrieval_success = True
    for package in packages:
        retrieved_data = hash_table.lookup(package['id'])
        if retrieved_data != package['data']:
            print(f"Error: Data mismatch for package ID {package['id']}. Expected: {package['data']}, Found: {retrieved_data}")
            retrieval_success = False
    
    if retrieval_success:
        print("All packages retrieved successfully!")
    else:
        print("There were errors in package retrieval.")

# Adjust the path to match your actual file location
test_hash_table_with_json_data("/home/jon/programming/WGU/c950/data/package_file.json")
