import struct
from typing import Generator, Union
import struct

class Murmur3_32:
    """
    Static class implementation of the Murmur3 hashing algorithm, known for its
    efficiency for integers, i.e. PackageID.
    (https://www.synnada.ai/glossary/murmurhash)
    
	Translated From:
 	- https://github.com/aappleby/smhasher/blob/master/src/MurmurHash3.cpp
    
    Attributes:
    - Constants (c1, c2, r1, r2, m, n): Predefined values used in the hash computation, as per
      the MurmurHash3 specification.
    """
    c1 = 0xcc9e2d51
    c2 = 0x1b873593
    r1 = 15
    r2 = 13
    m = 5
    n = 0xe6546b64
    
    @staticmethod
    def prepare_key(key: Union[str, int, bytes]) -> bytes:
        """
        Prepares the key for hashing by converting it into a byte sequence.
        
        This is the preprocessing step that ensures that the key, regardless of its
        original type, is in a uniform format suitable for the byte-level operations
        required by the MurmurHash3 algorithm.

        Complexity Analysis:
        - Time: O(N) for strings, where N is the length of the string, due to encoding.
                O(1) for integers and bytes, as these involve fixed-size operations.
        - Space: O(N), where N is the size of the input key in its byte representation.
                This is the additional memory required to store the converted key.

        Parameters:
        - key (Union[str, int, bytes]): The original key to be hashed. Can be a string,
                                        integer, or bytes.

        Returns:
        - bytes: The key converted into a byte sequence.

        Raises:
        - TypeError: If the key type is not one of the expected types (str, int, bytes).
        """
        if isinstance(key, str):
            # Strings are encoded to bytes. UTF-8 is chosen for its wide applicability
            # and compatibility with a broad range of characters, supporting internationalization.
            return key.encode('utf-8')
        elif isinstance(key, int):
            # Integers are packed into 4 bytes using little-endian order. This choice reflects
            # the algorithm's design, which processes 32-bit chunks. Little-endian is specified
            # to ensure consistency across different hardware architectures.
            return struct.pack('<I', key)
        elif isinstance(key, bytes):
            return key
        else:
            raise TypeError("Key must be of type str, int, or bytes.")
        
    @staticmethod
    def process_key_chunks(key: bytes) -> Generator[int, None, None]:
        """
        Processes the key in 4-byte chunks, applying mixing operations defined by the MurmurHash algorithm.

        This generator abstracts the complexity of iterating over the key in fixed-size segments,
        applying a series of bitwise transformations to each segment. These help achieve the hash
        function's goals of uniform distribution and collision resistance.

        Complexity Analysis:
        - Time: O(N/4), where N is the length of the key in bytes. This reflects the iteration over
                each 4-byte chunk. The actual time complexity is proportional to the size of the key.
        - Space: O(1), generates one integer at a time, independent of the input size, demonstrating
                efficient memory usage.

        Parameters:
        - key (bytes): The key in bytes to be hashed.
        
        Yields:
        - int: An integer representing the processed chunk ready for inclusion in the hash calculation.
        """
        for i in range(0, len(key), 4):
            # Extract a 4-byte chunk from the key
            k = key[i:i+4]
            # Convert the chunk to an integer using little-endian to match the packing in prepare_key
            k = int.from_bytes(k, byteorder='little', signed=False)
            # Apply the mix operation: multiply, rotate, and again multiply. 
            # These steps help with	dispersing the input key's patterns
            # across the hash space, contributing to the algorithm's "avalanche" effect.
            # https://www.geeksforgeeks.org/avalanche-effect-in-cryptography/
            k *= Murmur3_32.c1
            k = ((k << Murmur3_32.r1) | (k >> (32 - Murmur3_32.r1))) & 0xFFFFFFFF
            k *= Murmur3_32.c2
            yield k
            
    @staticmethod
    def hash(key: Union[str, int, bytes], seed) -> int:
        """
        Implements the MurmurHash3 algorithm for a 32-bit hash function,
        computing the 32-bit MurmurHash3 hash of the key.

        Complexity Analysis:
        - Time: O(N), where N is the length of the key. This is due to the processing of each chunk
                of the key and the final mixing steps.
                
        - Space: O(1), uses a constant amount of space regardless of the input size, demonstrating
                efficient memory management.

        Parameters:
        - key (Union[str, int, bytes]): The key to hash.

        Returns:
        - int: A 32-bit hash of the key.
        """
        key = Murmur3_32.prepare_key(key)
        hash_val = seed

        for chunk in Murmur3_32.process_key_chunks(key):
            hash_val ^= chunk
            hash_val = ((hash_val << Murmur3_32.r2) | (hash_val >> (32 - Murmur3_32.r2))) & 0xFFFFFFFF
            hash_val = (hash_val * Murmur3_32.m + Murmur3_32.n) & 0xFFFFFFFF

        return Murmur3_32.avalanche_effect(hash_val, key)

    @staticmethod
    def avalanche_effect(hash_val: int, key: bytes) -> int:
        """
        Applies avalanche mixing steps to the hash to
        ensure even distribution of high and low bits.

        This is the hash function's primary avalanche effect:
        - This ensures that similar keys do not produce similar hashes.
        - This function encapsulates the conclusion of the hashing process.

        Complexity Analysis:
        - Time: O(1), performs a fixed number of operations on the hash.
        - Space: O(1), does not require additional space based on input size.

        Parameters:
        - hash (int): The current hash value.
        - key (bytes): The original key used for the hash, in bytes.

        Returns:
        - The finalized 32-bit hash.
        """
        # Mix in the length of the key. This step adds another layer of input dependency,
        # ensuring that keys of different lengths contribute to the hash value.
        hash_val ^= len(key)
        # Perform a series of right shifts and multiplications. These operations 
        # scramble the bits, making sure that the hash function exhibits good avalanche
        # properties.
        #* Improve it with this in the future `http://paper.ijcsns.org/07_book/201101/20110116.pdf`
        hash_val ^= hash_val >> 16
        hash_val *= 0x85ebca6b
        hash_val &= 0xFFFFFFFF
        hash_val ^= hash_val >> 13
        hash_val *= 0xc2b2ae35
        hash_val &= 0xFFFFFFFF
        hash_val ^= hash_val >> 16
        return hash_val & 0xFFFFFFFF
