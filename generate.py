import random
import math


def is_prime(n, k=5):
    """Miller-Rabin primality test."""
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0:
        return False
    
    # Write n-1 as d*2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    
    for _ in range(k):
        a = random.randint(2, min(n - 2, 1 << 20))
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bit_length):
    """Generate a random prime number with specified bit length."""
    while True:
        num = random.getrandbits(bit_length)
        num |= (1 << bit_length - 1) | 1  # Ensure high bit set and odd
        if is_prime(num):
            return num

def modinv(a, m):
    """Modular inverse using extended Euclidean algorithm."""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        return None  # No inverse exists
    else:
        return x % m

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def generate_rsa_keys(bit_length=512):
    """Generate RSA key pair from scratch."""
    # Generate two distinct primes
    p = generate_prime(bit_length//2)
    q = generate_prime(bit_length//2)
    while p == q:
        q = generate_prime(bit_length//2)
    
    # Compute modulus and totient
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose public exponent
    e = 65537
    while math.gcd(e, phi) != 1:
        e = random.randint(3, phi - 1)
    
    # Compute private exponent
    d = modinv(e, phi)
    
    return (n, e), (n, d)

if __name__ == "__main__":
    public_key, private_key = generate_rsa_keys(512)
    print(f"public_key: {public_key[0]}:{public_key[1]}")
    print(f"private_key: {private_key[0]}:{private_key[1]}")