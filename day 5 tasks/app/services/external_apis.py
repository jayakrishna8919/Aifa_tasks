import httpx
import asyncio

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
    tasks = [fetch_single(url) for url in API_URLS]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
