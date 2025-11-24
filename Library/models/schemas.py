from pydantic import BaseModel, EmailStr, Field, validator
import re
from typing import Optional, List
from models.models import RoleEnum
from datetime import datetime,date

USERNAME_REGEX = re.compile(r"^[A-Za-z0-9_.]{3,30}$")
PASSWORD_REGEX = re.compile(
    r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
)

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: Optional[RoleEnum] = RoleEnum.user

    @validator("username")
    def username_valid(cls, v):
        
        if not USERNAME_REGEX.match(v):
            raise ValueError("username must be 3-30 chars long and only letters, numbers, _ or .")
        return v

    @validator("password")
    def password_valid(cls, v):
        if len(v.encode("utf-8")) > 72:
            raise ValueError("password too long for bcrypt (max 72 bytes) — use a shorter password or switch to bcrypt_sha256")
        
        if not PASSWORD_REGEX.match(v):
            raise ValueError("password must be at least 8 chars, include upper, lower, digit and special char")
        return v

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: RoleEnum
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None
    exp: Optional[int] = None

class LoginIn(BaseModel):
    username_or_email: str
    password: str

class BookCreate(BaseModel):
    title: str
    author: Optional[str] = None
    isbn: Optional[str] = None
    total_copies: int = Field(..., gt=0)

class BookOut(BaseModel):
    id: int
    title: str
    author: Optional[str]
    isbn: Optional[str]
    total_copies: int
    available_copies: int

    class Config:
        orm_mode = True

class BorrowOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrowed_at: datetime
    due_date: date
    returned_at: Optional[datetime]
    fine_amount: float

    class Config:
        orm_mode = True