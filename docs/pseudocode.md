# WGUPS ACO Pseudocode
```python
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
	
	RUNTIME COMPLEXITY:
		- BIG-O: O(n^2) 
		- Reasoning:
			Having two for loops shows us that the immediate complexity of
			of the function is O(n^2) where n is the number of locations
			However, the function is only called once at the beginning of the program
			so the overall complexity is O(n^2).

	SPACE COMPLEXITY:
		- BIG-O: O(n^2)
		- Reasoning: The adjacency matrix storage requirement grows quadratically with the number of locations.
	"""

	# numberOfLocations is dictated by the incoming total number of locations
	# we can grab this from the heuristic information
	adjacencyMatrix = createMatrix(numberOfLocations, numberOfLocations, value=INFINITY)
    
    # Populate the adjacency matrix with distances between locations
    for each location_i in numberOfLocations:
        for each location_j in numberOfLocations:
            if i == j:
				# Diagonal cells are set to 0
				# to represent the distance from a location to itself
                adjacencyMatrix[i][j] = 0
            else:
				    """
					Retrieves the distance between two locations given f(ω_i, ω_j).
					
					RUNTIME COMPLEXITY:
					- BIG-O: O(1)
					- Reasoning: Distance retrieval is assumed to be a direct access operation, a lookup, thus constant time.
					"""
                adjacencyMatrix[i][j] = getDistance(location_i, location_j)
    return adjacencyMatrix
```

``` python
function initializePheromoneMatrix(numberOfLocations, initialPheromoneValue):
    """
    1. Create a 2D array to represent the pheromone matrix

    2. The createMatrix function allows for a matrix of a given size to be created

    3. The matrix is initialized with a uniform initial pheromone value for all cells
    
    RUNTIME COMPLEXITY:
        - BIG-O: O(n^2)
        - Reasoning:
            The createMatrix function internally uses nested loops to initialize the matrix,
            resulting in a time complexity of O(n^2), where n is the number of locations.
            However, this function is called only once at the beginning of the program.

    SPACE COMPLEXITY:
        - BIG-O: O(n^2)
        - Reasoning: The pheromone matrix storage requirement grows quadratically with the number of locations, as it is a full matrix representing the pheromone levels between all pairs of locations.
    """
    pheromoneMatrix = createMatrix(
		numberOfLocations, 
		numberOfLocations, 
		value=initialPheromoneValue
	)
    return pheromoneMatrix

```