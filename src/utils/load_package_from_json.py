# Local
import json

def load_packages_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
