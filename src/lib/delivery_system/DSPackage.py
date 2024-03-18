# Stdlib
import json
# Local
from lib.dsa.data_structures.murmur_atkins_hash_table import MurMurAtkinsHashTable
from utils.load_package_from_json import load_packages_from_json

class DSPackage:
    def __init__(self, json_file_path):
        # Initialize Hash Table
        packages = load_packages_from_json("/home/jon/programming/WGU/c950/data/package_file.json")
        # hash_table = MurMurAtkinsHashTable(size=40)  # Adjust size as needed
        # self._populate_from_json(json_file_path)
    
    # def _populate_from_json(self, file_path):
    #     with open(file_path, 'r') as file:
    #         data = json.load(file)
    #         for package in data:
    #             package_id = package["id"]
    #             # Clean and restructure the package data for insertion
    #             package_data = {
    #                 "address": package["address"],
    #                 "city": package["city"].strip(),
    #                 "state": package["state"],
    #                 "zip": package["zip"],
    #                 "deadline": package["deadline"],
    #                 "weight": package["weight"],
    #                 "notes": package["notes"],
    #                 "status": "At the hub",  # Default status
    #             }
    #             self.insert_package(package_id, package_data)
    
    # def insert_package(self, package_id, details):
    #     self.packages.insert(package_id, details)
    
    # def get_package_details(self, package_id):
    #     return self.packages.lookup(package_id)
