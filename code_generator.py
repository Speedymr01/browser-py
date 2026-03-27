import secrets
import string

class AccessCodeGenerator:
    def __init__(self, length=10):
        self.length = length
        self.characters = string.ascii_letters + string.digits

    def generate_code(self):
        return ''.join(secrets.choice(self.characters) for _ in range(self.length))

    def validate_code(self, code):
        return len(code) == self.length and all(c in self.characters for c in code)

# Example usage (can be removed in production):
if __name__ == '__main__':
    generator = AccessCodeGenerator()
    code = generator.generate_code()
    print(f"Generated Code: {code}")
    print(f"Is the code valid? {generator.validate_code(code)}")