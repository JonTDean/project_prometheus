# C950 NHP3 Task 2 


## WGU Course Specs: C950 Data Structures and Algorithms II
### Assumptions

- Each truck can carry a maximum of 16 packages, and the ID number of each package is unique.
	- Truck Capacity > 1 && Truck Capacity <= 16
	- `for each Truck in TruckList Truck.PackageID == Unique` `

- The trucks travel at an average speed of 18 miles per hour and have an infinite amount of gas with no need to stop.
	- Truck.Speed == 18
	- Truck.Fuel == Infinite

- There are no collisions.
	- Path.Collisions == False

- Three trucks and two drivers are available for deliveries. Each driver stays with the same truck as long as that truck is in service.
	- TruckList.Count == 3
	- DriverList.Count == 2
	- If Truck.Status == EnRoute, Driver.Status == EnRoute

- Drivers leave the hub no earlier than 8:00 a.m., with the truck loaded, and can return to the hub for packages if needed.
	- Driver.Time >= 8:00 
	- Driver.Status == EnRoute

- The delivery and loading times are instantaneous (i.e., no time passes while at a delivery or when moving packages to a truck at the hub). This time is factored into the calculation of the average speed of the trucks.
	- Time.Delivery == Instantaneous
	- Time.Loading == Instantaneous
	
- There is up to one special note associated with a package.
	- Truck.Special

- The delivery address for package #9, Third District Juvenile Court, is wrong and will be corrected at 10:20 a.m. WGUPS is aware that the address is incorrect and will be updated at 10:20 a.m. However, WGUPS does not know the correct address (410 S. State St., Salt Lake City, UT 84111) until 10:20 a.m.

- The distances provided in the “WGUPS Distance Table” are equal regardless of the direction traveled.
	- Distances are the same in both directions.
	
-  The day ends when all 40 packages have been delivered.

### Requirements (WGU Course Material, 2023)

- [x] A - Develop a hash table, without using any additional libraries or classes, that has an insertion function that takes the package ID as input and inserts each of the following data components into the hash table:

	- [x] delivery address
	- [x] delivery deadline
	- [x] delivery city
	- [x] delivery zip code
	- [x] package weight
	- [x] delivery status (i.e., at the hub, en route, or delivered), including the delivery time

- [x] B - Develop a look-up function that takes the package ID as input and returns each of the following corresponding data components:

	- [x] delivery address
	- [x] delivery deadline
	- [x] delivery city
	- [x] delivery zip code
	- [x] package weight
	- [x] delivery status (i.e., at the hub, en route, or delivered), including the delivery time

- [x] C - Write an original program that will deliver all packages and meet all requirements using the attached supporting documents “Salt Lake City Downtown Map,” “WGUPS Distance Table,” and “WGUPS Package File.”

	- [x] Create an identifying comment within the first line of a file named “main.py” that includes your student ID.
	- [x] Include comments in your code to explain both the process and the flow of the program.

- [ ] D -  Provide an intuitive interface for the user to view the delivery status (including the delivery time) of any package at any time and the total mileage traveled by all trucks. (The delivery status should report the package as at the hub, en route, or delivered. Delivery status must include the time.)

	- [ ] Provide screenshots to show the status of all packages loaded onto each truck at a time between 8:35 a.m. and 9:25 a.m.
	- [ ] Provide screenshots to show the status of all packages loaded onto each truck at a time between 9:35 a.m. and 10:25 a.m.
	- [ ] Provide screenshots to show the status of all packages loaded onto each truck at a time between 12:03 p.m. and 1:12 p.m.

- [ ] E - Provide screenshots showing successful completion of the code that includes the total mileage traveled by all trucks.

- [ ] F - Justify the package delivery algorithm used in the solution as written in the original program by doing the following:

	- [ ] Describe two or more strengths of the algorithm used in the solution.
	- [ ] Verify that the algorithm used in the solution meets all requirements in the scenario.
	- [ ] Identify two other named algorithms that are different from the algorithm implemented in the solution and would meet all requirements in the scenario.
		- [ ] Describe how both algorithms identified in part F3 are different from the algorithm used in the solution.

- [ ] G - Describe what you would do differently, other than the two algorithms identified in part F3, if you did this project again, including details of the modifications that would be made.

- [ ] H - Verify that the data structure used in the solution meets all requirements in the scenario.

	- [ ] Identify two other data structures that could meet the same requirements in the scenario.
		- [ ] Describe how each data structure identified in H1 is different from the data structure used in the solution.