class SieveOfAtkin:
    """
    Implements the Sieve of Atkin, an efficient algorithm to find all prime numbers up to a specified limit.

    The main method, sieve_of_atkin, runs in O(N/log(log(N))) time complexity for generating primes up to N,
    leveraging modern computational optimizations.
    
    Translated From: 
    - https://cr.yp.to/papers/primesieves.pdf
    """
    
    @staticmethod
    def sieve_of_atkin(limit):
        """
        Generates all prime numbers up to the given limit using the Sieve of Atkin algorithm.
        
        Complexity Analysis:
        - Time: O(n/(log(log n))), where n is the limit.
            - Good explanation on this runtime: https://stackoverflow.com/questions/16472012/what-would-cause-an-algorithm-to-have-olog-log-n-complexity
        - Space: O(n), due to the storage requirements of the sieve array.
        
        Parameters:
        - limit (int): The upper bound to generate prime numbers.

        Returns:
        - list: A list of all prime numbers up to 'limit'.
        """
        if limit < 2:
            return []
        P = [2, 3]
        sieve = [False] * (limit + 1)
        # Main loop to flip the sieve values based on Atkin's conditions
        SieveOfAtkin._initialize_sieve(sieve, limit)
        # Mark multiples of squares as non-prime
        SieveOfAtkin._eliminate_multiples(sieve, limit)
        # Compile the list of primes
        P.extend(SieveOfAtkin._collect_primes(sieve, limit))
        return P

    @staticmethod
    def _initialize_sieve(sieve, limit):
        for x in range(1, int(limit**0.5) + 1):
            for y in range(1, int(limit**0.5) + 1):
                SieveOfAtkin._flip_sieve(sieve, x, y, limit)

    @staticmethod
    def _flip_sieve(sieve, x, y, limit):
        """
        Applies the specific rules of the Sieve of Atkin for identifying potential primes.
        Modifies the sieve list in-place by flipping the boolean values based on Atkin's conditions.

        Parameters:
        - sieve (list[bool]): The sieve list being used to track prime numbers.
        - x (int): The current x-coordinate in the sieve grid.
        - y (int): The current y-coordinate in the sieve grid.
        - limit (int): The upper bound for primes generation.
        """
        n = 4 * x**2 + y**2
        if n <= limit and (n % 12 == 1 or n % 12 == 5):
            sieve[n] = not sieve[n]
        n = 3 * x**2 + y**2
        if n <= limit and n % 12 == 7:
            sieve[n] = not sieve[n]
        n = 3 * x**2 - y**2
        if x > y and n <= limit and n % 12 == 11:
            sieve[n] = not sieve[n]

    @staticmethod
    def _eliminate_multiples(sieve, limit):
        for x in range(5, int(limit**0.5) + 1):
            if sieve[x]:
                for y in range(x**2, limit + 1, x**2):
                    sieve[y] = False

    @staticmethod
    def _collect_primes(sieve, limit):
        return [p for p in range(5, limit + 1) if sieve[p]]

    @staticmethod
    def next_prime(n):
        """
        Finds and returns the next prime number greater than a given integer using the Sieve of Atkin.

        Time Complexity: O(n), where n is the distance to the next prime. This is due to the repeated 
        doubling of the search limit until the next prime is found.
        Space Complexity: Depends on the size of the sieve array required to find the next prime.

        Parameters:
        - n (int): The integer from which to find the next prime number.

        Returns:
        - int: The next prime number greater than 'n'.
        """
        limit = n + 10  # Initial limit set slightly higher than n.
        while True:
            primes = SieveOfAtkin.sieve_of_atkin(limit)
            for prime in primes:
                if prime > n:
                    return prime
            limit *= 2

