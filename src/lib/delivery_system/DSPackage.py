# Local
from lib.algorithms.data_structures.LocalHashTable import LocalHashTable
import json

class DSPackage:
    def __init__(self, json_file_path):
        self.packages = LocalHashTable(size=40)  # Adjust size as needed
        self._populate_from_json(json_file_path)
    
    def _populate_from_json(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for package in data:
                package_id = package["Package\nID"]
                # Clean and restructure the package data for insertion
                package_data = {
                    "address": package["Address"],
                    "city": package["City "].strip(),
                    "state": package["State"],
                    "zip": package["Zip"],
                    "deadline": package["Delivery\nDeadline"],
                    "weight": package["Weight\nKILO"],
                    "notes": package["page 1 of 1PageSpecial Notes"],
                    "status": "At the hub",  # Default status
                }
                self.insert_package(package_id, package_data)
    
    def insert_package(self, package_id, details):
        self.packages.insert(package_id, details)
    
    def get_package_details(self, package_id):
        return self.packages.lookup(package_id)
