import random
import string


CHARACTERS = string.ascii_letters + string.digits


def random_string(length: int = 25) -> str:
    """
    Generate a random string of the specified length.

    Parameters:
    -----------
    length: int
        The length of the string. Default is 25.
    
    Returns:
    --------
    str:
        The random generated string.
    """
    return ''.join(random.choice(CHARACTERS) for _ in range(length))
