# Analytics Plan for C950 NHP3 Task 2

## A. Develop a Hash Table

### Objective
Implement a custom hash table for storing package information.

### Plan
1. **Define Hash Table Structure**: Determine the hash table size and collision handling method (e.g., chaining or open addressing).
2. **Implement Insertion Function**: Create a function that takes the package ID and stores package details in the hash table.
3. **Testing**: Write unit tests for the insertion function to ensure correct placement and collision handling.

## B. Develop a Look-up Function

### Objective
Create a function to retrieve package information by package ID.

### Plan
1. **Implement Lookup Function**: Use the package ID to find and return package details.
2. **Error Handling**: Manage cases where a package ID does not exist.
3. **Testing**: Test the lookup function for accuracy and error handling.

## C. Original Program for Package Delivery

### Objective
Deliver all packages while adhering to logistical constraints.

### Plan
1. **Route Optimization**: Select or develop an algorithm for optimizing delivery routes.
2. **Package Loading Strategy**: Design logic for assigning packages to trucks.
3. **Delivery Simulation**: Simulate package delivery, recording times and updating statuses.
4. **Validation**: Ensure all packages meet their delivery deadlines.
5. **Refinement**: Analyze results and refine strategies for efficiency.