# WGUPS ACO Pseudocode
```python
function initializeHeuristicInfo(locations, endLocation):
    """
    1. Create an empty hash table to store the heuristic information
    
	2. For each location in the locations list:
        a. Calculate the heuristic value for the location (distance from the location to the end location)
        b. Add an entry to the hash table with the location as the key and the heuristic value as the value
    
	3. Return the initialized heuristic information hash table (Converted from the WGUPS Distance Table)
    
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
        heuristicValue = calculateDistance(location, endLocation)
        addToHashTable(heuristicInfo, location, heuristicValue)
    
    return heuristicInfo
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
# Ant Decision Queue
function initializeAntDecisionQueue():
    """
    1. Create an empty Fibonacci heap to store the ant decisions
    
	2. Return the initialized ant decision queue
    
    RUNTIME COMPLEXITY:
        - BIG-O: O(1)
        - Reasoning: Initializing an empty Fibonacci heap takes constant time.
    SPACE COMPLEXITY:
        - BIG-O: O(1)
        - Reasoning: The function returns an empty Fibonacci heap, which initially takes constant space.
    """
	
    antDecisionQueue = createFibonacciHeap()
    return antDecisionQueue

```

```python
function runACO(startLocation, endLocation, locations, distanceTable, numAnts, numIterations, alpha, beta, evaporationRate):
    """
    1. Initialize the ACO graph using the locations and distance table

    2. Initialize the pheromone matrix with initial pheromone values

    3. Initialize the heuristic information using the locations and end location

    4. Create an empty list to store the best route found

    5. For each iteration:
        a. Create an empty list to store the routes for the current iteration
        b. For each ant:
            i. Perform ant routing to find a route from the start location to the end location
            ii. Add the found route to the current iteration's routes list
        c. Update the pheromone matrix based on the routes found in the current iteration
        d. Evaporate the pheromone values in the pheromone matrix
        e. Find the best route among the current iteration's routes
        f. If the current best route is better than the overall best route, update the overall best route

    6. Visualize the best route found

    7. Return the best route
    
    RUNTIME COMPLEXITY:
        - BIG-O: O(numIterations * numAnts * n^2)
        - Reasoning:
            - The outer loop runs for numIterations
            - For each iteration, there is a loop that runs for numAnts
            - Inside the ant loop, the ant routing function has a complexity of O(n^2)
            - The pheromone update and evaporation operations have a complexity of O(n^2)
            - Therefore, the overall complexity is O(numIterations * numAnts * n^2)

    SPACE COMPLEXITY:
        - BIG-O: O(n^2)
        - Reasoning:
            - The ACO graph and pheromone matrix require O(n^2) space
            - The heuristic information requires O(n) space
            - The space required for storing routes is O(numAnts * n) in each iteration
            - Therefore, the overall space complexity is O(n^2)
    """
    graph = initializeACOGraph(locations)
    pheromoneMatrix = initializePheromoneMatrix(len(locations), initialPheromoneValue)
    heuristicInfo = initializeHeuristicInfo(locations, endLocation)
    bestRoute = []

    for i in range(numIterations):
        iterationRoutes = []
        
        for j in range(numAnts):
            route = antRouting(startLocation, endLocation, graph, pheromoneMatrix, heuristicInfo, alpha, beta)
            iterationRoutes.append(route)
		"""
		1. Retrieve the pheromone updates from the pheromoneUpdateQueue

		2. Apply the pheromone updates to the corresponding cells in the pheromoneMatrix
		
		RUNTIME COMPLEXITY:
			- BIG-O: O(k), where k is the number of pheromone updates in the queue
			- Reasoning:
				The function iterates over the pheromone updates in the queue and applies them to the matrix.
				The time complexity depends on the number of updates in the queue.
		SPACE COMPLEXITY:
			- BIG-O: O(1)
			- Reasoning: The function uses the existing pheromoneMatrix and does not require additional space.
		"""
        updatePheromoneMatrix(pheromoneMatrix, iterationRoutes)
		"""
		1. Iterate over each cell in the pheromoneMatrix

		2. Reduce the pheromone value of each cell by the evaporationRate
		
		RUNTIME COMPLEXITY:
			- BIG-O: O(n^2)
			- Reasoning:
				The function uses nested loops to iterate over each cell in the matrix,
				resulting in a time complexity of O(n^2), where n is the number of locations.

		SPACE COMPLEXITY:
			- BIG-O: O(1)
			- Reasoning: The function modifies the existing pheromoneMatrix in-place and does not require additional space.
		"""
        evaporatePheromone(pheromoneMatrix, evaporationRate)
        
        currentBestRoute = findBestRoute(iterationRoutes)
        if isBetterRoute(currentBestRoute, bestRoute):
            bestRoute    
	"""
    1. Create a visualization of the route using the visualization lib

    2. Display the visualization
    
   RUNTIME COMPLEXITY:
        - BIG-O: O(n)
        - Reasoning: The visualization process typically is simply iterating over the locations in the route

    SPACE COMPLEXITY:
        - BIG-O: O(n)
        - Reasoning: The space required for the visualization depends on the number of locations in the route
    """
    visualizeRoute(bestRoute)
    return bestRoute

```

