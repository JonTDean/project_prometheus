import struct
from typing import Union

# xxHash seems to be good to use for a complementary algorithm for the MurmurHash3 algorithm.
# We're only going to target the 32bit version of xxHash, as it's the most relevant to our use case.
# https://github.com/Cyan4973/xxHash/blob/dev/doc/xxhash.cry
# https://github.com/Cyan4973/xxHash/blob/dev/doc/xxhash_spec.md


class XXHash32:
    """
    Implements the 32-bit version of the xxHash algorithm. xxHash is a fast non-cryptographic
    hash algorithm, working at speeds close to RAM limits. Designed for use in hash tables, 
    xxHash provides a highly distributed hash value for varied inputs, making it suitable for
    high-performance applications that require efficient data retrieval mechanisms.

    Attributes:
    - PRIME32_1 to PRIME32_5: Prime number constants defined by the xxHash specification.
    """

    PRIME32_1 = 0x9E3779B1
    PRIME32_2 = 0x85EBCA77
    PRIME32_3 = 0xC2B2AE3D
    PRIME32_4 = 0x27D4EB2F
    PRIME32_5 = 0x165667B1

    def __init__(self, seed: int = 0):
        """
        Initializes the xxHash32 object with an optional seed value. The seed can influence
        the outcome, allowing for varied hash results for the same input data.

        Parameters:
        - seed (int): A seed value to influence the hash calculation, defaulting to 0.

        Complexity:
        - Time: O(1), constant time initialization.
        - Space: O(1), fixed space allocation regardless of input size.
        """
        self.seed = seed
        self.reset()

    def reset(self):
        """
        Resets the internal state to begin a new hash calculation. This is useful for hashing
        multiple data sequences without creating new xxHash32 instances.

        Complexity:
        - Time: O(1), performs a fixed series of assignments.
        - Space: O(1), modifies existing attributes without additional allocation.
        """
        self.buffer = bytearray()
        self.total_len = 0
        self._initialize_state()

    def _initialize_state(self):
        """
        Sets up the initial state based on the seed value. This method configures accumulators
        for processing data in chunks, aligning with the xxHash algorithm's specifications.

        Complexity:
        - Time: O(1), straightforward assignments.
        - Space: O(1), operates within the object's attribute space.
        """
        # Accumulators are initialized differently based on the anticipated total length
        self.acc = self.seed + self.PRIME32_5 if self.total_len < 16 else None
        if self.total_len >= 16:
            self.acc1 = self.seed + self.PRIME32_1 + self.PRIME32_2
            self.acc2 = self.seed + self.PRIME32_2
            self.acc3 = self.seed
            self.acc4 = self.seed - self.PRIME32_1

    def update(self, input_bytes: Union[bytes, bytearray]):
        """
        Feeds new bytes into the hash calculation. This method can be called repeatedly
        as new data chunks become available, allowing for incremental hashing.

        Parameters:
        - input_bytes (Union[bytes, bytearray]): Bytes to include in the hash calculation.

        Complexity:
        - Time: O(n), linearly dependent on the length of input_bytes.
        - Space: O(n), storage requirements grow with the accumulation of input_bytes.
        """
        self.buffer += input_bytes
        self.total_len += len(input_bytes)

        if len(self.buffer) >= 16:
            self._process_stripes()

    def _process_stripes(self):
        """
        Processes each 16-byte stripe from the accumulated buffer. This core routine applies
        the xxHash algorithm's mixing formula to chunks of data, ensuring uniform dispersion.

        Complexity:
        - Time: O(m), where m is the number of 16-byte stripes processed.
        - Space: O(1), as it manipulates the internal state without requiring extra space.
        """
        while len(self.buffer) >= 16:
            self._process_stripe(self.buffer[:16])
            self.buffer = self.buffer[16:]

    def _process_stripe(self, stripe: bytes):
        """
        Applies the xxHash mixing operations to a single 16-byte stripe, updating the internal
        state accumulators accordingly.

        Parameters:
        - stripe (bytes): A 16-byte sequence extracted from the buffer.

        Complexity:
        - Time: O(1), a fixed series of operations are applied to the stripe.
        - Space: O(1), computation is performed within the scope of existing variables.
        """
        blocks = struct.unpack('<4I', stripe)
        self.acc1 = self._mix(self.acc1, blocks[0], self.PRIME32_2, self.PRIME32_1)
        self.acc2 = self._mix(self.acc2, blocks[1], self.PRIME32_2, self.PRIME32_1)
        self.acc3 = self._mix(self.acc3, blocks[2], self.PRIME32_2, self.PRIME32_1)
        self.acc4 = self._mix(self.acc4, blocks[3], self.PRIME32_2, self.PRIME32_1)

    def _mix(self, acc: int, block: int, prime_mul: int, prime_acc: int) -> int:
        """
        Performs a single mixing operation of the xxHash algorithm, updating an accumulator
        with data from one block (lane) of the input.

        Parameters:
        - acc (int): The current value of the accumulator.
        - block (int): The 32-bit block extracted from the stripe.
        - prime_mul (int): A prime multiplier for the block value.
        - prime_acc (int): A prime multiplier for updating the accumulator.

        Complexity:
        - Time: O(1), executes a fixed number of operations.
        - Space: O(1), operates without additional memory allocation.
        """
        acc += block * prime_mul
        acc = ((acc << 13) | (acc >> 19)) & 0xFFFFFFFF
        acc *= prime_acc
        return acc & 0xFFFFFFFF

    def _finalize(self) -> int:
        """
        Completes the hash calculation by mixing in the length, processing any remaining bytes,
        and applying the final avalanche to the accumulated state.

        Complexity:
        - Time: O(p), where p is the number of bytes remaining in the buffer.
        - Space: O(1), utilizes existing state for final computations.
        """
        acc = self.acc if self.total_len < 16 else (self.acc1 + self.acc2 + self.acc3 + self.acc4 + self.total_len)

        for byte in self.buffer:
            acc += byte * self.PRIME32_5
            acc = ((acc << 11) | (acc >> 21)) & 0xFFFFFFFF
            acc *= self.PRIME32_1

        # Final avalanche
        acc ^= acc >> 15
        acc *= self.PRIME32_2
        acc ^= acc >> 13
        acc *= self.PRIME32_3
        acc ^= acc >> 16

        return acc & 0xFFFFFFFF

    def digest(self) -> int:
        """
        Returns the final hash value and resets the hash object for future use. This method
        encapsulates the entire hash computation process from update to finalize.
        """
        result = self._finalize()
        self.reset()
        return result
