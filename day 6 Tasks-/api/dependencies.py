from enum import Enum
from fastapi import Depends, HTTPException, status
from auth.utils import get_current_user

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

def require_role(required_role: UserRole):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user["role"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker