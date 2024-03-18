## LocalHashTable for ACO Implementation

### To Do
- [ ] Design and implement dynamic resizing based on load factors to adapt to changing data volumes, maintaining operational efficiency.

- [ ] Consider concurrency and implement thread safety for parallel computations, crucial for leveraging multi-threaded optimizations in ACO heuristic calculations.

- [ ] Optimize for memory efficiency, especially in graph and pheromone matrix storage, to minimize the space complexity and enhance the scalability of ACO implementations.


---

### In Progress

- [ ] Implement a `keys` method for iterating over hash table keys, facilitating comprehensive access to heuristic information.

---

### Done
- [x] Implement robust collision handling using double hashing.
	- **Technical Description**: Double hashing employs a secondary hash function to compute an alternative hash when a collision occurs. Mathematically, the index for insertion or lookup is determined by:
	
	![\[ index = (h_1(key) + i \cdot h_2(key)) \mod table\_size \]](./images/insertion_lookup-double_hash.png)

	where \(h_1\) and \(h_2\) are the primary and secondary hash functions, respectively, \(i\) is the probe number (starting from 0), and \(table\_size\) is the size of the hash table.

	- **Features**:
		- Incorporated a secondary hash function (`xxHash_32`) to resolve collisions, enhancing the distribution uniformity and minimizing clustering.
		
		- Ensured that the secondary hash function's output is relatively prime to the table size, optimizing probe sequence effectiveness.
		
		- Added open addressing to systematically probe alternative slots until an empty slot is found, with an **asymptotic runtime** of O(1) in the best case and O(n) in the worst case, depending on the load factor and hash function quality.
		
		- Implemented bitwise XOR and Rotational mixing for combining hash functions, thus:
		 ![\[ H(key) = h_1(key) \oplus rotate\_left(h_2(key), r) \]](../images/double_hash_function.png)
		 
			where \(h_1\) is Murmur3, \(h_2\) is xxHash, \(\oplus\) denotes the bitwise XOR operation,, \(rotate\_left\) signifies left bitwise rotation, and \(r\) represents the bit rotation amount, enhancing the avalanche effect and key distribution.
		
		- Implemented a rehashing mechanism to dynamically resize the table when the load factor exceeds a predefined threshold, ensuring that performance degradation is minimized as data volume grows.
		
		- Ensured that the table size is always a prime number, a measure to minimize collisions due to common factors with hash values.

- [x] Define hash table structure with dynamic resizing capabilities, allowing the table to grow or shrink in response to changes in data volume, maintaining efficient access times.

- [x] Implement insertion function with collision handling, ensuring that new data can be added efficiently even as the table approaches its capacity limit.

- [x] Implement efficient lookup operations using the double hashing technique.