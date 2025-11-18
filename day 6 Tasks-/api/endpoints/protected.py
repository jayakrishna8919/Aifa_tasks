from fastapi import APIRouter, Depends
from auth.utils import get_current_user
from auth.models import UserRole
from api.dependencies import require_role

router = APIRouter(prefix="/protected", tags=["protected"])

@router.get("/user-data")
async def get_user_data(current_user=Depends(get_current_user)):
    return {
        "message": "User-specific data",
        "user_email": current_user["email"],
        "user_role": current_user["role"]
    }

@router.get("/admin-only")
async def admin_endpoint(current_user=Depends(require_role(UserRole.ADMIN))):
    return {"message": "Admin-only data", "admin_email": current_user["email"]}


