import random
import string

def generate_otp(length=6):
    """Generates a numeric OTP of given length."""
    return ''.join(random.choices(string.digits, k=length))

def generate_token(length=32):
    """Generates a random token for deep linking."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
