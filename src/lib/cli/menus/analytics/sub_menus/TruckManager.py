class TruckManager:
    def __init__(self):
        # Initialize truck data structure here
        self.trucks = {}

    def add_truck(self, truck_id, truck_info):
        """Add or update truck information."""
        self.trucks[truck_id] = truck_info

    def get_truck_info(self, truck_id):
        """Retrieve information for a specific truck."""
        return self.trucks.get(truck_id, "Truck not found.")

