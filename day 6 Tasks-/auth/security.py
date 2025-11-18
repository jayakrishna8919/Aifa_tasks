from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from auth.models import User, UserRole

# Secret key - in production use environment variable
SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"])

# In-memory storage 
users_db = {}
blacklisted_tokens = []

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)            #decoding the token
    print(f"payload---{payload}")
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data:dict,expires_delta:Optional[timedelta]=None)->str:
    to_encode = data.copy()
    expire=datetime.now(timezone.utc)+(expires_delta or timedelta(minutes=35))
    to_encode.update({"exp":expire})
    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    print(f"refresh token-{token}")
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def authenticate_user(email: str, password: str) -> User | None:
    user = users_db.get(email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def add_to_blacklist(token: str) -> None:
    blacklisted_tokens.append(token)

def is_token_blacklisted(token: str) -> bool:
    return token in blacklisted_tokens

def create_user(email: str, password: str, role: UserRole) -> User:
    hashed_password = get_password_hash(password)
    user = User(email=email, role=role)
    users_db[email] = type('UserInDB', (), {
        'email': email,
        'hashed_password': hashed_password,
        'role': role
    })()
    return user