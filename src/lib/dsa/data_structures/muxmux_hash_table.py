from lib.dsa.algorithms.sieve_of_atkin import sieve_of_atkin
from lib.dsa.algorithms.murmur_3 import Murmur3


class MuxMuxHashTable:
    def __init__(self, min_size, max_load_factor=0.7, min_load_factor=0.2):
        """
        Initializes a hash table with dynamic resizing based on [max, min] load factor.

        The hash table's size is determined by finding the next prime number greater
        than the specified minimum size via the `Sieve of Atkin`. This prime number
        sizing aims to reduce collision and improve hash distribution uniformity. 
        
        By using the hashing algorithm and dynamic table resizing based on the Sieve of Atkin 
        for prime number calculation, we are efficiently performing hash distribution and 
        minimizing collision likelihood, enhancing overall data storage and retrieval efficiency.
  
        Parameters:
        - min_size (int): Sets the minimum initial capacity of the hash table, which is then adjusted
          to the next prime number to ensure optimal hash distribution.
        - max_load_factor (float): The upper bound load factor before the table is resized upwards, 
          ensuring that the table does not become too dense, which could otherwise lead to increased 
          collisions and access times.
        - min_load_factor (float): The lower bound load factor before the table is resized downwards,
          optimizing memory usage when occupancy is low.

        Attributes:
        - max_load_factor (float): Stores the maximum load factor threshold.
        - min_load_factor (float): Stores the minimum load factor threshold.
        - count (int): Tracks the current number of key-value pairs stored in the hash table.
        - size (int): The current capacity of the hash table, always set to a prime number.
        - table (list): The underlying data structure, a list of buckets where each bucket is a list
          of key-value pairs or None if no entries are present.
        """
        self.max_load_factor = max_load_factor
        self.min_load_factor = min_load_factor
        self.count = 0  # Tracks the number of key-value pairs in the hash table.
        self.size = self._next_prime(min_size)
        self.table = [None for _ in range(self.size)]
        
    @staticmethod
    def _next_prime(n):
        """
        Utilizes the Sieve of Atkin to find and return the next
        prime number greater than a given integer, f(N) = Prime > N,
        in this case the size of our ingested package_file.json.
        
        Parameters:
        - n (int): The integer from which to find the next prime number.

        Returns:
        - int: The next prime number greater than 'n'.
        """
        limit = n + 10
        while True:
            primes = sieve_of_atkin(limit)
            for prime in primes:
                if prime > n:
                    return prime
            limit *= 2

    def _hash_function(self, key):
        """
        Computes and returns the hash value of a given key using the Murmur3 algorithm.

        Parameters:
        - key: The key to be hashed. Can be of any hashable type.

        Returns:
        - int: The computed hash value modulo the current table size,
               ensuring it maps to a valid bucket index.
        """
        return Murmur3.hash(key, seed=42) % self.size
        
    def load_factor(self):
        """
        Calculates and returns the current load factor of the hash table.

        The load factor is a measure of how full the hash table
        is, defined as the ratio of the number of stored entries to
        the total number of buckets. f(N) = N / M, where N is the
        number of stored entries and M is the number of buckets.

        Returns:
        - float: The current load factor of the hash table.
        """
        return self.count / self.size
    
    def _resize(self, new_size):
        """
        Resizes the hash table to a new capacity determined by
        'new_size', adjusting it to the next prime number.
        This method also rehashes all existing entries to ensure
        they are correctly distributed across the new 
        bucket array, maintaining the integrity and accessibility of the data.

        Parameters:
        - new_size (int): The proposed new size of the hash table,
                          which will be adjusted to the next prime number.
        """
        old_table = self.table
        self.size = self._next_prime(new_size)
        self.table = [None for _ in range(self.size)]
        old_count = self.count  # Preserve the old count
        self.count = 0  # Reset count to 0, as insert increments it
        for item in old_table:
            if item is not None:
                for key, value in item:
                    # Directly insert without resizing.
                    self._insert_direct(key, value)
        self.count = old_count  # Restore the actual item count

    def _resize_and_rehash(self):
        """
        Evaluates the current load factor and dynamically resizes
        the hash table either upwards or downwards,following 
        the thresholds defined by 'max_load_factor' and 'min_load_factor'.
        This method aims to ensure that the hash table operates
        within optimal load conditions, balancing between efficiency and memory usage.
        """
        load_factor = self.load_factor()
        if load_factor > self.max_load_factor:
            self._resize(self.size * 2)
        elif load_factor < self.min_load_factor and self.size > 10:
            # Ensure the size does not go below the initial minimum.
            self._resize(self.size // 2)

    def insert(self, key, value):
        """
        Inserts a key-value pair into the hash table. If the key
        already exists, its value is updated.Post-insertion, checks
        if the table needs resizing based on the current load factor.

        Parameters:
        - key: The key associated with the value to be inserted. Can be of any hashable type.
        - value: The value to be associated with the key. Can be of any type.
        """
        hash_key = self._hash_function(key)
        if self.table[hash_key] is None:
            self.table[hash_key] = []
        bucket = self.table[hash_key]
        for i, kv in enumerate(bucket):
            if kv[0] == key:
                bucket[i] = (key, value)
                break
        else:
            bucket.append((key, value))
            self.count += 1
        
        self._resize_and_rehash()
        


    def _insert_direct(self, key, value):
        """
        Insert directly without triggering resize.
        Used internally during resize operation to avoid recursion.
        """
        hash_key = self._hash_function(key)
        if self.table[hash_key] is None:
            self.table[hash_key] = []
        bucket = self.table[hash_key]
        for i, kv in enumerate(bucket):
            if kv[0] == key:
                bucket[i] = (key, value)
                return
        else:
            bucket.append((key, value))
    def lookup(self, key):
        """
        Searches for and returns the value associated with a given key 
        in the hash table. If the key is not found, returns None.

        Parameters:
        - key: The key whose associated value is to be returned.

        Returns:
        - The value associated with 'key' if found, otherwise None.
        """
        hash_key = self._hash_function(key)
        bucket = self.table[hash_key]
        if bucket is not None:
            for k, v in bucket:
                if k == key:
                    return v
        return None
    
    def keys(self):
        """
        A generator method that yields all the keys currently stored in the hash table.

        Yields:
        - keys: One by one, each key stored in the hash table.
        """
        for bucket in self.table:
            if bucket is not None:
                for k, _ in bucket:
                    yield k
