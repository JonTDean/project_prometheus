# Stdlib
import json
# Local
from src.lib.dsa.data_structures.muxmux_hash_table import MuxMuxHashTable
from src.utils.load_package_from_json import load_packages_from_json

class DSPackage:
    def __init__(self, json_file_path):
        # load JSON data to determine its size for hash table initialization
        packages_data = load_packages_from_json(json_file_path)
        initial_size = len(packages_data)
        
        # Initialize the hash table with a size based on the number of packages
        # to ensure that the initial hash table is large enough.
        # - f(min_size) = initial_size / desired_load_factor
        desired_load_factor = 0.7
        min_size = int(initial_size / desired_load_factor)
        
        self.packages = MuxMuxHashTable(min_size=min_size, max_load_factor=0.7, min_load_factor=0.2)
        
        # Populate the hash table with package data
        self._populate(packages_data)

    def _populate(self, packages_data):
        for package in packages_data:
            package_id = int(package["id"])
            self.insert_package(package_id, package)

    def insert_package(self, package_id, details):
        self.packages.insert(package_id, details)
    
    def get_package_details(self, package_id):
        return self.packages.lookup(package_id)

    def view_all_packages(self):
        for key in self.packages.keys():
            package = self.get_package_details(key)
            print(f"Package {key}: {package}")