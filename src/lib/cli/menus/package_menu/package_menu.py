from lib.cli.package_manager import PackageManager


class PackageMenu:
    def __init__(self, package_manager: PackageManager):
        self.package_manager = package_manager

    def display_package_info(self, package_id):
        package_info = self.package_manager.get_package(package_id)
        if package_info:
            for key, value in package_info.items():
                print(f"{key}: {value}")
        else:
            print("Package not found.")

    def solve_vrp_and_display_results(self):
        results = self.package_manager.solve_vrp()
        print("VRP Solution:")
        print(results)
