from enum import Enum
from pydantic import BaseModel, EmailStr

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.USER

class User(UserBase):
    role: UserRole

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token:str
    refresh_token_type:str

class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None