import struct
from typing import Generator, Union

def prepare_key(key: Union[str, int, bytes]) -> bytes:
    """
    Prepares the key for hashing by converting it into a byte sequence.
    
    This is the preprocessing step that ensures the key, regardless of its
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

def process_key_chunks(key: bytes, c1: int, c2: int, r1: int) -> Generator[int, None, None]:
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
    - c1, c2 (int): Constants used for bitwise operations in the hash calculation.
    - r1 (int): Rotation amount used in the hash calculations.

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
        k *= c1
        k = ((k << r1) | (k >> (32 - r1))) & 0xFFFFFFFF  # Ensure 32-bit arithmetic
        k *= c2
        yield k

def murmurhash3(key: Union[str, int, bytes], seed: int = 0) -> int:
    """
    Implements the MurmurHash3 algorithm for a 32-bit hash function.

    MurmurHash has greatperformance and collision resistance, making it suitable for
    our hash table.

    Complexity Analysis:
    - Time: O(N), where N is the length of the key. This is due to the processing of each chunk
            of the key and the final mixing steps.
            
    - Space: O(1), uses a constant amount of space regardless of the input size, demonstrating
             efficient memory management.

    Parameters:
    - key (Union[str, int, bytes]): The key to hash.
    - seed (int): An initial seed value for the hash calculation. Default is 0.

    Returns:
    - int: A 32-bit hash of the key.
    """
    key = prepare_key(key)
    # Constants are defined as per the MurmurHash3 specification. These values have been
    # chosen to optimize the hash function's dispersion and collision resistance characteristics.
    c1, c2 = 0xcc9e2d51, 0x1b873593
    r1, r2 = 15, 13
    m, n = 5, 0xe6546b64
    hash = seed
    
    for chunk in process_key_chunks(key, c1, c2, r1):
        hash ^= chunk
        hash = ((hash << r2) | (hash >> (32 - r2))) & 0xFFFFFFFF
        hash = (hash * m + n) & 0xFFFFFFFF

    return finalize_hash(hash, key)

def finalize_hash(hash: int, key: bytes) -> int:
    """
    Applies final mixing steps to the hash to ensure even distribution of high and low bits.

    This is the hash function's avalanche effect:
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
    hash ^= len(key)
    # Perform a series of right shifts and multiplications. These operations 
    # scramble the bits, making sure that the hash function exhibits good avalanche
    # properties.
    #* Improve it with this in the future `http://paper.ijcsns.org/07_book/201101/20110116.pdf`
    hash ^= hash >> 16
    hash *= 0x85ebca6b
    hash &= 0xFFFFFFFF
    hash ^= hash >> 13
    hash *= 0xc2b2ae35
    hash &= 0xFFFFFFFF
    hash ^= hash >> 16
    return hash & 0xFFFFFFFF
