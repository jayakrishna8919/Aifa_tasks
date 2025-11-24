from fastapi import APIRouter,HTTPException
from utils.dependencies import cache_key_for_user,cache,fetch_user_from_db
from configurations.db_config import AsyncSessionLocal

from sqlalchemy import select
from schemas.models import User
from schemas.schemas import UserOut,UserCreate
from fastapi import Response
from utils.dependencies import AccessCounterWindow,ACCESS_THRESHOLD,CACHE_TTL_SECONDS


router=APIRouter()



@router.post("/users/", response_model=UserOut)
async def create_user(payload: UserCreate):
    async with AsyncSessionLocal() as session:
        new_user = User(name=payload.name, email=payload.email)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

    
    # await cache.delete(cache_key_for_user(new_user.id))
    return UserOut(id=new_user.id, name=new_user.name, email=new_user.email)

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    key = cache_key_for_user(user_id)
    cached = await cache.get(key)
    if cached:
        return {"source": "cache", "user": {"id": cached.id, "name": cached.name, "email": cached.email}}

    user = await fetch_user_from_db(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # store in cache for 60 seconds
    await cache.set(key, user, ttl=60)
    return {"source": "db", "user": {"id": user.id, "name": user.name, "email": user.email}}

@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int, response: Response):
    key = cache_key_for_user(user_id)

    # 1) If already cached -> immediate HIT
    cached = await cache.get(key)
    if cached:
        response.headers["X-Cache"] = "HIT"
        return UserOut(**cached)

    # 2) Not cached -> increment access counter (within window)
    count = await AccessCounterWindow.hit(key)

    # 3) Fetch from DB on each miss (we always return the DB value)
    user = await fetch_user_from_db(user_id)
    if not user:
        # If user doesn't exist reset counter to avoid repeated wasted counts
        await AccessCounterWindow.reset(key)
        raise HTTPException(status_code=404, detail="User not found")

    user_data = {"id": user.id, "name": user.name, "email": user.email}

    # 4) Only set cache when threshold reached within window
    if count >= ACCESS_THRESHOLD:
        await cache.set(key, user_data, ttl=CACHE_TTL_SECONDS)
        await AccessCounterWindow.reset(key)
        response.headers["X-Cache"] = "SET"
    else:
        response.headers["X-Cache"] = "MISS"

    return UserOut(**user_data)


@router.put("/users/{user_id}")
async def update_user(user_id: int, payload: dict):
    async with AsyncSessionLocal() as session:
        q = await session.execute(select(User).where(User.id == user_id))
        user = q.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404)
        user.name = payload.get("name", user.name)
        user.email = payload.get("email", user.email)
        session.add(user)
        await session.commit()

    # invalidate cache after update
    await cache.invalidate(cache_key_for_user(user_id))
    return {"status": "ok"}
