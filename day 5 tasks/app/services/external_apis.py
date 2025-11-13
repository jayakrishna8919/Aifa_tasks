import httpx
import asyncio
from core.logger import logger
from datetime import datetime

API_URLS = [
    "https://jsonplaceholder.typicode.com/todos/1",
    "https://jsonplaceholder.typicode.com/todos/2",
]

async def fetch_single(url: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()

async def fetch_data_concurrently():
    try:
        logger.info(f"{str(datetime.now())}:: The fetching of data is started")
        
        tasks = [fetch_single(url) for url in API_URLS]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        logger.info(f"{str(datetime.now())} :: The fectching of data is ended !")
        return results
    except Exception as e:
        logger.exception(e)
    finally: 
        logger.info(f"{str(datetime.now())} :: Ended")
