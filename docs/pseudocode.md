# WGUPS ACO Pseudocode
```python
# Initialize the ACO Graph
function initializeACOGraph(numberOfLocations):
    """
	1. Create an empty adjacency matrix for graph representation
	
    2. The createMatrix function allows for a matrix of a given size to be created

	3. The matrix is initialized with a value of INFINITY for all cells
		in order to represent the absence of an edge between two locations

	4. The diagonal of the matrix is set to 0 to represent 
		the distance from a location to itself

	5. The getDistance function is used to populate the matrix 
		with the distances between locations
	
	RUNTIME:
		BIG-O: O(n^2) 
		Reasoning:
			Having two for loops shows us that the immediate complexity of
			of the function is O(n^2) where n is the number of locations
			However, the function is only called once at the beginning of the program
			so the overall complexity is O(n^2).
	"""
	adjacencyMatrix = createMatrix(numberOfLocations, numberOfLocations, value=INFINITY)
    
    # Populate the adjacency matrix with distances between locations
    for each location_i in numberOfLocations:
        for each location_j in numberOfLocations:
            if i == j:
				# Diagonal cells are set to 0
				# to represent the distance from a location to itself
                adjacencyMatrix[i][j] = 0
            else:
                adjacencyMatrix[i][j] = getDistance(location_i, location_j)
    return adjacencyMatrix
```