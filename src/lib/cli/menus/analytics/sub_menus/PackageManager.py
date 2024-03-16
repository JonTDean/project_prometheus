class PackageManager:
    def __init__(self):
        # Initialize package data structure here
        self.packages = {}

    def add_package(self, package_id, package_info):
        """Add or update package information."""
        self.packages[package_id] = package_info

    def get_package_info(self, package_id):
        """Retrieve information for a specific package."""
        return self.packages.get(package_id, "Package not found.")