```python
class Package:
    """
    Represents a package in the delivery system.
    
    Attributes:
        packageID: The unique identifier of the package.
        address: The delivery address of the package.
        city: The delivery city of the package.
        state: The delivery state of the package.
        zip: The delivery zip code of the package.
        deliveryDeadline: The deadline for delivering the package.
        weightKilo: The weight of the package in kilograms.
        specialNotes: Any special notes or instructions for the package.
        status: The current status of the package (e.g., "at the hub", "en route", "delivered").
        deliveryTime: The actual delivery time of the package (if delivered).
    """
    
    def __init__(self, packageID, address, city, state, zip, deliveryDeadline, weightKilo, specialNotes):
        """
        Initializes a new instance of the Package class.
        
        Parameters:
            packageID: The unique identifier of the package.
            address: The delivery address of the package.
            city: The delivery city of the package.
            state: The delivery state of the package.
            zip: The delivery zip code of the package.
            deliveryDeadline: The deadline for delivering the package.
            weightKilo: The weight of the package in kilograms.
            specialNotes: Any special notes or instructions for the package.
        """
        self.packageID = packageID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deliveryDeadline = deliveryDeadline
        self.weightKilo = weightKilo
        self.specialNotes = specialNotes
        self.status = "at the hub"
        self.deliveryTime = None
    
    def updateStatus(self, newStatus, deliveryTime=None):
        """
        Updates the status of the package.
        
        Parameters:
            newStatus: The new status of the package.
            deliveryTime: The actual delivery time of the package (if applicable).
        """
        self.status = newStatus
        self.deliveryTime = deliveryTime
    
    def getDeliveryDetails(self):
        """
        Retrieves the delivery details of the package.
        
        Returns:
            tuple: A tuple containing the package's address, city, state, zip, delivery deadline, weight, and special notes.
        """
        return (self.address, self.city, self.state, self.zip, self.deliveryDeadline, self.weightKilo, self.specialNotes)

class DeliveryManagementSystem:
    """
    Represents the delivery management system.
    
    Attributes:
        packages: A dictionary storing the packages, with package IDs as keys and Package objects as values.
    """
    
    def __init__(self):
        """
        Initializes a new instance of the DeliveryManagementSystem class.
        """
        self.packages = {}
    
    def addPackage(self, package):
        """
        Adds a package to the delivery management system.
        
        Parameters:
            package (Package): The package to be added.
        """
        self.packages[package.packageID] = package
    
    def getPackage(self, packageID):
        """
        Retrieves a package from the delivery management system based on the package ID.
        
        Parameters:
            packageID: The ID of the package to retrieve.
        
        Returns:
            Package: The package object corresponding to the given package ID, or None if not found.
        """
        return self.packages.get(packageID)
    
    def updatePackageStatus(self, packageID, newStatus, deliveryTime=None):
        """
        Updates the status of a package in the delivery management system.
        
        Parameters:
            packageID: The
	```