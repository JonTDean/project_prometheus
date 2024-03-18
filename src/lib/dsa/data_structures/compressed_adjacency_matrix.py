from typing import List, Tuple, Dict

class CompressedAdjacencyMatrix:
    """
    A class that represents a graph using a compressed adjacency matrix to efficiently
    store and manipulate sparse graphs. This representation is designed to minimize
    memory usage for graphs where the number of edges is significantly less than the
    square of the number of nodes. Additionally, it includes mechanisms for change
    tracking and pheromone decay, suitable for applications like Ant Colony Optimization algorithms.
    
    Attributes:
        nodes (List): A list of unique node identifiers in the graph.
        edges (List[Tuple]): A list of tuples representing edges in the graph, where each tuple is (start_node, end_node, weight).
        matrix (Dict): A deprecated attribute, kept for compatibility, but not used in current implementation.
        node_index (Dict): A dictionary mapping node identifiers to their respective index in the node list.
        block_size (int): The size of blocks used in compressing the adjacency matrix, affecting the granularity of compression.
        blocks (Dict): A nested dictionary structure storing the compressed adjacency matrix.
        update_queue (List[Tuple]): A queue of updates to be applied to the graph, where each update is a tuple (start_node, end_node, weight).
        change_log (List[Tuple]): A log of changes made to the graph for tracking modifications over time.
        decay_factor (float): The factor by which edge weights (pheromones) decay during the decay process.
        
    Methods:
        __init__(self, nodes: List, edges: List[Tuple], decay_factor: float = 0.95): Initializes a new instance of the CompressedAdjacencyMatrix.
        _create_index(self): Generates the node_index dictionary.
        _compress_matrix(self): Compresses the initial graph representation into the blocks structure.
        _queue_update(self, start_node, end_node, weight): Queues an update for later application to the graph.
        apply_updates(self): Applies all queued updates to the graph.
        _allocate_and_update_block(self, i: int, j: int, weight: float): Allocates blocks as needed and updates the weight of an edge within a block.
        get_weight(self, from_node, to_node): Retrieves the weight of the edge between two nodes, if it exists.
        apply_decay(self): Applies pheromone decay to all edges in the graph.
        get_changes(self): Retrieves a list of changes made to the graph since the last check.
        reset_changes(self): Clears the change log.
    """
    
    def __init__(self, nodes: List, edges: List[Tuple], decay_factor: float = 0.95):
        """
        Initializes a new instance of the CompressedAdjacencyMatrix class, setting up the internal
        structures based on the provided list of nodes and edges. It also initializes change tracking
        and sets the decay factor for pheromone decay.
        
        Parameters:
            nodes (List): The list of node identifiers in the graph.
            edges (List[Tuple]): The list of edges in the graph, where each edge is represented as a tuple (start_node, end_node, weight).
            decay_factor (float): The decay factor to be used in pheromone decay, defaults to 0.95.
        
        Complexity:
            Time: O(N + E), where N is the number of nodes and E is the number of edges, due to indexing and initial compression.
            Space: O(N + B), where B is the number of blocks allocated based on the block size and graph structure.
        """
        self.nodes = nodes
        self.edges = edges
        self.matrix = {}
        self.node_index = {}
        self.block_size = 10
        self.blocks = {}
        self.update_queue = []
        self.change_log = []  # Change tracking
        self.decay_factor = decay_factor  # Pheromone decay factor
        self._create_index()
        self._compress_matrix()

    def _create_index(self):
        """
        Generates a mapping from node identifiers to their respective indices. This index is used internally
        to efficiently locate nodes within the compressed structure.
        
        Complexity:
            Time: O(N), where N is the number of nodes.
            Space: O(N), for storing the index.
        """
        for index, node in enumerate(self.nodes):
            self.node_index[node] = index
    
    def _compress_matrix(self):
        """
        Compresses the initial graph represented by the edges list into a more memory-efficient
        block-based structure. This method initializes the compression process by queuing all
        provided edges for inclusion in the compressed adjacency matrix.
        
        Complexity:
            Time: O(E), where E is the number of edges, since each edge is queued for update.
            Space: O(1), not counting the space required for storing the updates themselves, which is handled separately.
        """
        for start_node, end_node, weight in self.edges:
            self._queue_update(start_node, end_node, weight)

    def _queue_update(self, start_node, end_node, weight):
        """
        Queues an update for later application to the graph. Each update represents an edge addition
        or modification, with the edge specified by its start and end nodes, and the weight representing
        the edge's weight or pheromone level.
        
        Parameters:
            start_node: The identifier of the edge's starting node.
            end_node: The identifier of the edge's ending node.
            weight: The weight or pheromone level to be associated with the edge.
        
        Complexity:
            Time: O(1), constant time to append an update to the queue.
            Space: O(U), where U is the number of updates queued, as each update takes a fixed amount of space.
        """
        self.update_queue.append((start_node, end_node, weight))
        # Record the change for tracking
        self.change_log.append(('update', start_node, end_node, weight))

    def apply_updates(self):
        """
        Applies all queued updates to the graph. This method processes each update in the queue,
        updating the compressed adjacency matrix to reflect the addition or modification of edges.
        Updates are applied in the order they were queued.
        
        Complexity:
            Time: O(U * log B), where U is the number of updates and B is the number of blocks, assuming block allocation is O(log B).
            Space: O(1), operates in constant space beyond the space required for the blocks themselves.
        """
        while self.update_queue:
            start_node, end_node, weight = self.update_queue.pop(0)
            i, j = self.node_index[start_node], self.node_index[end_node]
            if i > j:  # Maintain symmetry
                i, j = j, i
            self._allocate_and_update_block(i, j, weight)

    def _allocate_and_update_block(self, i: int, j: int, weight: float):
        """
        Allocates blocks as needed and updates the weight of an edge within a block. If the necessary blocks
        do not exist, they are created. Then, the edge weight is updated in the specified location within the
        block matrix.
        
        Parameters:
            i (int): The row index in the block matrix for the start node.
            j (int): The column index in the block matrix for the end node.
            weight (float): The weight or pheromone level to be set for the edge.
        
        Complexity:
            Time: O(1), assuming hash table insertions and lookups are O(1) on average.
            Space: O(B), where B is the number of blocks, as blocks are allocated dynamically.
        """
        block_i, block_j = i // self.block_size, j // self.block_size
        if block_i not in self.blocks:
            self.blocks[block_i] = {}
        if block_j not in self.blocks[block_i]:
            self.blocks[block_i][block_j] = {}
        self.blocks[block_i][block_j][(i % self.block_size, j % self.block_size)] = weight

    def get_weight(self, from_node, to_node):
        """
        Retrieves the weight of the edge between two nodes, if it exists. If no edge exists between
        the specified nodes, a default 'infinite' weight is returned to signify no connection.
        
        Parameters:
            from_node: The identifier of the starting node of the edge.
            to_node: The identifier of the ending node of the edge.
        
        Returns:
            The weight of the edge between the specified nodes, or float('inf') if no edge exists.
        
        Complexity:
            Time: O(1), assuming hash table lookups are O(1) on average.
            Space: O(1), operates in constant space.
        """
        i, j = self.node_index.get(from_node), self.node_index.get(to_node)
        if i is None or j is None:
            return float('inf')
        if i > j:
            i, j = j, i
        block_i, block_j = i // self.block_size, j // self.block_size
        block = self.blocks.get(block_i, {}).get(block_j, {})
        return block.get((i % self.block_size, j % self.block_size), float('inf'))

    def apply_decay(self):
        """
        Applies pheromone decay to all edges in the graph. This method iteratively reduces the weight
        of each edge by the decay factor, simulating the natural evaporation of pheromones over time.
        
        Complexity:
            Time: O(B * b^2), where B is the number of blocks and b is the block size, since each edge within each block must be updated.
            Space: O(1), operates in constant space beyond the initial storage requirements of the blocks.
        """
        for block_i in self.blocks:
            for block_j in self.blocks[block_i]:
                block = self.blocks[block_i][block_j]
                for key in block:
                    block[key] *= self.decay_factor  # Apply decay

    def get_changes(self):
        """
        Retrieves a list of changes made to the graph since the last check. This method allows for monitoring
        modifications to the graph, useful in applications where tracking the evolution of the graph is necessary.
        
        Returns:
            A list of tuples representing the changes made to the graph, with each tuple in the format (action, start_node, end_node, weight),
            where 'action' is the type of change (e.g., 'update').
        
        Complexity:
            Time: O(C), where C is the number of changes recorded.
            Space: O(1), returns a reference to the existing log without additional space allocation.
        """
        changes = self.change_log.copy()  # Return a copy to prevent external modifications
        return changes

    def reset_changes(self):
        """
        Clears the change log. This method is used after changes have been applied or checked,
        to reset the tracking log for the next set of updates.
        
        Complexity:
            Time: O(1), clearing the log is a constant time operation.
            Space: O(1), operates in constant space.
        """
        self.change_log.clear()

