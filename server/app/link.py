import random
import string


def generate_link():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=7))