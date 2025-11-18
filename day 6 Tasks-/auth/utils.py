
from typing import Optional, Tuple
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from auth.security import SECRET_KEY, ALGORITHM, is_token_blacklisted

security = HTTPBearer()

async def get_current_user_with_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Tuple[dict, str]:
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        #decoding of bearer token
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        email: Optional[str] = payload.get("sub")
        role: Optional[str] = payload.get("role")
        if email is None or role is None:
            raise credentials_exception
        user = {"email": email, "role": role}
        return user, token
    except JWTError:
        raise credentials_exception

async def get_current_user(
    user_token: Tuple[dict, str] = Depends(get_current_user_with_token)
):
    print(f"user-token {user_token}")
    return user_token[0]

async def get_current_token(
    user_token: Tuple[dict, str] = Depends(get_current_user_with_token)
):
    return user_token[1]
