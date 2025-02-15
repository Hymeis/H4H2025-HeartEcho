import secrets
import string
import math

def generate_unique_usernames(num_usernames=1, existing_usernames=None, username_length=7, max_attempts_per_username=1000):
    """
    Generates a sequence of unique usernames of a fixed length, with collision avoidance
    and a limit on generation attempts to prevent potential long loops.

    Args:
        num_usernames (int, optional): The number of unique usernames to generate. Defaults to 1.
        existing_usernames (set or list, optional): A set or list of usernames that already exist.
                                                    Defaults to None.
        username_length (int, optional): The desired length of each username. Defaults to 7.
        max_attempts_per_username (int, optional): Maximum attempts to generate a unique username
                                                     before giving up for a single username. Defaults to 1000.

    Returns:
        list: A list of unique usernames. May be shorter than num_usernames if uniqueness becomes too hard to achieve.

    Raises:
        ValueError: If num_usernames or username_length is not a positive integer,
                    or if the requested number of usernames exceeds the possible unique usernames
                    OR if it's not possible to generate the requested number of usernames within the attempt limit.
    """



    if not isinstance(num_usernames, int) or num_usernames <= 0:
        raise ValueError("num_usernames must be a positive integer.")
    if not isinstance(username_length, int) or username_length <= 0:
        raise ValueError("username_length must be a positive integer.")
    if not isinstance(max_attempts_per_username, int) or max_attempts_per_username <= 0:
        raise ValueError("max_attempts_per_username must be a positive integer.")


    if existing_usernames is None:
        existing_usernames = set()
    elif not isinstance(existing_usernames, (set, list)):
        raise TypeError("existing_usernames must be a set or a list.")
    else:
        existing_usernames = set(existing_usernames)

    unique_usernames = []
    characters_and_digits = string.ascii_lowercase + string.digits
    possible_combinations = pow(len(characters_and_digits), username_length)
    available_combinations = possible_combinations - len(existing_usernames)

    if num_usernames > available_combinations:
        raise ValueError(
            f"Requested {num_usernames} unique usernames, but only {available_combinations} possible "
            f"unique usernames available with length {username_length} and {len(existing_usernames)} existing usernames."
        )

    usernames_generated_count = 0
    while usernames_generated_count < num_usernames:
        attempts = 0
        while attempts < max_attempts_per_username:
            candidate_username = ''.join(secrets.choice(characters_and_digits) for _ in range(username_length))
            if candidate_username not in existing_usernames and candidate_username not in unique_usernames:
                unique_usernames.append(candidate_username)
                existing_usernames.add(candidate_username)
                usernames_generated_count += 1
                break # Found a unique username, move to next username to generate
            attempts += 1

        if attempts == max_attempts_per_username:
            if usernames_generated_count < num_usernames: # If we couldn't generate the requested number after attempts
                raise ValueError(
                    f"Failed to generate {num_usernames} unique usernames after {max_attempts_per_username} attempts per username. "
                    f"Generated {usernames_generated_count} usernames. "
                    f"Consider increasing username_length or reducing the number of usernames requested."
                )
            else:
                break # We have generated the requested number of usernames, even if some attempts failed for later ones, break the outer loop


    return unique_usernames

# # Example Usage (same as before, but now with attempt limit handling):
# if __name__ == "__main__":
#     # ... (rest of the example usage is the same as in the previous good response) ...
#     try:
#         # Example where generation might become difficult, especially with a short length and many existing usernames
#         large_existing = [ ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(5)) for _ in range(500000) ] # Simulate 500k existing usernames of length 5
#         generate_unique_usernames(num_usernames=1000, existing_usernames=large_existing, username_length=5) # Try to generate 1000 more of length 5
#     except ValueError as e:
#         print(f"Error during difficult generation: {e}")
# Example Usage:
if __name__ == "__main__":
    # Generate 5 unique 7-character usernames
    usernames1 = generate_unique_usernames(num_usernames=5)
    print("Generated usernames 1 (7 chars):", usernames1)

    # Generate another 3 unique 7-character usernames, considering the previous ones
    usernames2 = generate_unique_usernames(num_usernames=3, existing_usernames=usernames1)
    print("Generated usernames 2 (7 chars, considering previous):", usernames2)

    # Generate 10 unique 10-character usernames
    usernames3 = generate_unique_usernames(num_usernames=10, username_length=10)
    print("Generated usernames 3 (10 chars):", usernames3)

    # Example with initial existing usernames
    initial_existing = ["abc123d", "xyz789e", "1a2b3c4"]
    usernames4 = generate_unique_usernames(num_usernames=4, existing_usernames=initial_existing)
    print("Generated usernames 4 (7 chars, with initial existing):", usernames4)

    try:
        generate_unique_usernames(num_usernames=-2) # Example of invalid num_usernames
    except ValueError as e:
        print(f"Error: {e}")

    try:
        generate_unique_usernames(username_length=0) # Example of invalid username_length
    except ValueError as e:
        print(f"Error: {e}")

    try:
        # Example where generation might become difficult, especially with a short length and many existing usernames
        large_existing = [''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(5)) for _ in
                          range(500000)]  # Simulate 500k existing usernames of length 5
        generate_unique_usernames(num_usernames=1000, existing_usernames=large_existing,
                                  username_length=5)  # Try to generate 1000 more of length 5
    except ValueError as e:
        print(f"Error during difficult generation: {e}")
