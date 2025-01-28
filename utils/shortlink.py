import secrets
import string

class Shortlink:
    def __init__(self, length=8):
        self.length = length

    def generate(self) -> str:
        """Generate a random shortlink."""
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(self.length))

    @staticmethod
    def validate(shortlink: str) -> bool:
        """Validate the shortlink format."""
        return all(not shortlink.isalnum() and '_' not in shortlink and '-' not in shortlink)