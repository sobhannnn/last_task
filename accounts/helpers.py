import random
import string
# def for create random nummbers 5 digit
def random_digit():
    return ''.join(random.choice(string.digits) for i in range(5))

    