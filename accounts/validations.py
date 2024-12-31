import re
from django.core.exceptions import ValidationError

class PasswordValidator:
    def __init__(self):
        self.patterns = [
            re.compile(r'[A-Z]'),  # At least one uppercase letter
            re.compile(r'[a-z]'),  # At least one lowercase letter
            re.compile(r'\d'),      # At least one digit
            re.compile(r'[!@#$%^&*(),.?":{}|<>]')  # At least one special character
        ]
    
    def __call__(self, value):
        errors = []
        for pattern in self.patterns:
            if not pattern.search(value):
                errors.append("Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.")
        
        if errors:
            raise ValidationError(errors)
