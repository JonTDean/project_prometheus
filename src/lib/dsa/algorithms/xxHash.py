import struct
from typing import Union

"""
xxHash seems to be good to use for a complementary algorithm for the MurmurHash3 algorithm.
We're only going to target the 32bit version of xxHash, as it's the most relevant to our use case.

Translated From:
- https://github.com/Cyan4973/xxHash/blob/dev/doc/xxhash.cry
- https://github.com/Cyan4973/xxHash/blob/dev/doc/xxhash_spec.md
"""

class XXHash_32:
    """
    Implements the (static class) 32-bit version of the xxHash algorithm. 
    While xxHash is generally used for streams of data, in this case we are
    primarily using it for its state positive feature due to the package system
    having a dynamic delivery state.

    Attributes:
    - PRIME32_1 to PRIME32_5: Prime number constants defined by the xxHash specification.
    """
    
    
    #!
    #!    Note: What if I used the sieve of atkins to generate the prime number constants?
    #!    Something like 
    #!    ```pseudo
    #!        array = []
    #!        for (i = 0; i < 5; i++):
    #!            if sieve_of_atkins(random_number in range(1, 65536)):
    #!               array.push(prime)
    #!    ```
    
    PRIME32_1 = 0x9E3779B1
    PRIME32_2 = 0x85EBCA77
    PRIME32_3 = 0xC2B2AE3D
    PRIME32_4 = 0x27D4EB2F
    PRIME32_5 = 0x165667B1


    @staticmethod
    def prepare_key(key: Union[str, int, bytes]) -> bytes:
        """
        Prepares the key for hashing by converting it into a byte sequence.

        This method ensures that the key, regardless of its original type,
        is converted into a uniform byte sequence suitable for hashing.

        Parameters:
        - key (Union[str, int, bytes]): The original key to be hashed, which can be of type str, int, or bytes.

        Returns:
        - bytes: The key converted into a byte sequence suitable for hashing.

        Raises:
        - TypeError: If the key type is not str, int, or bytes.
        """
        if isinstance(key, str):
            return key.encode('utf-8')
        elif isinstance(key, int):
            # Converts the integer to bytes (little endian);
            # uses the minimum number of bytes needed to represent the integer.
            return key.to_bytes((key.bit_length() + 7) // 8, byteorder='little', signed=False)
        elif isinstance(key, bytes):
            return key
        else:
            raise TypeError("Key must be of type str, int, or bytes.")

    @staticmethod
    def process_chunks(input_bytes: bytes, initial_hash: int) -> int:
        """
        Processes each 16-byte chunk of the input, applying the xxHash algorithm's mixing formula.
        
        This function iteratively processes chunks of 16 bytes (128 bits), applying
        mixed operations defined by the xxHash algorithm to each chunk. The operation
        for a single 32-bit block k within a chunk is defined as:
        
        k = k * PRIME32_2
        k = (k << 13) | (k >> 19)
        k = k * PRIME32_1
        
        The updated hash value is then summed with this processed block.
        
        Complexity:
        - Time: O(n/16), where n is the length of the input_bytes. Each loop iteration processes 16 bytes.
        - Space: O(1), operates within constant space independent of the input size.
        """
        hash_val = initial_hash
        i = 0
        total_len = len(input_bytes)
        while i <= total_len - 16:
            for j in range(4):  # Process each of the four 32-bit blocks
                k = int.from_bytes(input_bytes[i:i+4], byteorder='little')
                hash_val += k * XXHash_32.PRIME32_2
                hash_val = ((hash_val << 13) | (hash_val >> 19)) & 0xFFFFFFFF
                hash_val = hash_val * XXHash_32.PRIME32_1 & 0xFFFFFFFF
                i += 4
        return hash_val, i

    @staticmethod
    def process_remaining(input_bytes: bytes, hash_val: int, index: int) -> int:
        """
        Processes any remaining bytes after chunk processing, applying the xxHash algorithm's mixing formula.
        
        For each remaining byte b in the input_bytes, the mixing operation applied is defined as:
        hash_val += b'' * PRIME32_5
        hash_val = (hash_val << 11) | (hash_val >> 21) mux 0xFFF
        hash_val = hash_val * (PRIME32_1 mux 0xFFF)
        
        Complexity:
        - Time: O(m), where m is the number of remaining bytes, less than 16.
        - Space: O(1), operates within constant space.
        """
        while index < len(input_bytes):
            hash_val += input_bytes[index] * XXHash_32.PRIME32_5
            hash_val = ((hash_val << 11) | (hash_val >> 21)) & 0xFFFFFFFF
            hash_val *= XXHash_32.PRIME32_1 & 0xFFFFFFFF
            index += 1
        return hash_val

    @staticmethod
    def avalanche_effect(hash_val: int) -> int:
        """
        Finalizes the hash calculation, applying an avalanche effect.
        
        Complexity:
        - Time: O(1), constant time complexity as operations do not depend on input size.
        - Space: O(1), constant space complexity.
        """
        hash_val ^= hash_val >> 15
        hash_val *= XXHash_32.PRIME32_2 & 0xFFFFFFFF
        hash_val ^= hash_val >> 13
        hash_val *= XXHash_32.PRIME32_3 & 0xFFFFFFFF
        hash_val ^= hash_val >> 16
        return hash_val

    @staticmethod
    def hash(key: Union[str, int, bytes], seed: int = 0) -> int:
        """
        Calculates the xxHash32 hash of the input bytes using the provided seed.

        Oorchestrates the hashing process by preparing the key, processing chunks, 
        handling any remaining bytes, and finalizing the hash calculation
        with the avalanche effect.


        Parameters:
        - key (Union[str, int, bytes]): The key to hash, which can be of type str, int, or bytes.
        - seed (int): An initial value to influence the hash result, defaulting to 0.

        Returns:
        - int: The computed 32-bit hash value, modulo 2^32.

        Complexity:
        - Time: O(n), where n is the length of the input_bytes. This encompasses the initial preparation,
                processing of all 16-byte chunks, handling remaining bytes, and finalization steps.
        - Space: O(1), operates within constant space.
        """
        input_bytes = XXHash_32.prepare_key(key)
        # The initial hash value is computed as: H_0 = seed + PRIME32_5 + len(input_bytes),
        # where len(input_bytes) is the total length of the input in bytes.
        hash_val = seed + XXHash_32.PRIME32_5 + len(input_bytes) 
        hash_val, index = XXHash_32.process_chunks(input_bytes, hash_val)
        hash_val = XXHash_32.process_remaining(input_bytes, hash_val, index)
        hash_val = XXHash_32.avalanche_effect(hash_val)
        return hash_val & 0xFFFFFFFF
    
    
