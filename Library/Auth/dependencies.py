from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database.config import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from utils.jwt_utils import decode_token
from fastapi import HTTPException,status,Depends
from models.models import User,RoleEnum

security = HTTPBearer()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                           db: AsyncSession = Depends(get_db)) -> User:
    token = credentials.credentials
    payload = decode_token(token)
    if not payload.sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    user_id = payload.sub
    user = await db.get(User, int(user_id))
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
    return user

def require_role(*allowed_roles: RoleEnum):
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user
    return role_checker