# app/utils/profiler.py
import time
from functools import wraps

def profile(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[PROFILE] {func.__name__} executed in {end - start:.4f}s")
        return result
    return wrapper
