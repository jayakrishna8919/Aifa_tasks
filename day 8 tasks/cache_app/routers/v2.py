from fastapi import APIRouter, HTTPException
from schemas.schemas import UserOutV2,UserCreateV2
from schemas.models import User
from utils.dependencies import fetch_user_from_db
from configurations.db_config import AsyncSessionLocal


routerv2 = APIRouter()

@routerv2.get("/users/v2/{user_id}", response_model=UserOutV2)
async def get_user_v1(user_id: int):
    user = await fetch_user_from_db(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # v1 INtentionally omitting email
    return {"id": user.id, "name": user.name,"email":user.email}

@routerv2.post("/users/", response_model=UserOutV2, status_code=201)
async def create_user_v1(payload: UserCreateV2):
    async with AsyncSessionLocal() as session:
        new_user = User(name=payload.name, email=payload.email)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
    return UserOutV2(id=new_user.id, name=new_user.name, email=new_user.email)


