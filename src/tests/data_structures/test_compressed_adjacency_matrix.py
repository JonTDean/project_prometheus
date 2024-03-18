# Stdlib
import unittest
# Local
from src.tests.BaseTest import BaseTest
from src.lib.dsa.data_structures.compressed_adjacency_matrix import CompressedAdjacencyMatrix

class TestCompressedAdjacencyMatrix(BaseTest):
    """
    Test suite for the CompressedAdjacencyMatrix class.
    """

    def setUp(self):
        """
        Setup common test data used in the tests.
        """
        self.nodes = ['A', 'B', 'C', 'D']
        self.edges = [('A', 'B', 1.0), ('B', 'C', 2.0), ('C', 'D', 3.0)]
        self.matrix = CompressedAdjacencyMatrix(self.nodes, self.edges)

    def test_initialization(self):
        """
        Test initialization of the CompressedAdjacencyMatrix.
        """
        self.assertEqual(len(self.matrix.nodes), 4, "Incorrect number of nodes.")
        self.assertEqual(len(self.matrix.edges), 3, "Incorrect number of edges.")

    def test_apply_updates(self):
        """
        Test applying updates to the matrix.
        """
        self.matrix._queue_update('A', 'D', 4.0)
        self.matrix.apply_updates()
        weight = self.matrix.get_weight('A', 'D')
        self.assertEqual(weight, 4.0, "Update application failed.")

    def test_pheromone_decay(self):
        """
        Test pheromone decay on all edges.
        """
        self.matrix.apply_decay()
        # Check decayed weight
        for start_node, end_node, original_weight in self.edges:
            decayed_weight = self.matrix.get_weight(start_node, end_node)
            expected_weight = original_weight * self.matrix.decay_factor
            self.assertAlmostEqual(decayed_weight, expected_weight, msg=f"Decay failed for edge {start_node}-{end_node}.")

    def test_change_tracking(self):
        """
        Test tracking of changes.
        """
        self.matrix._queue_update('A', 'D', 4.0)
        changes = self.matrix.get_changes()
        self.assertIn(('update', 'A', 'D', 4.0), changes, "Change tracking failed.")

    def test_reset_changes(self):
        """
        Test resetting the change log.
        """
        self.matrix._queue_update('A', 'D', 4.0)
        self.matrix.reset_changes()
        changes = self.matrix.get_changes()
        self.assertEqual(len(changes), 0, "Change log reset failed.")

    def test_update_coalescing(self):
        """
        Test that multiple updates to the same edge are coalesced properly,
        ensuring that only the last update affects the final weight.
        """
        self.matrix._queue_update('A', 'B', 1.5)
        self.matrix._queue_update('A', 'B', 2.0)  # This update should override the previous one
        self.matrix.apply_updates()
        weight = self.matrix.get_weight('A', 'B')
        self.assertEqual(weight, 2.0, "Update coalescing failed. The weight does not match the last update made.")

    def test_dynamic_allocation(self):
        """
        Test dynamic allocation of blocks as edges are added, ensuring that
        blocks are created as needed to accommodate updates.
        """
        # This update should trigger the allocation of a new block that wasn't initially needed
        self.matrix._queue_update('A', 'D', 4.0)
        self.matrix.apply_updates()
        block_i, block_j = self.matrix.node_index['A'] // self.matrix.block_size, self.matrix.node_index['D'] // self.matrix.block_size
        self.assertIn(block_i, self.matrix.blocks, "Dynamic allocation failed. Block row missing.")
        self.assertIn(block_j, self.matrix.blocks[block_i], "Dynamic allocation failed. Block column missing.")

    def test_symmetric_compression(self):
        """
        Test symmetric compression by ensuring that the weight is the same regardless
        of the direction of the edge queried.
        """
        self.matrix._queue_update('A', 'D', 4.0)
        self.matrix.apply_updates()
        weight_ad = self.matrix.get_weight('A', 'D')
        weight_da = self.matrix.get_weight('D', 'A')
        self.assertEqual(weight_ad, weight_da, "Symmetric compression failed. Weights do not match in reverse direction.")

    def test_block_compression(self):
        """
        Test block compression efficiency by checking that the number of allocated
        blocks does not exceed the expected amount based on the number of nodes and
        the block size.
        """
        # Assuming a block size of 10, all nodes and edges should fit within a single block
        # due to the small size of the example graph
        expected_blocks = (len(self.nodes) + self.matrix.block_size - 1) // self.matrix.block_size
        self.matrix.apply_updates()  # Ensure all updates are applied
        actual_blocks = len(self.matrix.blocks)
        self.assertLessEqual(actual_blocks, expected_blocks, "Block compression inefficiency detected. More blocks allocated than expected.")
