from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth.models import UserCreate, User, Token
from auth.security import authenticate_user,create_access_token,create_user,ACCESS_TOKEN_EXPIRE_MINUTES,add_to_blacklist,users_db,create_refresh_token
from auth.utils import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=User)
async def register(user: UserCreate):
    if user.email in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return create_user(user.email, user.password, user.role)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub":user.email,"role":user.role})
    return {"access_token": access_token, "token_type": "bearer","refresh_token":refresh_token,"refresh_token_type":"bearer"}



@router.post("/logout")
async def logout(token: str = Depends(get_current_user)):
    add_to_blacklist(token)
    return {"message": "Successfully logged out"}


