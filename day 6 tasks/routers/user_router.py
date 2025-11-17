from fastapi import APIRouter, Depends
from dependencies.auth_dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
def get_profile(user=Depends(get_current_user)):
    return {
        "username": user.username,
        "role": user.role
    }
