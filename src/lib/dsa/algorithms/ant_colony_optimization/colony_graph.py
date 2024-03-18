from lib.dsa.data_structures.compressed_adjacency_matrix import AdjacencyMatrix


class ColonyGraph:
    def __init__(self, json_data):
        self.adjacency_matrix = AdjacencyMatrix(json_data)
        # Initialize pheromone levels or other ACO-related data structures here

    # Example: Method to calculate the cost of a given route
    def calculate_route_cost(self, route):
        cost = 0
        for i in range(len(route) - 1):
            from_hub = route[i]
            to_hub = route[i + 1]
            cost += self.adjacency_matrix.get_distance(from_hub, to_hub)
        return cost


