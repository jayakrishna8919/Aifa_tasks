from pydantic import BaseModel, EmailStr
class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    
# v1 schema: minimal
class UserOutV1(BaseModel):
    id: int
    name: str
class UserCreateV1(BaseModel):
    name: str
class UserCreateV2(BaseModel):
    name: str
    email: EmailStr

# v2 schema: extended with email
class UserOutV2(BaseModel):
    id: int
    name: str
    email: EmailStr