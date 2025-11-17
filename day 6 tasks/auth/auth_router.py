from fastapi import APIRouter, Depends, HTTPException
from schemas.user_schemas import UserCreate, UserLogin, UserResponse
from schemas.token_schemas import Token
from auth.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    created = AuthService.register(user.username, user.password, user.role)
    if not created:
        raise HTTPException(400, "User already exists")
    return {"username": created.username, "role": created.role}

@router.post("/login", response_model=Token)
def login(login_data: UserLogin):
    user = AuthService.authenticate(login_data.username, login_data.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")

    token = AuthService.generate_token(user.username, user.role)
    return {"access_token": token}

@router.post("/logout")
def logout(token: str):
    AuthService.logout(token)
    return {"message": "Logged out successfully"}
