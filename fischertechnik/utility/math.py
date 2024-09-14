import math

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

def bitwise_not(n):
    return (1 << n.bit_length()) - 1 - n

def round_up(n, decimals):
    factor = math.pow(10, decimals)
    return math.ceil(n * factor) / factor

def round_down(n, decimals):
    factor = math.pow(10, decimals)
    return math.floor(n * factor) / factor

def is_nan(n):
    if isinstance(n, (int, float)):
        return False
    return True

def is_prime(n):
    # https://en.wikipedia.org/wiki/Primality_test#Naive_methods
    # If n is not a number but a string, try parsing it.
    if not isinstance(n, (int, float)):
        try:
            n = float(n)
        except:
            return False
    if n == 2 or n == 3:
        return True
    # False if n is negative, is 1, or not whole, or if n is divisible by 2 or 3.
    if n <= 1 or n % 1 != 0 or n % 2 == 0 or n % 3 == 0:
        return False
    # Check all the numbers of form 6k +/- 1, up to sqrt(n).
    for x in range(6, int(math.sqrt(n)) + 2, 6):
        if n % (x - 1) == 0 or n % (x + 1) == 0:
            return False
    return True
