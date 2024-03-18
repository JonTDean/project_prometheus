# Adjacency Matrix

## Goals:
The aim of this stage is to construct a detailed and functional representation of the WGUPS delivery network and initialize the core structures of the ACO algorithm. This involves setting up a graph to represent the delivery area, initializing a pheromone matrix to track path desirability, defining ant solutions, and preparing heuristic information storage. The completion of this stage will result in a robust framework ready for the implementation of the ACO algorithm's core logic.

## Tasks:

- [x] Matrix Compression
	https://people.cs.uchicago.edu/~risi/papers/MMCaistats.pdf Bad for mc but good source
	https://web.stanford.edu/~pilanci/papers/lplr.pdf
	
	- [x] Symmetric Compression
	https://www.stce.rwth-aachen.de/files/elearning/JacobianCompression_II.pdf

	- [x] Block Compression
	https://ronny.cswp.cs.technion.ac.il/wp-content/uploads/sites/54/2016/05/compress.pdf
	https://www.researchgate.net/publication/266153631_A_Block_Compression_Algorithm_for_Computing_Preconditioners


- [x] Pheremone Decay
	https://www.rose-hulman.edu/class/cs/csse453/archive/2011-12/presentations/PheromoneDecay.pdf

- [x] Update Coalescing
	https://arxiv.org/pdf/2011.08451.pdf

- [x] Dynamic Allocation
	https://users.cs.utah.edu/~kirby/Publications/dynamic-csr.pdf

- [x] Change Tracking
	https://codereview.stackexchange.com/questions/120496/a-graph-representation-of-adjacent-matrix-in-python
