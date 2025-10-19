import random
import string

def convert(length : int = 6):
    characters = string.ascii_letters + string.digits 
    return ''.join(random.choices(characters, k=length))