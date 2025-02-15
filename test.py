import random
import string

def generate_unique_usernames(base_username="user", num_usernames=1, existing_usernames=None, username_length=8):
    """
    Generates a sequence of unique usernames with a combination of characters and numbers.

    Args:
        base_username (str, optional): The base username to start with. Defaults to "user".
        num_usernames (int, optional): The number of unique usernames to generate. Defaults to 1.
        existing_usernames (set or list, optional): A set or list of usernames that already exist.
                                                    This helps to avoid generating duplicate usernames.
                                                    Defaults to None.
        username_length (int, optional): The total length of the generated username (including base username and random part).
                                          Defaults to 8.  The random part will adjust based on the base username length.

    Returns:
        list: A list of unique usernames.

    Raises:
        ValueError: If num_usernames is not a positive integer or username_length is too short.
    """

    if not isinstance(num_usernames, int) or num_usernames <= 0:
        raise ValueError("num_usernames must be a positive integer.")
    if not isinstance(username_length, int) or username_length <= 4:  # Minimum length for some randomness
        raise ValueError("username_length must be an integer greater than 4 to ensure randomness.")

    if existing_usernames is None:
        existing_usernames = set()
    elif not isinstance(existing_usernames, (set, list)):
        raise TypeError("existing_usernames must be a set or a list.")
    else:
        existing_usernames = set(existing_usernames)

    unique_usernames = []
    retry_count = 0
    max_retries = num_usernames * 10  # Heuristic to avoid infinite loops in extreme collision cases

    while len(unique_usernames) < num_usernames and retry_count < max_retries:
        candidate_username = base_username

        # Calculate the length of the random part
        random_part_length = max(1, username_length - len(base_username))  # Ensure at least 1 random char

        # Generate a random string of characters and numbers
        characters = string.ascii_letters + string.digits
        random_suffix = ''.join(random.choice(characters) for _ in range(random_part_length))
        candidate_username += random_suffix

        if candidate_username not in existing_usernames and candidate_username not in unique_usernames:
            unique_usernames.append(candidate_username)
            existing_usernames.add(candidate_username)
            retry_count = 0 # Reset retry count after finding a unique name
        else:
            retry_count += 1

    if retry_count >= max_retries:
        print(f"Warning: Could not generate {num_usernames} unique usernames after {max_retries} retries. "
              f"Consider increasing username_length or base_username uniqueness.")

    return unique_usernames


# Example Usage:
if __name__ == "__main__":
    # Generate 5 unique usernames starting with "coder" with default length 8
    usernames1 = generate_unique_usernames(base_username="coder", num_usernames=5)
    print("Generated usernames 1:", usernames1)

    # Generate 3 unique usernames with base "shorty" and length 10
    usernames2 = generate_unique_usernames(base_username="shorty", num_usernames=3, username_length=10)
    print("Generated usernames 2:", usernames2)

    # Generate usernames with a longer base and length 12
    usernames3 = generate_unique_usernames(base_username="verylongusernamebase", num_usernames=4, username_length=12)
    print("Generated usernames 3:", usernames3)

    # Using existing usernames
    existing_list = ["testuserabc1", "testuserdef2"]
    usernames4 = generate_unique_usernames(base_username="testuser", num_usernames=3, existing_usernames=existing_list, username_length=10)
    print("Generated usernames 4 (with existing):", usernames4)

    # Example with shorter length - will still try to be unique
    usernames5 = generate_unique_usernames(base_username="u", num_usernames=5, username_length=5)
    print("Generated usernames 5 (short length):", usernames5)

    try:
        generate_unique_usernames(username_length=3) # Example of invalid username_length
    except ValueError as e:
        print(f"Error: {e}")