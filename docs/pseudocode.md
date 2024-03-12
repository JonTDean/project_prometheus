# WGUPS ACO Pseudocode
```python
function initializeHeuristicInfo(locations, endLocation):
    """
    1. Create an empty hash table to store the heuristic information
    2. For each location in the locations list:
        a. Calculate the heuristic value for the location (distance from the location to the end location)
        b. Add an entry to the hash table with the location as the key and the heuristic value as the value
    3. Return the initialized heuristic information hash table
    
    Example:
    - locations: ["Western Governors University", "International Peace Gardens", "Sugar House Park", ...]
    - endLocation: "Western Governors University"
    - heuristicInfo (hash table):
        - key: "Western Governors University", value: 0.0
        - key: "International Peace Gardens", value: 7.2
        - key: "Sugar House Park", value: 3.8
        - ...
    
    RUNTIME COMPLEXITY:
        - BIG-O: O(n)
        - Reasoning: The function iterates over the locations list once to calculate and store the heuristic values.
    SPACE COMPLEXITY:
        - BIG-O: O(n)
        - Reasoning: The function creates a hash table with an entry for each location, taking space proportional to the number of locations.
    """
    heuristicInfo = createHashTable()
    
    for each location in locations:
        heuristicValue = calculateDistance(location, endLocation)
        addToHashTable(heuristicInfo, location, heuristicValue)
    
    return heuristicInfo

function calculateDistance(location1, location2):
    """
    1. Look up the distance between location1 and location2 in the distance table
    2. Return the distance value
    
    Example:
    - location1: "Western Governors University"
    - location2: "International Peace Gardens"
    - Distance: 7.2 (retrieved from the distance table)
    
    RUNTIME COMPLEXITY:
        - BIG-O: O(1)
        - Reasoning: Looking up the distance between two locations in the distance table takes constant time.
    SPACE COMPLEXITY:
        - BIG-O: O(1)
        - Reasoning: The function returns a single distance value, taking constant extra space.
    """
    # Implementation details omitted for brevity
    # Assume the distance table is stored in a suitable data structure for efficient lookup
    return distanceTable[location1][location2]
```

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

```python
function antRouting(startLocation, endLocation, adjacencyMatrix, pheromoneMatrix, heuristicInfo, alpha, beta):
    """
    1. Initialize an empty path list to store the locations visited by the ant
    2. Set the current location to the start location
    3. While the current location is not the end location:
        a. Get the available next locations from the current location using the adjacency matrix
        b. Calculate the probability of moving to each available next location using the pheromone and heuristic information
        c. Select the next location based on the calculated probabilities
        d. Add the selected location to the path list
        e. Update the current location to the selected location
    4. Return the path list representing the route taken by the ant
    
    RUNTIME COMPLEXITY:
        - BIG-O: O(n^2)
        - Reasoning:
            The while loop runs until the end location is reached, which in the worst case could be all locations.
            Inside the loop, calculating probabilities and selecting the next location takes O(n) time.
            Therefore, the overall time complexity is O(n^2), where n is the number of locations.
    SPACE COMPLEXITY:
        - BIG-O: O(n)
        - Reasoning:
            The path list stores the locations visited by the ant, which in the worst case could be all locations.
            Therefore, the space complexity is O(n), where n is the number of locations.
    """
    path = []
    currentLocation = startLocation
    
    while currentLocation != endLocation:
		"""
		1. Get the row corresponding to the current location from the adjacency matrix
		2. Find the indices of the cells in the row that have a value other than INFINITY
		3. Return the list of available next locations
		
		RUNTIME COMPLEXITY:
			- BIG-O: O(n)
			- Reasoning: The function iterates over the row of the adjacency matrix, which has n elements.
		SPACE COMPLEXITY:
			- BIG-O: O(n)
			- Reasoning: The function returns a list of available next locations, which in the worst case could be all locations.
		"""
        availableLocations = getAvailableLocations(currentLocation, adjacencyMatrix)
		"""
		1. Initialize an empty list to store the probabilities
		2. For each available next location:
			a. Calculate the pheromone factor using the pheromone matrix and the alpha parameter
			b. Calculate the heuristic factor using the heuristic information and the beta parameter
			c. Calculate the probability by multiplying the pheromone factor and heuristic factor
			d. Add the calculated probability to the probabilities list
		3. Normalize the probabilities list to ensure they sum up to 1
		4. Return the normalized probabilities list
		
		RUNTIME COMPLEXITY:
			- BIG-O: O(n)
			- Reasoning: The function iterates over the available next locations, which in the worst case could be all locations.
		SPACE COMPLEXITY:
			- BIG-O: O(n)
			- Reasoning: The function returns a list of probabilities, which has the same length as the available next locations.
		"""
        probabilities = calculateProbabilities(
			currentLocation, 
			availableLocations, 
			pheromoneMatrix, 
			heuristicInfo, 
			alpha, 
			beta
		)
		"""
		1. Generate a random number between 0 and 1
		2. Iterate over the probabilities list and accumulate the probabilities
		3. If the accumulated probability exceeds the random number, return the corresponding location
		
		RUNTIME COMPLEXITY:
			- BIG-O: O(n)
			- Reasoning: The function iterates over the probabilities list, which has a length proportional to the number of available locations.
		SPACE COMPLEXITY:
			- BIG-O: O(1)
			- Reasoning: The function uses a constant amount of extra space for the random number and accumulated probability.
		"""
        nextLocation = selectNextLocation(probabilities)
        path.append(nextLocation)
        currentLocation = nextLocation
    
    return path
```

```python
# Pheromone Update Queue
function initializePheromoneUpdateQueue():
    """
    1. Create an empty min-heap to store the pheromone updates
    2. Return the initialized pheromone update queue
    
    RUNTIME COMPLEXITY:
        - BIG-O: O(1)
        - Reasoning: Initializing an empty min-heap takes constant time.
    SPACE COMPLEXITY:
        - BIG-O: O(1)
        - Reasoning: The function returns an empty min-heap, which initially takes constant space.
    """
    pheromoneUpdateQueue = createMinHeap()
    return pheromoneUpdateQueue

function addPheromoneUpdate(pheromoneUpdateQueue, location_i, location_j, pheromoneValue):
    """
    1. Create a pheromone update object with the given location_i, location_j, and pheromoneValue
    2. Insert the pheromone update object into the min-heap
    
    RUNTIME COMPLEXITY:
        - BIG-O: O(log k)
        - Reasoning: Inserting an element into a min-heap takes logarithmic time, where k is the number of elements in the heap.
    SPACE COMPLEXITY:
        - BIG-O: O(1)
        - Reasoning: The function adds a single pheromone update object to the min-heap, taking constant extra space.
    """
    pheromoneUpdate = createPheromoneUpdate(location_i, location_j, pheromoneValue)
    insertIntoMinHeap(pheromoneUpdateQueue, pheromoneUpdate)

function getNextPheromoneUpdate(pheromoneUpdateQueue):
    """
    1. If the pheromone update queue is empty, return None
    2. Otherwise, remove and return the minimum pheromone update from the min-heap
    
    RUNTIME COMPLEXITY:
        - BIG-O: O(log k)
        - Reasoning: Removing the minimum element from a min-heap takes logarithmic time, where k is the number of elements in the heap.
    SPACE COMPLEXITY:
        - BIG-O: O(1)
        - Reasoning: The function returns a single pheromone update object, taking constant extra space.
    """
    if isEmpty(pheromoneUpdateQueue):
        return None
    else:
        return removeMinFromMinHeap(pheromoneUpdateQueue)

```