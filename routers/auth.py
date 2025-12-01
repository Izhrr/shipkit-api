from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from auth import authenticate_user, create_access_token
from schemas import LoginRequest, TokenResponse
from config import JWT_EXPIRATION_MINUTES

router = APIRouter(
    prefix="/api/v1",
    tags=["Authentication"]
)

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Endpoint untuk login dan mendapatkan JWT token.
    
    Kredensial default:
    - username: admin, password: admin123
    - username: user, password: user123
    """
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Access token
    access_token_expires = timedelta(minutes=JWT_EXPIRATION_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, 
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=JWT_EXPIRATION_MINUTES
    )