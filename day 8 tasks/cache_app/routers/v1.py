from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from schemas.schemas import UserOutV1,UserCreateV1
from schemas.models import User
from utils.dependencies import fetch_user_from_db
from configurations.db_config import AsyncSessionLocal

routerv1 = APIRouter()



# In a real app replace this with DB call (fetch_user_from_db)
# sample in-memory store for demo


@routerv1.get("/users/v1/{user_id}", response_model=UserOutV1)
async def get_user_v1(user_id: int):
    user = await fetch_user_from_db(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"id": user.id, "name": user.name}



@routerv1.post("/users/", response_model=UserOutV1, status_code=201)
async def create_user_v1(payload: UserCreateV1):
    async with AsyncSessionLocal() as session:
        new_user = User(name=payload.name, email=payload.email)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
    return UserOutV1(id=new_user.id, name=new_user.name, email=new_user.email)
