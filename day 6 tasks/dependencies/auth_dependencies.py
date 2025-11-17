from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from core.jwt_utils import decode_access_token
from db.memory_db import fake_users_db, blacklisted_tokens

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(401, "Token invalidated")

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(401, "Invalid token")

    username = payload.get("sub")
    user = fake_users_db.get(username)
    if not user:
        raise HTTPException(404, "User not found")

    return user


def require_role(role: str):
    def inner(user=Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(403, "Forbidden: insufficient role")
        return user
    return inner
