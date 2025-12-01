from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi. security import HTTPBearer, HTTPAuthorizationCredentials
from config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_MINUTES
from schemas import TokenData

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token
security = HTTPBearer()

# Dummy Database
FAKE_USERS_DB = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context. hash("admin123"),
    },
    "user1": {
        "username": "user",
        "hashed_password": pwd_context.hash("user123"),
    }
}

# Helper Function
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifikasi password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    """Ambil user dari db"""
    if username in FAKE_USERS_DB:
        return FAKE_USERS_DB[username]
    return None

def authenticate_user(username: str, password: str):
    """Autentikasi user"""
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Buat JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

# Dependencies
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency untuk memverifikasi JWT token pada endpoint yang dilindungi.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user