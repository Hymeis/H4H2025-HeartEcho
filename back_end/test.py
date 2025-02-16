import time

def generate_pseudo_random_string(length=10, seed=None):
    """Generate a pseudo-random alphanumeric string using LCG."""
    CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    A = 1664525
    C = 1013904223
    M = 2**32

    # Use current time as seed if none is provided
    if seed is None:
        seed = int(time.time())

    result = []
    Xn = seed  # Initialize with seed

    for _ in range(length):
        Xn = (A * Xn + C) % M  # Apply LCG formula
        result.append(CHARSET[Xn % len(CHARSET)])  # Map to charset

    return "".join(result)

# Example Usage
random_string = generate_pseudo_random_string(7)
print(random_string)  # Example output: "G3AqzX8KdNmY2bW9"
