# utils/hashing.py
from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_password(password: str) -> str:
    """Encrypt the password before saving."""
    return ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if the password entered matches the hashed one."""
    try:
        return ph.verify(hashed_password, plain_password)
    except Exception:
        return False
