from lib.algorithms import VRPAlgorithm


class PackageManager:
    def __init__(self, algorithm: VRPAlgorithm):
        self.algorithm = algorithm
        self.packages = {}  # Store package information, e.g., using a simple dictionary or a custom hash table

    def add_package(self, package_id, package_info):
        self.packages[package_id] = package_info

    def get_package(self, package_id):
        return self.packages.get(package_id)

    def solve_vrp(self):
        # Use the selected VRP algorithm to solve the problem
        result = self.algorithm.solve(self.packages)
        return result
