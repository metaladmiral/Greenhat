import random
import string


def gen_rand_str(random_string_length):
    return "".join(
        random.choices(string.ascii_uppercase + string.digits, k=random_string_length)
    )
