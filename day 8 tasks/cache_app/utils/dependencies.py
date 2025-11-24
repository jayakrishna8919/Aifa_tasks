from configurations.db_config import AsyncSessionLocal

from sqlalchemy import select
from schemas.models import User

import time
import asyncio
from typing import Any, Dict, Tuple,Optional

CACHE_TTL_SECONDS = 60           # how long cached items live
ACCESS_THRESHOLD = 4             # how many accesses required to add to cache
ACCESS_WINDOW_SECONDS = 60       # time window in which accesses count

class SimpleAsyncTTLCache:
    
    def __init__(self):
        self._data: Dict[str, Tuple[Any, float]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            val = self._data.get(key)
            if not val:
                return None
            value, expires_at = val
            if time.time() > expires_at:
                del self._data[key]
                return None
            return value

    async def set(self, key: str, value: Any, ttl: int = CACHE_TTL_SECONDS):
        expires_at = time.time() + ttl
        async with self._lock:
            self._data[key] = (value, expires_at)

    async def delete(self, key: str):
        async with self._lock:
            if key in self._data:
                del self._data[key]

    async def clear(self):
        async with self._lock:
            self._data.clear()


class AccessCounterWindow:
   
    def __init__(self):
        self._counts: Dict[str, Tuple[int, float]] = {}
        self._lock = asyncio.Lock()

    async def hit(self, key: str) -> int:
       
        now = time.time()
        async with self._lock:
            existing = self._counts.get(key)
            if not existing or now > existing[1]:
                # start new window
                self._counts[key] = (1, now + ACCESS_WINDOW_SECONDS)
                return 1
            count, expires_at = existing
            count += 1
            self._counts[key] = (count, expires_at)
            return count

    async def reset(self, key: str):
        async with self._lock:
            if key in self._counts:
                del self._counts[key]

    async def get(self, key: str) -> int:
        async with self._lock:
            existing = self._counts.get(key)
            if not existing or time.time() > existing[1]:
                return 0
            return existing[0]


# Instantiate singletons
cache = SimpleAsyncTTLCache()
access_counter = AccessCounterWindow()



# fetch user from DB (and cache)
async def fetch_user_from_db(user_id: int):
    async with AsyncSessionLocal() as session:
        q = await session.execute(select(User).where(User.id == user_id))
        user = q.scalar_one_or_none()
        return user

def cache_key_for_user(user_id: int) -> str:
    return f"user:{user_id}"
