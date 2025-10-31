# utils/jwt_utils.py
from datetime import datetime, timedelta
from jose import jwt
from jose import jwt, JWTError
from config.config import settings

def create_access_token(data: dict):
    """Create JWT access token with expiry."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
def decode_access_token(token: str):
    """Decode JWT and return payload or None if invalid."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
