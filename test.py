import random

def generate_unique_usernames(base_username="user", num_usernames=1, existing_usernames=None):
    """
    Generates a sequence of unique usernames.

    Args:
        base_username (str, optional): The base username to start with. Defaults to "user".
        num_usernames (int, optional): The number of unique usernames to generate. Defaults to 1.
        existing_usernames (set or list, optional): A set or list of usernames that already exist.
                                                    This helps to avoid generating duplicate usernames.
                                                    Defaults to None.

    Returns:
        list: A list of unique usernames.

    Raises:
        ValueError: If num_usernames is not a positive integer.
    """

    if not isinstance(num_usernames, int) or num_usernames <= 0:
        raise ValueError("num_usernames must be a positive integer.")

    if existing_usernames is None:
        existing_usernames = set()  # Use a set for efficient lookups if no existing usernames are provided
    elif not isinstance(existing_usernames, (set, list)):
        raise TypeError("existing_usernames must be a set or a list.")
    else:
        existing_usernames = set(existing_usernames) # Convert to set for efficient lookup

    unique_usernames = []
    counter = 0

    while len(unique_usernames) < num_usernames:
        candidate_username = base_username

        # Add a counter or random element to ensure uniqueness
        if counter > 0:
            candidate_username = f"{base_username}_{counter}"
        else:
            # Add a small random number initially to make the starting usernames a bit less predictable
            candidate_username = f"{base_username}_{random.randint(1, 10)}"


        if candidate_username not in existing_usernames and candidate_username not in unique_usernames:
            unique_usernames.append(candidate_username)
            existing_usernames.add(candidate_username) # Add to existing set to avoid future duplicates
            counter = 0 # Reset counter after finding a unique name (for initial randomness)
        else:
            counter += 1 # Increment counter if username is not unique

    return unique_usernames

# Example Usage:
if __name__ == "__main__":
    # Generate 5 unique usernames starting with "myuser"
    usernames1 = generate_unique_usernames(base_username="myuser", num_usernames=5)
    print("Generated usernames 1:", usernames1)

    # Generate another 3 unique usernames, considering the previous ones
    usernames2 = generate_unique_usernames(base_username="myuser", num_usernames=3, existing_usernames=usernames1)
    print("Generated usernames 2 (considering previous):", usernames2)

    # Generate usernames with a different base and a larger number
    usernames3 = generate_unique_usernames(base_username="coder", num_usernames=10)
    print("Generated usernames 3:", usernames3)

    # Example with a list of existing usernames already
    initial_existing = ["testuser_1", "testuser_2", "testuser_5"]
    usernames4 = generate_unique_usernames(base_username="testuser", num_usernames=4, existing_usernames=initial_existing)
    print("Generated usernames 4 (with initial existing usernames):", usernames4)

    try:
        generate_unique_usernames(num_usernames=-2) # Example of invalid num_usernames
    except ValueError as e:
        print(f"Error: {e}")