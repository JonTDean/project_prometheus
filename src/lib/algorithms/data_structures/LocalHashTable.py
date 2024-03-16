class LocalHashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(self.size)]
    
    def _hash_function(self, key):
        return hash(key) % self.size
    
    def keys(self):
        """Returns a list of all keys in the hash table."""
        all_keys = []
        for bucket in self.table:
            for k, _ in bucket:
                all_keys.append(k)
        return all_keys
    
    def insert(self, key, value):
        hash_key = self._hash_function(key)
        key_exists = False
        bucket = self.table[hash_key]
        for i, kv in enumerate(bucket):
            k, _ = kv
            if key == k:
                key_exists = True
                break
        if key_exists:
            bucket[i] = (key, value)
        else:
            bucket.append((key, value))
    
    def lookup(self, key):
        hash_key = self._hash_function(key)
        bucket = self.table[hash_key]
        for k, v in bucket:
            if k == key:
                return v
        return None
