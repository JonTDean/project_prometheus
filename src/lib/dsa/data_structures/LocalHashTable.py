from lib.dsa.algorithms.sieve_of_atkin import sieve_of_atkin
from lib.dsa.algorithms.murmur_3 import murmurhash3


class MurMurAtkinsHashTable:
    def __init__(self, min_size=10, max_load_factor=0.7, min_load_factor=0.2):
        """
        Initializes a hash table with dynamic resizing based on [max, min] load factor.

        The hash table's size is determined by finding the next prime number greater
        than the specified minimum size via the `Sieve of Atkin`. This prime number
        sizing aims to reduce collision and improve hash distribution uniformity.

        Parameters:
        - min_size (int): Minimum initial size of the hash table.
        - max_load_factor (float): Load factor threshold for upsizing the table.
        - min_load_factor (float): Load factor threshold for downsizing the table.
        """
        self.max_load_factor = max_load_factor
        self.min_load_factor = min_load_factor
        self.count = 0  # Tracks the number of key-value pairs in the hash table.
        self.size = self._next_prime(min_size)
        self.table = [None for _ in range(self.size)]
        
    @staticmethod
    def _next_prime(n):
        limit = n + 10
        while True:
            primes = sieve_of_atkin(limit)
            for prime in primes:
                if prime > n:
                    return prime
            limit *= 2

    def _hash_function(self, key):
        return murmurhash3(key, seed=42) % self.size
        
    def load_factor(self):
        return self.count / self.size
    
    def _resize(self, new_size):
        old_table = self.table
        self.size = self._next_prime(new_size)
        self.table = [None for _ in range(self.size)]
        self.count = 0
        for item in old_table:
            if item is not None:
                for key, value in item:
                    self.insert(key, value)

    def _resize_and_rehash(self):
        load_factor = self.load_factor()
        if load_factor > self.max_load_factor:
            self._resize(self.size * 2)
        elif load_factor < self.min_load_factor and self.size > 10:
            # Ensure the size does not go below the initial minimum.
            self._resize(self.size // 2)

    def insert(self, key, value):
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

    def lookup(self, key):
        hash_key = self._hash_function(key)
        bucket = self.table[hash_key]
        if bucket is not None:
            for k, v in bucket:
                if k == key:
                    return v
        return None
    
    def keys(self):
        for bucket in self.table:
            if bucket is not None:
                for k, _ in bucket:
                    yield k
