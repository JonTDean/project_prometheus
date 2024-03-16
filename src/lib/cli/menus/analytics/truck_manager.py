class TruckManager:
    def __init__(self, cli_manager, ds_truck):
        self.cli_manager = cli_manager
        self.ds_truck = ds_truck

    def add_truck(self, truck_id, truck_info):
        print("\nTruck Management Menu")

        