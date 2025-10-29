from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Initialize the password hasher with recommended parameters
ph = PasswordHasher(
    time_cost=2,        # Number of iterations
    memory_cost=102400, # Memory usage in kibibytes (100 MB)
    parallelism=8,      # Number of parallel threads
    hash_len=32,        # Length of the hash in bytes
    salt_len=16         # Length of the salt in bytes
)

def hash_password(password: str) -> str:
    """
    Hash the password using Argon2id (default variant).
    Argon2 won the Password Hashing Competition and is considered the best choice for password hashing.
    """
    if not isinstance(password, str):
        password = str(password)
    return ph.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    """
    Verify a password against a hash using Argon2.
    Returns True if the password matches, False otherwise.
    """
    if not isinstance(password, str):
        password = str(password)
    try:
        return ph.verify(hashed_pass, password)
    except VerifyMismatchError:
        return False

# def verify_password(plain_password: str, hashed_password: str):
#     """
#     Verify plain password with hash, handling bcrypt 72-byte limit safely.
#     """
#     if not isinstance(plain_password, str):
#         plain_password = str(plain_password)
#     if len(plain_password.encode("utf-8")) > 72:
#         plain_password = plain_password[:72]
#     return pwd_context.verify(plain_password, hashed_password)
