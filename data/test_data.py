import random
import string


class TestDataGenerator:
    
    @staticmethod
    def generate_random_string(length=8):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))
    
    @staticmethod
    def generate_unique_login(prefix="test"):
        return f"{prefix}_{TestDataGenerator.generate_random_string(8)}"